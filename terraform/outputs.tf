output "api_invoke_url" {
  description = "Base URL for the HTTP API"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "lambda_function_name" {
  description = "Name of the sentiment Lambda function"
  value       = aws_lambda_function.sentiment_lambda.function_name
}

output "lambda_log_group_name" {
  description = "CloudWatch log group with 14-day retention"
  value       = aws_cloudwatch_log_group.lambda.name
}
