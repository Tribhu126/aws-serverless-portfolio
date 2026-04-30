import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

contact_table = dynamodb.Table('contact-messages')
counter_table = dynamodb.Table('visitor-count')

sns = boto3.client('sns')

TOPIC_ARN = "arn:aws:sns:eu-central-1:760460643761:MyPortfolioSNSTopic"


# =========================
# Visitor Counter Logic
# =========================
def increment_counter():
    response = counter_table.update_item(
        Key={'id': 'visits'},
        UpdateExpression='SET #c = #c + :inc',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':inc': 1},
        ReturnValues="UPDATED_NEW"
    )
    return int(response['Attributes']['count'])


def get_counter():
    response = counter_table.get_item(Key={'id': 'visits'})
    return int(response['Item']['count'])


# =========================
# Lambda Handler
# =========================
def lambda_handler(event, context):
    try:
        print("Received event:", event)

        method = event.get("requestContext", {}).get("http", {}).get("method")
        params = event.get("queryStringParameters") or {}

        # =========================
        # GET → Visitor Counter
        # =========================
        if method == "GET":
            if params.get("read") == "true":
                visits = get_counter()  # read only
            else:
                visits = increment_counter()  # increment

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"visits": visits})
            }

        # =========================
        # POST → Contact Form
        # =========================
        if method == "POST":
            body = event.get("body")

            if isinstance(body, str):
                body = json.loads(body)

            item = {
                "id": str(uuid.uuid4()),
                "name": body.get("name"),
                "email": body.get("email"),
                "message": body.get("message")
            }

            # Validation
            if not item["name"] or not item["email"] or not item["message"]:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"error": "All fields are required"})
                }

            print("Saving item:", item)

            contact_table.put_item(Item=item)

            # SNS Notification
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

            print("SNS publish triggered")

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "Data saved successfully"})
            }

        # =========================
        # Unsupported Method
        # =========================
        return {
            "statusCode": 405,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Method not allowed"})
        }

    except Exception as e:
        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }