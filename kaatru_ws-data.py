import boto3
import websocket
import json
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'tmu-sustainability'

def save_to_s3(data):
    """Save data to S3 bucket."""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    file_name = f"stream_data/{timestamp}.json"
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=json.dumps(data))
        logger.info(f"Data saved to S3: {file_name}")
    except Exception as e:
        logger.error(f"Failed to save data to S3: {e}")

def on_open(ws):
    """WebSocket on_open callback."""
    logger.info("WebSocket connection opened")
    try:
        # Optional: Send a greeting message
        message = {"type": "greeting", "message": "Hello WebSocket server!"}
        ws.send(json.dumps(message))
        logger.info("Greeting message sent")
    except Exception as e:
        logger.error(f"Error sending message: {e}")

def on_message(ws, message):
    """WebSocket on_message callback."""
    try:
        data = json.loads(message)  # Parse the WebSocket message
        logger.info(f"Received data: {data}")
        save_to_s3(data)  # Save the parsed data to S3
    except Exception as e:
        logger.error(f"Failed to process message: {e}")

def on_close(ws, close_status_code, close_msg):
    """WebSocket on_close callback."""
    logger.info(f"WebSocket connection closed: {close_status_code}, {close_msg}")

def on_error(ws, error):
    """WebSocket on_error callback."""
    logger.error(f"WebSocket error occurred: {error}")

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    websocket_url = "wss://bw06.kaatru.org/stream/prod/gur/SA/sen"
    ws = websocket.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
        on_error=on_error
    )
    try:
        # Run the WebSocket connection
        ws.run_forever()
    except Exception as e:
        logger.error(f"Failed to run WebSocket client: {e}")
