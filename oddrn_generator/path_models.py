from typing import Optional

from pydantic import BaseModel

from oddrn_generator.exceptions import WrongPathOrderException, PathDoestExistException, EmptyPathValueException


class BasePathsModel(BaseModel):
    class Config:
        dependencies_map = {}
        data_source_path = None
        allows_null = []
        extra = 'forbid'
        allow_population_by_field_name = True

    def __validate_path(self, field) -> None:
        for deps in reversed(self.__config__.dependencies_map[field]):
            deps_value = getattr(self, deps, None)
            # allow dependency null if it is in allow_null list
            if deps_value is None and deps in self.__config__.allows_null:
                return
            if not deps_value:
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
    topics: Optional[str]

    class Config:
        dependencies_map = {
            'topics':    ('topics',),
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
    warehouses: str
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
            'owners':     ('warehouses', 'databases', 'owners'),
        }
        data_source_path = 'warehouses'


class AirflowPathsModel(BasePathsModel):
    dags: Optional[str]
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            'dags':        ('dags',),
            'tasks':       ('dags', 'tasks'),
            'runs':        ('dags', 'tasks', 'runs'),
        }


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
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'tables':     ('tables',),
            'columns':    ('tables', 'columns'),
        }


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
    columns: Optional[str]

    class Config:
        dependencies_map = {
            'catalogs':  ('catalogs',),
            'databases': ('catalogs', 'databases'),
            'tables':    ('catalogs', 'databases', 'tables'),
            'columns':   ('catalogs', 'databases', 'tables', 'columns'),
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


class PrefectPathsModel(BasePathsModel):
    flows: str
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            'flows':       ('flows',),
            'tasks':       ('flows', 'tasks'),
            'runs':        ('flows', 'tasks', 'runs'),
        }


class TableauPathsModel(BasePathsModel):
    sites: str
    databases: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]
    workbooks: Optional[str]
    sheets: Optional[str]

    class Config:
        dependencies_map = {
            'sites':      ('sites',),
            'databases':  ('sites', 'databases',),
            'schemas':    ('sites', 'databases', 'schemas'),
            'tables':     ('sites', 'databases', 'schemas', 'tables'),
            'columns':    ('sites', 'databases', 'schemas', 'tables', 'columns'),
            'workbooks':  ('sites', 'workbooks',),
            'sheets':     ('sites', 'workbooks', 'sheets'),
        }
        data_source_path = 'sites'
        allows_null = ['schemas']


class Neo4jPathsModel(BasePathsModel):
    databases: str
    nodes: Optional[str]

    class Config:
        dependencies_map = {
            'databases': ('databases',),
            'nodes':    ('databases', 'nodes'),
        }
        data_source_path = 'databases'


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
