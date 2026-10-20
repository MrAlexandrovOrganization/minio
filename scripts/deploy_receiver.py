"""Receive a checked MinIO configuration revision through the SSH relay."""

import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    raw = sys.stdin.buffer.read(1025)
    release = json.loads(raw)
    if len(raw) > 1024 or set(release) != {"revision"} or not re.fullmatch(r"[a-f0-9]{40}", release["revision"]):
        raise ValueError("invalid revision")
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    lock = (Path.home() / ".minio-deploy.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX)
    if subprocess.check_output(["git", "status", "--porcelain"], text=True).strip():
        raise ValueError("dirty checkout")
    if subprocess.check_output(["git", "branch", "--show-current"], text=True).strip() != "main":
        raise ValueError("wrong branch")
    subprocess.run(["git", "fetch", "--quiet", "origin", "refs/heads/main"], check=True)
    if subprocess.check_output(["git", "rev-parse", "FETCH_HEAD"], text=True).strip() != release["revision"]:
        raise ValueError("stale release")
    subprocess.run(["git", "merge", "--quiet", "--ff-only", release["revision"]], check=True)
    subprocess.run(["make", "check", "up"], check=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, subprocess.CalledProcessError):
        raise SystemExit("MinIO configuration deployment failed") from None
