import json
import boto3
dynamodb = boto3.resource("dynamodb")

sessions = dynamodb.Table("ws-sessions")
cart = dynamodb.Table('cart')

def lambda_handler(event, context):
    
    connectionId = event["requestContext"]["connectionId"]
    sessions.put_item(Item={"connectionId": connectionId})

    print("** CONNECTED TO WS **")
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {'status': 'success'},
        'body': "success"
    }
    
