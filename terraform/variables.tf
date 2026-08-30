variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name tag"
  type        = string
  default     = "aws-serverless-sentiment-lab"
}

variable "owner" {
  description = "Generic portfolio owner tag used for resource grouping"
  type        = string
  default     = "portfolio-lab"
}

