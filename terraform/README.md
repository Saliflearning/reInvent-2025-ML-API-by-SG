# Terraform module

This root packages `../lambda/app.py` and defines:

- AWS provider configuration and generic tags
- Lambda execution role with log-group-scoped write permissions
- CloudWatch log group with 14-day retention
- Python 3.12 Lambda package, memory, and timeout settings
- API Gateway HTTP API, `POST /predict`, Lambda integration, and invoke permission
- default-stage throttling of 10 requests/second with burst 20
- API URL, function name, and log-group outputs

Validation does not contact or mutate an AWS account:

```bash
terraform init -backend=false
terraform fmt -check -recursive
terraform validate
```

An apply requires authorized AWS credentials and creates billable cloud resources.
State and variable-value files are intentionally ignored.
