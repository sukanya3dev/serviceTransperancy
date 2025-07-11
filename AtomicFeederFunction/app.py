import json
import boto3
import uuid
import os
from datetime import datetime
import hashlib
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ.get('TABLE_NAME'))

def lambda_handler(event, context):

    body = json.loads(event['body'])
    parcel_id = body.get('parcel_id', f"PCL-{uuid.uuid4().hex[:6]}")
    owner_name = body.get('owner_name')
    comment = body.get('comment')
    timestamp = datetime.now().isoformat()
    record_id = str(uuid.uuid4())
    combined_data = f"{parcel_id}|{owner_name}|{comment}|{timestamp}"
    record_hash = hashlib.sha256(combined_data.encode('utf-8')).hexdigest()

    logger.info(f"Received data: {body}")

    item = {
        'record_id': record_id,
        'parcel_id': parcel_id,
        'owner_name': owner_name,
        'comment': comment,
        'timestamp': timestamp,
        'record_hash': record_hash,
        'status': 'pending',
        }
    
    try:
        table.put_item(Item=item)
        logger.info(f"Item inserted into DynamoDB: {item}")    
    except Exception as e:
        logger.info(f"Error inserting item into DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
    
    return{
        'statusCode': 200,
        'body': json.dumps('Data feeding successful!'),
        'headers': {
            'Content-Type': 'application/json'
        }
    }