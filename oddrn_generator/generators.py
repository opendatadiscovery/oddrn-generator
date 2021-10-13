from oddrn_generator.path_models import (
    BasePathsModel, PostgresqlPathsModel, MysqlPathsModel, KafkaPathsModel, GluePathsModel, SnowflakePathsModel,
    AirflowPathsModel, HivePathsModel, DynamodbPathsModel, OdbcPathsModel,
    MssqlPathsModel, OraclePathsModel, RedshiftPathsModel, ClickHousePathsModel, KafkaConnectorPathsModel,
    AthenaPathsModel, QuicksightPathsModel, DbtPathsModel
)
from oddrn_generator.server_models import AbstractServerModel, AWSCloudModel, HostnameModel


class Generator:
    source: str = None
    server_model = None
    paths_model = None

    def __init__(self, *, cloud_settings: dict = None, host_settings: str = None, **path_attributes):
        if cloud_settings:
            server_settings = cloud_settings
        elif host_settings:
            server_settings = {'host': host_settings}
        else:
            raise ValueError("You must specify at least one parameter: 'cloud_settings' or 'host_settings'")
        self.server_obj: AbstractServerModel = self.__build_server(server_settings)
        self.paths_obj: BasePathsModel = self.__build_paths(**path_attributes)

    def __build_server(self, server: dict) -> AbstractServerModel:
        return self.server_model(**server)

    def __build_paths(self, **paths) -> BasePathsModel:
        path_obj: BasePathsModel = self.paths_model(**paths)
        path_obj.validate_all_paths()
        return path_obj

    @property
    def base_oddrn(self) -> str:
        return f"//{self.source}/{self.server_obj}/"

    @property
    def available_paths(self) -> tuple:
        return tuple(self.paths_obj.__config__.dependencies_map.keys())

    def get_oddrn_by_path(self, path: str, new_value: str = None) -> str:
        dependency = self.paths_obj.get_dependency(path)
        if new_value:
            self.paths_obj.set_path_value(path, new_value)
        else:
            self.paths_obj.check_if_path_is_set(path)
        paths_dict = self.paths_obj.dict(include=set(dependency), exclude_none=True, by_alias=True)
        return self.base_oddrn + '/'.join([f'{k}/{v}' for k, v in paths_dict.items()])

    def set_oddrn_paths(self, **new_paths) -> None:
        old_paths = {
            k: v for k, v in self.paths_obj.dict(exclude_none=True).items() if k not in [f for f in new_paths.keys()]
        }
        self.paths_obj = self.__build_paths(**old_paths, **new_paths)

    def get_data_source_oddrn(self):
        return self.get_oddrn_by_path(self.paths_obj.data_source_path) if self.paths_obj.data_source_path else self.base_oddrn


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


# class TableauGenerator(Generator):  # todo:
#     source = "tableau"
#     path_model = TableauPathsModel
#     server_model = HostnameModel
#
#
# class KubeflowGenerator(Generator):  # todo:
#     source = "kubeflow"
#     path_model = KubeflowPathsModel
#     server_model = AWSCloudModel
#
#
# class DVCGenerator(Generator):  # todo:
#     source = "dvc"
#     path_model = DVCPathsModel
#     server_model = HostnameModel
#
#
# class GreatExpectationsGenerator(Generator):  # todo:
#     source = "great_expectations"
#     paths_model = GreatExpectationsPathsModel
#     server_model = AWSCloudModel
