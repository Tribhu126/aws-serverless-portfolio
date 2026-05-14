# AWS Serverless Portfolio Website

# Overview

This project is a fully serverless 3-tier AWS web application designed to demonstrate modern cloud-native architecture patterns using managed AWS services.

The application combines a responsive frontend with a serverless backend capable of handling:

- visitor tracking
- contact form submissions
- event-driven notifications
- lightweight API protection
- backend-controlled visitor validation

The project evolved significantly through multiple architectural improvements focused on scalability, security, and realistic visitor tracking behavior.

---

# Live Demo

https://tribhuvansharma.com/

---

# Architecture

![Architecture](architecture.png)
> The visitor tracking system uses layered frontend and backend protection mechanisms including browser cooldown optimization, IP-based validation using DynamoDB, custom API request validation, and API Gateway CORS controls.

Serverless 3-tier architecture using:
- Presentation Layer
- Application Layer
- Data Layer

### Architecture Flow

User  
→ Route 53  
→ CloudFront  
→ S3 Static Frontend  
→ API Gateway (HTTP API)  
→ Lambda  
→ DynamoDB  
→ SNS  

---

# Application Flow

## Website Access

1. User accesses the website through Amazon CloudFront using HTTPS
2. CloudFront serves the static frontend hosted in Amazon S3

---

## Visitor Counter Flow

1. Frontend calls:
   - `GET /visits`
2. API Gateway triggers AWS Lambda
3. Lambda:
   - validates custom request headers
   - checks visitor cooldown state
   - validates visitor IP against DynamoDB
4. DynamoDB:
   - retrieves existing visitor count
   - conditionally increments the counter
5. Updated visitor count is returned to frontend

---

## Contact Form Flow

1. User submits contact form
2. Frontend calls:
   - `POST /contact`
3. API Gateway triggers Lambda
4. Lambda:
   - validates request body
   - stores submission in DynamoDB
   - publishes SNS notification
5. SNS sends email notification

---

# Tech Stack

| Service | Purpose |
|---|---|
| Amazon S3 | Static website hosting |
| Amazon CloudFront | CDN + HTTPS delivery |
| Amazon Route 53 | DNS management |
| Amazon API Gateway (HTTP API) | Serverless HTTP endpoints |
| AWS Lambda | Backend business logic |
| Amazon DynamoDB | Visitor tracking + contact storage |
| Amazon SNS | Email notifications |
| Amazon CloudWatch | Logging & monitoring |
| AWS IAM | Access control |

---

# Key Features

- Fully serverless AWS architecture
- Responsive frontend portfolio website
- HTTPS delivery using CloudFront + ACM
- Contact form with frontend and backend validation
- DynamoDB-based visitor tracking
- SNS email notifications
- CloudWatch logging and monitoring
- API Gateway HTTP API integration
- Custom API request validation
- Browser cooldown optimization
- Backend IP-based visitor cooldown logic
- CORS preflight handling
- Canonical domain handling
- Lightweight bot/crawler protection

---

# Visitor Tracking Design

The visitor counter uses a layered protection model to reduce artificial counter inflation while maintaining a lightweight serverless design.

## Frontend Protection Layer

The frontend implements:

- browser localStorage cooldown logic
- read-only mode for repeated visits
- reduced unnecessary API calls

This prevents repeated page refreshes from incrementing the counter continuously.

---

## Backend Protection Layer

Lambda performs backend-controlled visitor validation using:

- source IP extraction
- DynamoDB-based visitor tracking
- 24-hour cooldown validation

This significantly improves visitor count realism compared to frontend-only tracking.

---

## API Protection Layer

The API includes additional protection mechanisms:

- custom request header validation
- CORS preflight handling
- restricted direct API access

This helps reduce casual bot/crawler-triggered increments and direct endpoint abuse.

---

# Architectural Evolution

The visitor tracking system evolved through multiple iterations during development.

## Initial Implementation

Originally:
- every refresh incremented the visitor count
- visitor numbers inflated rapidly

---

## Problems Identified

### 1. Frontend Refresh Inflation
Repeated browser refreshes continuously incremented the counter.

### 2. Multi-Domain localStorage Separation
Separate localStorage behavior between:

- `tribhuvansharma.com`
- `www.tribhuvansharma.com`

caused duplicate counting.

### 3. Direct API Access
Bots and crawlers could directly hit the API endpoint.

---

## Final Solution

The implementation evolved into a layered architecture including:

1. Canonical domain enforcement
2. Browser cooldown logic
3. Custom request header validation
4. API Gateway CORS configuration
5. Backend IP-based cooldown validation using DynamoDB

This significantly improved visitor count realism while preserving a fully serverless design.

---

# Security Considerations

- HTTPS enforced via CloudFront + ACM
- Least-privilege IAM policies
- Restricted DynamoDB permissions
- Input validation inside Lambda
- API protection using custom headers
- CORS preflight handling implemented
- Backend-controlled visitor validation
- Separate read-only visitor retrieval logic

---

# Key Learnings

- Designing serverless AWS architectures
- Using API Gateway HTTP API with Lambda
- Building event-driven applications using SNS
- Implementing DynamoDB atomic counters
- Designing layered visitor tracking protection
- Understanding frontend vs backend validation tradeoffs
- Handling CORS preflight (`OPTIONS`) requests
- Debugging CloudFront cache invalidation
- Managing browser localStorage behavior
- Implementing lightweight bot protection techniques
- Designing backend-controlled visitor tracking systems

---

# Challenges Faced

- API route configuration issues
- DynamoDB IAM permission errors
- SNS subscription auto-deactivation
- Lambda event structure debugging
- Decimal JSON serialization issues
- Preventing duplicate visitor increments
- Browser CORS preflight failures
- CloudFront caching delays
- localStorage inconsistencies across domains
- Direct API access protection
- Bot/crawler-triggered visitor inflation
- Python indentation and Lambda control flow debugging

---

# Future Improvements

- Implement DynamoDB TTL for automatic visitor cleanup
- Add AWS WAF integration
- Implement CI/CD pipeline using GitHub Actions
- Add authentication using Amazon Cognito
- Implement analytics-grade visitor tracking
- Use CloudFront Functions or Lambda@Edge
- Infrastructure as Code using Terraform
- Add ECS/Fargate-based containerized workloads

---

# Project Structure

```text
aws-serverless-portfolio/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│
├── backend/
│   ├── lambda_function.py
│
├── architecture.png
├── Portfolio_Website_Screenshot.png
├── README.md
```

---

# Author

**Tribhuvan Sharma**  
AWS Certified Solutions Architect  
Aspiring Solutions Consultant / Pre-Sales Engineer

---

##  Portfolio Preview

![Portfolio Website Screenshot](Portfolio_Website_Screenshot.png)


