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


def response_body(response):
    return json.loads(response["body"])


class LambdaHandlerTests(unittest.TestCase):
    def test_returns_positive_sentiment_with_keyword_evidence(self):
        response = lambda_handler(
            {"text": "I love this workshop and the results are amazing"}, None
        )

        self.assertEqual(response["statusCode"], 200)
        body = response_body(response)
        self.assertEqual(body["label"], "POSITIVE")
        self.assertEqual(body["method"], "keyword_heuristic")
        self.assertEqual(body["matched_keywords"]["positive"], ["amazing", "love"])

    def test_returns_negative_sentiment_with_keyword_evidence(self):
        response = lambda_handler(
            {"text": "This was disappointing and frustrating"}, None
        )

        self.assertEqual(response["statusCode"], 200)
        body = response_body(response)
        self.assertEqual(body["label"], "NEGATIVE")
        self.assertEqual(
            body["matched_keywords"]["negative"], ["disappointing", "frustrating"]
        )

    def test_returns_neutral_when_no_keywords_match(self):
        response = lambda_handler({"text": "The workshop starts at noon"}, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response_body(response)["label"], "NEUTRAL")

    def test_returns_neutral_when_positive_and_negative_matches_tie(self):
        response = lambda_handler({"text": "great but frustrating"}, None)

        self.assertEqual(response_body(response)["label"], "NEUTRAL")

    def test_matches_complete_tokens_instead_of_substrings(self):
        response = lambda_handler({"text": "The greatest session"}, None)

        self.assertEqual(response_body(response)["label"], "NEUTRAL")

    def test_accepts_api_gateway_body_shape_and_trims_text(self):
        response = lambda_handler(
            {"body": json.dumps({"text": "  happy to test this API  "})}, None
        )

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response_body(response)["input_text"], "happy to test this API")

    def test_rejects_missing_or_non_string_text(self):
        for payload in ({}, {"text": None}, {"text": 42}, {"text": []}):
            with self.subTest(payload=payload):
                response = lambda_handler(payload, None)
                self.assertEqual(response["statusCode"], 400)
                self.assertNotIn("Traceback", response["body"])

    def test_rejects_blank_text(self):
        response = lambda_handler({"text": "   "}, None)

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(
            response_body(response)["error"], "Field 'text' must not be empty"
        )

    def test_rejects_malformed_json_without_exception_details(self):
        response = lambda_handler({"body": "{not-json"}, None)

        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(
            response_body(response)["error"], "Request body must be valid JSON"
        )
        self.assertNotIn("Expecting", response["body"])

    def test_rejects_non_object_request_shapes(self):
        for event in (None, [], "text", {"body": "[]"}, {"body": '"text"'}):
            with self.subTest(event=event):
                response = lambda_handler(event, None)
                self.assertEqual(response["statusCode"], 400)
                self.assertIn("JSON object", response_body(response)["error"])

    def test_rejects_oversized_text(self):
        response = lambda_handler(
            {"text": "x" * (MODULE.MAX_TEXT_LENGTH + 1)}, None
        )

        self.assertEqual(response["statusCode"], 413)
        self.assertIn(str(MODULE.MAX_TEXT_LENGTH), response["body"])

    def test_rejects_oversized_raw_body_before_parsing(self):
        response = lambda_handler(
            {"body": " " * (MODULE.MAX_BODY_LENGTH + 1)}, None
        )

        self.assertEqual(response["statusCode"], 413)
        self.assertIn(str(MODULE.MAX_BODY_LENGTH), response["body"])


if __name__ == "__main__":
    unittest.main()
