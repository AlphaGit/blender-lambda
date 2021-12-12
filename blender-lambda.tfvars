default_tags = {
    "project" = "blender-lambda"
}

producer_api_gateway_name = "blender-lambda-api"

producer_lambda_source_path = "./blender-lambda-producer"

producer_invocation_route_key = "POST /render-job"

producer_lambda_function_name = "blender-lambda-producer"

producer_ecr_repo = "blender-lambda-producer"

consumer_lambda_source_path = "./blender-lambda-consumer"

consumer_lambda_function_name = "blender-lambda-consumer"

consumer_ecr_repo = "blender-lambda-consumer"

queue_name = "blender-lambda-queue"