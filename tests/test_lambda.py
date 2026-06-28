import importlib.util
import json
import pathlib
import unittest

APP_PATH = pathlib.Path(__file__).resolve().parents[1] / "lambda" / "app.py"
SPEC = importlib.util.spec_from_file_location("lambda_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
lambda_handler = MODULE.lambda_handler


class LambdaHandlerTests(unittest.TestCase):
    def test_returns_positive_sentiment_for_positive_words(self):
        event = {"text": "I love this workshop and the results are amazing"}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["label"], "POSITIVE")
        self.assertGreaterEqual(body["score"], 0.9)

    def test_returns_negative_sentiment_for_non_positive_text(self):
        event = {"text": "This was disappointing and frustrating"}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["label"], "NEGATIVE")

    def test_accepts_api_gateway_body_shape(self):
        event = {"body": json.dumps({"text": "happy to test this API"})}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["input_text"], "happy to test this API")

    def test_returns_400_when_text_is_missing(self):
        event = {"body": json.dumps({})}

        response = lambda_handler(event, None)

        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("Missing 'text' field", body["error"])


if __name__ == "__main__":
    unittest.main()
