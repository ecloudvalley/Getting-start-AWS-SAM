import boto3

def lambda3_handler(event, context):
    db_client = boto3.client('dynamodb')
    resp = db_client.scan(
        TableName = 'user',
    )['Items'][0]
    
    #temperature = eval(resp['temperature']['S'])
    print(resp)
    # if temperature > 28:
    #     print('too hot')
    # elif temperature < 15:
    #     print('too cold')