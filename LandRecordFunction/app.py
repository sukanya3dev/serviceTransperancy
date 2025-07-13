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
    logger.info(f"Received event: {json.dumps(event)}")

    # Extract record_id from query string parameters (GET method)
    record_id = event.get('queryStringParameters', {}).get('record_id')

    if not record_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required field: record_id'})
        }

    try:
        response = table.get_item(Key={'record_id': record_id})
    except Exception as e:
        logger.error(f"Error fetching record: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Record not found'})
        }

    item = response['Item']
    combined_data = f"{item['parcel_id']}{item['owner_name']}{item['comment']}{item['timestamp']}"
    recalculated_hash = hashlib.sha256(combined_data.encode()).hexdigest()
    status = 'valid' if recalculated_hash == item.get('record_hash') else 'tampered'

    return {
        'statusCode': 200,
        'headers' : {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'record_id': record_id,
            'status': status,
            'parcel_id': item.get('parcel_id'),
            'owner_name': item.get('owner_name'),
            'comment': item.get('comment'),
            'timestamp': item.get('timestamp')
        })
    }
