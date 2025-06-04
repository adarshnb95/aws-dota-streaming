import os
import json
import boto3
import requests

KINESIS_STREAM = os.environ.get('STREAM_NAME', 'DotaLiveStream')
OPENDOTA_URL   = 'https://api.opendota.com/api/live'

kinesis = boto3.client('kinesis')

def lambda_handler(event, context):
    # 1) Try fetching OpenDota live data
    try:
        resp = requests.get(OPENDOTA_URL, timeout=5)
        resp.raise_for_status()
        live_games = resp.json()
        print(f"Fetched {len(live_games)} live games from OpenDota")
    except Exception as e:
        print(f"ERROR fetching OpenDota live: {e}")
        return { 'error': str(e) }

    # 2) Ingest each game into Kinesis
    ingested = 0
    for game in live_games:
        try:
            payload = json.dumps(game)
            kinesis.put_record(
                StreamName=KINESIS_STREAM,
                Data=payload.encode('utf-8'),
                PartitionKey=str(game.get('match_id', 'unknown'))
            )
            ingested += 1
        except Exception as e:
            print(f"ERROR putting to Kinesis for match {game.get('match_id')}: {e}")

    # 3) Log how many were ingested
    print(f"Ingested {ingested} games into Kinesis stream {KINESIS_STREAM}")
    return { 'ingested_games': ingested }
