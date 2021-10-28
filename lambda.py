# pepegram-email/lambda_function.py
import boto3, re, json

def sanitize(email):
    return re.sub('[^A-Za-z0-9.@_]+', '', email)
    # return re.sub('[^@]+@[^@]+\.[^@]+', '', email)

def subscribe(event):
    email = sanitize(event['queryStringParameters']['email'])
    encoded_string = email.encode("utf-8")

    boto3.resource("s3").Bucket("pepegram").put_object(Key="subscribe/"+email, Body=encoded_string)
    return email

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(subscribe(event))
    }
