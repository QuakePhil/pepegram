# pepegram-subscribe/lambda_function.py
import boto3, re, json

def sanitize(email):
    return re.sub('[^A-Za-z0-9.@_]+', '', email)
    # return re.sub('[^@]+@[^@]+\.[^@]+', '', email)

def subscribe(event):
    if 'queryStringParameters' not in event:
        return {
            'statusCode': 500,
            'body': 'Missing: event[queryStringParameters]'
        }
    if 'email' not in event['queryStringParameters']:
        return {
            'statusCode': 500,
            'body': 'Missing: event[queryStringParameters][email]'
        }

    email = sanitize(event['queryStringParameters']['email'])
    encoded_string = email.encode("utf-8")

    boto3.resource("s3").Bucket("pepegram").put_object(Key="subscribe/"+email, Body=encoded_string)
    return {
        'statusCode': 200,
        'body': 'Subscribed: ' + email # json.dumps(email)
    }

def lambda_handler(event, context):
    return subscribe(event)
