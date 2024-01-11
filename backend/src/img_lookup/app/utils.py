from botocore.config import Config
from django.conf import settings
import boto3
from botocore.errorfactory import ClientError


def s3_get_client(external=False):
    """
    Get S3 client. Use external to get a client-accessible url.
    """
    endpoint = settings.AWS_S3_ENDPOINT_URL
    if external:
        endpoint = settings.AWS_S3_CUSTOM_DOMAIN 
    return boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=endpoint,
        config=Config(signature_version='s3v4')
    )


def s3_key_exists(file_key: str):
    try:
        s3_get_client().head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        return True
    except ClientError as e:
        pass
    return False


def s3_remove_object(file_key: str):
    try:
        s3_get_client().delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
        return True
    except ClientError as e:
        pass
    return False


def s3_generate_presigned_get(file_path: str):
    s3_client = s3_get_client(external=True)

    presigned_data = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": file_path,
        },
        ExpiresIn=settings.AWS_QUERYSTRING_EXPIRE,
        HttpMethod="GET",
    )

    return presigned_data


def s3_generate_presigned_put(file_path: str, content_type: str):
    s3_client = s3_get_client(external=True)

    presigned_data = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": file_path,
            "ContentType": content_type,
        },
        ExpiresIn=settings.AWS_QUERYSTRING_EXPIRE,
        HttpMethod="PUT",
    )

    return presigned_data


def get_file_extension(file_name: str):
    return file_name.split(".")[-1].lower()
