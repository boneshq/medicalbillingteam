#!/usr/bin/env python3
"""gnosis-secretscan - deterministic, stdlib-only secret detector for the wiki repo.

ONE scanner, THREE call sites:
  1. write-time inside gnosis.py / reconcile.py (block a write before it touches the wiki)
  2. a client-side pre-push hook on both machines
  3. a GitHub Action = required PR status check (the authoritative backstop)

Design:
  - Deterministic (no network). Portable pure stdlib (Windows + Spark container).
  - Fails CLOSED: exit 2 on a hit; exit 1 on ANY incomplete/failed scan (a git error,
    an unreadable blob, an unparsable range) — never report "clean" when coverage is
    partial. Exit 0 only when the FULL requested set scanned with zero hits.
  - Modes: `<file>...` | `--staged` | `--range BASE..TIP` (all NUL-safe; filenames with
    spaces are the norm in this wiki, so name lists are parsed with -z, never whitespace).
  - `--range` scans EVERY blob newly reachable from TIP but not BASE (incl. intermediate
    commits + renames/copies), not just the endpoint tree.

Allowlist: a line may opt out with `# secretscan:allow <reason>` — the reason is REQUIRED,
and it only suppresses ANNOTATABLE rules (never live private/cloud keys).
"""
import sys
import re
import os
import tempfile
import subprocess

# Protected empty hooks dir for every git child (set once per run).
# Prefer caller-injected GIT_CONFIG_VALUE_0; else create a temp empty dir.
_hooks_empty_dir = None


def _hooks_path():
    global _hooks_empty_dir
    env_val = os.environ.get("GIT_CONFIG_VALUE_0")
    if env_val:
        return env_val
    if _hooks_empty_dir is None:
        _hooks_empty_dir = tempfile.mkdtemp(prefix="secretscan-hooks-")
    return _hooks_empty_dir


def _git_runner(args, **kwargs):
    """Every git subprocess goes through here.

    Prepends ``-c core.hooksPath=<protected empty dir>``. GIT_DIR / GIT_WORK_TREE
    (and other env) still apply via normal subprocess inheritance — callers may
    also inject hooksPath via GIT_CONFIG_* as defense-in-depth.
    """
    hooks = _hooks_path()
    cmd = ["git", "-c", f"core.hooksPath={hooks}"] + list(args)
    return subprocess.run(cmd, **kwargs)

# (name, compiled regex, annotatable?) — annotatable=False can NEVER be allowlisted.
RULES = [
    ("google-api-key",      re.compile(r"AIza[0-9A-Za-z_\-]{35}"),                        False),
    ("aws-access-key",      re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),                 False),
    ("aws-secret-key",      re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?[0-9A-Za-z/+]{40}"), False),
    ("github-pat",          re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}"),                    False),
    ("github-fine-pat",     re.compile(r"github_pat_[0-9A-Za-z_]{60,}"),                  False),
    ("slack-token",         re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}"),                 False),
    ("stripe-live",         re.compile(r"sk_live_[0-9A-Za-z]{20,}"),                      False),
    ("openai-key",          re.compile(r"sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}"),     False),
    ("private-key",         re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP |DSA |ENCRYPTED )?PRIVATE KEY-----"), False),
    ("google-oauth-secret", re.compile(r"GOCSPX-[0-9A-Za-z_\-]{20,}"),                    False),
    ("jwt",                 re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), True),
    # generic secret-ish assignment. Key name may be quoted (JSON) and/or prefixed/suffixed
    # (client_secret, OPENAI_API_KEY, refresh_token). Value = group 1.
    ("generic-secret-assign",
     re.compile(r"""(?ix)
        ["']?[\w.\-]{0,24}
        (?:api[_-]?key|secret|token|password|passwd|access[_-]?key|private[_-]?key)
        [\w.\-]{0,24}["']?
        \s*[:=]\s*
        ["']?([^\s"',;]{20,})"""),
     True),
]

# A captured VALUE that IS a placeholder / code reference (checked with fullmatch on the
# value ONLY — NOT a substring test over the whole line, so a real secret that merely
# CONTAINS "example" is still caught).
PLACEHOLDER_VALUE = re.compile(r"""(?ix)^(
    your[_-][\w\-]* | example[\w\-]* | placeholder[\w\-]* | x{3,} | \.{3,} | <[^>]*> |
    \$\{?[a-z_]\w*\}? |
    (?:os\.environ|getenv|process\.env|env|config|settings|self|cls)\.[\w.]+ |
    (?-i:[A-Z][A-Z0-9_]{3,}) |
    [\w~:/\\.\-]*master\.env |
    redacted | dummy[\w\-]* | test[_-]?key[\w\-]* | sk_test_[\w]*
)$""")

ALLOW = re.compile(r"#\s*secretscan:allow\s+(\S.+)")   # reason (group 1) is REQUIRED

SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
            ".gz", ".tar", ".db", ".sqlite", ".woff", ".woff2", ".ttf", ".mp4",
            ".docx", ".xlsx", ".pptx"}


class ScanError(Exception):
    """Any condition that makes the scan INCOMPLETE — must fail closed (exit 1)."""


def mask(tok):
    tok = tok.strip().strip("'\"")
    if len(tok) <= 8:
        return "*" * len(tok)
    return tok[:4] + "…" + tok[-2:] + f"<{len(tok)}ch>"


def scan_text(text, path):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        am = ALLOW.search(line)
        allowed = bool(am and am.group(1).strip())     # allow only with a real reason
        for name, rx, annotatable in RULES:
            for m in rx.finditer(line):                 # ALL matches, not just the first
                captured = (m.group(1) if m.groups() else m.group(0))
                if name == "generic-secret-assign":
                    # trim wrapping quotes/backticks + trailing sentence punctuation so a
                    # documented var NAME like `WP_ALT_APP_PASSWORD`. is recognized as a
                    # placeholder; real secrets are random and never fullmatch regardless
                    val = re.sub(r"^['\"`]+|['\"`.,;:)]+$", "", captured.strip())
                    if PLACEHOLDER_VALUE.fullmatch(val):  # value IS a placeholder/code ref
                        continue
                if allowed and annotatable:
                    continue
                hits.append((path, i, name, mask(captured)))
    return hits


def _git(args):
    r = _git_runner(args, capture_output=True)
    if r.returncode != 0:
        raise ScanError(f"git {' '.join(args)} failed rc={r.returncode}: "
                        f"{r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout


def _scan_blob(sha, path):
    r = _git_runner(["cat-file", "blob", sha], capture_output=True)
    if r.returncode != 0:
        raise ScanError(f"cat-file blob {sha} ({path}) failed")
    return scan_text(r.stdout.decode("utf-8", "replace"), path)


def scan_paths(paths):
    hits = []
    for path in paths:
        if any(path.lower().endswith(e) for e in SKIP_EXT):
            continue
        try:
            with open(path, "rb") as f:
                data = f.read()
        except IsADirectoryError:
            continue
        except (FileNotFoundError, PermissionError, OSError) as e:
            raise ScanError(f"cannot read {path}: {e}")   # unreadable target != clean
        hits += scan_text(data.decode("utf-8", "replace"), path)
    return hits


def scan_staged():
    out = _git(["diff", "--cached", "-z", "--name-only", "--diff-filter=ACMT"])
    hits = []
    for pb in out.split(b"\0"):
        if not pb:
            continue
        path = pb.decode("utf-8", "replace")
        if any(path.lower().endswith(e) for e in SKIP_EXT):
            continue
        # staged blob sha via ls-files --stage keeps NUL paths intact
        ls = _git(["ls-files", "--stage", "-z", "--", path])
        rec = ls.split(b"\0", 1)[0].decode("utf-8", "replace").split()
        if len(rec) < 2:
            raise ScanError(f"no staged blob for {path}")
        hits += _scan_blob(rec[1], path)
    return hits


def scan_range(rng):
    zero = "0" * 40
    if ".." in rng:
        base, tip = rng.split("..", 1)
    else:
        base, tip = "", rng
    tip = tip or "HEAD"
    # enumerate every blob reachable from TIP but not BASE (covers intermediate commits,
    # renames, copies). All-zero / empty base -> everything new vs the remote refs.
    if not base or base == zero:
        revargs = [tip, "--not", "--remotes"]
    else:
        if _git_runner(["cat-file", "-e", base + "^{commit}"],
                       capture_output=True).returncode != 0:
            revargs = [tip, "--not", "--remotes"]        # unknown base -> scan all new
        else:
            revargs = [f"{base}..{tip}"]
    out = _git(["rev-list", "--objects"] + revargs)
    # lines: "<sha> [path]" ; a blob line has a path, commits/trees usually don't
    seen = {}
    for line in out.decode("utf-8", "replace").splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2 and parts[1]:
            seen.setdefault(parts[0], parts[1])
    hits = []
    for sha, path in seen.items():
        if any(path.lower().endswith(e) for e in SKIP_EXT):
            continue
        # confirm it's a blob (paths can also decorate tags); non-blobs are skipped safely
        t = _git_runner(["cat-file", "-t", sha], capture_output=True, text=True)
        if t.returncode != 0:
            raise ScanError(f"cat-file -t {sha} failed")
        if t.stdout.strip() != "blob":
            continue
        hits += _scan_blob(sha, path)
    return hits


def main():
    args = sys.argv[1:]
    try:
        if "--staged" in args:
            hits = scan_staged()
        elif "--range" in args:
            i = args.index("--range")
            if i + 1 >= len(args):
                print("usage: secretscan.py --range BASE..TIP", file=sys.stderr)
                return 1
            hits = scan_range(args[i + 1])
        else:
            files = [a for a in args if not a.startswith("--")]
            if not files:
                print("usage: secretscan.py <file>... | --staged | --range BASE..TIP",
                      file=sys.stderr)
                return 1
            hits = scan_paths(files)
    except ScanError as e:
        print(f"SECRET SCAN INCOMPLETE (failing closed): {e}", file=sys.stderr)
        return 1

    if hits:
        print(f"SECRET SCAN FAILED — {len(hits)} potential secret(s):", file=sys.stderr)
        for path, ln, name, masked in hits:
            print(f"  {path}:{ln}  [{name}]  {masked}", file=sys.stderr)
        print("\nRefusing. Remove the secret or reference master.env. Annotatable "
              "false positives: append `# secretscan:allow <reason>`.", file=sys.stderr)
        return 2
    print("secret scan: clean", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
