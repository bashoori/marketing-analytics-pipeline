# etl/extract/trigger_lambda.py

import boto3
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def trigger_lambda_function():
    client = boto3.client(
        'lambda',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
    )

    response = client.invoke(
        FunctionName='extract_marketing_data_to_s3',
        InvocationType='RequestResponse'  # Or 'Event' for async
    )

    response_payload = response['Payload'].read().decode('utf-8')
    print("Lambda Response:", response_payload)