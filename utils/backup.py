import boto3
import os
from config import YANDEX_ACCESS_KEY, YANDEX_SECRET_KEY, YANDEX_BUCKET, YANDEX_ENDPOINT, DATABASE_PATH
from datetime import datetime

async def start_backup_task():
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3",
        endpoint_url=YANDEX_ENDPOINT,
        aws_access_key_id+YANDEX_ACCESS_KEY,
        aws_secret_access_key=YANDEX_SECRET_KEY,
    )

    backup_filename = f"backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.dp"
    s3.upload_file(DATABASE_PATH, YANDEX_BUCKET, backup_filename)