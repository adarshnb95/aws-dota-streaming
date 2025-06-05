import json
import os
import boto3
import base64
from decimal import Decimal

# Initialize DynamoDB table resource
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']  # e.g., "DotaLiveGames"
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    ingested = 0

    for record in event['Records']:
        encoded_payload = record['kinesis']['data']
        try:
            data_json = json.loads(base64.b64decode(encoded_payload))
        except Exception as e:
            print(f"ERROR decoding record from Kinesis: {e}")
            continue

        # Convert match_id to a Python int (or Decimal) so DynamoDB sees it as N
        raw_match_id = data_json.get('match_id')
        if raw_match_id is None:
            print("WARN: Record without match_id, skipping")
            continue

        try:
            # If match_id came as a JSON string, cast to int
            data_json['match_id'] = int(raw_match_id)
        except Exception:
            # If it's already a number, you can also wrap with Decimal to be safe
            data_json['match_id'] = Decimal(raw_match_id)

        # Now write to DynamoDB
        try:
            table.put_item(Item=data_json)
            ingested += 1
        except Exception as e:
            print(f"ERROR writing match {data_json['match_id']} to DynamoDB: {e}")

    print(f"Ingested {ingested} records into DynamoDB")
    return {"ingested": ingested}