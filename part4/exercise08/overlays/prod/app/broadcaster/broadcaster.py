import json
import nats
import requests
import asyncio
import threading
from nats.aio.client import Client as NATS

class Broadcaster:
    def __init__(self, nats_url: str, subject: str, frontend_url: str):
        self.nats_url = nats_url
        self.subject = subject
        self.frontend_url = frontend_url
        self.nc = None

    async def connect_to_nats(self):
        """ Connect to NATS server """
        self.nc = NATS()
        await self.nc.connect(self.nats_url)
        print(f"Connected to NATS at {self.nats_url}")

    async def handle_message(self, msg):
        """ Handle the incoming NATS message and forward it to the frontend """
        try:
            # Parse the message from NATS (assume it's JSON)
            task_data = json.loads(msg.data.decode())
            print(f"Received new task data: {task_data}")

            # Send the task data to the frontend service
            response = requests.post(self.frontend_url, json=task_data)
            print(f"Sent data to frontend at {self.frontend_url}, response status: {response.status_code}")

        except Exception as e:
            print(f"Error handling message: {e}")

    async def subscribe_to_nats(self):
        """ Subscribe to NATS subject for new/updated to-dos """
        queue_group = "todo-tasks-group"
        await self.nc.subscribe(self.subject, queue=queue_group, cb=self.handle_message)
        print(f"Subscribed to subject {self.subject}")

    async def run(self):
        """ Main loop to connect and subscribe to NATS """
        await self.connect_to_nats()
        await self.subscribe_to_nats()

        # Keep the connection open and listening for messages
        while True:
            await asyncio.sleep(1)

def start_nats_loop():
    """ Start the NATS loop in a separate thread """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcaster.run())

if __name__ == "__main__":
    # Instantiate the broadcaster class
    broadcaster = Broadcaster(
        nats_url="nats://my-nats.default:4222",
        subject="todo.tasks",
        frontend_url="http://reverseproxy-svc:2345/received-tasks"
    )

    # Start the NATS event loop in a separate thread
    nats_thread = threading.Thread(target=start_nats_loop)
    nats_thread.daemon = True  # Ensures the thread stops when the main program exits
    nats_thread.start()

    # No Flask app needed anymore
    while True:
        pass  # Keeps the process alive, or use `await asyncio.sleep(1)` if you want an async event loop.

