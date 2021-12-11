set -e

if [ -z "$AWS_ACCOUNT" ] || [ -z "$AWS_REGION" ] || [ -z "$PRODUCER_REPO" ] || [ -z "$CONSUMER_REPO" ]; then
  echo "AWS_ACCOUNT, AWS_REGION, PRODUCER_REPO and CONSUMER_REPO must be set"
  exit 1
fi

ECR=$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t $ECR/$PRODUCER_REPO:latest \
    -f blender-lambda-producer/producer.Dockerfile \
    blender-lambda-producer/

docker build -t $ECR/$CONSUMER_REPO:latest \
   -f blender-lambda-consumer/consumer.Dockerfile \
   blender-lambda-consumer/

aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR

docker push $ECR/$PRODUCER_REPO:latest
docker push $ECR/$CONSUMER_REPO:latest

export TF_VAR_aws_account_id=$AWS_ACCOUNT
export TF_VAR_aws_region=$AWS_REGION
export TF_VAR_producer_ecr_repo=$PRODUCER_REPO
export TV_VAR_consumer_ecr_repo=$CONSUMER_REPO
terraform apply -var-file=blender-lambda.tfvars
