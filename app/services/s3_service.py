import boto3
import os
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
import uuid
from app.utils.constants import CROP_TYPES
from dotenv import load_dotenv

load_dotenv()


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION')
        )
        self.bucket_name = os.environ.get('AWS_BUCKET_NAME')

    def upload_file(self, file_stream, crop_type, original_filename):
        if crop_type not in CROP_TYPES:
            raise ValueError(f"Invalid crop type. Must be one of {CROP_TYPES}")

        try:
            # Generate safe filename
            safe_filename = secure_filename(original_filename)
            ext = os.path.splitext(safe_filename)[1].lower()
            filename = f"{crop_type}/{uuid.uuid4().hex}{ext}"

            # Upload from stream
            self.s3_client.upload_fileobj(
                file_stream,
                self.bucket_name,
                filename,
                ExtraArgs={'ACL': 'public-read'}
            )

            return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"

        except ClientError as e:
            print(f"S3 upload error: {str(e)}")
            return None
        except Exception as e:
            print(f"General upload error: {str(e)}")
            return None