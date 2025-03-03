import boto3
import os
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION')
        )
        self.bucket_name = os.environ.get('AWS_BUCKET_NAME')

    def upload_file(self, file):
        try:
            # Generate unique filename
            ext = os.path.splitext(file.filename)[1]
            filename = f"{str(uuid.uuid4())}{ext}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            
            # Return the URL of the uploaded file
            return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
        
        except ClientError as e:
            print(e)
            return None 