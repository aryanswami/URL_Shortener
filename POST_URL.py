import os
import json
import boto3
import shortuuid
from time import strftime, time
from custom_encoder import CustomEncoder

ddb = boto3.resource('dynamodb', region_name = 'us-east-1').Table('ShortURLs')

# create a function for generating the time at which the short key is created.
def generate_timestamp():
    response = strftime("%Y-%m-%dT%H:%M:%S")
    return response

# create a function which checks for the short key in the table.
def check_id(ShortKey):
    if 'Item' in ddb.get_item(Key={'ShortKey': ShortKey}):
        response = generate_id()
    else:
        return ShortKey
        
# create a function which generates a short key of length 5 for the long url provided. 
def generate_id():
    ShortKey = shortuuid.ShortUUID().random(length=5) # imported from the shortuuid built-in library.
    print(ShortKey)
    response = check_id(ShortKey)
    return response

def lambda_handler(event, context):
    print(event)
    try:
        ShortKey = generate_id()
        short_url = ShortKey
        baseUrl =  "https://0mz8m03m21.execute-api.us-east-1.amazonaws.com/t/" # The response will be printed along with the base url.
        originalURL = json.loads(event.get('body')).get('originalURL')
        timestamp = generate_timestamp()
        # store the details in the dynamodb table.
        response = ddb.put_item(
            Item={
                'ShortKey': ShortKey,
                'short_url': short_url,
                'originalURL': originalURL,
                'createdOn': timestamp,
                'hits': int(0)
        }
    )
        res = {"shortURL": baseUrl + ShortKey} # return the short key along with the base url.
        return buildResponse('200', res)
    
    except:
        return {
            'statusCode': '500',
            'body': 'Internal Server Error.'
        
    }
# create a custom function which builds a response in json format and prints it for the user.
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' 
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response