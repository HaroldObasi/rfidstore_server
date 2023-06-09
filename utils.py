import json

def send_response(object, statusCode):
    response = {
    'statusCode': statusCode,
    'headers': {
        'Access-Control-Allow-Origin': '*',  
        'Access-Control-Allow-Headers': '*', 
        'Access-Control-Allow-Methods': '*', 
        'Access-Control-Max-Age': '86400', 
        },
    'body': json.dumps(object, default=str), 
    }
    return response


def send_message(ws, connections, message, sessions): 
    for connection in connections:
        connectionId = connection["connectionId"]
        try:
            ws.post_to_connection(ConnectionId = connectionId, Data = message)
        except ws.exceptions.GoneException:
            sessions.delete_item(Key={'connectionId': connectionId}) 
                