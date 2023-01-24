from pathlib import Path

from oddrn_generator.generators import FilesystemGenerator


def test_file_system_generator():
    root_path = str(Path().cwd().resolve())
    generator = FilesystemGenerator(host_settings="local", path=root_path)
    assert (
        generator.get_oddrn_by_path("path")
        == "//filesystem/host/local/path/\\\\Users\\\\pavelmakarichev\\\\Documents\\\\projects\\\\odd\\\\oddrn-generator"
    )
