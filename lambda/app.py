# Lambda handler placeholder
# This file will contain the Lambda function for invoking the SageMaker endpoint.

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Lambda is configured correctly."
    }
