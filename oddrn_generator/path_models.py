from typing import Optional

from pydantic import BaseModel

from oddrn_generator.exceptions import WrongPathOrderException, PathDoestExistException, EmptyPathValueException


class BasePathsModel(BaseModel):
    class Config:
        dependencies_map = {}
        data_source_path = None
        extra = 'forbid'
        allow_population_by_field_name = True

    def __validate_path(self, field) -> None:
        for deps in reversed(self.__config__.dependencies_map[field]):
            if not getattr(self, deps, None):
                raise WrongPathOrderException(f"'{field}' can not be without '{deps}' attribute")

    def validate_all_paths(self) -> None:
        for field in self.__fields_set__:
            self.__validate_path(field)

    def get_dependency(self, field) -> tuple:
        dependency = self.__config__.dependencies_map.get(field)
        if not dependency:
            raise PathDoestExistException(f"Path '{field}' doesn't exist in generator")
        return dependency

    def check_if_path_is_set(self, path: str) -> None:
        if not getattr(self, path, None):
            raise EmptyPathValueException(f"Path '{path}' is not set up")

    def set_path_value(self, path: str, value: str) -> None:
        setattr(self, path, value)
        self.__validate_path(path)

    @property
    def data_source_path(self):
        return self.__config__.data_source_path


class PostgresqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases':   ('databases',),
            'schemas':     ('databases', 'schemas', ),
            'tables':      ('databases', 'schemas', 'tables'),
            'columns':     ('databases', 'schemas', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class MysqlPathsModel(BasePathsModel):
    databases: str
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'tables':    ('databases', 'tables'),
            'columns':   ('databases', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class KafkaPathsModel(BasePathsModel):
    units: str
    topics: str

    class Config:
        dependencies_map = {
            'units':     ('units',),
            'topics':    ('units', 'topics'),
        }


class KafkaConnectorPathsModel(BasePathsModel):
    connectors: str

    class Config:
        dependencies_map = {
            'connectors': ('connectors',),
        }


class GluePathsModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]
    owners: Optional[str]
    jobs: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'tables':    ('databases', 'tables'),
            'columns':   ('databases', 'tables', 'columns'),
            'owners':    ('owners',),
            'jobs':      ('jobs',),
            'runs':      ('jobs', 'runs'),
        }


class SnowflakePathsModel(BasePathsModel):
    warehouses: Optional[str]
    databases: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    owners: Optional[str]

    class Config:
        dependencies_map = {
            'warehouses': ('warehouses',),
            'databases':  ('warehouses', 'databases'),
            'schemas':    ('warehouses', 'databases', 'schemas'),
            'tables':     ('warehouses', 'databases', 'schemas', 'tables'),
            'views':      ('warehouses', 'databases', 'schemas', 'views'),
            'columns':    ('warehouses', 'databases', 'schemas', 'tables', 'columns'),
            'owners':     ('owners',),
        }


class AirflowPathsModel(BasePathsModel):
    dags: str
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            'dags':        ('dags',),
            'tasks':       ('dags', 'tasks'),
            'runs':        ('dags', 'tasks', 'runs'),
        }
        data_source_path = 'dags'


class HivePathsModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    owners: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'tables':    ('databases', 'tables'),
            'columns':   ('databases', 'tables', 'columns'),
            'owners':    ('owners',),
        }
        data_source_path = 'databases'


class DynamodbPathsModel(BasePathsModel):
    schemas: str
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'schemas':    ('schemas',),
            'databases':  ('schemas', 'databases'),
            'tables':     ('schemas', 'databases', 'tables'),
            'columns':    ('schemas', 'databases', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class OdbcPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'schemas':   ('databases', 'schemas'),
            'tables':    ('databases', 'schemas', 'tables'),
            'columns':   ('databases', 'schemas', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class MssqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'schemas':   ('databases', 'schemas'),
            'tables':    ('databases', 'schemas', 'tables'),
            'columns':   ('databases', 'schemas', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class OraclePathsModel(BasePathsModel):
    schemas: str
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'schemas':   ('schemas',),
            'databases': ('schemas', 'databases'),
            'tables':    ('schemas', 'databases', 'tables'),
            'columns':   ('schemas', 'databases', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class RedshiftPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'schemas':   ('databases', 'schemas'),
            'tables':    ('databases', 'schemas', 'tables'),
            'columns':   ('databases', 'schemas', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class ClickHousePathsModel(BasePathsModel):
    databases: str
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'tables':    ('databases', 'tables'),
            'columns':   ('databases', 'tables', 'columns'),
        }
        data_source_path = 'databases'


class AthenaPathsModel(BasePathsModel):
    catalogs: Optional[str]
    databases: Optional[str]
    tables: Optional[str]

    class Config:
        dependencies_map = {
            'catalogs':  ('catalogs',),
            'databases': ('catalogs', 'databases'),
            'tables':    ('catalogs', 'databases', 'tables'),
        }


class QuicksightPathsModel(BasePathsModel):
    datasets: Optional[str]
    analyses: Optional[str]
    dashboards: Optional[str]
    data_sources: Optional[str]

    class Config:
        dependencies_map = {
            'datasets':     ('datasets',),
            'analyses':     ('analyses',),
            'dashboards':   ('dashboards',),
            'data_sources': ('data_sources',)
        }


class DbtPathsModel(BasePathsModel):
    databases: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'schemas':   ('databases', 'schemas'),
            'tables':    ('databases', 'schemas', 'tables'),
            'columns':   ('databases', 'schemas', 'tables', 'columns'),
        }


# class TableauPathsModel(BasePathsModel):  # todo:
#     schemas: Optional[str]
#     databases: Optional[str]
#     tables: Optional[str]
#     columns: Optional[str]
#     workbooks: Optional[str]
#     worksheets: Optional[str]
#
#     class Config:
#         dependencies_map = {
#             'schemas':    ('schemas',),
#             'databases':  ('schemas', 'databases'),
#             'tables':     ('schemas', 'databases', 'tables'),
#             'columns':    ('schemas', 'databases', 'tables', 'columns'),
#             'workbooks':  ('workbooks',),
#             'worksheets': ('workbooks', 'worksheets'),
#         }
#
#
# class KubeflowPathsModel(BasePathsModel):  # todo:
#     pipelines: Optional[str]
#     experiments: Optional[str]
#     runs: Optional[str]
#
#     class Config:
#         dependencies_map = {
#             'pipelines':   ('pipelines',),
#             'experiments': ('experiments',),
#             'runs':        ('experiments', 'runs',),
#         }
#
#
# class DVCPathsModel(BasePathsModel):  # todo:
#     pass
#
#
# class GreatExpectationsPathsModel(BasePathsModel):  # todo:
#     suits: Optional[str]
#     runs: Optional[str]
#     suits_types: Optional[str] = Field(alias='types')
#     runs_types: Optional[str] = Field(alias='types')
#
#     class Config:
#         dependencies_map = {
#             'suits':        ('suits',),
#             'suits_types':  ('suits', 'suits_types'),
#             'runs':         ('runs',),
#             'runs_types':   ('runs', 'runs_types'),
#         }
