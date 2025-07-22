# QR Code Generator API

This project implements an AWS Lambda function that generates QR Code images from input text or URLs. The function is deployed as a container image on AWS ECR, integrated with API Gateway, and stores the generated images in an Amazon S3 bucket.

---

## Overview

The API accepts a JSON payload containing a `text` field, generates a QR Code image, uploads it to an S3 bucket, and returns the public URL of the image.

---

## Features

- Receives HTTP POST requests with JSON body
- Generates QR Codes from arbitrary text or URLs
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
**Endpoint:** `https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/generate`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "text": "https://example.com"
}
```

### Response

```json
{
  "qr_code_url": "https://<bucket-name>.s3.<region>.amazonaws.com/qrcodes/qr_20250722_113055123456.png"
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

---

## Permissions

The Lambda execution role must have permissions to write objects to the S3 bucket:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject"],
  "Resource": "arn:aws:s3:::<bucket-name>/*"
}
```

To make QR Code images publicly accessible, configure the S3 bucket policy to allow public read on the uploaded objects, or set the `ACL` to `public-read` when uploading.

### Making S3 Objects Publicly Accessible

Example bucket policy to allow public read access to all objects:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<bucket-name>/*"
    }
  ]
}
```

---

## Running the API with `curl`

```bash
curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/<stage>/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "https://example.com"}'
```

---

## Notes

- The QR Code image filename is generated using a timestamp to ensure uniqueness.
- Images are stored inside a `qrcodes/` prefix within the S3 bucket.
- The Lambda function handles both direct JSON payloads and API Gateway event formats.
- The Docker image includes all dependencies, including `qrcode` and `Pillow`.

---

## Author

Developed by Thiago Vieira  
https://thiagoaraujovieira.com.br