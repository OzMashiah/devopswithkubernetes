import json
import asyncio
import nats
from nats.aio.client import Client as NATS

# Create a NATS client instance
nc = NATS()

async def message_handler(msg):
    """ This is where we handle the NATS message and log it to a file. """
    try:
        # Parse the JSON message
        json_data = json.loads(msg.data.decode())
        
        # Log the JSON to a file
        with open('nats_messages.json', 'a') as f:
            json.dump(json_data, f, indent=2)
            f.write("\n")  # Add a newline between each JSON object
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {str(e)}")
    
async def run():
    """ Function to connect to NATS and subscribe to the required topic """
    # Connect to the NATS server
    await nc.connect("nats://localhost:4222")  # Adjust the server URL as needed
    
    # Subscribe to a NATS topic
    await nc.subscribe("your_topic", cb=message_handler)

    # Keep the connection alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

# Example entry point
import asyncio
asyncio.run(run())

