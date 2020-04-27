import boto3
user_table = 'pleasant_pixel_users'
client = boto3.client('dynamodb')

settings = ('color_theme', 'reminder_time')


def user_exists(email):
    if get_user(email) is not None:
        return True
    else:
        return False


def get_user(email):
    response = client.get_item(
        TableName=user_table,
        Key={
            'email': {
                'S': email.lower()
            }
        }
    )
    return response.get('Item', None)


def change_settings(email, payload):
    user = get_user(email)
    if not user:
        return None
    if not user.get('settings'):
        user.settings = {'M': {}}
    for setting in settings:
        if payload.get(setting):
            user['settings']['M'][setting] = {
                'S': payload.get(setting)
            }
    response = client.put_item(
        TableName=user_table,
        Item=user
    )
    return response
