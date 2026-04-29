import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('contact-messages')

sns = boto3.client('sns')

TOPIC_ARN = "arn:aws:sns:eu-central-1:760460643761:MyPortfolioSNSTopic"

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        body = event.get("body")

        if isinstance(body, str):
            body = json.loads(body)

        item = {
            "id": str(uuid.uuid4()),
            "name": body.get("name"),
            "email": body.get("email"),
            "message": body.get("message")
        }

        # Validation (correctly indented)
        if not item["name"] or not item["email"] or not item["message"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "All fields are required"})
            }

        print("Saving item:", item)

        table.put_item(Item=item)

        # SNS part
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="New Contact Form Submission",
            Message=f"""
New message received:

Name: {item['name']}
Email: {item['email']}
Message: {item['message']}
"""
        )

        print("SNS publish triggered")  # moved before return

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data saved successfully"})
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }