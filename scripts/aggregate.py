#!/usr/bin/env python3
"""Rebuild data/directory.json (players) and data/teams.json from u/*/ and g/*/."""
import glob
import json
import os

os.makedirs("data", exist_ok=True)


def load(pattern, keep):
    out = []
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path) as f:
                d = json.load(f)
        except Exception:
            continue
        out.append({k: d.get(k) for k in keep})
    return out


players = load("u/*/profile.json",
               ["username", "displayName", "tagline", "avatar", "games",
                "lookingForTeam", "socials", "updated"])
teams = load("g/*/group.json",
             ["slug", "name", "event", "game", "tagline", "members",
              "openSlots", "updated"])

for name, data in (("data/directory.json", players), ("data/teams.json", teams)):
    with open(name, "w") as f:
        json.dump(data, f, indent=2)
    print(f"{name}: {len(data)} entries")
