from typing import Optional

from pydantic import Field

from oddrn_generator.generators import Generator
from oddrn_generator.path_models import BasePathsModel
from oddrn_generator.server_models import HostnameModel


class ExamplePathModel(BasePathsModel):
    field_1: str
    field_2: str
    field_3: Optional[str] = None
    field_4: Optional[str] = None
    field_5_1: Optional[str] = Field(None, alias="field_5")
    field_5_2: Optional[str] = Field(None, alias="field_5")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "field_1": ("field_1",),
            "field_2": ("field_1", "field_2"),
            "field_3": ("field_1", "field_2", "field_3"),
            "field_4": ("field_1", "field_2", "field_3", "field_4"),
            "field_5_1": ("field_1", "field_2", "field_3", "field_4", "field_5_1"),
            "field_5_2": ("field_1", "field_2", "field_3", "field_4", "field_5_2"),
        }

    data_source_path: str = Field(default_factory=lambda: None)
    dependencies_map: dict = Field(default_factory=lambda: ExamplePathModel._dependencies_map_factory())


class ExampleGenerator(Generator):
    source = "example_source"
    paths_model = ExamplePathModel
    server_model = HostnameModel


example_generator_settings = {
    "host_settings": "testhost.com:3841",
    "paths": {
        "field_1": "some_field_1",
        "field_2": "some_field_2",
        "field_3": "some_field_3",
        "field_4": "some_field_4",
        "field_5_1": "some_field_5_1",
        "field_5_2": "some_field_5_2",
    },
    "aliases": {
        "field_5_1": "field_5",
        "field_5_2": "field_5",
    },
}
