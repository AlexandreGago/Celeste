import asyncio
import websockets
import argparse

async def server_handler(websocket, path):
    while True:
        try:
            # Wait for a message from the client
            message = await websocket.recv()
            print(f"Received message: {message}")

            # Send a response back to the client
            response = f"Server received: {message}"
            await websocket.send(response)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break

async def start_server(port=8765):
    server = await websockets.serve(
        server_handler, "0.0.0.0", port
    )
    print(f"WebSocket server started on ws://localhost:{port}")

    # Keep the server running
    await server.wait_closed()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Websocket Server')
    parser.add_argument('--port', type=int, default=8765, help='port number')
    args = parser.parse_args()
    asyncio.run(start_server(args.port))