# variable "aws_account_id" {
#     description = "AWS Account ID"

#     type = string
# }

variable "aws_region" {
    description = "AWS region for all resources"

    type = string
    default = "us-east-1"
}

variable "producer_ecr_repo" {
    description = "ECR repository name for producer function"

    type = string
}

variable "consumer_ecr_repo" {
    description = "ECR repository name for consumer function"

    type = string
}

variable "lambda_bucket" {
    description = "Bucket for all lambda archives"

    type = string
    default = "temp-lambda-archive-bucket"
}

variable "default_tags" {
    type = map
    description = "Default tags to apply to all resources"
    default = {}
}

variable "producer_lambda_function_name" {
    description = "Name of the producer lambda function"

    type = string
    default = "producer-lambda-function"
}

variable "producer_api_gateway_name" {
    description = "Name of the producer api gateway"

    type = string
    default = "producer-api-gateway"
}

variable "producer_lambda_source_path" {
    description = "Path to the producer lambda source"

    type = string
    default = "./producer_function"
}

variable "producer_lambda_runtime" {
    description = "Runtime for the producer lambda"

    type = string
    default = "python3.8"
}

variable "producer_lambda_handler" {
    description = "Handler for the producer lambda"

    type = string
    default = "producer_function.lambda_handler"
}

variable "producer_apigateway_stage_name" {
    description = "Name of the API gateway stage for the producer lambda"

    type = string
    default = "prod"
}

variable "producer_invocation_route_key" {
    description = "Route key for the producer lambda"

    type = string
    default = "POST /queue"
}

variable "consumer_lambda_function_name" {
    description = "Name of the consumer lambda"

    type = string
    default = "consumer-lambda-function"
}

variable "consumer_lambda_runtime" {
    description = "Runtime for the consumer lambda"

    type = string
    default = "python3.8"
}

variable "consumer_lambda_handler" {
    description = "Handler for the consumer lambda"

    type = string
    default = "consumer_function.lambda_handler"
}

variable "consumer_lambda_source_path" {
    description = "Path to the consumer lambda source"

    type = string
    default = "./consumer_function"
}

variable "queue_name" {
    description = "Name of the queue"

    type = string
    default = "producer-consumer-queue"
}

variable "consumer_timeout_seconds" {
    description = "Timeout for the consumer lambda"

    type = number
    default = 900
}