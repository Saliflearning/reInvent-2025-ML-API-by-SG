# reInvent 2025 Serverless Sentiment API Lab

This repository is a compact AWS serverless lab built around Terraform, Lambda, API Gateway, IAM, and CloudWatch logging.

It exposes a single `/predict` endpoint backed by a Python Lambda function. The current sentiment logic is intentionally lightweight and deterministic; it is a placeholder seam for a future real model integration rather than a claim of deployed SageMaker inference.

## What this project demonstrates

- Terraform-driven provisioning for a small AWS API surface
- Lambda and API Gateway integration
- scoped IAM setup for execution and invocation
- automated Lambda packaging through Terraform
- environment-based preparation for a future SageMaker endpoint
- basic testability and CI for Python logic and Terraform validation

## Scope honesty

This is not a production ML platform and it does not currently run a real SageMaker model.

Today, the Lambda uses simple keyword heuristics:

- positive keywords return `POSITIVE`
- everything else currently returns `NEGATIVE`

The project is best understood as:

- a compact AWS, IaC, and serverless engineering lab
- supporting evidence of cloud engineering fundamentals
- an extensible foundation for a future model endpoint

## Architecture

```text
Client
  ->
API Gateway HTTP API
  ->
AWS Lambda (Python 3.12)
  ->
CloudWatch Logs
```

Terraform provisions:

- Lambda execution role and logging policy
- HTTP API and Lambda integration
- API Gateway invoke permission
- Lambda package generated from `lambda/app.py`
- placeholder `SAGEMAKER_ENDPOINT_NAME` environment configuration

## Repository layout

```text
/lambda        Lambda source
/terraform     AWS infrastructure as code
/tests         Lambda unit tests and sample payload
/architecture  lightweight architecture notes
```

## Local verification

```bash
python -m unittest discover -s tests -p "test_*.py" -v
terraform -chdir=terraform fmt -check
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

## CI

GitHub Actions runs:

- Lambda unit tests
- Terraform formatting checks
- Terraform initialization without a backend
- Terraform validation

## Packaging

Lambda packaging is automated through Terraform using the `archive_file` provider. Terraform generates `lambda/lambda.zip` from `lambda/app.py`; generated ZIP artifacts should not be committed.

## Deployment

1. Configure AWS credentials locally.
2. Review the Terraform variables and planned resources.
3. Initialize and apply:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

4. Use the API Gateway output URL to call `POST /predict`.

Example payload:

```json
{
  "text": "I love this workshop"
}
```

## Future SageMaker seam

The repository prepares for a future `SAGEMAKER_ENDPOINT_NAME` configuration, but the Lambda does not invoke SageMaker today. A production integration would also require:

- a deployed model endpoint
- scoped `sagemaker:InvokeEndpoint` IAM permission
- `boto3` invocation and response parsing
- request validation, alarms, throttling, and cost controls

## Next improvements

- replace heuristic logic with a real model endpoint
- add stronger request validation and error envelopes
- add throttling, alarms, and cost controls
- add deployment screenshots and sample API responses
- replace the text architecture summary with a polished visual diagram

## License

MIT
