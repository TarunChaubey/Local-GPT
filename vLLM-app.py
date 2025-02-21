from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
import uvicorn
import json
import httpx
import asyncio

app = FastAPI()

# Store WebSocket connections
user_data: Dict[str, WebSocket] = {}

# API Configuration
headers = {"Content-Type": "application/json"}
route = "v1/chat/completions"
url = f"http://localhost:9000/{route}"

async def stream_response(websocket: WebSocket, response):
    """Handle streaming response and send chunks to websocket"""
    buffer = ""
    async for chunk in response.aiter_lines():  # Using aiter_lines for async streaming
        if chunk:
            try:
                chunk_str = chunk.decode('utf-8') if isinstance(chunk, bytes) else chunk
                if chunk_str.startswith('data: '):
                    json_str = chunk_str[6:].strip()
                    if json_str:
                        data = json.loads(json_str)
                        message = data.get('choices', {})[0].get('delta', {}).get('content', '')
                        if message:
                            await websocket.send_json({"message": message})
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing chunk: {e}")
                break
        await asyncio.sleep(0.01)  # Small delay to prevent blocking

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    user_data[user_id] = websocket
    
    try:
        await websocket.send_json({
            "message": "Welcome! How can I assist you today?"
        })
        
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del user_data[user_id]
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {e}")
        if user_id in user_data:
            del user_data[user_id]
        await websocket.close()

async def fetch_model_response(payload):
    """Fetch the response from the model using httpx"""
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response

@app.post("/chat")
async def generate_text(user_id: str, user_input: Optional[str], background_tasks: BackgroundTasks):
    if user_id not in user_data:
        return {"status": 404, "message": "User not found"}

    payload = {
        "model": "smollm-360m-instruct-v0.2",
        "messages": [
            {
                "role": "system",
                "content": """You are working as a Helpful Assistant, and your job is to understand the goal, aim, and objective of the user's question. You should follow a logical thought process, break down the problem into smaller subprocesses, and provide the most optimized and justifiable answer."""
            },
            {
                "role": "user",
                "content": f"User Query: {user_input}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2048,
        "stream": True  # Keep stream flag here for the server-side API
    }

    try:
        # Add the background task to fetch the model's response asynchronously
        background_tasks.add_task(process_user_request, user_id, payload)
        return {"status": 200, "message": "Processing your request"}
    
    except Exception as e:
        print(f"Exception: {e}")
        await user_data[user_id].send_json({
            "message": f"Error: {str(e)}"
        })
        return {"status": 500, "message": "Internal Server Error"}

async def process_user_request(user_id: str, payload):
    try:
        # Get the model response asynchronously
        response = await fetch_model_response(payload)
        if response.status_code == 200:
            await stream_response(user_data[user_id], response)
        else:
            await user_data[user_id].send_json({
                "message": f"Error: {response.status_code}"
            })
    except Exception as e:
        print(f"Error processing user request: {e}")
        if user_id in user_data:
            await user_data[user_id].send_json({
                "message": f"Error: {str(e)}"
            })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
