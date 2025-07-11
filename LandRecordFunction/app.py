import json
import boto3
import os
import hashlib
import logging

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ['TABLE_NAME'])
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    record_id = body.get('record_id')

    if not record_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required field: record_id'})
        }
    response = table.get_item(Key={'record_id': record_id})
    print(response)
    print(record_id)
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Record not found'})
        }
    item = response['Item']
    combined_data = f"{item['parcel_id']}{item['owner']}{item['comment']}{item['timestamp']}"
    recalculated_hash = hashlib.sha256(combined_data.encode()).hexdigest()
    if recalculated_hash == item.get('record_hash'):
        status = 'valid'
    else:
        status = 'tampered'
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'record_id': record_id,
            'status': status,
            'parcel_id': item.get('parcel_id'),
            'owner': item.get('owner'),
            'comment': item.get('comment'),
            'timestamp': item['timestamp']
        })
    }



