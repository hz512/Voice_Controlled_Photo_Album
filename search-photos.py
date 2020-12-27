import requests
import boto3
import json
import time

# update for demo!!!
lex = boto3.client('lex-runtime')
ES_URL = "https://search-photos-w5sjiy7nbbibxmg2cgggwbrtim.us-east-1.es.amazonaws.com/photos/_search"
HEADERS = {"Content-Type": "application/json"}

def lambda_handler(event, context):
	queryString = event['queryStringParameters']['q']
	response = lex.post_text(
		botName='photo_album',
		botAlias='photo_album',
		userId= 'haoran',
		inputText= queryString
	)
	print("lex response:", response)
	slots = response["slots"]
	topics = [value if value for key, value in slots.items()]
	print("topics:", topics)

	result = {}
	for topic in topics:
		query = {
        	"size": 5,
        	"query": {
	            "multi_match": {
	                "query": topic,
	                "fields": ["labels"]
	            }
			}
		}
		response = requests.get(ES_URL, headers=HEADERS, data=json.dumps(query)).json()
		photos = response['hits']['hits']
		for photo in photos:
			photo_name = photo['_source']['objectKey']
			bucket_name = photo['_source']['bucket']
			result[photo_name] = 'https://' + bucket_name +  '.s3.amazonaws.com/' + photo_name
			print(topic, photo_name)

	return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            "Access-Control-Allow-Origin" : "*"
            }
    }
