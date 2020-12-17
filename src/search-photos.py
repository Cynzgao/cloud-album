import json
import requests
import boto3
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
es_host = 'https://vpc-photos-3m3fbbiusvhbxwsdggq3ir47zm.us-east-1.es.amazonaws.com/'
s3 = boto3.resource('s3')
album = s3.Bucket('photos-hw3b2')

def lambda_handler(event, context):
    print("hi")
    print("test")
    # initialize lex
    print(context)
    lex_client = boto3.client("lex-runtime")
    # given search query q
    print(event)
    text = event["params"]['q']
    print(text)

    '''
    # TODO: check LEX part
    lex_response = client.post_text(
        botName = 'PhotoBot',
        botAlias = 'test',
        userId = '',
        inputText = text
        )
    lex_response = {"slots": {"key1": "raccoon"}}
    print(lex_response)
    if 'slots' in lex_response:
        key = [lex_response['slots']['key1']]
        print(key)
        output = es_search(key)
        ## TODO: check response body format
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(output),
            "isBase64Encoded": False
        }

    else:
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": [],
            "isBase64Encoded": False
        }

    return response
    '''
    output = es_search([text])
    print("output is:", output)
    return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(output),
        }

def es_search(key):
    headers = {'content-type': 'application/json'}
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
    geturl = es_host+"photos/_search?q="
    # use signed http request to get es result
    response = []
    # search two keys maybe?
    for k in key:
        if (k != ''):
            url = geturl + k
            r = requests.get(url, auth = awsauth)
            response.append(r.json())

    res = []
    # if there are hits, retrieve from s3 bucket 2
    for r in response:
        if 'hits' in r:
            hit = r['hits']['hits']
            print(hit)
            if hit:
                for h in hit:
                    path = h['_source']['objectKey']
                    #object_url = "https://s3.us-east-1.amazonaws.com/photos-hw3b2/" + path
                    res.append(path)

    print(res)

    return res
