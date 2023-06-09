import boto3
import json
from utils import send_response

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print("event: ", event)
    print("context: ", context)
    
    if event["resource"] == "/addtocart/{userId}":
        print("this is an add to cart operation")
        product_id = event["pathParameters"]["userId"]
        
        products_table = dynamodb.Table("rfid_store")
        cart = dynamodb.Table("cart")
        
        res = products_table.get_item(Key = {"product_id": product_id})
        requested_item = res['Item']
        
        print("requested item: ", requested_item)
        
        temp = requested_item["product_id"]
        
        requested_item["id"] = temp
        del requested_item["product_id"]
        
        if not requested_item: 
            return send_response({"message": 'no product found'}, 401)
        
        # cart.put_item(Item= requested_item, Key = {"product_id": requested_item["product_id"]})
        cart.put_item(Item = requested_item)
        
        return send_response({"message": "item added to cart"}, 200)
        
        
    if event["resource"] == "/getitem/{itemId}":
        product_id = event["pathParameters"]["itemId"]
        
        products_table = dynamodb.Table("rfid_store")
        
        res = products_table.get_item(Key={
        'product_id': product_id,
        })  
        
        item = res['Item']
        
        if not item:
            return send_response({"message": "no product found"}, 401)
        
        print("dynamo item: ", item)
        return send_response(item, 200)

    return send_response("unhandled route", "500")

