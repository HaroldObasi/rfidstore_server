import json
import boto3 

ws = boto3.client("apigatewaymanagementapi", endpoint_url="https://70yashkdmb.execute-api.eu-central-1.amazonaws.com/production")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("ws-sessions")
cartDB = dynamodb.Table('cart')

def lambda_handler(event, context):
    
    cartItems = cartDB.scan()
    cartItems = cartItems["Items"]
    
    connectionId = event["requestContext"]["connectionId"]
    
    message = json.dumps({
        'type': 'cart_init',
        'payload': cartItems
    }, default = str)
    
    try:
        ws.post_to_connection(ConnectionId = connectionId, Data = message)
    except ws.exceptions.GoneException:
        print("connection invalid")
        table.delete_item(Key={'connectionId': connectionId}) 
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
