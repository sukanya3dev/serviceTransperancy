import boto3, os, zipfile
from urllib import request
import cfnresponse

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):

    try:
        if event['RequestType'] in ['Create', 'Update']:
            with zipfile.ZipFile('/tmp/FrontendUploader.zip', 'r') as z:
                z.extractall('/tmp/frontend')

            for root, dirs, files in os.walk('/tmp/frontend'):
                for file in files:
                    file_path = os.path.join(root, file)
                    s3_key = os.path.relpath(file_path, '/tmp/frontend')
                    s3.upload_file(file_path, bucket_name, s3_key,
                                      ExtraArgs={'ContentType': guess_content_type(file_path)})
                    
        cnfresponse.send(event, context, cfnresponse.SUCCESS, {}, "FrontendUploadSuccess")
    except Exception as e:
        print(f"Error: {e}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, "FrontendUploadFailed")
    
def guess_content_type(file_path):
    if file_path.endswith('.html'):
        return 'text/html'
    if file_path.endswith('.css'):
        return 'text/css'
    if file_path.endswith('.js'):
        return 'application/javascript'
    return "binary/octet-stream"
    