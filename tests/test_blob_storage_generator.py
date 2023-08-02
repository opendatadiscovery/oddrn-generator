import pytest

from oddrn_generator.generators import AzureBlobStorageGenerator


def test_blob_storage_generator():
    generator = AzureBlobStorageGenerator(
        azure_cloud_settings={
            "account": "test_account_name",
            "container": "test_container_name"
        }
    )
    generator.set_oddrn_paths(keys="test.csv", columns="age")

    # Data source oddrn.
    assert (
        generator.get_data_source_oddrn()
        == "//blob_storage/cloud/azure/account/test_account_name/container/test_container_name"
    )

    # Oddrn by path.
    assert (
        generator.get_oddrn_by_path("columns")
        == "//blob_storage/cloud/azure/account/test_account_name/container/test_container_name/keys/test.csv/columns/age"
    )


def test_blob_storage_generator_with_empty_params():
    """
    Empty the azure_cloud_settings params.
    Expected value: {'account_name': 'account_name', 'container_name': 'container_name'}
    """

    with pytest.raises(ValueError):
        generator = AzureBlobStorageGenerator(
            azure_cloud_settings=None
        )
