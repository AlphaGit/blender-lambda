import boto3
import json
import os

QUEUE_NAME = os.environ['QUEUE_NAME']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def lambda_handler(event, context):
    print('Starting producer lambda function')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    files = [obj.key for obj in bucket.objects.all()]

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

    for obj in files:
        message = json.dumps({'file': obj})
        print('Sending message to queue: ' + message)
        queue.send_message(MessageBody=message)

    return {
        'statusCode': 200,
        'body': json.dumps({ 'files_queued': len(files) }),
    }
