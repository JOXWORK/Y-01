import subprocess
import sys
from pathlib import Path


def func_main():
    while True:
        SANDBOX_DIR = Path(__file__).parent / "pystorage"

        exclude_files = ["sandbox.py"]
        PYFILES = [x for x in SANDBOX_DIR.rglob("*.py") if x.name not in exclude_files]

        for index, file in enumerate(PYFILES):
            if file.name == "sandbox.py":
                continue
            print(f"[{index}]: {file}")

        cmd = input(">>")

        if cmd == "stop":
            sys.exit(0)

        if cmd.isdigit():
            file_index = int(cmd)
            if file_index <= len(PYFILES) - 1:
                subprocess.run(["python", PYFILES[file_index]])

        continue
