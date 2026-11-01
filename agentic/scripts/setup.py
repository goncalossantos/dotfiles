#!/usr/bin/env python3
"""Safely link this checkout's personal instructions and skills. Dry-run by default."""
import argparse
import os
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
CLIENTS = ("pi", "claude", "codex")


def absolute(value):
    return Path(os.path.abspath(os.path.expanduser(str(value))))


def make_plan(home, clients, pi_dir=None, claude_dir=None, codex_dir=None):
    """Explicit directories override defaults. Never read ambient client env vars here."""
    instructions = REPO / "agentic/instructions/AGENTS.md"
    roots = {
        "pi": absolute(pi_dir) if pi_dir else home / ".pi/agent",
        "claude": absolute(claude_dir) if claude_dir else home / ".claude",
        "codex": absolute(codex_dir) if codex_dir else home / ".codex",
    }
    plan = {}
    for client in clients:
        target = roots[client] / ("CLAUDE.md" if client == "claude" else "AGENTS.md")
        plan[target] = instructions
    # Pi and Codex both discover ~/.agents/skills. Avoid duplicate Pi registrations.
    skill_roots = set()
    if "pi" in clients or "codex" in clients:
        skill_roots.add(home / ".agents/skills")
    if "claude" in clients:
        skill_roots.add(roots["claude"] / "skills")
    for root in sorted(skill_roots):
        for source in sorted((REPO / "agentic/skills").iterdir()):
            if (source / "SKILL.md").is_file():
                plan[root / source.name] = source
    return plan


def matches(target, source):
    # Compare lexical absolute link targets so dangling owned links can be removed.
    return target.is_symlink() and absolute(target.parent / os.readlink(target)) == source


def conflicts(plan, remove=False):
    problems = []
    for target, source in plan.items():
        if not remove and not source.exists():
            problems.append(f"Missing source: {source}")
        override = target.with_name("AGENTS.override.md")
        if not remove and target.name == "AGENTS.md" and os.path.lexists(override):
            problems.append(f"Review higher-priority instructions before installing: {override}")
        if os.path.lexists(target) and not matches(target, source):
            problems.append(f"Refusing to replace unmanaged path: {target}")
        for parent in target.parents:
            if os.path.lexists(parent) and not parent.is_dir():
                problems.append(f"Parent is not a directory: {parent}")
                break
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=absolute, default=Path.home(), help="Target user's home")
    parser.add_argument("--client", action="append", choices=CLIENTS, help="Repeat; default: all three")
    parser.add_argument("--pi-dir", help="Explicit PI_CODING_AGENT_DIR")
    parser.add_argument("--claude-dir", help="Explicit CLAUDE_CONFIG_DIR")
    parser.add_argument("--codex-dir", help="Explicit CODEX_HOME (instructions only)")
    parser.add_argument("--apply", action="store_true", help="Make changes; otherwise only print plan")
    parser.add_argument("--remove", action="store_true", help="Remove only matching symlinks; keep directories")
    args = parser.parse_args(argv)
    # Avoid accidentally configuring the wrong profile or this harness's agent directory.
    overrides = {"PI_CODING_AGENT_DIR": args.pi_dir, "CLAUDE_CONFIG_DIR": args.claude_dir,
                 "CODEX_HOME": args.codex_dir}
    for env, explicit in overrides.items():
        client = {"PI_CODING_AGENT_DIR": "pi", "CLAUDE_CONFIG_DIR": "claude", "CODEX_HOME": "codex"}[env]
        if os.environ.get(env) and not explicit and client in (args.client or CLIENTS):
            parser.error(f"{env} is set. Pass its matching --*-dir option explicitly (or unset it).")
    plan = make_plan(args.home, args.client or CLIENTS, args.pi_dir, args.claude_dir, args.codex_dir)
    problems = conflicts(plan, args.remove)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    for target, source in plan.items():
        owned = matches(target, source)
        action = "REMOVE" if args.remove and owned else "KEEP" if owned else "ABSENT" if args.remove else "LINK"
        print(f"{action}: {target} -> {source}")
        if args.apply:
            if args.remove and owned:
                target.unlink()
            elif not args.remove and not owned:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(source, target_is_directory=source.is_dir())
    print("Applied." if args.apply else "Dry run only. Review, then repeat with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
