import urllib3
import json

http = urllib3.PoolManager()

def send(event, context, responseStatus, responseData, reason=None, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']
    responseBody = {
        'Status': responseStatus,
        'Reason': reason or f'See the details in CloudWatch Log Stream: (context.log_stream_name)',
        'PhysicalResourceId': physicalResourceId or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'noEcho': noEcho,
        'Data': responseData
    }

    json_responseBody = json.dumps(responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, body=responseBody, headers=headers)
        print("Response: ", response.status)
    except Exception as e:
        print("send(..) failed executing http.request(..): ", e)