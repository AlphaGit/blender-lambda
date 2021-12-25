# Blender on Lambda

Render Blender scenes on the distributed serverless cloud!

This repository is based on the architecture laid out by [TAS-PC](https://github.com/AlphaGit/tas-pc).

This repository aids in the following tasks:

- Setting up cloud infrastructure in AWS for rendering blender scenes
- Executing multiple concurrent jobs for rendering each frame
- Uploading and downloading scene and support files
- Removing infrastructure

## A few notes on the chosen architecture

The infrastructure created is called Serverless, through an AWS service called Lambda functions. These are charged per-use, and have a monthly free tier that costs nothing to use. AWS Lambdas do not currently support GPU rendering, but are easily scaled to concurrent executions, saving time.

## How to use

1. Create an AWS Account.
2. Download the AWS CLI. Install it and configure your credentials (`aws configure`).
3. Download terraform.
4. Clone this repository
5. Create a `blender-lambda.tfvars` file for configuration. Use these values as startup, but modify them as you will.
    ```tf
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
    ```
6. Execute `./apply.sh` and accept the changes to have the infrastructure be created on your AWS account.
7. Execute `./upload_files.sh <sceneFile> <file1> <file2> <file3>` to upload your files (the scene file and any supporting meadia files).
8. Execute `./render.sh <sceneFile> <file1> <file2>...` to start the render job.
9. Wait.
10. Execute `./download_rendered.sh` to download the results of the render.
11. Execute `./destroy.sh` to remove all the infrastructure from your AWS account.


## More information

This work is based on these previous investigations:

- [TAS-PC](https://blog.alphasmanifesto.com/2021/11/22/tas-pc/)
- [Rendering Blender Scenes in the cloud with AWS Lambda](https://blog.theodo.com/2021/08/blender-serverless-lambda/), by JR Beaudoin
- [Blender-docker](https://github.com/nytimes/rd-blender-docker) by the NYTimes Research Team
