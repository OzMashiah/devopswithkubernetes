I decided to add an endpoint to the frontend at /recieved-tasks that gets the messages from the broadcasters instead of using a messaging app.
After a new task was added or changed through the frontend, the frontend contacts the backend which write the new data in the postgres database and send an update to the NATS. The broadcaster receives the update from the NATS and POSTs it to the frontend, which saves the jsons in memory. 
This also works with scaling of the broadcaster since subscribing to a queue group.
