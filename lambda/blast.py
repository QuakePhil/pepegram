# pepegram-blast/lambda_function.py
import boto3, re, json

def to():
    to = ''
    comma = ''
    bucket = boto3.resource("s3").Bucket("pepegram")
    for path in bucket.objects.filter(Prefix='subscribe/'):
        to += comma + path.key[10:]
        comma = ','
    # bucket.objects.filter(Prefix="subscribe/").delete()
    return to

def blast(event):
    recipients = to()
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Pepegram subscription</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
    """
    BODY_TEXT = ("Pepegram subscription\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
    # boto3.client('ses').verify_email_identity(EmailAddress="phil.nyc@gmail.com")

    response = boto3.client('ses').send_email(
        Destination={
            'ToAddresses': [
                recipients,
            ],
        },
        Message={
            'Body': {
                'Html': { 'Charset': "UTF-8", 'Data': BODY_HTML, },
                'Text': { 'Charset': "UTF-8", 'Data': BODY_TEXT, },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': 'Pepegram subscription',
            },
        },
        Source="phil.nyc@gmail.com",
    )
    # except ClientError as e:
    #     print(e.response['Error']['Message'])
    # else:
    print(response) # ['MessageId'])
    print(response['Error'])
    
    return {
        'statusCode': 200,
        'body': json.dumps(recipients)
    }

def lambda_handler(event, context):
    return blast(event)
