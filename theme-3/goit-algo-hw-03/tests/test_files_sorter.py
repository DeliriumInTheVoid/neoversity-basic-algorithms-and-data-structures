import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from sources.files_sorter import sort_files, sort_files_rec


class TestSortFiles:
    def test_sort_files_basic(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            (source / "file1.txt").write_text("content1")
            (source / "file2.jpg").write_text("image")
            (source / "file3.py").write_text("code")

            sort_files(str(source), str(dest))

            assert (dest / "txt" / "file1.txt").exists()
            assert (dest / "jpg" / "file2.jpg").exists()
            assert (dest / "py" / "file3.py").exists()

    def test_sort_files_no_extension(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            (source / "README").write_text("readme content")
            (source / "Makefile").write_text("make content")

            sort_files(str(source), str(dest))

            assert (dest / "no_extension" / "README").exists()
            assert (dest / "no_extension" / "Makefile").exists()

    def test_sort_files_destination_inside_source_raises_error(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            source.mkdir()
            dest = source / "dest"

            (source / "file1.txt").write_text("content")

            with pytest.raises(ValueError, match="Destination directory cannot be inside the source directory"):
                sort_files(str(source), str(dest))

    def test_sort_files_invalid_source(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "nonexistent"
            dest = Path(temp_dir) / "dest"

            with pytest.raises(NotADirectoryError):
                sort_files(str(source), str(dest))

    def test_sort_files_source_is_file(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "file.txt"
            source.write_text("content")
            dest = Path(temp_dir) / "dest"

            with pytest.raises(NotADirectoryError):
                sort_files(str(source), str(dest))

    def test_sort_files_duplicate_filenames(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            # files with same name in different subdirectories
            (source / "dir1").mkdir()
            (source / "dir2").mkdir()
            (source / "dir1" / "file.txt").write_text("content1")
            (source / "dir2" / "file.txt").write_text("content2")

            sort_files(str(source), str(dest))

            # file should be overwritten
            assert (dest / "txt" / "file.txt").exists()
            # file should contain one of the contents
            content = (dest / "txt" / "file.txt").read_text()
            assert content in ["content1", "content2"]

    def test_sort_files_multiple_extensions(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            extensions = ["txt", "pdf", "jpg", "png", "py", "js", "html", "css", "json", "xml"]
            for i, ext in enumerate(extensions):
                (source / f"file{i}.{ext}").write_text(f"content{i}")

            sort_files(str(source), str(dest))

            for i, ext in enumerate(extensions):
                assert (dest / ext / f"file{i}.{ext}").exists()

    def test_sort_files_mixed_content(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            (source / "file1.txt").write_text("content1")
            (source / "empty_dir").mkdir()
            (source / "dir_with_file").mkdir()
            (source / "dir_with_file" / "file2.py").write_text("code")

            sort_files(str(source), str(dest))

            assert (dest / "txt" / "file1.txt").exists()
            assert (dest / "py" / "file2.py").exists()


class TestSortFilesRec:

    def test_sort_files_rec_basic(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            (source / "file1.txt").write_text("content")

            sort_files_rec(source, dest)

            assert (dest / "txt" / "file1.txt").exists()

    def test_sort_files_rec_invalid_source(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "nonexistent"
            dest = Path(temp_dir) / "dest"

            with pytest.raises(NotADirectoryError):
                sort_files_rec(source, dest)

    def test_sort_files_rec_deep_nesting(self):
        with TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source"
            dest = Path(temp_dir) / "dest"
            source.mkdir()

            # deep nesting
            current = source
            for i in range(5):
                current = current / f"level{i}"
                current.mkdir()
                (current / f"file{i}.txt").write_text(f"content{i}")

            sort_files_rec(source, dest)

            for i in range(5):
                assert (dest / "txt" / f"file{i}.txt").exists()
