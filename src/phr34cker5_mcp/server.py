"""
PHR34CKER5 MCP server.

Serves a corpus of phreaking lore — zine-flavored markdown organized by topic
(blueboxing, redboxing, CN/A, 2600Hz, BBS, war dialing, ESS, tandem stacking…)
— as MCP resources with tools to list, read, search, and roll a random file.

The corpus lives on disk under the package (installed copy) or under
`knowledge/` at the repo root (dev mode). Skills are shipped separately under
`skills/` and installed into Claude Code / opencode's skill directories.
"""

from __future__ import annotations

import argparse
import os
import random
import re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from mcp.server.fastmcp import FastMCP

URI_SCHEME = "phr34cker5"


# --- corpus location ---------------------------------------------------------


def _candidate_roots() -> list[Path]:
    """Locations where the knowledge corpus may live, in preference order."""
    roots: list[Path] = []

    env = os.environ.get("PHR34CKER5_KNOWLEDGE")
    if env:
        roots.append(Path(env).expanduser().resolve())

    # Installed wheel: force-included at phr34cker5_mcp/_knowledge
    try:
        pkg_root = resources.files("phr34cker5_mcp").joinpath("_knowledge")
        as_path = Path(str(pkg_root))
        if as_path.exists():
            roots.append(as_path)
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    # Dev mode: repo-root/knowledge/ (two parents up from this file:
    # src/phr34cker5_mcp/server.py -> repo root)
    here = Path(__file__).resolve()
    roots.append(here.parents[2] / "knowledge")

    return roots


def _resolve_knowledge_root() -> Path:
    for r in _candidate_roots():
        if r.exists() and r.is_dir():
            return r
    # Fall back to the dev-mode path even if missing — errors surface clearly.
    return _candidate_roots()[-1]


KNOWLEDGE_ROOT = _resolve_knowledge_root()


# --- corpus helpers ----------------------------------------------------------


@dataclass(frozen=True)
class LoreFile:
    topic: str
    name: str  # filename without extension
    path: Path

    @property
    def uri(self) -> str:
        return f"{URI_SCHEME}://{self.topic}/{self.name}"


def _iter_lore(root: Path) -> list[LoreFile]:
    if not root.exists():
        return []
    out: list[LoreFile] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        parts = rel.parts
        if len(parts) == 1:
            topic = "_root"
            name = md.stem
        else:
            topic = parts[0]
            name = "/".join(parts[1:])[:-3]  # strip .md
        out.append(LoreFile(topic=topic, name=name, path=md))
    return out


def _find_lore(root: Path, topic: str, name: str) -> LoreFile | None:
    for lf in _iter_lore(root):
        if lf.topic == topic and lf.name == name:
            return lf
    return None


# --- server ------------------------------------------------------------------


mcp = FastMCP(
    name="phr34cker5",
    instructions=(
        "PHR34CKER5 is a phreaking knowledge server — a zine archive from the "
        "golden era of the phone network. Use `list_topics` to see what's in "
        "the stacks, `read_lore` to pull a specific file, `search_lore` to "
        "grep the corpus, and `random_lore` when you want to be surprised. "
        "Each markdown file is also exposed as a resource under the "
        f"`{URI_SCHEME}://` scheme."
    ),
)


@mcp.tool()
def list_topics() -> dict:
    """List all phreaking topics in the corpus and the files under each."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    topics: dict[str, list[str]] = {}
    for lf in lore:
        topics.setdefault(lf.topic, []).append(lf.name)
    return {
        "root": str(root),
        "topic_count": len(topics),
        "file_count": len(lore),
        "topics": topics,
    }


@mcp.tool()
def read_lore(topic: str, name: str) -> str:
    """
    Read a single lore file.

    Args:
        topic: topic directory name (e.g. 'blueboxing', 'cna', '2600hz').
        name: file name without the .md extension.
    """
    root = _resolve_knowledge_root()
    lf = _find_lore(root, topic, name)
    if lf is None:
        raise ValueError(
            f"no lore file for topic={topic!r} name={name!r} "
            f"(root={root}). Try list_topics()."
        )
    return lf.path.read_text(encoding="utf-8")


@mcp.tool()
def search_lore(query: str, max_results: int = 20) -> dict:
    """
    Search the corpus for a term (case-insensitive substring / regex).

    Returns per-file hit counts and the first matching line from each file.
    """
    root = _resolve_knowledge_root()
    try:
        pattern = re.compile(query, re.IGNORECASE)
    except re.error:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

    hits = []
    for lf in _iter_lore(root):
        try:
            text = lf.path.read_text(encoding="utf-8")
        except OSError:
            continue
        matching_lines = [ln for ln in text.splitlines() if pattern.search(ln)]
        if not matching_lines:
            continue
        hits.append(
            {
                "topic": lf.topic,
                "name": lf.name,
                "uri": lf.uri,
                "match_count": len(matching_lines),
                "first_match": matching_lines[0].strip()[:240],
            }
        )
    hits.sort(key=lambda h: h["match_count"], reverse=True)
    return {"query": query, "hit_count": len(hits), "results": hits[:max_results]}


@mcp.tool()
def random_lore() -> dict:
    """Return one random lore file — text and metadata. For inspiration."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    if not lore:
        raise ValueError(f"corpus is empty (root={root})")
    lf = random.choice(lore)
    return {
        "topic": lf.topic,
        "name": lf.name,
        "uri": lf.uri,
        "content": lf.path.read_text(encoding="utf-8"),
    }


@mcp.resource(f"{URI_SCHEME}://index")
def _index() -> str:
    """Human-readable index of the corpus."""
    root = _resolve_knowledge_root()
    lore = _iter_lore(root)
    lines = [f"# PHR34CKER5 corpus", f"root: {root}", ""]
    by_topic: dict[str, list[LoreFile]] = {}
    for lf in lore:
        by_topic.setdefault(lf.topic, []).append(lf)
    for topic in sorted(by_topic):
        lines.append(f"## {topic}")
        for lf in by_topic[topic]:
            lines.append(f"- [{lf.name}]({lf.uri})")
        lines.append("")
    return "\n".join(lines)


@mcp.resource(URI_SCHEME + "://{topic}/{name}")
def _lore_resource(topic: str, name: str) -> str:
    """Serve a lore file as an MCP resource."""
    root = _resolve_knowledge_root()
    lf = _find_lore(root, topic, name)
    if lf is None:
        raise ValueError(f"no lore file: {topic}/{name}")
    return lf.path.read_text(encoding="utf-8")


# --- entrypoint --------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(prog="phr34cker5-mcp")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP transport (default: stdio, which is what Claude Desktop / opencode use).",
    )
    parser.add_argument(
        "--knowledge",
        help="Override corpus root (also readable from $PHR34CKER5_KNOWLEDGE).",
    )
    args = parser.parse_args()

    if args.knowledge:
        os.environ["PHR34CKER5_KNOWLEDGE"] = args.knowledge
        global KNOWLEDGE_ROOT
        KNOWLEDGE_ROOT = _resolve_knowledge_root()

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
