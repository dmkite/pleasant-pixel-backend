import boto3
user_table = 'pleasant_pixel_users'
client = boto3.client('dynamodb')

# email: xxx@yyy.zzz
# password: hash
# preferences:
#     reminderTime: 00:00 - 24:00
#     colorScheme: id

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