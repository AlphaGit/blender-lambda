data "archive_file" "consumer_lambda" {
    type = "zip"
    source_dir = var.consumer_lambda_source_path
    output_path = "${path.module}/tmp/consumer_lambda.zip"
}

resource "aws_s3_bucket_object" "consumer_lambda" {
    bucket = aws_s3_bucket.lambda_bucket.id

    key = "consumer_lambda.zip"
    source = data.archive_file.consumer_lambda.output_path

    etag = filemd5(data.archive_file.consumer_lambda.output_path)
}

resource "aws_lambda_function" "consumer_lambda" {
    function_name = var.consumer_lambda_function_name

    s3_bucket = aws_s3_bucket.lambda_bucket.id
    s3_key = aws_s3_bucket_object.consumer_lambda.key

    runtime = var.consumer_lambda_runtime
    handler = var.consumer_lambda_handler

    source_code_hash = data.archive_file.consumer_lambda.output_base64sha256

    role = aws_iam_role.lambda_exec.arn

    environment {
        variables = {
            "QUEUE_NAME" = aws_sqs_queue.queue.name
        }
    }
}

resource "aws_lambda_event_source_mapping" "event_source_mapping" {
    event_source_arn = aws_sqs_queue.queue.arn
    enabled = true
    function_name = aws_lambda_function.consumer_lambda.arn
    batch_size = 1
}


resource "aws_cloudwatch_log_group" "consumer_lambda_log_group" {
    name = "/aws/lambda/${aws_lambda_function.consumer_lambda.function_name}"

    retention_in_days = 30
}