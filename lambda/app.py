import json

def lambda_handler(event, context):
    """
    Basic Lambda handler for the reInvent-2025-ML-API-by-SG project.

    For now, this:
    - Accepts a JSON payload with a "text" field
    - Returns a fake sentiment result (POSITIVE/NEGATIVE)
    - Is structured so we can later plug in a real SageMaker endpoint
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

        # --- Placeholder "AI" logic for now ---
        lowered = text.lower()
        if any(word in lowered for word in ["love", "great", "excited", "amazing", "happy"]):
            sentiment = "POSITIVE"
            score = 0.95
        else:
            sentiment = "NEGATIVE"
            score = 0.65

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
