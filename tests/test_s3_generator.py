import pytest

from oddrn_generator.exceptions import EmptyPathValueException, WrongPathOrderException
from oddrn_generator.generators import S3Generator


def test_s3_generator():
    generator = S3Generator(buckets="accounts")
    generator.set_oddrn_paths(keys="developers.csv", columns="age")

    assert (
        generator.get_oddrn_by_path("columns")
        == "//s3/cloud/aws/buckets/accounts/keys/developers.csv/columns/age"
    )


def test_s3_generator_from_s3_url():
    generator = S3Generator.from_s3_url("s3://accounts/company/developers/middle.csv")
    assert (
        generator.get_oddrn_by_path("keys")
        == "//s3/cloud/aws/buckets/accounts/keys/company\\\\developers\\\\middle.csv"
    )


def test_s3_generator_with_empty_bucket():
    generator = S3Generator()

    with pytest.raises(WrongPathOrderException):
        generator.set_oddrn_paths(keys="developers.csv", columns="age")

    with pytest.raises(EmptyPathValueException):
        generator.get_data_source_oddrn()
