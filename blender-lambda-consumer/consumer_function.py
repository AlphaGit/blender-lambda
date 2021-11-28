import json

def lambda_handler(event, context):
    received_body = event['Records'][0]['body']
    record = json.loads(received_body)
    print('Received message for file: ' + record['file'])
