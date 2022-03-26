module "producer_docker_image" {
    source = "terraform-aws-modules/lambda/aws//modules/docker-build"

    create_ecr_repo = true
    ecr_repo = var.producer_ecr_repo
    source_path = abspath(var.producer_lambda_source_path)
}

resource "aws_lambda_function" "producer_lambda" {
    function_name = var.producer_lambda_function_name

    package_type = "Image"
    image_uri = module.producer_docker_image.image_uri
    role = aws_iam_role.lambda_exec.arn
    timeout = 120

    environment {
        variables = {
            "QUEUE_NAME" = aws_sqs_queue.queue.name,
            "S3_BUCKET_NAME" = aws_s3_bucket.lambda_bucket.id,
        }
    }
}

resource "aws_cloudwatch_log_group" "producer_lambda_log_group" {
    name = "/aws/lambda/${aws_lambda_function.producer_lambda.function_name}"

    retention_in_days = 30
}

resource "aws_apigatewayv2_api" "lambda" {
    name = var.producer_api_gateway_name
    protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
    api_id = aws_apigatewayv2_api.lambda.id

    name = var.producer_apigateway_stage_name
    auto_deploy = true

    access_log_settings {
        destination_arn = aws_cloudwatch_log_group.api_gw.arn

        format = jsonencode({
            requestId = "$context.requestId",
            sourceIp = "$context.identity.sourceIp",
            requestTime = "$context.requestTime",
            protocol = "$context.protocol",
            httpMethod = "$context.httpMethod",
            resourcePath = "$context.resourcePath",
            routeKey = "$context.routeKey",
            status = "$context.status",
            responseLength = "$context.responseLength",
            integrationErrorMessage = "$context.integrationErrorMessage",
        })
    }
}

resource "aws_apigatewayv2_integration" "queue" {
    api_id = aws_apigatewayv2_api.lambda.id

    integration_uri = aws_lambda_function.producer_lambda.invoke_arn
    integration_type = "AWS_PROXY"
    integration_method = "POST"
}

resource "aws_apigatewayv2_route" "queue" {
    api_id = aws_apigatewayv2_api.lambda.id

    route_key = var.producer_invocation_route_key
    target = "integrations/${aws_apigatewayv2_integration.queue.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
    name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

    retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
    statement_id = "AllowExecutionFromAPIGateway"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.producer_lambda.function_name
    principal = "apigateway.amazonaws.com"

    source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
