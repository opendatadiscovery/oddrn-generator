from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, FilePath

from oddrn_generator.exceptions import (
    EmptyPathValueException,
    PathDoesntExistException,
    WrongPathOrderException,
)

DependenciesMap = dict[str, tuple[str, ...]]


class BasePathsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    dependencies_map: DependenciesMap = {}
    data_source_path: str = None
    allows_null: list = []

    def __validate_path(self, field) -> None:
        for deps in reversed(self.dependencies_map.get(field)):
            deps_value = getattr(self, deps, None)
            # allow dependency null if it is in allow_null list
            if deps_value is None and deps in self.allows_null:
                return
            if not deps_value:
                raise WrongPathOrderException(
                    f"'{field}' can not be without '{deps}' attribute"
                )

    def validate_all_paths(self) -> None:
        # hotfix to ignore BasePathsModel's attributes that don't belong to path dependency objects
        model_fields_to_ignore_set = {
            "dependencies_map",
            "data_source_path",
            "allows_null",
        }

        model_fields_set = self.model_fields_set - model_fields_to_ignore_set
        for field in model_fields_set:
            self.__validate_path(field)

    def get_dependency(self, field) -> tuple:
        dependency = self.dependencies_map.get(field)
        if not dependency:
            raise PathDoesntExistException(f"Path '{field}' doesn't exist in generator")
        return dependency

    def check_if_path_is_set(self, path: str) -> None:
        if not getattr(self, path, None):
            raise EmptyPathValueException(f"Path '{path}' is not set up")

    def set_path_value(self, path: str, value: str) -> None:
        setattr(self, path, value)
        self.__validate_path(path)


class PostgresqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")
    relationships: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "relationships": ("databases", "schemas", "tables", "relationships"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: PostgresqlPathsModel._dependencies_map_factory()
    )


class MysqlPathsModel(BasePathsModel):
    databases: str
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: MysqlPathsModel._dependencies_map_factory()
    )


class KafkaPathsModel(BasePathsModel):
    topics: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {"topics": ("topics",)}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: KafkaPathsModel._dependencies_map_factory()
    )


class KafkaConnectorPathsModel(BasePathsModel):
    connectors: str

    @classmethod
    def _dependencies_map_factory(cls):
        return {"connectors": ("connectors",)}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: KafkaConnectorPathsModel._dependencies_map_factory()
    )


class GluePathsModel(BasePathsModel):
    databases: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None
    owners: Optional[str] = None
    jobs: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
            "owners": ("owners",),
            "jobs": ("jobs",),
            "runs": ("jobs", "runs"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: GluePathsModel._dependencies_map_factory()
    )


class SnowflakePathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")
    pipes: Optional[str] = None
    relationships: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "pipes": ("databases", "schemas", "pipes"),
            "relationships": ("databases", "schemas", "tables", "relationships"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: SnowflakePathsModel._dependencies_map_factory()
    )


class AirflowPathsModel(BasePathsModel):
    dags: Optional[str] = None
    tasks: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "dags": ("dags",),
            "tasks": ("dags", "tasks"),
            "runs": ("dags", "tasks", "runs"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: AirflowPathsModel._dependencies_map_factory()
    )


class HivePathsModel(BasePathsModel):
    databases: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")
    owners: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
            "owners": ("owners",),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: HivePathsModel._dependencies_map_factory()
    )


class ElasticSearchPathsModel(BasePathsModel):
    templates: Optional[str] = None
    streams: Optional[str] = None
    indices: Optional[str] = None
    fields: Optional[str] = None
    indices_fields: Optional[str] = Field(None, alias="fields")
    templates_fields: Optional[str] = Field(None, alias="fields")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "indices": ("indices",),
            "indices_fields": ("indices", "indices_fields"),
            "streams": ("streams",),
            "templates": ("templates",),
            "templates_fields": ("templates", "templates_fields"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: ElasticSearchPathsModel._dependencies_map_factory()
    )


class FeastPathsModel(BasePathsModel):
    featureviews: Optional[str] = None
    features: Optional[str] = None
    subfeatures: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "featureviews": ("featureviews",),
            "features": ("featureviews", "features"),
            "subfeatures": ("featureviews", "features", "subfeatures"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: FeastPathsModel._dependencies_map_factory()
    )


class DynamodbPathsModel(BasePathsModel):
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {"tables": ("tables",), "columns": ("tables", "columns")}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DynamodbPathsModel._dependencies_map_factory()
    )


class OdbcPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: OdbcPathsModel._dependencies_map_factory()
    )


class MssqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: MssqlPathsModel._dependencies_map_factory()
    )


class OraclePathsModel(BasePathsModel):
    schemas: str
    databases: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    columns: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "schemas": ("schemas",),
            "databases": ("schemas", "databases"),
            "tables": ("schemas", "databases", "tables"),
            "views": ("schemas", "databases", "views"),
            "tables_columns": ("schemas", "databases", "tables", "tables_columns"),
            "views_columns": ("schemas", "databases", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: OraclePathsModel._dependencies_map_factory()
    )


class RedshiftPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: RedshiftPathsModel._dependencies_map_factory()
    )


class ClickHousePathsModel(BasePathsModel):
    databases: str
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: ClickHousePathsModel._dependencies_map_factory()
    )


class AthenaPathsModel(BasePathsModel):
    catalogs: Optional[str] = None
    databases: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "catalogs": ("catalogs",),
            "databases": ("catalogs", "databases"),
            "tables": ("catalogs", "databases", "tables"),
            "views": ("catalogs", "databases", "views"),
            "tables_columns": ("catalogs", "databases", "tables", "tables_columns"),
            "views_columns": ("catalogs", "databases", "views", "views_columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: AthenaPathsModel._dependencies_map_factory()
    )


class QuicksightPathsModel(BasePathsModel):
    datasets: Optional[str] = None
    analyses: Optional[str] = None
    dashboards: Optional[str] = None
    data_sources: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "datasets": ("datasets",),
            "analyses": ("analyses",),
            "dashboards": ("dashboards",),
            "data_sources": ("data_sources",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: QuicksightPathsModel._dependencies_map_factory()
    )


class DbtPathsModel(BasePathsModel):
    databases: Optional[str] = None
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")
    tests: Optional[str] = None
    runs: Optional[str] = None
    models: Optional[str] = None
    seeds: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "tests": ("databases", "tests"),
            "runs": ("databases", "tests", "runs"),
            "models": ("models",),
            "seeds": ("seeds",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DbtPathsModel._dependencies_map_factory()
    )


class PrefectPathsModel(BasePathsModel):
    flows: str
    tasks: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "flows": ("flows",),
            "tasks": ("flows", "tasks"),
            "runs": ("flows", "tasks", "runs"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: PrefectPathsModel._dependencies_map_factory()
    )


class TableauPathsModel(BasePathsModel):
    sites: str
    databases: Optional[str] = None
    schemas: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None
    workbooks: Optional[str] = None
    sheets: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "sites": ("sites",),
            "databases": ("sites", "databases"),
            "schemas": ("sites", "databases", "schemas"),
            "tables": ("sites", "databases", "schemas", "tables"),
            "columns": ("sites", "databases", "schemas", "tables", "columns"),
            "workbooks": ("sites", "workbooks"),
            "sheets": ("sites", "workbooks", "sheets"),
        }

    allows_null: list = ["schemas"]
    data_source_path: str = "sites"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: TableauPathsModel._dependencies_map_factory()
    )


class Neo4jPathsModel(BasePathsModel):
    databases: str
    nodes: Optional[str] = None
    fields: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "nodes": ("databases", "nodes"),
            "fields": ("databases", "nodes", "fields"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: Neo4jPathsModel._dependencies_map_factory()
    )


class S3PathsModel(BasePathsModel):
    buckets: Optional[str] = None
    keys: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }

    data_source_path: str = "buckets"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: S3PathsModel._dependencies_map_factory()
    )


class S3CustomPathsModel(BasePathsModel):
    buckets: Optional[str] = None
    keys: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }

    data_source_path: str = "buckets"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: S3CustomPathsModel._dependencies_map_factory()
    )


class CassandraPathsModel(BasePathsModel):
    keyspaces: str
    tables: Optional[str] = None
    views: Optional[str] = None
    columns: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "keyspaces": ("keyspaces",),
            "tables": ("keyspaces", "tables"),
            "views": ("keyspaces", "views"),
            "tables_columns": ("keyspaces", "tables", "tables_columns"),
            "views_columns": ("keyspaces", "views", "views_columns"),
        }

    data_source_path: str = "keyspaces"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: CassandraPathsModel._dependencies_map_factory()
    )


class SagemakerPathsModel(BasePathsModel):
    experiments: Optional[str] = None
    trials: Optional[str] = None
    jobs: Optional[str] = None
    artifacts: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "experiments": ("experiments",),
            "trials": ("experiments", "trials"),
            "jobs": ("experiments", "trials", "jobs"),
            "artifacts": ("experiments", "trials", "artifacts"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: SagemakerPathsModel._dependencies_map_factory()
    )


class KubeflowPathsModel(BasePathsModel):
    pipelines: Optional[str] = None
    experiments: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "pipelines": ("pipelines",),
            "experiments": ("experiments",),
            "runs": ("experiments", "runs"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: KubeflowPathsModel._dependencies_map_factory()
    )


class TarantoolPathsModel(BasePathsModel):
    spaces: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {"spaces": ("spaces",), "columns": ("spaces", "columns")}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: TarantoolPathsModel._dependencies_map_factory()
    )


class KinesisPathsModel(BasePathsModel):
    streams: Optional[str] = None
    shards: Optional[str] = None
    data_records: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "streams": ("streams",),
            "shards": ("streams", "shards"),
            "data_records": ("streams", "shards", "data_records"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: KinesisPathsModel._dependencies_map_factory()
    )


class MongoPathsModel(BasePathsModel):
    databases: str
    collections: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "collections": ("databases", "collections"),
            "columns": ("databases", "collections", "columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: MongoPathsModel._dependencies_map_factory()
    )


class VerticaPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: VerticaPathsModel._dependencies_map_factory()
    )


class PrestoPathsModel(BasePathsModel):
    catalogs: Optional[str] = None
    schemas: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: PrestoPathsModel._dependencies_map_factory()
    )


class SupersetPathsModel(BasePathsModel):
    databases: Optional[str] = None
    datasets: Optional[str] = None
    columns: Optional[str] = None
    dashboards: Optional[str] = None
    charts: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "datasets": ("databases", "datasets"),
            "columns": ("databases", "datasets", "columns"),
            "charts": ("charts",),
            "dashboards": ("dashboards",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: SupersetPathsModel._dependencies_map_factory()
    )


class CubeJsPathModel(BasePathsModel):
    cubes: str = ""

    @classmethod
    def _dependencies_map_factory(cls):
        return {"cubes": ("cubes",)}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: CubeJsPathModel._dependencies_map_factory()
    )


class MetabasePathModel(BasePathsModel):
    collections: str = ""
    dashboards: Optional[str] = None
    cards: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "collections": ("collections",),
            "dashboards": ("collections", "dashboards"),
            "cards": ("collections", "cards"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: MetabasePathModel._dependencies_map_factory()
    )


class DmsPathsModel(BasePathsModel):
    tasks: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {"tasks": ("tasks",), "runs": ("tasks", "runs")}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DmsPathsModel._dependencies_map_factory()
    )


class PowerBiPathModel(BasePathsModel):
    datasets: Optional[str] = None
    dashboards: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "datasets": ("datasets",),
            "dashboards": ("dashboards",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: PowerBiPathModel._dependencies_map_factory()
    )


class RedashPathsModel(BasePathsModel):
    queries: Optional[str] = None
    dashboards: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "queries": ("queries",),
            "dashboards": ("dashboards",),
            "jobs": ("jobs",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: RedashPathsModel._dependencies_map_factory()
    )


class AirbytePathsModel(BasePathsModel):
    connections: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "connections": ("connections",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: AirbytePathsModel._dependencies_map_factory()
    )


class FilesystemPathModel(BasePathsModel):
    path: Optional[str] = None
    fields: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {"path": ("path",), "fields": ("path", "fields")}

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: FilesystemPathModel._dependencies_map_factory()
    )


class GreatExpectationsPathsModel(BasePathsModel):
    suites: Optional[str] = None
    types: Optional[str] = None
    runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "suites": ("suites",),
            "types": ("suites", "types"),
            "runs": ("suites", "types", "runs"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: GreatExpectationsPathsModel._dependencies_map_factory()
    )


class DatabricksLakehousePathModel(BasePathsModel):
    databases: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DatabricksLakehousePathModel._dependencies_map_factory()
    )


class DatabricksUnityCatalogPathModel(BasePathsModel):
    catalogs: Optional[str] = None
    schemas: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DatabricksUnityCatalogPathModel._dependencies_map_factory()
    )


class DatabricksFeatureStorePathModel(BasePathsModel):
    databases: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DatabricksFeatureStorePathModel._dependencies_map_factory()
    )


class SingleStorePathsModel(BasePathsModel):
    databases: str
    tables: Optional[str] = None
    views: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: SingleStorePathsModel._dependencies_map_factory()
    )


class AzureSQLPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    columns: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }

    data_source_path: str = "databases"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: AzureSQLPathsModel._dependencies_map_factory()
    )


class FivetranPathsModel(BasePathsModel):
    transformers: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "transformers": ("transformers",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: FivetranPathsModel._dependencies_map_factory()
    )


class LambdaPathsModel(BasePathsModel):
    functions: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "functions": ("functions",),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: LambdaPathsModel._dependencies_map_factory()
    )


class CouchbasePathsModel(BasePathsModel):
    buckets: str
    scopes: Optional[str] = None
    collections: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "buckets": ("buckets",),
            "scopes": ("buckets", "scopes"),
            "collections": ("buckets", "scopes", "collections"),
            "columns": ("buckets", "scopes", "collections", "columns"),
        }

    data_source_path: str = "buckets"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: CouchbasePathsModel._dependencies_map_factory()
    )


class SQLitePathsModel(BasePathsModel):
    path: Optional[FilePath] = None
    tables: Optional[str] = None
    views: Optional[str] = None
    columns: Optional[str] = None
    tables_columns: Optional[str] = Field(None, alias="columns")
    views_columns: Optional[str] = Field(None, alias="columns")

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "path": ("path",),
            "tables": ("path", "tables"),
            "views": ("path", "views"),
            "tables_columns": ("path", "tables", "tables_columns"),
            "views_columns": ("path", "views", "views_columns"),
        }

    data_source_path: str = "path"
    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: SQLitePathsModel._dependencies_map_factory()
    )


class BigTablePathsModel(BasePathsModel):
    instances: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "instances": ("instances",),
            "tables": ("instances", "tables"),
            "columns": ("instances", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: BigTablePathsModel._dependencies_map_factory()
    )


class DuckDBPathsModel(BasePathsModel):
    catalogs: Optional[str] = None
    schemas: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: DuckDBPathsModel._dependencies_map_factory()
    )


class GCSPathsModel(BasePathsModel):
    buckets: Optional[str] = None
    keys: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: GCSPathsModel._dependencies_map_factory()
    )


class BlobPathsModel(BasePathsModel):
    keys: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "keys": ("keys",),
            "columns": (
                "keys",
                "columns",
            ),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: BlobPathsModel._dependencies_map_factory()
    )


class BigQueryStoragePathsModel(BasePathsModel):
    datasets: Optional[str] = None
    tables: Optional[str] = None
    columns: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "datasets": ("datasets",),
            "tables": ("datasets", "tables"),
            "columns": ("datasets", "tables", "columns"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: BigQueryStoragePathsModel._dependencies_map_factory()
    )


class CKANPathsModel(BasePathsModel):
    organizations: Optional[str] = None
    groups: Optional[str] = None
    datasets: Optional[str] = None
    resources: Optional[str] = None
    fields: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "organizations": ("organizations",),
            "groups": ("groups",),
            "datasets": ("organizations", "datasets"),
            "resources": ("organizations", "datasets", "resources"),
            "fields": ("organizations", "datasets", "resources", "fields"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: CKANPathsModel._dependencies_map_factory()
    )


class AzureDataFactoryPathsModel(BasePathsModel):
    factories: Optional[str] = None
    datasets: Optional[str] = None
    pipelines: Optional[str] = None
    pipelines_runs: Optional[str] = None
    activities: Optional[str] = None
    activities_runs: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "factories": ("factories",),
            "datasets": ("factories", "datasets"),
            "pipelines": ("factories", "pipelines"),
            "pipelines_runs": ("factories", "pipelines", "pipelines_runs"),
            "activities": ("factories", "pipelines", "activities"),
            "activities_runs": (
                "factories",
                "pipelines",
                "activities",
                "activities_runs",
            ),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: AzureDataFactoryPathsModel._dependencies_map_factory()
    )


class ApiPathsModel(BasePathsModel):
    resources: Optional[str] = None
    fields: Optional[str] = None

    @classmethod
    def _dependencies_map_factory(cls):
        return {
            "resources": ("resources",),
            "fields": ("resources", "fields"),
        }

    dependencies_map: DependenciesMap = Field(
        default_factory=lambda: ApiPathsModel._dependencies_map_factory()
    )
