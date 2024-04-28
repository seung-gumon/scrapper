import boto3
import os


# 환경 변수에서 자격 증명을 가져옴
# aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

aws_access_key_id = 'd5za0a'
aws_secret_access_key = 'hh0ci'

# 실제 Production DB는 아래와 같이 써주어야하고 현재는 Local DB를 사용하므로 localhost로 설정
# aws_default_region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-2')  # Default region을 설정하였습니다.
aws_default_region = 'localhost'

# DynamoDB Local의 endpoint_url 설정 (Local에서 테스트할 때 사용)
endpoint_url = 'http://localhost:8000'

# DynamoDB 리소스를 생성
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key= aws_secret_access_key,
    region_name=aws_default_region,
    # EndPoint URL을 설정해주어야 Local에서도 동작함 (Local에서 테스트할 때 사용)
    endpoint_url=endpoint_url
)

# 테이블 이름
table_name = 'posts'

# 테이블 객체를 생성
table = dynamodb.Table(table_name)
def save_post_data(response_arr) :
    for item in response_arr:
        table.put_item(Item=item)
    print("Data saved successfully 🥹")