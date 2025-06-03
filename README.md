# aws-dota-streaming
A live e-sports score aggregator using Kinesis Data Streams, Lambda, DynamoDB, Amazon Elasticsearch Service, WebSockets (API Gateway)

# Dota Live Scores (Day 1)

**Overview:**  
- Poll OpenDota’s `/api/live` every minute  
- Push each live-game JSON into a Kinesis Data Stream

**Tech Stack (Day 1):**  
- AWS Kinesis Data Stream  
- AWS Lambda (Python)  
- EventBridge Rule  