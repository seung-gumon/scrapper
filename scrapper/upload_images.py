import boto3
import os
import requests
from PIL import Image
from io import BytesIO
import uuid
from dotenv import load_dotenv


# Load .env
load_dotenv()
# Remove PIL memory limits
Image.MAX_IMAGE_PIXELS = None


class Config:
    def __init__(self):
        self.aws_access_key_id = os.environ.get('aws_access_key_id')
        self.aws_secret_access_key = os.environ.get('aws_secret_access_key')
        self.bucket_name = os.environ.get('image_bucket_name')
        self.user_agent = os.environ.get('user_agent')

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

class AssetsProcessor:
    def __init__(self, referer_url):
        self.referer_url = referer_url
        self.user_agent = os.environ.get('user_agent')
    
    def download(self, url):
        headers = {
            'User-Agent': self.user_agent,
            'Referer': self.referer_url
        }
        response = requests.get(url, headers=headers)
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

class AssetsUploader:
    def __init__(self, s3_client: S3Client, image_processor: AssetsProcessor, referer_url):
        self.s3_client = s3_client
        self.image_processor = image_processor
        self.referer_url = referer_url
        self.user_agent = os.environ.get('user_agent')

    def upload_images(self, image_urls, folder_name):
        try:
            for index, ele in enumerate(image_urls):
                if 'https' not in ele['src']:
                    ele['src'] = 'https:' + ele['src']
                unique_id = str(uuid.uuid4())
                headers = {
                    'User-Agent': self.user_agent,
                    'Referer': self.referer_url
                }
                response = requests.get(ele['src'] , headers=headers)
                original_image = self.image_processor.download(ele['src'])        


                # Check the size of the image in bytes and convert it to megabytes
                
                image_size_MB = len(response.content) / (1024 * 1024)
                print("이미지 사이즈 :::", image_size_MB , ele['src'])
                # If image is animated or size exceeds 3MB, treat it as a GIF
                if self.image_processor.is_animated(original_image) or image_size_MB > 3:
                    output_io = BytesIO(response.content)
                    output_io.seek(0)
                    extension = 'gif'
                    content_type = 'image/gif'
                else:
                    output_io = self.image_processor.convert_to_webp(original_image)
                    extension = 'webp'
                    content_type = 'image/webp'
                
                upload_url = self.s3_client.upload(output_io, folder_name, unique_id, content_type, extension)
                
                ele['src'] = upload_url
                

        except Exception as e:
            print(f'upload images methods 에서 에러났음 :::  {e}')
        return image_urls
    
    
    def upload_videos(self, video_urls, folder_name):
        try:
            for index, ele in enumerate(video_urls):
                if 'https' not in ele['src']:
                    ele['src'] = 'https:' + ele['src']
                unique_id = str(uuid.uuid4())
                headers = {
                    'User-Agent': self.user_agent,
                    'Referer': self.referer_url
                }
                response = requests.get(ele['src'], headers=headers)
                
                video_size_MB = len(response.content) / (1024 * 1024)
                print("비디오 사이즈 :::", video_size_MB , ele['src'])
                # Assuming all URLs in video_urls are actually videos
                output_io = BytesIO(response.content)
                output_io.seek(0)
                extension = 'mp4'  # Assuming the video is in mp4 format
                content_type = 'video/mp4'
                
                upload_url = self.s3_client.upload(output_io, folder_name, unique_id, content_type, extension)
                
                ele['src'] = upload_url
        except Exception as e:
            print(f'upload vidoes methods 에서 에러났음 :::  {e}')
        return video_urls


def upload_images(images, bucket_name , referer_url):
    config = Config()
    s3_client = S3Client(config)
    image_processor = AssetsProcessor(referer_url)
    
    uploader = AssetsUploader(s3_client, image_processor, referer_url)
    return uploader.upload_images(images, bucket_name)

def upload_videos(videos , bucket_name , referer_url):
    config = Config()
    s3_client = S3Client(config)
    video_processor = AssetsProcessor(referer_url)
    
    uploader = AssetsUploader(s3_client, video_processor, referer_url)
    return uploader.upload_videos(videos, bucket_name)