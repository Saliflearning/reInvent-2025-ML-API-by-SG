variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name tag"
  type        = string
  default     = "reInvent-2025-ML-API-by-SG"
}

variable "owner" {
  description = "Owner tag used for resource tagging"
  type        = string
  default     = "SG"
}
