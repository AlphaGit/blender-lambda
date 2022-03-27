resource "aws_s3_bucket" "lambda_bucket" {
    bucket = var.lambda_bucket
    acl = "private"
    force_destroy = true
}

resource "aws_iam_role" "lambda_exec" {
    name = "lambda_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [{
            Action = "sts:AssumeRole",
            Effect = "Allow",
            Sid = "",
            Principal = {
                Service = "lambda.amazonaws.com"
            }
        }]
    })
}

data "aws_iam_policy_document" "lambda_policy_document" {
    statement {
        sid = "LambdaPolicyQueueAccess"
        actions = [
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes",
            "sqs:SendMessage",
            "sqs:GetQueueUrl"
        ]
        resources = [
            aws_sqs_queue.queue.arn
        ]
    }

    statement {
        sid = "LambdaPolicyS3Access"
        actions = [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:GetBucketPolicy",
            "s3:GetBucketTagging",
            "s3:GetBucketVersioning",
            "s3:GetBucketWebsite",
            "s3:GetLifecycleConfiguration",
        ]
        resources = [
            aws_s3_bucket.lambda_bucket.arn,
            format("%s%s", aws_s3_bucket.lambda_bucket.arn, "/*")
        ]
    }
}

resource "aws_iam_policy" "lambda_policy" {
    name = "lambda_policy"
    policy = data.aws_iam_policy_document.lambda_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_sqs_policy" {
    role = aws_iam_role.lambda_exec.name
    policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic_policy" {
    role = aws_iam_role.lambda_exec.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_sqs_queue" "queue" {
    name = var.queue_name

    visibility_timeout_seconds = var.consumer_timeout_seconds
}