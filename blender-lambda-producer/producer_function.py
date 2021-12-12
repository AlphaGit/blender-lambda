from typing import Tuple

import json
import os
import boto3

QUEUE_NAME = os.environ['QUEUE_NAME']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
LOCAL_RENDER_FILE = '/tmp/render_file.blend'

def handler(event, context):
    print('Starting producer lambda function')
    render_request = json.loads(event['body'])

    (is_valid, error_message) = request_is_valid(render_request)
    if not is_valid:
        return get_response(status_code=400, body={ 'error': error_message })

    file_name = render_request['file_name']
    (is_downloaded, error_message) = retrieve_file_from_s3(file_name)
    if not is_downloaded:
        return get_response(status_code=500, body={ 'error': error_message })

    # TODO: Verify that the file contains a valid frame range
    frame_start = render_request['frame_start']
    frame_end = render_request['frame_end']

    # queue the render jobs
    (is_queued, error_message) = queue_render_jobs(file_name, frame_start, frame_end)
    if not is_queued:
        return get_response(status_code=500, body={ 'error': error_message })

    return get_response(body={
        'file_name': file_name,
        'jobs_queued': frame_end - frame_start + 1
    })


def queue_render_jobs(file_name, frame_start, frame_end):
    try:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        for frame in range(frame_start, frame_end + 1):
            message = json.dumps({
                'file_name': file_name,
                'frame': frame
            })
            print('Sending message to queue: ' + message)
            queue.send_message(MessageBody=message)
        return True, None
    except Exception as exception:
        return (False, 'Failed to send message to SQS: ' + str(exception))


def retrieve_file_from_s3(file_name):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(S3_BUCKET_NAME)
        bucket.download_file(file_name, LOCAL_RENDER_FILE)
        return True, None
    except Exception as exception:
        return (False, 'Failed to download file from S3: ' + str(exception))

def request_is_valid(render_request) -> Tuple[bool, str]:
    if 'file_name' not in render_request:
        return False, "'file_name' parameter is missing"

    if 'frame_start' not in render_request:
        return False, "'frame_start' parameter is missing"

    if 'frame_end' not in render_request:
        return False, "'frame_end' parameter is missing"

    frame_start = render_request['frame_start']
    if not isinstance(frame_start, int):
        return False, "'frame_start' must be an integer"

    frame_end = render_request['frame_end']
    if not isinstance(frame_end, int):
        return False, "'frame_end' must be an integer"

    if frame_start > frame_end:
        return False, "'frame_end' must be equal or greater than 'frame_start'"

    if not isinstance(render_request['file_name'], str):
        return False, "'file_name' must be a string"

    return True, None

def get_response(status_code = 200, body = {}, headers = { 'Content-Type': 'application/json' }):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }
