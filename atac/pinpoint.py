# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http:#aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError

def send_sms_pinpoint():
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


def send_email_pinpoint():
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


def send_email_smtp():
    # If you're using Amazon Pinpoint in a region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon Pinpoint SMTP
    # endpoint in the appropriate AWS Region.
    HOST = "email-smtp.us-west-2.amazonaws.com"
    
    # The port to use when connecting to the SMTP server.
    PORT = 587
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified.
    SENDER = 'Mary Major <sender@example.com>'
    
    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address has to be verified.
    RECIPIENT  = 'recipient@example.com'
    
    # CC and BCC addresses. If your account is in the sandbox, these
    # addresses have to be verified.
    CCRECIPIENT = "cc_recipient@example.com"
    BCCRECIPIENT = "bcc_recipient@example.com"
    
    # Replace smtp_username with your Amazon Pinpoint SMTP user name.
    USERNAME_SMTP = "AKIAIOSFODNN7EXAMPLE"
    
    # Replace smtp_password with your Amazon Pinpoint SMTP password.
    PASSWORD_SMTP = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # (Optional) the name of a configuration set to use for this message.
    # If you comment out this line, you also need to remove or comment out
    # the "X-Pinpoint-CONFIGURATION-SET:" header below.
    CONFIGURATION_SET = "ConfigSet"
    
    # The subject line of the email.
    SUBJECT = 'Amazon Pinpoint Test (Python smtplib)'
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon Pinpoint Test\r\n"
                 "This email was sent through the Amazon Pinpoint SMTP "
                 "Interface using the Python smtplib package."
                )
    
    # Create a MIME part for the text body.
    textPart = MIMEText(BODY_TEXT, 'plain')
    
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon Pinpoint SMTP Email Test</h1>
      <p>This email was sent with Amazon Pinpoint using the
        <a href='https://www.python.org/'>Python</a>
        <a href='https://docs.python.org/3/library/smtplib.html'>
        smtplib</a> library.</p>
    </body>
    </html>
                """
    
    # Create a MIME part for the HTML body.
    htmlPart = MIMEText(BODY_HTML, 'html')
    
    # The message tags that you want to apply to the email.
    TAG0 = "key0=value0"
    TAG1 = "key1=value1"
    
    # Create message container. The correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    
    # Add sender and recipient addresses to the message
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Cc'] = CCRECIPIENT
    msg['Bcc'] = BCCRECIPIENT
    
    # Add the subject line, text body, and HTML body to the message.
    msg['Subject'] = SUBJECT
    msg.attach(textPart)
    msg.attach(htmlPart)
    
    # Add  headers for configuration set and message tags to the message.
    msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
    msg.add_header('X-SES-MESSAGE-TAGS',TAG0)
    msg.add_header('X-SES-MESSAGE-TAGS',TAG1)
    
    # Open a new connection to the SMTP server and begin the SMTP conversation.
    try:
        with smtplib.SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls()
            #stmplib docs recommend calling ehlo() before and after starttls()
            server.ehlo()
            server.login(USERNAME_SMTP, PASSWORD_SMTP)
            #Uncomment the next line to send SMTP server responses to stdout
            #server.set_debuglevel(1)
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")

    
        