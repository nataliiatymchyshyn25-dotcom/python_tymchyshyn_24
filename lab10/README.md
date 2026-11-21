A simple console chat using Python's `socket` and `threading` libraries. The server handles multiple clients using separate threads and forwards messages between them.

### Running

- Run `server.py` to start the server on `127.0.0.1:5000`.
- Run `client.py` in a separate terminal and enter your name.
- Open additional terminals and run `client.py` to connect more users.

### Usage

Once connected, users can type messages and press Enter to send them. The server displays received messages and forwards them to all other connected clients.

Users are notified when someone joins or leaves the chat. To disconnect, enter `/exit`. The server can be stopped using `Ctrl+C`.