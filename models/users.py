import boto3
user_table = 'pleasant_pixel_users'
client = boto3.client('dynamodb')

# email: xxx@yyy.zzz
# password: hash
# preferences:
#     reminderTime: 00:00 - 24:00
#     colorScheme: id

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
    print(payload)
    new_settings = {}
    for setting in settings:
        if payload.get(setting):
            new_settings[setting] = {
                'S': payload.get(setting)
            }

    print (new_settings)
    response = client.put_item(
            TableName=user_table,
            Item={
                'email': {
                    'S': email.lower()
                },
                'settings': {
                    'M': new_settings
                }
            }
        )
    print(response)
    return True