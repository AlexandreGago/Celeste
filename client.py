import asyncio
import websockets
import argparse
async def client(port=8765):
    uri = f"ws://192.168.151.152:{port}"
    async with websockets.connect(uri) as websocket:
        while True:
            # Send a message to the server
            message = input("Enter a message to send to the server (or 'exit' to quit): ")
            await websocket.send(message)

            if message.lower() == 'exit':
                break

            # Receive and print the server's response
            response = await websocket.recv()
            print(f"Server response: {response}")

# Run the client
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Websocket Client')
    parser.add_argument('--port', type=int, default=8765, help='port number')
    args = parser.parse_args()
    asyncio.run(client(args.port))