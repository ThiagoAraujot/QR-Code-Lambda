# QR Code Generator API

This project implements an AWS Lambda function that generates QR Code images from input URLs. The function is deployed as a container image on AWS ECR, integrated with API Gateway, and stores the generated images in an Amazon S3 bucket.

---

## Overview

The API accepts a JSON payload containing a `url` field, generates a QR Code image, uploads it to an S3 bucket, and returns the public URL of the image.

---

## Features

- Receives HTTP POST requests with JSON body
- Generates QR Codes from arbitrary URLs
- Stores PNG images in S3 bucket under `qrcodes/` folder
- Returns the public URL for the generated QR Code image
- Uses Docker container deployed on AWS Lambda (via ECR)

---

## Technologies Used

- AWS Lambda (Container Image)
- Amazon Elastic Container Registry (ECR)
- Amazon S3 for image storage
- API Gateway for HTTP endpoint
- Python 3.12
- Python libraries: `qrcode`, `boto3`, `Pillow`

---

## API Usage

### Request

**Method:** POST  
**Endpoint:** `https://3grrhgboa8.execute-api.us-east-1.amazonaws.com/prod/generate`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "url": "https://thiagoaraujovieira.com.br"
}
```

### Response

```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"qr_code_url\": \"https://s3-bucket-qrcodes-thiagodev.s3.us-east-1.amazonaws.com/qrcodes/qr_20250722_183117802702.png\"}"
}
```

---

## Environment Variables

The Lambda container expects the following environment variables:

| Variable | Description |
|----------|-------------|
| `BUCKET_NAME` | Name of the S3 bucket for uploads |
| `REGION` | AWS region of the S3 bucket |

---

## Deployment Details

- The Lambda function is packaged as a Docker container image.
- The image is pushed to AWS Elastic Container Registry (ECR).
- Lambda is configured to use this container image.
- API Gateway triggers the Lambda function via HTTP requests.
- 
---

## Running the API with `curl`

```bash
curl -X POST https://3grrhgboa8.execute-api.us-east-1.amazonaws.com/prod/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://aws.amazon.com/"}'
```

---
