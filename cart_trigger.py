import json
import boto3 
from utils import send_message

ws = boto3.client("apigatewaymanagementapi", endpoint_url="https://70yashkdmb.execute-api.eu-central-1.amazonaws.com/production")
dynamodb = boto3.resource("dynamodb")

cartDB = dynamodb.Table("cart")
sessions = dynamodb.Table("ws-sessions")

def lambda_handler(event, context):
    connections = sessions.scan()
    connections = connections["Items"]
    
    cartItems = cartDB.scan()
    cartItems = cartItems["Items"]
    
    print("cart: ", cartItems )
    print("records: ", event["Records"])
    
    for record in event["Records"]:
        if record["eventName"] == "MODIFY": 
            message = json.dumps({
                'type': 'cart_updated',
                'payload': cartItems
            }, default = str)
            send_message(ws, connections, message, sessions)
            
        if record["eventName"] == "INSERT": 
            message = json.dumps({
                'type': "cart_add", 
                'payload': cartItems
            }, default = str)
            send_message(ws, connections, message, sessions)
        
        if record["eventName"] == "REMOVE": 
            message = json.dumps({
                'type': 'cart_delete',
                'payload': cartItems
            }, default=str)
            send_message(ws, connections, message, sessions)
            