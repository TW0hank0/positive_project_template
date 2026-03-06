import subprocess
import sys
import os
import time
import workflow_ci


class Config:
    project_name: str = "PROJECT_NAME"
    is_rust_project: bool = True
    is_python_project: bool = True
    enable_pyinstaller: bool = False
    pyinstaller_spec_path: str = ""


def main():
    config = Config()
    start_time = time.time()
    if config.is_rust_project:
        rust_command()
    print("-" * 10, "zip file", "-" * 10)
    workflow_ci.zi
    print("-" * 20)
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
