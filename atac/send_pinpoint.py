
import boto3
from botocore.exceptions import ClientError

def send_email:

    # The AWS Region that you want to use to send the email. For a list of
    # AWS Regions where the Amazon Pinpoint API is available, see
    # https://docs.aws.amazon.com/pinpoint/latest/apireference/
    AWS_REGION = "us-west-2"
    
    # The "From" address. This address has to be verified in
    # Amazon Pinpoint in the region you're using to send email.
    SENDER = "Mary Major <sender@example.com>"
    
    # The addresses on the "To" line. If your Amazon Pinpoint account is in
    # the sandbox, these addresses also have to be verified.
    TOADDRESS = "recipient@example.com"
    
    # The Amazon Pinpoint project/application ID to use when you send this message.
    # Make sure that the email channel is enabled for the project or application
    # that you choose.
    APPID = "ce796be37f32f178af652b26eexample"
    
    # The subject line of the email.
    SUBJECT = "Amazon Pinpoint Test (SDK for Python (Boto 3))"
    
    # The body of the email for recipients whose email clients don't support HTML
    # content.
    BODY_TEXT = """Amazon Pinpoint Test (SDK for Python)
    -------------------------------------
    This email was sent with Amazon Pinpoint using the AWS SDK for Python (Boto 3).
    For more information, see https:#aws.amazon.com/sdk-for-python/
                """
    
    # The body of the email for recipients whose email clients can display HTML
    # content.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon Pinpoint Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https:#aws.amazon.com/pinpoint/'>Amazon Pinpoint</a> using the
        <a href='https:#aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto 3)</a>.</p>
    </body>
    </html>
                """
    
    # The character encoding that you want to use for the subject line and message
    # body of the email.
    CHARSET = "UTF-8"
    
    # Create a new client and specify a region.
    client = boto3.client('pinpoint',region_name=AWS_REGION)
    try:
        response = client.send_messages(
            ApplicationId=APPID,
            MessageRequest={
                'Addresses': {
                    TOADDRESS: {
                         'ChannelType': 'EMAIL'
                    }
                },
                'MessageConfiguration': {
                    'EmailMessage': {
                        'FromAddress': SENDER,
                        'SimpleEmail': {
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT
                            },
                            'HtmlPart': {
                                'Charset': CHARSET,
                                'Data': BODY_HTML
                            },
                            'TextPart': {
                                'Charset': CHARSET,
                                'Data': BODY_TEXT
                            }
                        }
                    }
                }
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Message sent! Message ID: "
                + response['MessageResponse']['Result'][TOADDRESS]['MessageId'])

                
def send_sms:

    # The AWS Region that you want to use to send the message. For a list of
    # AWS Regions where the Amazon Pinpoint API is available, see
    # https://docs.aws.amazon.com/pinpoint/latest/apireference/
    region = "us-east-1"
    
    # The phone number or short code to send the message from. The phone number
    # or short code that you specify has to be associated with your Amazon Pinpoint
    # account. For best results, specify long codes in E.164 format.
    originationNumber = "+12065550199"
    
    # The recipient's phone number.  For best results, you should specify the
    # phone number in E.164 format.
    destinationNumber = "+14255550142"
    
    # The content of the SMS message.
    message = ("This is a sample message sent from Amazon Pinpoint by using the "
               "AWS SDK for Python (Boto 3).")
    
    # The Amazon Pinpoint project/application ID to use when you send this message.
    # Make sure that the SMS channel is enabled for the project or application
    # that you choose.
    applicationId = "ce796be37f32f178af652b26eexample"
    
    # The type of SMS message that you want to send. If you plan to send
    # time-sensitive content, specify TRANSACTIONAL. If you plan to send
    # marketing-related content, specify PROMOTIONAL.
    messageType = "TRANSACTIONAL"
    
    # The registered keyword associated with the originating short code.
    registeredKeyword = "myKeyword"
    
    # The sender ID to use when sending the message. Support for sender ID
    # varies by country or region. For more information, see
    # https://docs.aws.amazon.com/pinpoint/latest/userguide/channels-sms-countries.html
    senderId = "MySenderID"
    
    # Create a new client and specify a region.
    client = boto3.client('pinpoint',region_name=region)
    try:
        response = client.send_messages(
            ApplicationId=applicationId,
            MessageRequest={
                'Addresses': {
                    destinationNumber: {
                        'ChannelType': 'SMS'
                    }
                },
                'MessageConfiguration': {
                    'SMSMessage': {
                        'Body': message,
                        'Keyword': registeredKeyword,
                        'MessageType': messageType,
                        'OriginationNumber': originationNumber,
                        'SenderId': senderId
                    }
                }
            }
        )
    
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Message sent! Message ID: "
                + response['MessageResponse']['Result'][destinationNumber]['MessageId'])
    
    
                