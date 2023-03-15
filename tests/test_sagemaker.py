from oddrn_generator.generators import SagemakerGenerator


def test_sagemaker():
    generator = SagemakerGenerator(
        cloud_settings={"account": "account", "region": "region"}
    )

    assert generator.base_oddrn == "//sagemaker/cloud/aws/account/account/region/region"
    assert generator.available_paths == ("experiments", "trials", "jobs", "artifacts")

    generator.set_oddrn_paths(experiments="A")
    assert (
        generator.get_oddrn_by_path("experiments")
        == f"{generator.base_oddrn}/experiments/A"
    )

    generator.set_oddrn_paths(trials="B")
    assert (
        generator.get_oddrn_by_path("trials")
        == f"{generator.base_oddrn}/experiments/A/trials/B"
    )

    generator.set_oddrn_paths(experiments="C")

    assert (
        generator.get_oddrn_by_path("trials")
        == f"{generator.base_oddrn}/experiments/C/trials/B"
    )

    generator.set_oddrn_paths(**{"jobs": "JobD"})

    assert (
        generator.get_oddrn_by_path("jobs")
        == f"{generator.base_oddrn}/experiments/C/trials/B/jobs/JobD"
    )

    generator.set_oddrn_paths(**{"artifacts": "artifactE"})

    assert (
        generator.get_oddrn_by_path("artifacts")
        == f"{generator.base_oddrn}/experiments/C/trials/B/artifacts/artifactE"
    )
