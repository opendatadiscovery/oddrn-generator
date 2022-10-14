from typing import Type
from urllib.parse import urlparse

from oddrn_generator.path_models import (
    AirflowPathsModel,
    AthenaPathsModel,
    BasePathsModel,
    CassandraPathsModel,
    ClickHousePathsModel,
    CubeJsPathModel,
    DmsPathsModel,
    DbtPathsModel,
    DynamodbPathsModel,
    ElasticSearchPathsModel,
    FeastPathsModel,
    GluePathsModel,
    HivePathsModel,
    KafkaConnectorPathsModel,
    KafkaPathsModel,
    KinesisPathsModel,
    KubeflowPathsModel,
    MetabasePathModel,
    MongoPathsModel,
    MssqlPathsModel,
    MysqlPathsModel,
    Neo4jPathsModel,
    OdbcPathsModel,
    OraclePathsModel,
    PostgresqlPathsModel,
    PowerBiPathModel,
    PrefectPathsModel,
    PrestoPathsModel,
    RedashPathsModel,
    QuicksightPathsModel,
    RedshiftPathsModel,
    S3PathsModel,
    SagemakerPathsModel,
    SnowflakePathsModel,
    SupersetPathsModel,
    TableauPathsModel,
    TarantoolPathsModel,
    VerticaPathsModel,
)
from oddrn_generator.server_models import (
    AbstractServerModel,
    AWSCloudModel,
    AzureCloudSettings,
    AzureCloudModel,
    CloudSettings,
    HostnameModel,
    HostSettings,
    S3CloudModel,
    ServerModelConfig,
)

from .utils import escape


class Generator:
    source: str = None
    server_model: Type[AbstractServerModel] = None
    paths_model: Type[BasePathsModel] = None

    def __new__(cls, *args, **kwargs):
        # TODO: didn't find any case when kwargs has data_source
        if not kwargs.get("data_source"):
            return super(Generator, cls).__new__(cls)

        # TODO: looks like useless statement
        subclass = {subclass.source: subclass for subclass in cls.__subclasses__()}.get(
            kwargs["data_source"]
        )

        if not subclass:
            raise ValueError("data_source is invalid")

        return super(Generator, subclass).__new__(subclass)

    def __init__(
        self,
        *,
        data_source=None,
        cloud_settings: dict = None,
        azure_cloud_settings: dict = None,
        host_settings: str = None,
        **paths,
    ):
        config = ServerModelConfig(
            cloud_settings=CloudSettings(**cloud_settings) if cloud_settings else None,
            azure_cloud_settings=AzureCloudSettings(**azure_cloud_settings)
            if azure_cloud_settings
            else None,
            host_settings=HostSettings(host=host_settings) if host_settings else None,
        )

        self.server_obj: AbstractServerModel = self.server_model.create(config)
        self.paths_obj: BasePathsModel = self.__build_paths(**paths)

    def __build_paths(self, **paths) -> BasePathsModel:
        escaped = {k: escape(v) for k, v in paths.items()}

        path_obj: BasePathsModel = self.paths_model(**escaped)
        path_obj.validate_all_paths()
        return path_obj

    @property
    def base_oddrn(self) -> str:
        return f"//{self.source}/{self.server_obj}"

    @property
    def available_paths(self) -> tuple:
        return tuple(self.paths_obj.__config__.dependencies_map.keys())

    def get_oddrn_by_path(self, path: str, new_value: str = None) -> str:
        dependency = self.paths_obj.get_dependency(path)
        if new_value:
            self.paths_obj.set_path_value(path, new_value)
        else:
            self.paths_obj.check_if_path_is_set(path)
        paths_dict = self.paths_obj.dict(
            include=set(dependency), exclude_none=True, by_alias=True
        )
        return (
            f"{self.base_oddrn}/{'/'.join([f'{k}/{v}' for k, v in paths_dict.items()])}"
        )

    def set_oddrn_paths(self, **new_paths) -> None:
        old_paths = {
            k: v
            for k, v in self.paths_obj.dict(exclude_none=True).items()
            if k not in list(new_paths.keys())
        }

        self.paths_obj = self.__build_paths(**old_paths, **new_paths)

    def get_data_source_oddrn(self):
        return (
            self.get_oddrn_by_path(self.paths_obj.data_source_path)
            if self.paths_obj.data_source_path
            else self.base_oddrn
        )


class PostgresqlGenerator(Generator):
    source = "postgresql"
    paths_model = PostgresqlPathsModel
    server_model = HostnameModel


class GlueGenerator(Generator):
    source = "glue"
    paths_model = GluePathsModel
    server_model = AWSCloudModel


class MysqlGenerator(Generator):
    source = "mysql"
    paths_model = MysqlPathsModel
    server_model = HostnameModel


class KafkaGenerator(Generator):
    source = "kafka"
    paths_model = KafkaPathsModel
    server_model = HostnameModel


class KafkaConnectGenerator(Generator):
    source = "kafkaconnect"
    paths_model = KafkaConnectorPathsModel
    server_model = HostnameModel


class SnowflakeGenerator(Generator):
    source = "snowflake"
    paths_model = SnowflakePathsModel
    server_model = HostnameModel


class AirflowGenerator(Generator):
    source = "airflow"
    paths_model = AirflowPathsModel
    server_model = HostnameModel


class HiveGenerator(Generator):
    source = "hive"
    paths_model = HivePathsModel
    server_model = HostnameModel


class ElasticSearchGenerator(Generator):
    source = "elasticsearch"
    paths_model = ElasticSearchPathsModel
    server_model = HostnameModel


class FeastGenerator(Generator):
    source = "feast"
    paths_model = FeastPathsModel
    server_model = HostnameModel


class DynamodbGenerator(Generator):
    source = "dynamodb"
    paths_model = DynamodbPathsModel
    server_model = AWSCloudModel


class OdbcGenerator(Generator):
    source = "odbc"
    paths_model = OdbcPathsModel
    server_model = HostnameModel


class MssqlGenerator(Generator):
    source = "mssql"
    paths_model = MssqlPathsModel
    server_model = HostnameModel


class OracleGenerator(Generator):
    source = "oracle"
    paths_model = OraclePathsModel
    server_model = HostnameModel


class PrestoGenerator(Generator):
    source = "presto"
    paths_model = PrestoPathsModel
    server_model = HostnameModel


class TrinoGenerator(PrestoGenerator):
    source = "trino"


class RedshiftGenerator(Generator):
    source = "redshift"
    paths_model = RedshiftPathsModel
    server_model = HostnameModel


class ClickHouseGenerator(Generator):
    source = "clickhouse"
    paths_model = ClickHousePathsModel
    server_model = HostnameModel


class AthenaGenerator(Generator):
    source = "athena"
    paths_model = AthenaPathsModel
    server_model = AWSCloudModel


class QuicksightGenerator(Generator):
    source = "quicksight"
    paths_model = QuicksightPathsModel
    server_model = AWSCloudModel


class DbtGenerator(Generator):
    source = "dbt"
    paths_model = DbtPathsModel
    server_model = HostnameModel


class TableauGenerator(Generator):
    source = "tableau"
    paths_model = TableauPathsModel
    server_model = HostnameModel


class PrefectGenerator(Generator):
    source = "prefect"
    paths_model = PrefectPathsModel
    server_model = HostnameModel


class Neo4jGenerator(Generator):
    source = "neo4j"
    paths_model = Neo4jPathsModel
    server_model = HostnameModel


class S3Generator(Generator):
    source = "s3"
    paths_model = S3PathsModel
    server_model = S3CloudModel

    @classmethod
    def from_s3_url(cls, url: str):
        parsed = urlparse(url)
        bucket = parsed.netloc
        keys = parsed.path.lstrip("/")

        generator = cls()
        generator.set_oddrn_paths(buckets=bucket, keys=keys)

        return generator


class CassandraGenerator(Generator):
    source = "cassandra"
    paths_model = CassandraPathsModel
    server_model = HostnameModel


class SagemakerGenerator(Generator):
    source = "sagemaker"
    paths_model = SagemakerPathsModel
    server_model = AWSCloudModel


class KinesisGenerator(Generator):
    source = "kinesis"
    paths_model = KinesisPathsModel
    server_model = AWSCloudModel


class KubeflowGenerator(Generator):
    source = "kubeflow"
    paths_model = KubeflowPathsModel
    server_model = HostnameModel


class TarantoolGenerator(Generator):
    source = "tarantool"
    paths_model = TarantoolPathsModel
    server_model = HostnameModel


class MongoGenerator(Generator):
    source = "mongo"
    paths_model = MongoPathsModel
    server_model = HostnameModel


class VerticaGenerator(Generator):
    source = "vertica"
    paths_model = VerticaPathsModel
    server_model = HostnameModel


class CubeJsGenerator(Generator):
    source = "cubejs"
    paths_model = CubeJsPathModel
    server_model = HostnameModel


class SupersetGenerator(Generator):
    source = "superset"
    paths_model = SupersetPathsModel
    server_model = HostnameModel


class MetabaseGenerator(Generator):
    source = "metabase"
    paths_model = MetabasePathModel
    server_model = HostnameModel


class DmsGenerator(Generator):
    source = "dms"
    paths_model = DmsPathsModel
    server_model = AWSCloudModel


class PowerBiGenerator(Generator):
    source = "powerbi"
    paths_model = PowerBiPathModel
    server_model = AzureCloudModel


class RedashGenerator(Generator):
    source = "redash"
    paths_model = RedashPathsModel
    server_model = HostnameModel


#
#
# class DVCGenerator(Generator):  # todo:
#     source = "dvc"
#     paths_model = DVCPathsModel
#     server_model = HostnameModel
#
#
# class GreatExpectationsGenerator(Generator):  # todo:
#     source = "great_expectations"
#     paths_model = GreatExpectationsPathsModel
#     server_model = AWSCloudModel
