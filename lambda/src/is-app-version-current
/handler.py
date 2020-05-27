import json

CURRENT_VERSION = "1.0.2"

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    user_version = body['version']
    
    ret = {'current': user_version == CURRENT_VERSION}

    return {
        'statusCode': 200,
        'body': json.dumps(ret)
    }
