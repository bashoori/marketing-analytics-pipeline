from dotenv import load_dotenv
import os
import boto3

load_dotenv()  # Loads .env into environment variables

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# Example usage
s3.upload_file('localfile.json', 'bashoori-s3-01', 'folder/localfile.json')