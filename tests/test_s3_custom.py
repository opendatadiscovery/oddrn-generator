from oddrn_generator.generators import S3CustomGenerator
from oddrn_generator.utils import escape


def test_generator():
    generator = S3CustomGenerator(endpoint="localhost:9000")
    assert generator.get_data_source_oddrn() == "//s3-custom/endpoint/localhost:9000"

    generator.set_oddrn_paths(buckets="bucket1")
    assert (
        generator.get_oddrn_by_path("buckets")
        == "//s3-custom/endpoint/localhost:9000/buckets/bucket1"
    )

    generator.set_oddrn_paths(keys="object1")
    assert (
        generator.get_oddrn_by_path("keys")
        == "//s3-custom/endpoint/localhost:9000/buckets/bucket1/keys/object1"
    )

    generator.set_oddrn_paths(columns="age")
    assert (
        generator.get_oddrn_by_path("columns")
        == "//s3-custom/endpoint/localhost:9000/buckets/bucket1/keys/object1/columns/age"
    )

    generator.set_oddrn_paths(keys="object2/object3")
    assert (
        generator.get_oddrn_by_path("keys")
        == "//s3-custom/endpoint/localhost:9000/buckets/bucket1/keys/object2\\\\object3"
    )
