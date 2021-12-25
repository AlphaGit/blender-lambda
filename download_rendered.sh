BUCKET=$(terraform output -raw lambda_bucket_name) 

aws s3 cp s3://$BUCKET/ . --recursive --exclude "*" --include "rendered*"