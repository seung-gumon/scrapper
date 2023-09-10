import boto3
import os
import requests
from PIL import Image, ImageSequence
from io import BytesIO
import uuid
from dotenv import load_dotenv
import urllib.parse


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

    def upload(self, output_io, folder_name, unique_id, content_type='image/webp', extension='webp'):
        object_name = f"{folder_name}/{unique_id}.{extension}"
        self.client.upload_fileobj(
            output_io,
            self.config.bucket_name,
            object_name,
            ExtraArgs={'ContentType': content_type}
        )
        return f"https://{self.config.bucket_name}.s3.amazonaws.com/{object_name}"

class ImageProcessor:
    def download(self, url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def is_animated(self, image):
        try:
            image.seek(1)
        except EOFError:
            return False
        return True

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
            for index, ele in enumerate(image_urls):
                unique_id = str(uuid.uuid4())
                
                response = requests.get(ele['src'])
                original_image = self.image_processor.download(ele['src'])
                
                # Check the size of the image in bytes and convert it to megabytes
                image_size_MB = len(response.content) / (1024 * 1024)

                # If image is animated or size exceeds 3MB, treat it as a GIF
                if self.image_processor.is_animated(original_image) or image_size_MB > 3:
                    output_io = BytesIO(response.content)
                    output_io.seek(0)
                    parsed_url = urllib.parse.urlparse(ele['src'])
                    extension = 'gif'
                    content_type = 'image/gif'
                else:
                    output_io = self.image_processor.convert_to_webp(original_image)
                    extension = 'webp'
                    content_type = 'image/webp'
                
                upload_url = self.s3_client.upload(output_io, folder_name, unique_id, content_type, extension)
                
                ele['src'] = upload_url

        except Exception as e:
            print(f'An exception occurred: {e}')
        return image_urls

def upload_images(images, bucket_name):
    config = Config()
    s3_client = S3Client(config)
    image_processor = ImageProcessor()
    
    uploader = ImageUploader(s3_client, image_processor)
    return uploader.upload_images(images, bucket_name)
