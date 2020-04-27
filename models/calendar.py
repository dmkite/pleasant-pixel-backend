import boto3

client = boto3.client('dynamodb')
calendar_table = 'pleasant_pixel_calendars'


# email: {
#     'M': {
#         2020: {
#             'M': {
#                 4: {
#                     'M': {
#                         1: {
#                             'M': {
#                                 'rating': {
#                                     'N': 1 - 5
#                                 },
#                                 'notes': {
#                                     'S': '150 char limit'
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }