import os
import uuid
import requests
import boto3

from PIL import Image
from io import BytesIO

from config.settings.default import MASTER_DATA

master_data_file_path = os.path.join(MASTER_DATA, 'logo.png')

if 'S3_BUCKET_NAME' in os.environ:
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
else:
    S3_BUCKET_NAME = 'retheadev'

if 'REGION_NAME' in os.environ:
    REGION_NAME = os.getenv("REGION_NAME")
else:
    REGION_NAME = 'ap-southeast-1'

DEFAULT_PATH = 'images'

s3 = boto3.client('s3')


def watermark_photo(url):
    output_image_path = '/tmp/{}'.format(get_filename_in_path(url).replace('.jpg', '.png'))
    print(output_image_path)
    res = requests.get(url)
    base_image = Image.open(BytesIO(res.content))
    watermark_image = Image.open(master_data_file_path)
    width, height = base_image.size
    position = (width // 2 - 50, height // 2 - 35)

    # add water mark to image
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark_image, position, mask=watermark_image)
    # transparent.show()
    transparent.save(output_image_path)
    return output_image_path


def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


def get_filename_in_path(file_path):
    return file_path.split('/')[-1]


def upload_file(file_path, bucket_name=S3_BUCKET_NAME, region_name=REGION_NAME):
    file = get_filename_in_path(file_path)
    s3_file_path = 'images/{}'.format(file)
    s3_location = 'https://{}.s3-{}.amazonaws.com/{}'
    s3.upload_file(file_path, bucket_name, s3_file_path)
    return s3_location.format(bucket_name, region_name, s3_file_path)
