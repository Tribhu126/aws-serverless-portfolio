# AWS Serverless Portfolio Website

## Overview
This project is a fully serverless web application built on AWS. It allows users to submit contact messages, which are processed and stored using cloud-native services.

## Architecture
The application uses a serverless architecture:

- Amazon S3: Hosts static frontend
- Amazon CloudFront: CDN and HTTPS delivery
- API Gateway: Handles API requests
- AWS Lambda: Backend logic
- DynamoDB: Stores messages
- SNS: Sends email notifications

## Features
- Serverless architecture
- Secure HTTPS access
- Contact form with validation
- Data storage using DynamoDB
- Email notifications via SNS
- CloudWatch logging for monitoring

## Challenges Faced
- Debugging CloudFront caching issues
- Handling CORS between frontend and API
- Fixing IAM permission issues
- Managing Lambda runtime errors

## Future Improvements
- Add email auto-reply using SES
- Custom domain using Route 53
- Authentication (Cognito)

## Live Demo
https://d2ur4gm3dnah1e.cloudfront.net/
