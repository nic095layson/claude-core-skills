#!/usr/bin/env python3
"""Full-tree license audit via npm registry API (no node/npm installed on host).

Recursively resolves runtime `dependencies` for each of the 12 seed packages,
starting from each package's `latest` dist-tag, then walking each subsequent
dependency's declared semver range by fetching that range's best-effort
resolution (registry `latest` when the range is unbounded-ish, else the
highest version satisfying the range from the full versions list).

Caveat baked into the output: this is NOT npm's real resolver (no hoisting/
dedupe/peerDependency semantics), so version selection can differ at the
margins from what `npm install` would actually produce. Good enough for a
license census; not a substitute for a real lockfile-based audit.
"""
import json
import re
import sys
import urllib.request
from urllib.error import HTTPError, URLError

SEEDS = ["axios", "lodash", "express", "chalk", "commander", "dayjs", "zod",
         "pino", "undici", "ws", "yargs", "nanoid"]

REGISTRY = "https://registry.npmjs.org"
seen = {}          # name -> {version, license, parents:set}
errors = []
MAX_PACKAGES = 3000

def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "license-audit-script"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def best_version(versions, rng):
    """Very rough semver-range resolver: strip ^ ~ >= etc, exact-match if
    present, else fall back to the highest listed version. Not a real semver
    engine -- flagged as a limitation in the report."""
    if rng in ("*", "", "latest", "x"):
        return sorted(versions, key=version_key)[-1]
    m = re.match(r"^[\^~>=<]*\s*([0-9][0-9A-Za-z.\-+]*)", rng)
    if m and m.group(1) in versions:
        return m.group(1)
    # else: highest version <= no constraint check (best-effort only)
    return sorted(versions, key=version_key)[-1]

def version_key(v):
    parts = re.split(r"[.\-]", v)
    out = []
    for p in parts:
        out.append(int(p) if p.isdigit() else -1)
    return out

def license_str(manifest):
    lic = manifest.get("license")
    if isinstance(lic, dict):
        return lic.get("type", "UNKNOWN")
    if isinstance(lic, str):
        return lic
    lics = manifest.get("licenses")
    if isinstance(lics, list) and lics:
        return "/".join(sorted(set(l.get("type", "UNKNOWN") for l in lics if isinstance(l, dict))))
    return "UNKNOWN"

def walk(name, range_spec, parent, depth=0, max_depth=40):
    key_name = name
    if key_name in seen:
        seen[key_name]["parents"].add(parent)
        return
    if len(seen) >= MAX_PACKAGES or depth > max_depth:
        errors.append(f"SAFETY CAP HIT at {name} (depth={depth}, total={len(seen)})")
        return
    try:
        pkg = fetch(f"{REGISTRY}/{name}")
    except (HTTPError, URLError, TimeoutError, Exception) as e:
        errors.append(f"{name}: fetch failed ({e})")
        seen[key_name] = {"version": "UNRESOLVED", "license": "FETCH_ERROR", "parents": {parent}}
        return

    versions = pkg.get("versions", {})
    dist_tags = pkg.get("dist-tags", {})
    if not versions:
        errors.append(f"{name}: no versions in registry response")
        seen[key_name] = {"version": "UNRESOLVED", "license": "NO_VERSIONS", "parents": {parent}}
        return

    if range_spec is None:
        ver = dist_tags.get("latest") or sorted(versions.keys(), key=version_key)[-1]
    else:
        ver = best_version(list(versions.keys()), range_spec)
        if ver not in versions:
            ver = dist_tags.get("latest") or sorted(versions.keys(), key=version_key)[-1]

    manifest = versions.get(ver, {})
    lic = license_str(manifest)
    seen[key_name] = {"version": ver, "license": lic, "parents": {parent}}

    deps = manifest.get("dependencies", {}) or {}
    for dep_name, dep_range in deps.items():
        walk(dep_name, dep_range, f"{name}@{ver}", depth + 1, max_depth)

def main():
    for s in SEEDS:
        walk(s, None, "SEED")

    rows = []
    for name, info in seen.items():
        rows.append({
            "name": name,
            "version": info["version"],
            "license": info["license"],
            "parents": sorted(info["parents"]),
        })
    rows.sort(key=lambda r: r["name"])

    out = {"total_packages": len(rows), "packages": rows, "errors": errors}
    with open("full_tree_result.json", "w") as f:
        json.dump(out, f, indent=2)

    from collections import Counter
    lic_counts = Counter(r["license"] for r in rows)
    print(f"Total unique packages resolved: {len(rows)}")
    print("License breakdown:")
    for lic, cnt in lic_counts.most_common():
        print(f"  {lic}: {cnt}")
    if errors:
        print(f"\n{len(errors)} errors/warnings:")
        for e in errors[:20]:
            print(f"  {e}")

if __name__ == "__main__":
    main()
