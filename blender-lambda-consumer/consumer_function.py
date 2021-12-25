import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
LOCAL_RENDER_FILE = '/tmp/render_file.blend'


def handler(event, context):
    try:
        received_body = event['Records'][0]['body']
        record = json.loads(received_body)

        file_name = record['file_name']
        frame = record['frame']
        support_files = record['support_files']

        logger.info(f'Received message for file: {file_name} and frame: {frame}')

        retrieve_files_from_s3(file_name, support_files)

        frame_str = str(frame).zfill(4)
        output_file = f'/tmp/rendered_{frame_str}.png'
        render_frame(frame, output_file)

        upload_file_to_s3(output_file)

        logger.info('Done.')
    except Exception as e:
        logger.exception(e)
        raise e


def render_frame(frame, output_file):
    logger.info(f'Rendering frame: {frame}')

    os.system(f"blender -b -P render_frame.py -- {LOCAL_RENDER_FILE} {output_file} {frame}")

    logger.info(f'Rendering frame: {frame} done')


def retrieve_files_from_s3(file_name, support_files):
    logger.info(f'Retrieving file: {file_name} from S3 bucket: {S3_BUCKET_NAME}')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.download_file(file_name, LOCAL_RENDER_FILE)

    logger.info(f'Retrieving file: {file_name} from S3 bucket: {S3_BUCKET_NAME} done')

    for file in support_files:
        logger.info(f'Retrieving file: {file} from S3 bucket: {S3_BUCKET_NAME}')

        bucket.download_file(file, f'/tmp/{file}')

        logger.info(f'Retrieving file: {file} from S3 bucket: {S3_BUCKET_NAME} done')


def upload_file_to_s3(file_name):
    logger.info(f'Uploading file: {file_name} to S3 bucket: {S3_BUCKET_NAME}')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_file(file_name, os.path.basename(file_name))

    logger.info(f'Uploading file: {file_name} to S3 bucket: {S3_BUCKET_NAME} done')
