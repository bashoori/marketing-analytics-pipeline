import json
import boto3
import requests
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

# ----------------------------------------
# Load environment variables from .env file
# ----------------------------------------
load_dotenv()

# ----------------------------------------
# Retrieve AWS credentials and region from environment
# These should be defined in your .env file:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# ----------------------------------------
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')  # Default to us-west-2

# ----------------------------------------
# Initialize boto3 S3 client using loaded credentials
# This allows local testing without IAM roles
# ----------------------------------------
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# ----------------------------------------
# S3 bucket name and external API URL
# Replace ReqRes_url with your own valid API key
# ----------------------------------------
BUCKET_NAME = 'bashoori-s3-01'
ReqRes_url = 'https://jsonplaceholder.typicode.com/posts'  # Replace with a valid key

# ----------------------------------------
# Main Lambda handler function (also usable for local testing)
# ----------------------------------------
def lambda_handler(event=None, context=None):
    try:
        # Step 1: Fetch JSON data from Mockaroo API
        response = requests.get(ReqRes_url)
        response.raise_for_status()  # Raise error if response is not 200
        marketing_data = response.json()

        # Step 2: Generate a unique timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'marketing_data_{timestamp}_{uuid.uuid4().hex[:6]}.json'

        # Step 3: Upload the data to S3 bucket under the marketing_raw/ folder
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f'marketing_raw/{filename}',
            Body=json.dumps(marketing_data),
            ContentType='application/json'
        )

        # Success message
        print(f"✅ Upload successful: {filename}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Upload successful',
                'file_name': filename,
                'bucket': BUCKET_NAME
            })
        }

    except Exception as e:
        # Print and return error details
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

# ----------------------------------------
# Local execution entry point
# ----------------------------------------
if __name__ == '__main__':
    lambda_handler()