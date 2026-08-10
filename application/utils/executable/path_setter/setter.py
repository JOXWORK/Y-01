import os
import site
from pathlib import Path
from sys import path as sys_path

PTH_FILE_NAME = "application_custom_paths.pth"


def setter(path: str | None = None) -> None:
    site_packages = site.getsitepackages()[0]
    pth_file = os.path.join(site_packages, PTH_FILE_NAME)

    if not os.path.exists(pth_file):
        open(pth_file, "w")

    with open(pth_file, "r+") as file:
        print(f"Paths contains in {pth_file}")
        for line in file:
            line = line.strip()
            if not line.startswith("#"):
                print(">>", line)
        print("." * 20)

        if path:
            file.write(f"{path}\n")
            print("Path successfully added!")

        print("Sys paths")
        for p in sys_path:
            print(f">>{p.strip()}")


def main() -> None:
    APPLICATION_DIR = Path(__file__).parents[3]
    setter(path=str(APPLICATION_DIR))


if __name__ == "__main__":
    main()
