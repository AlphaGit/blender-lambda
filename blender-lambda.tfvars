default_tags = {
    "project" = "blender-lambda"
}

producer_api_gateway_name = "blender-lambda-api"

producer_lambda_source_path = "./blender-lambda-producer"

producer_invocation_route_key = "POST /render-job"

consumer_lambda_source_path = "./blender-lambda-consumer"

queue_name = "blender-lambda-queue"