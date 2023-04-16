from oddrn_generator import LambdaGenerator


def test_lambda():
    generator = LambdaGenerator(cloud_settings={"region": "us-east-1", "account": "123456789012"})
    generator.set_oddrn_paths(functions="my_function")
    assert generator.get_oddrn_by_path('functions') == "//lambda/cloud/aws/account/123456789012/region/us-east-1/functions/my_function"

def test_lambda_creation():
    generator = LambdaGenerator.from_params(region="us-east-1", account="123456789012", function_name="my_function")
    assert generator.get_oddrn_by_path('functions') == "//lambda/cloud/aws/account/123456789012/region/us-east-1/functions/my_function"