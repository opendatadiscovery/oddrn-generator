from pathlib import Path

from oddrn_generator.generators import FilesystemGenerator
from oddrn_generator.utils import escape


def test_file_system_generator():
    root_path = str(Path().cwd().resolve())

    generator = FilesystemGenerator(host_settings="local", path=root_path)
    assert generator.get_oddrn_by_path(
        "path"
    ) == "//filesystem/host/local/path/" + escape(root_path)
