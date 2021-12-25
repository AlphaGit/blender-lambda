FILENAME=$1
BUCKET=$(terraform output -raw lambda_bucket_name) 

aws s3 cp $FILENAME s3://$BUCKET/$FILENAME