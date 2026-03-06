import zipfile
import os
import platform
import typer

app = typer.Typer()


@app.command()
def main(
    is_rust_project: bool,
    is_python_project: bool,
    project_name: str,
    project_version: str,
    *,
    extra_include_files: list[str] | None = None,
):
    include_files = []
    include_files.extend(
        extra_include_files if extra_include_files is not None else []
    )
    target_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "target",
        "release",
    )
    for file in os.listdir(target_path):
        full_file_path = os.path.join(target_path, file)
        if os.path.isfile(full_file_path) is True:
            match platform.system():
                case "Linux":
                    if len(file.split(".")) == 1:
                        include_files.append(full_file_path)
                case "Windows":
                    if (file.split(".")[1] == "exe") and (
                        len(file.split(".")) > 1
                    ):
                        include_files.append(full_file_path)
    match platform.system():
        case "Linux":
            pf = "linux"
        case "Windows":
            pf = "windows"
        case _:
            pf = "unknown"
    zip_file_name = f"positive_mahjong_v{project_version}_{pf}.zip"
    with zipfile.ZipFile(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            zip_file_name,
        ),
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as zipf:
        for file in include_files:
            zipf.write(file, arcname=os.path.basename(file))
    print(zip_file_name)


if __name__ == "__main__":
    app()
