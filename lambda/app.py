import json
import os
# import boto3  # Uncomment when integrating with SageMaker


def lambda_handler(event, context):
    """
    Basic Lambda handler for the reInvent-2025-ML-API-by-SG project.

    For now, this:
    - Accepts a JSON payload with a "text" field
    - Returns a fake sentiment result (POSITIVE/NEGATIVE)
    - Is structured so we can later plug in a real SageMaker endpoint

    Future plan:
    - Read the SageMaker endpoint name from the SAGEMAKER_ENDPOINT_NAME environment variable
    - Use boto3 + SageMaker Runtime to get a true model prediction
    """

    try:
        # If the request comes from API Gateway HTTP API, the body is a JSON string
        if "body" in event and event["body"]:
            body = json.loads(event["body"])
        else:
            # Allow direct Lambda test invocation with a JSON object
            body = event

        text = body.get("text")

        if not text:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing 'text' field in request body"})
            }

        # --------------------------------------------------------------------
        # Placeholder "AI" logic for now (simple heuristic sentiment)
        # --------------------------------------------------------------------
        lowered = text.lower()
        if any(word in lowered for word in ["love", "great", "excited", "amazing", "happy"]):
            sentiment = "POSITIVE"
            score = 0.95
        else:
            sentiment = "NEGATIVE"
            score = 0.65

        # --------------------------------------------------------------------
        # Future SageMaker Integration (design only for now)
        #
        # endpoint_name = os.getenv("SAGEMAKER_ENDPOINT_NAME")
        #
        # if endpoint_name:
        #     runtime = boto3.client("sagemaker-runtime")
        #     sm_response = runtime.invoke_endpoint(
        #         EndpointName=endpoint_name,
        #         ContentType="application/json",
        #         Body=json.dumps({"text": text})
        #     )
        #     result = json.loads(sm_response["Body"].read())
        #     sentiment = result.get("label", sentiment)
        #     score = result.get("score", score)
        #
        # This makes it easy to switch from mock logic → real ML model
        # just by:
        #   1. Deploying a SageMaker endpoint
        #   2. Setting the SAGEMAKER_ENDPOINT_NAME environment variable
        # --------------------------------------------------------------------

        response = {
            "input_text": text,
            "label": sentiment,
            "score": score
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response)
        }

    except Exception as e:
        # Basic error handling for debugging
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
