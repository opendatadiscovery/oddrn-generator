from abc import ABC, abstractmethod

from pydantic import BaseModel


class HostSettings(BaseModel):
    host: str


class CloudSettings(BaseModel):
    account: str
    region: str


class AzureCloudSettings(BaseModel):
    domain: str


class ServerModelConfig(BaseModel):
    host_settings: HostSettings = None
    cloud_settings: CloudSettings = None
    azure_cloud_settings: AzureCloudSettings = None


class AbstractServerModel(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @classmethod
    def create(cls, config: ServerModelConfig):
        raise NotImplementedError


class HostnameModel(AbstractServerModel, BaseModel):
    host: str

    def __str__(self) -> str:
        return f"host/{self.host}"

    @classmethod
    def create(cls, config: ServerModelConfig):
        host_settings = config.host_settings

        if host_settings:
            return cls(host=host_settings.host)
        else:
            raise ValueError("You must specify host settings")


class AWSCloudModel(AbstractServerModel, BaseModel):
    account: str
    region: str

    def __str__(self) -> str:
        return f"cloud/aws/{'/'.join('{}/{}'.format(*p) for p in self.dict().items())}"

    @classmethod
    def create(cls, config: ServerModelConfig):
        cloud_settings = config.cloud_settings

        if cloud_settings:
            return cls(account=cloud_settings.account, region=cloud_settings.region)
        else:
            raise ValueError("You must specify cloud settings")


class AzureCloudModel(AbstractServerModel, BaseModel):
    domain: str

    def __str__(self) -> str:
        return (
            f"cloud/azure/{'/'.join('{}/{}'.format(*p) for p in self.dict().items())}"
        )

    @classmethod
    def create(cls, config: ServerModelConfig):
        azure_cloud_settings = config.azure_cloud_settings

        if azure_cloud_settings:
            return cls(domain=azure_cloud_settings.domain)
        else:
            raise ValueError("You must specify cloud settings")


class S3CloudModel(AbstractServerModel, BaseModel):
    """Bucket name is unique across AWS"""

    def __str__(self) -> str:
        return "cloud/aws"

    @classmethod
    def create(cls, config):
        return cls()
