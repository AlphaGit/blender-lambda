from typing import Tuple

import json
import os
import subprocess
import boto3
import re

QUEUE_NAME = os.environ['QUEUE_NAME']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
LOCAL_RENDER_FILE = '/tmp/render_file.blend'

request_id = None

def handler(event, context):
    print('Starting producer lambda function')

    try:
        render_request = json.loads(event['body'])
        request_id = render_request['request_id']
        assert_request_is_valid(render_request)
    except Exception as exception:
        return get_response(status_code=400, body={ 'error': str(exception) })

    try:
        file_name = render_request['file_name']
        retrieve_file_from_s3(file_name)

        (frame_start, frame_end) = get_frame_range(render_request)
        queue_render_jobs(file_name, frame_start, frame_end)

        return get_response(body={
            'file_name': file_name,
            'jobs_queued': frame_end - frame_start + 1
        })
    except Exception as exception:
        log(f'Exception: {exception}')
        return get_response(status_code=500, body={ 'error': str(exception) })


def get_frame_range(render_request: dict) -> Tuple[int, int]:
    log(f'Getting frame range from {LOCAL_RENDER_FILE}')
    proc = subprocess.Popen(['blender', '-b', LOCAL_RENDER_FILE, '-P', 'get_frames.py'], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    log(f'get_frames output: {out}')
    log(f'get_frames error: {err}')

    matches = re.findall(r'\d+-\d+', out.decode('utf-8'))
    if len(matches) == 0:
        raise Exception('No frame range found in file')
    (file_frame_start, file_frame_end) = matches[0].split('-')

    if (not file_frame_start or not file_frame_end):
        raise Exception(f'Failed to get frame range from file.')

    frame_start = render_request['frame_start'] if 'frame_start' in render_request else int(file_frame_start)
    frame_end = render_request['frame_end'] if 'frame_end' in render_request else int(file_frame_end)

    return frame_start, frame_end


def queue_render_jobs(file_name, frame_start, frame_end):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    for frame in range(frame_start, frame_end + 1):
        message = json.dumps({
            'file_name': file_name,
            'frame': frame
        })
        print('Sending message to queue: ' + message)
        queue.send_message(MessageBody=message)


def retrieve_file_from_s3(file_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.download_file(file_name, LOCAL_RENDER_FILE)


def assert_request_is_valid(render_request) -> Tuple[bool, str]:
    log(f'Validating request {render_request}')

    if 'file_name' not in render_request:
        raise TypeError("'file_name' parameter is missing")

    if not isinstance(render_request['file_name'], str):
        raise TypeError("'file_name' must be a string")

    if 'frame_start' in render_request:
        if not isinstance(render_request['frame_start'], int):
            raise TypeError('frame_start must be an integer')

    if 'frame_end' in render_request:
        if not isinstance(render_request['frame_end'], int):
            raise TypeError('frame_end must be an integer')

    if 'frame_start' in render_request and 'frame_end' in render_request and render_request['frame_start'] > render_request['frame_end']:
        raise ValueError('frame_start must be less than or equal to frame_end')

    log('Request is valid.')


def get_response(status_code = 200, body = {}, headers = { 'Content-Type': 'application/json' }):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }

def log(message):
    prefix = f'[{request_id}] ' if request_id else ''
    print(f'{prefix}{message}')

