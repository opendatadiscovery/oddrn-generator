from pathlib import Path

from oddrn_generator.generators import FilesystemGenerator


def test_metabase_generator():
    path = Path("user/foo/bar").as_posix()
    generator = FilesystemGenerator(path=path)

    assert generator.get_data_source_oddrn() == "//filesystem/filesystem"

    assert (
        generator.get_oddrn_by_path("path")
        == "//filesystem/filesystem/path/user\\\\foo\\\\bar"
    )
