import boto3
from PIL import Image
import requests
from io import BytesIO




def upload_images(image_urls):
    try:
        aws_access_key_id = ''
        aws_secret_access_key = ''
        bucket_name = 'kill-time'


        # S3 클라이언트 생성
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        for index, url in enumerate(image_urls):
            # 원격 URL로부터 이미지 다운로드
            print("images_urls :::" , image_urls);
            response = requests.get(url)
            original_image = Image.open(BytesIO(response.content))

            # 이미지를 webp 포맷으로 변환
            output_io = BytesIO()
            original_image.save(output_io, format="WEBP")
            output_io.seek(0)

            # AWS S3 버킷에 업로드
            s3.upload_fileobj(output_io, bucket_name, f"image_{index}.webp", ExtraArgs={'ContentType': 'image/webp'})
        
    except Exception as e:
        print('Catch the Exception ::: ',e);
        
        
        