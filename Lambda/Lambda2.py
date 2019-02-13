import boto3
import json

def lambda2_handler(event, context):
    db_client = boto3.client('dynamodb')
    resp = db_client.scan(
        TableName = '<YOUR_TABLE_NAME>'
    )

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS 
        },
        'body': json.dumps({
            "message": "hello world",
            "data": json.dumps(resp['Items'])
        })
    }
    
    