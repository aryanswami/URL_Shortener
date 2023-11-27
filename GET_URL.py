import os
import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb = boto3.resource('dynamodb', region_name = 'us-east-1').Table('ShortURLs')

def lambda_handler(event, context):
    ShortKey = event['pathParameters']['ShortKey'] # Pass the short key as a path parameter.
    print(event)
    print(ShortKey)
    try:
        item = ddb.get_item(Key={'ShortKey': ShortKey}) # Get the short key from the table.
        if item.get('Item') is None:
            print(ShortKey + "Not Found.")
            return{
                'statusCode': 404,
                'body': 'Not found. Please enter a correct Short Key and try again. '
            }
        originalURL = item.get('Item').get('originalURL') # Get the original url pointing to the short key.
        # Update the hits value in the table when a correct short key is retrieved.
        ddb.update_item(
            Key={'ShortKey': ShortKey},
            UpdateExpression='set hits = hits + :val',
            ExpressionAttributeValues={':val': 1}
            )
        # Redirect the user to the Original url using 302 status code.
        return {
            "statusCode": 302,
            "headers": {
                "location": originalURL
            }
        }
    except:
        logger.exception('Error.')
        return {
            'statusCode': 500,
            'body': 'Internal Server Error. '
        }
    
