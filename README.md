# **reInvent-2025-ML-API-by-SG**

AI-powered sentiment analysis API deployed serverlessly using **Terraform**, **AWS Lambda**, and **API Gateway**.
Built live during **AWS re:Invent 2025** as a hands-on showcase of cloud engineering, IaC, and ML integration.

## 🚀 **Project Overview**

This project exposes a **POST /predict** API endpoint that accepts user text and returns a sentiment-style response.
The system is fully serverless and designed so the Lambda function can later integrate with a real **SageMaker** model.

### Example Request

```json
{
  "text": "I am really excited about AWS re:Invent 2025!"
}
```

### Example Response

```json
{
  "input_text": "I am really excited about AWS re:Invent 2025!",
  "label": "POSITIVE",
  "score": 0.95
}
```

> ⚠️ **Note:** The current sentiment result is mock logic inside Lambda.
> The handler is intentionally structured to be easily replaced by a real **SageMaker inference call** in the next iteration.

---

## **Architecture**

```
Client → API Gateway (HTTP API) → Lambda → (future) SageMaker Endpoint
                                ↓
                         CloudWatch Logs
```

All resources are created automatically using **Terraform**.

---

## **Tech Stack**

| Layer       | Technology                           |
| ----------- | ------------------------------------ |
| IaC         | Terraform                            |
| Compute     | AWS Lambda (Python 3.10)             |
| API Layer   | API Gateway v2 (HTTP API)            |
| IAM         | Execution Role, Basic Lambda Logging |
| Logging     | CloudWatch                           |
| ML (Future) | Amazon SageMaker Endpoint            |

---

## 📦 **Repository Structure**

```
reInvent-2025-ML-API-by-SG/
│
├── architecture/     # Diagrams + future architecture documents
├── lambda/           # Lambda function code (Python)
├── terraform/        # Terraform IaC (API Gateway, Lambda, IAM)
├── tests/            # Example request payloads
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## ⚙️ **Deployment Guide**

### **1️⃣ Prerequisites**

Make sure you have installed:

* **Terraform** → [https://developer.hashicorp.com/terraform/install](https://developer.hashicorp.com/terraform/install)
* **AWS CLI** → [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Configure AWS credentials:

```bash
aws configure
```

IAM user should have permissions for:

* Lambda
* API Gateway
* IAM
* CloudWatch

---

## **2️⃣ Clone the repository**

```bash
git clone https://github.com/Saliflearning/reInvent-2025-ML-API-by-SG.git
cd reInvent-2025-ML-API-by-SG
```


## **3️⃣ Package the Lambda function**

From **PowerShell**:

```powershell
cd .\lambda\
Compress-Archive -Path app.py -DestinationPath lambda.zip -Force
cd ..\terraform\
```


## **4️⃣ Deploy with Terraform**

```powershell
terraform init
terraform plan
terraform apply
```

Type **yes** to confirm.

Terraform will output:

api_invoke_url = "https://xxxxx.execute-api.us-east-1.amazonaws.com"
lambda_function_name = "sg-reinvent-sentiment-lambda"
```

## **Testing the API**

Replace `YOUR_API_URL` with the URL from Terraform.

```powershell
(Invoke-WebRequest -Uri "https://YOUR_API_URL/predict" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"text": "I am really excited about AWS re:Invent 2025!"}'
).Content
```

Expected output:

```json
{"input_text": "...", "label": "POSITIVE", "score": 0.95}
```

## 🔮 **Future Enhancement — SageMaker Integration**

The Lambda handler (`lambda/app.py`) is already structured to allow:

* Injecting a SageMaker endpoint name via env variables
* Using `boto3` to call the SageMaker Runtime API
* Returning real model predictions

Planned next steps:

* Deploy HuggingFace or AWS-provided sentiment model via SageMaker
* Add CloudWatch metrics (latency, model time, error rates)
* Add request logging to DynamoDB or S3

This upgrade will transform the API from a mock ML service → into a **production-ready inference pipeline**.


## 👤 **Author**

**(Salif. G)**
Associate Cloud Engineer • UX Researcher • AI Enthusiast
Built live during **AWS re:Invent 2025**.

