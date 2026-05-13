import time
import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

contact_table = dynamodb.Table('contact-messages')
counter_table = dynamodb.Table('visitor-count')
visitors_table = dynamodb.Table('portfolio-visitors')

sns = boto3.client('sns')

TOPIC_ARN = "arn:aws:sns:eu-central-1:760460643761:MyPortfolioSNSTopic"


# =========================
# Visitor Counter Logic
# =========================
def increment_counter():

    response = counter_table.update_item(
        Key={'id': 'visits'},
        UpdateExpression='SET #c = #c + :inc',
        ExpressionAttributeNames={
            '#c': 'count'
        },
        ExpressionAttributeValues={
            ':inc': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    return int(response['Attributes']['count'])


def get_counter():

    response = counter_table.get_item(
        Key={'id': 'visits'}
    )

    return int(response['Item']['count'])


# =========================
# Visitor IP Tracking Logic
# =========================
def should_increment(ip_address):

    # Safety fallback
    if not ip_address:
        return False

    COOLDOWN_HOURS = 24

    current_time = int(time.time())

    response = visitors_table.get_item(
        Key={
            'ip': ip_address
        }
    )

    item = response.get("Item")

    # First visit
    if not item:

        visitors_table.put_item(
            Item={
                'ip': ip_address,
                'last_visit': current_time
            }
        )

        return True

    last_visit = item.get("last_visit", 0)

    hours_passed = (
        current_time - int(last_visit)
    ) / 3600

    # Cooldown expired
    if hours_passed >= COOLDOWN_HOURS:

        visitors_table.put_item(
            Item={
                'ip': ip_address,
                'last_visit': current_time
            }
        )

        return True

    return False


# =========================
# Lambda Handler
# =========================
def lambda_handler(event, context):

    try:

        print("Received event:", json.dumps(event))

        method = (
            event.get("requestContext", {})
                 .get("http", {})
                 .get("method")
            or event.get("httpMethod")
        )

        params = event.get("queryStringParameters") or {}

        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        }

        # =========================
        # OPTIONS → CORS
        # =========================
        if method == "OPTIONS":

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": ""
            }

        # =========================
        # GET → Visitor Counter
        # =========================
        if method == "GET":

            headers = event.get("headers") or {}

            print("Headers:", headers)

            portfolio_key = (
                headers.get("x-portfolio-key")
                or headers.get("X-Portfolio-Key")
            )

            # API protection
            if portfolio_key != "tribhu-secret":

                return {
                    "statusCode": 403,
                    "headers": cors_headers,
                    "body": json.dumps({
                        "error": "Forbidden"
                    })
                }

            # Get source IP
            source_ip = (
                event.get("requestContext", {})
                     .get("http", {})
                     .get("sourceIp")
            )

            print("Source IP:", source_ip)

            # Frontend read-only mode
            if params.get("read") == "true":

                visits = get_counter()

            else:

                should_count = should_increment(source_ip)

                if should_count:
                    visits = increment_counter()
                else:
                    visits = get_counter()

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({
                    "visits": visits
                })
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
            if (
                not item["name"]
                or not item["email"]
                or not item["message"]
            ):

                return {
                    "statusCode": 400,
                    "headers": cors_headers,
                    "body": json.dumps({
                        "error": "All fields are required"
                    })
                }

            print("Saving item:", item)

            contact_table.put_item(
                Item=item
            )

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
                "headers": cors_headers,
                "body": json.dumps({
                    "message": "Data saved successfully"
                })
            }

        # =========================
        # Unsupported Method
        # =========================
        return {
            "statusCode": 405,
            "headers": cors_headers,
            "body": json.dumps({
                "error": "Method not allowed"
            })
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }