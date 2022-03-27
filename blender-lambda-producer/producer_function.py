from typing import Tuple

import json
import os
import subprocess
import boto3
import re
import logging
import sys

# from https://gist.github.com/niranjv/fb95e716151642e8ca553b0e38dd152e
logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
h = logging.StreamHandler(sys.stdout)
FORMAT = '[%(levelname)s] %(message)s'
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)
logger.setLevel(logging.INFO)

QUEUE_NAME = os.environ['QUEUE_NAME']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
LOCAL_RENDER_FILE = '/tmp/render_file.blend'

s3_bucket = boto3.resource('s3').Bucket(S3_BUCKET_NAME)
sqs_queue = boto3.resource('sqs').get_queue_by_name(QueueName=QUEUE_NAME)

def handler(event, context):
    logger.info('Starting producer lambda function')

    try:
        render_request = json.loads(event['body'])
        assert_request_is_valid(render_request)
    except Exception as exception:
        return get_response(status_code=400, body={ 'error': str(exception) })

    try:
        file_name = render_request['file_name']
        retrieve_file_from_s3(file_name)

        support_files = render_request['support_files'] if 'support_files' in render_request else []
        for support_file in support_files:
            check_s3_file_exists(support_file)

        (frame_start, frame_end) = get_frame_range(render_request)

        queue_render_jobs(file_name, frame_start, frame_end, support_files)

        logger.info(f'Finished producing lambda function')

        return get_response(body={
            'file_name': file_name,
            'jobs_queued': frame_end - frame_start + 1
        })
    except Exception as exception:
        logger.exception(exception)
        return get_response(status_code=500, body={ 'error': str(exception) })


def get_frame_range(render_request: dict) -> Tuple[int, int]:
    if 'frame_start' in render_request and 'frame_end' in render_request:
        return (int(render_request['frame_start']), int(render_request['frame_end']))

    logger.info(f'Getting frame range from {LOCAL_RENDER_FILE}')
    proc = subprocess.Popen(['blender', '-b', LOCAL_RENDER_FILE, '-P', 'get_frames.py'], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    logger.debug(f'get_frames output: {out}')
    logger.debug(f'get_frames error: {err}')

    matches = re.findall(r'Frame range: (\d+-\d+)', out.decode('utf-8'))
    if len(matches) == 0:
        raise Exception('No frame range found in file, output found:' + out.decode('utf-8'))
    (file_frame_start, file_frame_end) = matches[0].split('-')

    if (not file_frame_start or not file_frame_end):
        raise Exception(f'Failed to get frame range from file.')

    return (int(file_frame_start), int(file_frame_end))


def queue_render_jobs(file_name, frame_start, frame_end, support_files):
    for frame in range(frame_start, frame_end + 1):
        message = json.dumps({
            'file_name': file_name,
            'frame': frame,
            'support_files': support_files
        })
        logger.debug('Sending message to queue: ' + message)
        sqs_queue.send_message(MessageBody=message)


def check_s3_file_exists(file_name):
    try:
        s3_bucket.Object(file_name).load()
    except Exception as exception:
        raise Exception(f'File {file_name} does not exist in S3 bucket {S3_BUCKET_NAME}')
    logger.info(f'File {file_name} exists in S3 bucket {S3_BUCKET_NAME}')


def retrieve_file_from_s3(file_name):
    logger.info(f'Retrieving file {file_name} from S3 bucket {S3_BUCKET_NAME} to {LOCAL_RENDER_FILE}')
    s3_bucket.download_file(file_name, LOCAL_RENDER_FILE)


def assert_request_is_valid(render_request: dict) -> None:
    logger.debug(f'Validating request {render_request}')

    if not isinstance(render_request, dict):
        raise TypeError(f"data is not valid json, instead is {str(type(render_request))}")

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

    logger.debug('Request is valid.')


def get_response(status_code = 200, body = {}, headers = { 'Content-Type': 'application/json' }):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }
