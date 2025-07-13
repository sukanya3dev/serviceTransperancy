import json
import boto3
import uuid
import os
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(os.environ.get('TABLE_NAME'))

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    body = event.get('body', event)  # fallback to whole event
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Malformed JSON in request body'})
            }

    # Extract and validate fields
    comment = body.get('comment', '').strip()
    sla_time = body.get('sla_time', '').strip()
    department = body.get('department', '').strip()
    status = body.get('status', 'pending')
    submitted_by = body.get('submitted_by', 'anonymous')

    if not comment or not sla_time or not department:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required fields'})
        }

    # Construct item
    feedback_id = str(uuid.uuid4())
    submitted_on = datetime.now().isoformat()
    item = {
        'feedback_id': feedback_id,
        'comment': comment,
        'sla_time': sla_time,
        'department': department,
        'status': status,
        'submitted_by': submitted_by,
        'submitted_on': submitted_on
    }

    # Store in DynamoDB
    try:
        table.put_item(Item=item)
        logger.info(f"Feedback stored successfully: {item}")
    except Exception as e:
        logger.error(f"Error storing feedback: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

    # Success response
    return {
        'statusCode': 201,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback_id,
            'submitted_on': submitted_on
        })
    }
