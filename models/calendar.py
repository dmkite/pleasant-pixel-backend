import boto3

client = boto3.client('dynamodb')
calendar_table = 'pleasant_pixel_calendars'


def get_all(email):
    response = client.get_item(
        TableName=calendar_table,
        Key={
            'email': {
                'S': email.lower()
            }
        }
    )
    if not response:
        print('whoops')
    else:
        print(response)
    return response.get('Item')


def update_day(email, payload):
    response = client.update_item(
        TableName=calendar_table,
        Key={
            'email': {
                'S': email.lower()
            }
        },
        AttributeUpdates={
            email.lower(): {
                'Value': payload
            }
        }
    )
    print(response)
    return True
