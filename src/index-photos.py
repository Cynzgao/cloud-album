import json
import requests
import boto3

def lambda_handler(event, context):
    print(event)
    body = event['Records'][0]
    objectKey = body['s3']['object']['key']
    bucket = body['s3']['bucket']['name']
    createdTimestamp = body['eventTime']

    #detech labels
    rek_client=boto3.client('rekognition')
    res = rek_client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':objectKey}})
    labels = [l['Name'] for l in res['Labels']]
    print(labels)

    #data to be added to ES
    data = json.dumps({'objectKey':objectKey, 'bucket':bucket, 'createdTimestamp':createdTimestamp, 'labels':labels})

    # post to ES
    host = 'https://vpc-photos-3m3fbbiusvhbxwsdggq3ir47zm.us-east-1.es.amazonaws.com/photos/photo'
    headers = {'content-type': 'application/json'}
    response = requests.post(host, data = data, headers=headers)
    print(response.content)


    # helper code to verify photo is posted to ES, only for testing purposes - query returns all documents in ES
    geturl = 'https://vpc-photos-3m3fbbiusvhbxwsdggq3ir47zm.us-east-1.es.amazonaws.com/photos/_search?pretty=true&q=*:*'
    headers = {'content-type': 'application/json'}
    r = requests.get(geturl, headers=headers)
    print(r.json())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
