import boto3
import os


# 환경 변수에서 자격 증명을 가져옴
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-2')  # Default region을 설정하였습니다.

# DynamoDB 리소스를 생성
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id= os.environ.get('aws_access_key_id'),
    aws_secret_access_key= os.environ.get('aws_secret_access_key'),
    region_name='ap-northeast-2'
)

# 테이블 이름
table_name = 'posts'

# 테이블 객체를 생성
table = dynamodb.Table(table_name)
def save_post_data(response_arr) :
    for item in response_arr:
        table.put_item(Item=item)
