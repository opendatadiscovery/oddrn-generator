from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractServerModel(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class HostnameModel(AbstractServerModel, BaseModel):
    host: str

    def __str__(self) -> str:
        return f"host/{self.host}"


class AWSCloudModel(AbstractServerModel, BaseModel):
    account: str
    region: str

    def __str__(self) -> str:
        return f"cloud/aws/{'/'.join('{}/{}'.format(*p) for p in self.dict().items())}"

