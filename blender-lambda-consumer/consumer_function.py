import json

def handler(event, context):
    received_body = event['Records'][0]['body']
    record = json.loads(received_body)

    file_name = record['file_name']
    frame = record['frame']

    print(f'Received message for file: {file_name} and frame: {frame}')

    print('Done')