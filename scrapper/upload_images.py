import boto3
import os
import requests
from PIL import Image
from io import BytesIO
import uuid
from dotenv import load_dotenv

# Load .env
load_dotenv()

class Config:
    def __init__(self):
        self.aws_access_key_id = os.environ.get('aws_access_key_id')
        self.aws_secret_access_key = os.environ.get('aws_secret_access_key')
        self.bucket_name = os.environ.get('image_bucket_name')


class S3Client:
    def __init__(self, config: Config):
        self.config = config
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.config.aws_access_key_id,
            aws_secret_access_key=self.config.aws_secret_access_key
        )

    def upload(self, output_io, folder_name, unique_id):
        self.client.upload_fileobj(
            output_io,
            self.config.bucket_name,
            f"{folder_name}/{unique_id}.webp",
            ExtraArgs={'ContentType': 'image/webp'}
        )


class ImageProcessor:
    def download(self, url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def convert_to_webp(self, original_image):
        output_io = BytesIO()
        original_image.save(output_io, format="WEBP")
        output_io.seek(0)
        return output_io


class ImageUploader:
    def __init__(self, s3_client: S3Client, image_processor: ImageProcessor):
        self.s3_client = s3_client
        self.image_processor = image_processor

    def upload_images(self, image_urls, folder_name):
        try:
            for index, url in enumerate(image_urls):
                unique_id = str(uuid.uuid4())
                
                original_image = self.image_processor.download(url)
                output_io = self.image_processor.convert_to_webp(original_image)
                
                self.s3_client.upload(output_io, folder_name, unique_id)

        except Exception as e:
            print(f'An exception occurred: {e}')


def upload_images(images,bucket_name):
    config = Config()
    s3_client = S3Client(config)
    image_processor = ImageProcessor()
    
    uploader = ImageUploader(s3_client, image_processor)
    uploader.upload_images(images, bucket_name)
