# pepegram-blast/lambda_function.py
import boto3, re, json

def recipients():
    result = []
    bucket = boto3.resource("s3").Bucket("pepegram")
    for path in bucket.objects.filter(Prefix='subscribe/'):
        result.append(path.key[10:])
    return result


def blast_one_email(recipient):
    # bucket.objects.filter(Prefix="subscribe/"+recipient).delete()
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

    try:
        response = boto3.client('ses').send_email(
            Source="phil.nyc@gmail.com",
            Destination={'ToAddresses': [ recipient ]},
            Message={
                'Body': {   'Html': { 'Charset': "UTF-8", 'Data': BODY_HTML, },
                            'Text': { 'Charset': "UTF-8", 'Data': BODY_TEXT, },},
                'Subject': {'Charset': "UTF-8",'Data': 'Pepegram subscription',},
            },
        )
        print("Email sent to: " + recipient)
        print(response) # ['MessageId'])
    except Exception as e:
        print("Error while emailing " + recipient)
        print(e)

def blast():
    emails = recipients()
    for email in emails:
        blast_one_email(email)
    return {
        'statusCode': 200,
        'body': json.dumps(emails)
    }

def lambda_handler(event, context):
    return blast()
