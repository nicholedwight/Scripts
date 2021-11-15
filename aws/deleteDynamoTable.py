import json
import boto3
import decimal
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name='<region_name>')
table = dynamodb.Table('<table_name>')

def get_user():
    activeUsers = {}
    exemptedUsers = ['<list_of_exempted_values>']
    deleteUserDict = {}
    
    try:
        user = table.scan()
        for i in user['Items']:
            json_str = json.dumps(i, cls=DecimalEncoder)
            resp_dict = json.loads(json_str)
            activeUsers[resp_dict.get('uid')] = resp_dict.get('email')
            
        for k, v in activeUsers.items():
            if v not in exemptedUsers:
                deleteUserDict[k] = v
        
        delete_user(deleteUserDict)
    except ClientError as e:
        print(e.response['Error']['Message'])
    
def delete_user(deleteUserDict):
    try:
        for uid, email in deleteUserDict.items():
            response = table.delete_item(
                Key={
                    'uid': uid
                }
            )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

def lambda_handler(event, context):
    get_user()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
