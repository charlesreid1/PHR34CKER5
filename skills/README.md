# PHR34CKER5 SKILLS

Skills that ride on top of the `phr34cker5` MCP server. Install by symlink
(so `git pull` updates them in place) or copy.

## Install into Claude Code

```sh
# from the repo root
ln -s "$PWD/skills/phreaking" ~/.claude/skills/phreaking
```

Claude Code auto-discovers `~/.claude/skills/*/SKILL.md` on next start.
Confirm it's loaded by asking Claude to `/help` — the skill should appear
in the skills list.

## Install into opencode

opencode's skill loader looks under `~/.config/opencode/skills/` (or
whatever `$XDG_CONFIG_HOME/opencode/skills/` resolves to on your system):

```sh
mkdir -p ~/.config/opencode/skills
ln -s "$PWD/skills/phreaking" ~/.config/opencode/skills/phreaking
```

If your opencode build uses a different skills path, symlink there
instead — the `SKILL.md` format is portable.

## What's here

- `phreaking/` — top-level skill. Teaches the assistant to consult the
  `phr34cker5` MCP server before answering phreaking-adjacent questions,
  and to cite files by URI.

Add sub-skills as directories alongside `phreaking/`; each needs its own
`SKILL.md` with frontmatter.
