"""Bounded Lambda handler for an educational sentiment-classification lab."""

import json

MAX_TEXT_LENGTH = 2_000
MAX_BODY_LENGTH = 8_192
POSITIVE_KEYWORDS = frozenset({"amazing", "excited", "great", "happy", "love"})
NEGATIVE_KEYWORDS = frozenset(
    {"angry", "disappointing", "frustrating", "hate", "sad", "terrible"}
)


def _response(status_code, payload):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }


def _parse_body(event):
    if not isinstance(event, dict):
        return None, _response(400, {"error": "Request must be a JSON object"})

    body = event.get("body", event)
    if isinstance(body, str):
        if len(body) > MAX_BODY_LENGTH:
            return None, _response(
                413,
                {"error": f"Request body must be {MAX_BODY_LENGTH} characters or fewer"},
            )
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return None, _response(400, {"error": "Request body must be valid JSON"})

    if not isinstance(body, dict):
        return None, _response(400, {"error": "Request body must be a JSON object"})

    text = body.get("text")
    if not isinstance(text, str):
        return None, _response(400, {"error": "Field 'text' must be a string"})

    text = text.strip()
    if not text:
        return None, _response(400, {"error": "Field 'text' must not be empty"})
    if len(text) > MAX_TEXT_LENGTH:
        return None, _response(
            413,
            {"error": f"Field 'text' must be {MAX_TEXT_LENGTH} characters or fewer"},
        )

    return text, None


def classify_sentiment(text):
    """Return a deterministic label and the matched keyword evidence."""

    tokens = {token.strip(".,!?;:'\"()[]{}").lower() for token in text.split()}
    positive_matches = sorted(tokens & POSITIVE_KEYWORDS)
    negative_matches = sorted(tokens & NEGATIVE_KEYWORDS)

    if len(positive_matches) > len(negative_matches):
        label = "POSITIVE"
    elif len(negative_matches) > len(positive_matches):
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return label, {
        "positive": positive_matches,
        "negative": negative_matches,
    }


def lambda_handler(event, context):
    """Handle direct Lambda or API Gateway HTTP API invocation."""

    del context  # The deterministic lab does not use runtime context.
    text, error_response = _parse_body(event)
    if error_response is not None:
        return error_response

    label, matches = classify_sentiment(text)
    return _response(
        200,
        {
            "input_text": text,
            "label": label,
            "method": "keyword_heuristic",
            "matched_keywords": matches,
        },
    )
