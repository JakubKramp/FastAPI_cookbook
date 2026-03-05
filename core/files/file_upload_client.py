from fastapi import HTTPException, UploadFile
from google.cloud.storage import Client

from config import settings


class FileUploader:
    def __init__(self, file: UploadFile):
        self.file = file
        self.validate_file()
        self.client = self.get_client()

    def validate_file(self):
        if self.file.filename and self.file.filename.split(".")[-1] not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        if self.file.size and self.file.size > settings.FILE_MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

    def upload_file(self):
        raise NotImplementedError

    @staticmethod
    def get_client():
        raise NotImplementedError

    @staticmethod
    def delete_file(filename: str):
        raise NotImplementedError


class GcloudFileUploader(FileUploader):
    @staticmethod
    def get_client() -> Client:
        return Client.from_service_account_json(settings.GCLOUD_KEY_FILE)

    async def upload_file(self):
        self.validate_file()
        bucket = self.client.bucket(settings.GCLOUD_BUCKET_NAME)
        blob = bucket.blob(self.file.filename)
        contents = await self.file.read()
        blob.upload_from_string(contents, content_type=self.file.content_type)

    @staticmethod
    def delete_file(filename: str):
        client = Client.from_service_account_json(settings.GCLOUD_KEY_FILE)
        bucket = client.bucket(settings.GCLOUD_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.delete()


class TestFileUploader(FileUploader):
    @staticmethod
    async def get_client():
        return None

    async def upload_file(self):
        return "FakeUrl"

    @staticmethod
    def delete_file(filename: str):
        return "Deleted"
