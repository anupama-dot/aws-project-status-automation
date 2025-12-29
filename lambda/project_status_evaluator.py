import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')

# SNS Topic ARN
TOPIC_ARN = "<SNS_TOPIC_ARN>"

def lambda_handler(event, context):
    # Get bucket name and object key from the S3 event
    # Lambda is configured with an S3 event notification set to trigger on object creation events (like uploading files).
    # Every time any file is uploaded to that bucket (or matching prefix/suffix if configured), an event is sent to Lambda.
    # The Lambda receives the event payload with details about exactly which object triggered it — including the bucket name and the object key (filename).
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Fetch the project status file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(response['Body'].read())

    status = "GREEN"
    messages = []

    today = datetime.today()

    # Check risks for high severity open over 14 days
    for risk in data.get('risks', []):
        if risk['severity'] == "High" and risk['daysOpen'] > 14:
            status = "RED"
            messages.append(f"High risk open for more than 14 days: {risk['description']}")

    # Check milestones for overdue incomplete items
    for milestone in data.get('migrationMilestones', []):
        if 'dueDate' not in milestone:
            continue
        due_date = datetime.strptime(milestone['dueDate'], "%Y-%m-%d")
        if milestone['status'] != "Completed" and due_date < today:
            status = "RED"
            messages.append(f"Milestone overdue: {milestone['milestoneName']}")

    # Send SNS alert if issues found
    if status != "GREEN":
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"Project Status Alert: {status}",
            Message="\n".join(messages)
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "Status": status,
            "Messages": messages
        })
    }
