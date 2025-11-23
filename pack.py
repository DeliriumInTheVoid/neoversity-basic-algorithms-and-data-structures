import os
import sys
import zipfile

from pathlib import Path

def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: python pack.py <directory_path>")
        return

    path = Path(args[1])
    folder_to_pack = path.resolve()
    if not folder_to_pack.is_dir() or not folder_to_pack.exists():
        print(f"The path {folder_to_pack} is not a valid directory.")
        return

    output_zip_file_name = f"{folder_to_pack.name}.zip"

    create_pack_zip(folder_to_pack, output_zip_file_name)

def should_exclude(name):
    exclude_list = [
        '.git', '.github', '.gitignore', 'venv', '.idea', '__pycache__', '.pytest_cache', '.venv_mac', '.venv_win'
    ]
    for pattern in exclude_list:
        if name.endswith(pattern) or os.path.basename(name) == pattern:
            return True
    return False


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_exclude(file_path):
                ziph.write(file_path, os.path.relpath(str(file_path), os.path.join(path, '..')))


def create_pack_zip(src_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(src_folder, zipf)
    print(f'packed to {output_zip}')


if __name__ == '__main__':
    main()
