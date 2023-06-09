import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ws-sessions")

def lambda_handler(event, context):

    connectionId = event["requestContext"]["connectionId"]
    print("connection id of client: ", connectionId)
    table.delete_item(
       Key={"connectionId": connectionId}
    )
    print("**DISCONNECTED FROM WS**")
    
    return { "statusCode": 200 }
    
