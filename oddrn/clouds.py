from dataclasses import dataclass


@dataclass
class AWS:
    region: str
    account: str

    def get_oddrn(self):
        return f"aws/regions/{self.region}/accounts/{self.account}"


cloud_map = {
    "aws": AWS
}
