# reInvent 2025 Serverless Sentiment API Lab

This repository is a compact AWS serverless lab built around Terraform, Lambda, API Gateway, IAM, and CloudWatch logging.

It exposes a single `/predict` endpoint backed by a Python Lambda function. The current sentiment logic is intentionally lightweight and deterministic; it is a placeholder seam for a future real model integration rather than a claim of deployed SageMaker inference.

## What this project demonstrates

- Terraform-driven provisioning for a small AWS API surface
- Lambda + API Gateway integration
- scoped IAM setup for execution and invocation
- a clean path for automating deployment packaging instead of relying on manual ZIP creation
- basic testability and CI for both Python logic and Terraform validation

## Scope honesty

This is not a production ML platform and it does not currently run a real SageMaker model.

Today, the Lambda uses simple keyword heuristics:

- positive keywords return `POSITIVE`
- everything else currently returns `NEGATIVE`

That means the right way to read this repo is:

- strong as a compact AWS/IaC/serverless lab
- useful as supporting cloud engineering evidence
- not a flagship AI modeling project

## Architecture

```text
Client
  ->
API Gateway HTTP API
  ->
AWS Lambda (Python)
  ->
CloudWatch Logs
```

Terraform provisions:

- Lambda execution role
- CloudWatch logging policy attachment
- HTTP API
- API Gateway to Lambda integration
- invoke permission from API Gateway to Lambda

## Repository layout

```text
/lambda        Lambda source
/terraform     AWS infrastructure as code
/tests         Lambda unit tests and sample payload
/architecture  lightweight architecture notes
```

## Local verification

This repo now supports a simple local verification path:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

## CI

GitHub Actions now runs:

- Lambda unit tests
- Terraform fmt check
- Terraform init
- Terraform validate

## Packaging

Lambda packaging is now automated through Terraform using the `archive_file` provider.

You do not need to hand-build and commit a `lambda.zip` artifact. Terraform generates it from `lambda/app.py` during validation/apply flows.

## Deployment notes

1. Configure AWS credentials locally
2. Review Terraform configuration in `terraform/`
3. Initialize and apply:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

4. Use the API Gateway output URL to call:

```text
POST /predict
```

Example payload:

```json
{
  "text": "I love this workshop"
}
```

## Next improvement options

- replace heuristic logic with a real model endpoint
- add request validation and better error envelopes
- add throttling, alarms, and cost controls
- add deployment screenshots or sample API responses
- improve the architecture note into a polished visual diagram

## License

MIT
