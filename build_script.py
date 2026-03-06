import subprocess
import sys
import platform

# import os
import time

from positive_tool import pt

from workflow import zip_files


class Config:
    project_name: str = "PROJECT_NAME"
    """**必要**

    專案名稱

    change it to project's name"""
    project_version: str = "0.1.0"
    """未啟動 `auto_detect_project_version` 時需手動更改
    change it to project's version when auto_detect_project_version is False"""
    auto_detect_project_version: bool = True
    """使用 `positive_tool` 取得專案版本"""
    is_rust_project: bool = True
    """change it if project use rust"""
    is_python_project: bool = True
    """change it if project use python"""
    enable_pyinstaller: bool = False
    """change it if project use pyinstaller"""
    pyinstaller_spec_path: str = ""
    """change it if project use pyinstaller to spec file's path"""
    pyinstaller_dist_filename: str = ""
    """if project use pyinstaller to the exec file in spec file"""

    def __init__(self) -> None:
        match platform.system():
            case "Windows":
                self.pyinstaller_dist_filename = (
                    self.pyinstaller_dist_filename
                    if self.pyinstaller_dist_filename == ""
                    else (self.pyinstaller_dist_filename + ".exe")
                )
        #
        if self.auto_detect_project_version is True:
            project_info = pt.ProjectInfo(
                self.project_name, auto_get=True
            )
            self.project_version = str(project_info.project_version)


def main():
    config = Config()
    start_time = time.time()
    if config.is_rust_project:
        rust_command()
    print("-" * 10, "zip file", "-" * 10)
    zip_files.main(
        config.is_rust_project,
        config.is_python_project,
        config.project_name,
        config.project_version,
    )
    print("-" * 10, "Summary", "-" * 10)
    print("finish in", time.time() - start_time)


def rust_command():
    print("-" * 10, "cargo-about", "-" * 10)
    subprocess.run(
        [
            "cargo-about",
            "generate",
            "--output-file",
            "ThirdPartyLicense-Rust.html",
            "about_html.hbs",
            "--threshold",
            "1.0",
        ],
        check=True,
        stdout=sys.stdout,
        stdin=sys.stdin,
        stderr=sys.stderr,
    )
    subprocess.run(
        [
            "cargo-about",
            "generate",
            "--output-file",
            "src/licenses_rust.json",
            "about_json.hbs",
            "--threshold",
            "1.0",
        ],
        check=True,
        stdout=sys.stdout,
        stdin=sys.stdin,
        stderr=sys.stderr,
    )
    print("-" * 10, "cargo build", "-" * 10)
    subprocess.run(
        ["cargo", "build", "--release"],
        check=True,
        stdout=sys.stdout,
        stdin=sys.stdin,
        stderr=sys.stderr,
    )


def pyinstaller_command(config: Config):
    print("-" * 10, "pyinstaller", "-" * 10)
    subprocess.run(
        ["uv", "run", "pyinstaller", config.pyinstaller_spec_path],
        check=True,
        stdout=sys.stdout,
        stdin=sys.stdin,
        stderr=sys.stderr,
    )


if __name__ == "__main__":
    main()
