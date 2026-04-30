# AWS Serverless Portfolio Website

## 🚀 Overview

This project is a fully serverless web application built on AWS. It demonstrates how modern cloud-native architectures can be used to build scalable, cost-efficient, and event-driven applications.

The application features a modern, responsive frontend combined with a serverless backend that handles real-time form submissions, visitor tracking, and email notifications.

---

## 🌐 Live Demo

👉 https://d2ur4gm3dnah1e.cloudfront.net/

---

## 🏗️ Architecture

![Architecture](architecture.png)

### 🔄 Application Flow

1. User accesses the website via Amazon CloudFront (HTTPS)
2. Static frontend is served from Amazon S3
3. On page load:

   * API Gateway triggers Lambda (`GET /visits`)
   * DynamoDB updates or retrieves visitor count
4. User submits the contact form:

   * API Gateway triggers Lambda (`POST /contact`)
5. Lambda:

   * Validates input
   * Stores data in DynamoDB
   * Sends notification via SNS
6. Response is returned to frontend

---

## 🧰 Tech Stack

| Service            | Purpose                |
| ------------------ | ---------------------- |
| Amazon S3          | Static website hosting |
| Amazon CloudFront  | CDN + HTTPS            |
| Amazon API Gateway | REST endpoints         |
| AWS Lambda         | Backend logic          |
| Amazon DynamoDB    | Data storage           |
| Amazon SNS         | Email notifications    |
| Amazon CloudWatch  | Logging & monitoring   |

---

## ✨ Features

* Fully serverless architecture
* Responsive, modern UI with animations
* Contact form with validation (frontend + backend)
* Visitor counter using DynamoDB
* Event-driven email notifications via SNS
* CloudWatch logging for observability
* Clean separation of frontend and backend

---

## 🔐 Security

* Least-privilege IAM policies
* Restricted DynamoDB access (PutItem, UpdateItem, GetItem)
* HTTPS via CloudFront
* CORS configured in API Gateway
* Input validation in Lambda

---

## 🧠 Key Learnings

* Designing serverless architectures using AWS
* Building REST APIs using API Gateway and Lambda
* Using DynamoDB for both storage and atomic counters
* Preventing duplicate visitor counts using frontend logic
* Handling JSON serialization issues (Decimal)
* Debugging CORS and API integration issues
* Implementing event-driven architecture using SNS
* Improving UI/UX for technical portfolios

---

## ⚠️ Challenges Faced

* API returning "Not Found" due to route configuration
* IAM permission issues affecting DynamoDB access
* SNS subscription auto-deactivation
* Lambda errors due to incorrect event handling
* Decimal serialization issues in responses
* Preventing duplicate visitor counts
* Frontend-backend integration debugging

---

## 🔮 Future Improvements

* Implement auto-reply emails using Amazon SES
* Add custom domain using Route 53
* Implement CI/CD pipeline (GitHub Actions)
* Add authentication using Amazon Cognito
* Expand project portfolio (3-tier architecture)

---

## 📁 Project Structure

```
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

## 📌 Author

**Tribhuvan Sharma**
AWS Certified Solutions Architect
Aspiring Solutions Consultant / Pre-Sales Engineer

---

## 📸 Portfolio Preview

![Portfolio Website Screenshot](Portfolio_Website_Screenshot.png)

