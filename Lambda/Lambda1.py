import json
import datetime
import ast
import boto3

def lambda1_handler(event, context):
    db_client = boto3.client('dynamodb')
    data = ast.literal_eval(event['body'])
    
    db_client.put_item(
        TableName = '<YOUR_TABLE_NAME>',
        Item = {
            "id": {'S':str(datetime.datetime.now())},
            "username": { 'S':data['username']},
            "address": {'S':data['address']},
            "phone": {'S':data['phone']}
        }
    )
    
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work.
            "Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS 
        },
        "body": json.dumps(
            {"message": "hello world"}
        )
    }
