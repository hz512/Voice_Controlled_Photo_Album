import requests
import boto3
import json

# update for cloudformation demo
rekognition = boto3.client("rekognition")
ES_URL = "https://search-photos-w5sjiy7nbbibxmg2cgggwbrtim.us-east-1.es.amazonaws.com/photos/Photo"

def lambda_handler(event, context):
	for photo in event['Records']:
		objectKey = photo['s3']['object']['key']
		bucket = photo['s3']['bucket']['name']
		createdTimestamp = photo['eventTime']
		print("bucket:{}; key:{}; time:{}".format(bucket, objectKey, createdTimestamp))
		
		rekog_result = rekognition.detect_labels(
			Image = {
                'S3Object': {
                    'Bucket': bucket,
                    'Name': objectKey
                }
            }
        )
		print("labels: " + str(rekog_result['Labels']))
		photo_labels = [label["Name"] for label in rekog_result['Labels']]
		json_obj = {
        	"objectKey": objectKey,
        	"bucket": bucket,
        	"createdTimestamp": createdTimestamp,
        	"labels": photo_labels
        }
		response = requests.post(ES_URL,
            data = json.dumps(json_obj).encode("utf-8"),
            headers = { "Content-Type": "application/json" }
        )
		print(response)

	return {
        'statusCode': 200,
        'body': json.dumps("Photo indexed into ES!")
	}
