import json
import qrcode
import boto3
import os
from io import BytesIO
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = os.environ.get('BUCKET_NAME')
REGION = os.environ.get('REGION')

def lambda_handler(event, context):
    try:
        
        if not BUCKET_NAME or not REGION:
            raise ValueError("Missing required environment variables: BUCKET_NAME or REGION")

        if "body" in event:
            try:
                body = json.loads(event["body"])
            except Exception:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid body format.'})
                }
        else:
            body = event

        text = body.get('url')
        if not text:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing "url" in request.'})
            }

        img = qrcode.make(text)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        filename = f"qrcodes/qr_{datetime.now().strftime('%Y%m%d_%H%M%S%f')}.png"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=buffer.getvalue(),
            ContentType='image/png',
        )

        region = REGION
        public_url = f"https://{BUCKET_NAME}.s3.{region}.amazonaws.com/{filename}"

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'qr_code_url': public_url})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
