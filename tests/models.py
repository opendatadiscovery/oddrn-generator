from typing import Optional

from pydantic import Field

from oddrn.generators import Generator
from oddrn.path_models import BasePathsModel
from oddrn.server_models import HostnameModel


class ExamplePathModel(BasePathsModel):
    field_1: str
    field_2: str
    field_3: Optional[str]
    field_4: Optional[str]
    field_5_1: Optional[str] = Field(alias='field_5')
    field_5_2: Optional[str] = Field(alias='field_5')

    class Config:
        dependencies_map = {
            'field_1':   ('field_1',),
            'field_2':   ('field_1', 'field_2'),
            'field_3':   ('field_1', 'field_2', 'field_3'),
            'field_4':   ('field_1', 'field_2', 'field_3', 'field_4'),
            'field_5_1': ('field_1', 'field_2', 'field_3', 'field_4', 'field_5_1'),
            'field_5_2': ('field_1', 'field_2', 'field_3', 'field_4', 'field_5_2'),
        }


class ExampleGenerator(Generator):
    source = "example_source"
    paths_model = ExamplePathModel
    server_model = HostnameModel


example_generator_settings = {
    'host_settings': 'testhost.com:3841',
    'paths': {
        'field_1': 'some_field_1',
        'field_2': 'some_field_2',
        'field_3': 'some_field_3',
        'field_4': 'some_field_4',
        'field_5_1': 'some_field_5_1',
        'field_5_2': 'some_field_5_2',
    },
    'aliases': {
        'field_5_1': 'field_5',
        'field_5_2': 'field_5',
    }
}
