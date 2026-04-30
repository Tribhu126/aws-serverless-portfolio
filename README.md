# AWS Serverless Portfolio Website

## 🚀 Overview

This project is a fully serverless web application built on AWS. It allows users to submit messages through a contact form, which are processed, stored, and trigger real-time email notifications.

The application also includes a visitor tracking feature using DynamoDB, demonstrating state management in a serverless architecture.

The system is designed using cloud-native services and follows best practices such as event-driven architecture, least-privilege IAM, and frontend-backend separation.

---

## 🌐 Live Demo

👉 https://d2ur4gm3dnah1e.cloudfront.net/

---

## 🏗️ Architecture

![Architecture](architecture.png)

---

### 🔄 Application Flow

1. User accesses the website via Amazon CloudFront (HTTPS)
2. Static frontend (HTML/CSS) is served from Amazon S3
3. On page load:

   * A request is sent to API Gateway (`GET /visits`)
   * Lambda increments or reads visitor count
   * DynamoDB stores and updates the count
4. User submits the contact form:

   * Request is sent to API Gateway (`POST /contact`)
   * API Gateway triggers AWS Lambda
5. Lambda:

   * Validates input (server-side validation)
   * Stores message in DynamoDB
   * Sends notification via SNS
6. Visitor count and form submission results are returned to the frontend

---

## 🧰 Tech Stack

| Service            | Purpose                                        |
| ------------------ | ---------------------------------------------- |
| Amazon S3          | Static website hosting                         |
| Amazon CloudFront  | CDN + HTTPS delivery                           |
| Amazon API Gateway | API endpoints (`GET /visits`, `POST /contact`) |
| AWS Lambda         | Backend logic                                  |
| Amazon DynamoDB    | Stores messages and visitor count              |
| Amazon SNS         | Email notifications                            |
| Amazon CloudWatch  | Logging and monitoring                         |

---

## ✨ Features

* Fully serverless architecture (no servers managed)
* Secure HTTPS delivery via CloudFront
* Contact form with validation (frontend + backend)
* Persistent storage using DynamoDB
* Visitor tracking using DynamoDB atomic counters
* Event-driven email notifications using SNS
* CloudWatch logging for observability
* Clean separation of frontend and backend

---

## 🔐 Security

* Implemented least-privilege IAM policies for Lambda
* Restricted DynamoDB access to specific actions (`PutItem`, `UpdateItem`, `GetItem`)
* Enabled HTTPS using CloudFront
* Configured API Gateway with CORS handling
* Input validation to prevent malformed requests

---

## 🧠 Key Learnings

* Designing a serverless architecture using AWS managed services
* Implementing RESTful API endpoints using API Gateway
* Using DynamoDB for both data storage and atomic counters
* Preventing duplicate visitor counts using frontend session tracking
* Handling DynamoDB data types (Decimal → JSON serialization)
* Debugging CORS issues between frontend and backend
* Implementing least-privilege IAM roles and policies
* Managing CloudFront caching and invalidation
* Understanding limitations of SNS for email delivery

---

## ⚠️ Challenges Faced

* API returning "Not Found" due to incorrect route configuration
* IAM permission issues preventing DynamoDB operations
* SNS subscription auto-deactivation behavior
* Lambda failing due to incorrect event parsing and indentation errors
* Handling Decimal serialization errors in Lambda responses
* Preventing duplicate visitor counts caused by page refreshes
* Debugging frontend-to-backend integration issues

---

## 🔮 Future Improvements

* Implement user auto-reply emails using Amazon SES
* Add custom domain using Route 53
* Implement CI/CD pipeline (GitHub Actions)
* Add authentication using Amazon Cognito
* Improve UI/UX with modern frontend framework (React)
* Implement advanced analytics (unique visitors, session tracking)

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
├── README.md
```

---

## 🧪 How to Run (High-Level)

1. Upload frontend files to S3 and enable static hosting
2. Configure CloudFront distribution
3. Create API Gateway with routes:

   * `GET /visits`
   * `POST /contact`
4. Deploy Lambda function
5. Create DynamoDB tables:

   * `contact-messages`
   * `visitor-count`
6. Insert initial item into `visitor-count`:

   ```json
   { "id": "visits", "count": 0 }
   ```
7. Configure SNS topic and email subscription
8. Attach IAM role with required permissions
9. Connect frontend to API Gateway endpoint
10. Configure CORS settings

---

## 📌 Author

**Tribhuvan Sharma**
Aspiring Pre-Sales/Solutions Consultant (AWS Certified)

