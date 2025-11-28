import shutil
from pathlib import Path


def sort_files(source_dir: str, dest_dir: str="dist"):
    source_path = Path(source_dir).resolve()

    if not dest_dir:
        dest_dir = "dist"
    dest_path = Path(dest_dir)

    if not dest_path.is_absolute():
        dest_path = source_path.parent / dest_path

    dest_path = dest_path.resolve()

    if dest_path.is_relative_to(source_path):
        raise ValueError("Destination directory cannot be inside the source directory.")

    sort_files_rec(source_path, dest_path)


def sort_files_rec(source_dir: Path, dest_dir: Path):
    if not source_dir.is_dir():
        raise NotADirectoryError(f"The source path {source_dir} is not a valid directory.")

    for item in source_dir.iterdir():
        if item.is_dir():
            sort_files_rec(item, dest_dir)
        elif item.is_file():
            if item.name.startswith('.') and not item.suffix:
                file_extension = "dotfiles"
            elif item.suffix:
                file_extension = item.suffix[1:]
            else:
                file_extension = "no_extension"

            target_dir = dest_dir / file_extension
            target_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy2(item, target_dir / item.name)
