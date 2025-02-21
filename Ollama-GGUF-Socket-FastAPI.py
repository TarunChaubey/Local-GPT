from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
from llama_cpp import Llama
import uvicorn
import asyncio

app = FastAPI()

# The `llm = Llama(...)` code block is initializing an instance of the `Llama` class. Here's a
# breakdown of the parameters being passed to the `Llama` constructor:
llm = Llama(
    model_path='LLM-Quantize-Model/qwen2.5-1.5b-instruct-q5_k_m.gguf',  # Ensure model is optimized for CPU
    temperature=0.7,  # Lower temperature for less randomness, faster processing
    top_p=0.9,        # More focused sampling (decreases computational complexity)
    n_ctx=4096,       # Increase context window size if memory allows
    max_tokens=1024,  # Limit output length to 1024 tokens
    repeat_penalty=1.1,  # Slightly reduce the penalty for repetition
    stop=['<|im_end|>'],  # Control output termination
    verbose=False,    # Disable verbose logging for efficiency
)

print("Model Loaded")

# Store WebSocket connections for users
# The line `user_data: Dict[str, WebSocket] = {}` is creating a dictionary named `user_data` that will
# store WebSocket connections for users. The dictionary is defined with keys of type `str` (user_id)
# and values of type `WebSocket` (WebSocket connection objects). This dictionary will be used to keep
# track of WebSocket connections for different users within the FastAPI application.
user_data: Dict[str, WebSocket] = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    This Python function creates a WebSocket endpoint with a specific user ID path parameter.    
    :param websocket: WebSocket is a class that represents a WebSocket connection in FastAPI. It allows
    bidirectional communication between the client and the server over a single, long-lived connection.
    In this context, it is used to handle WebSocket connections for the specified endpoint
    :type websocket: WebSocket
    :param user_id: The `user_id` parameter in the WebSocket endpoint represents the unique identifier
    of the user connecting to the WebSocket. This identifier can be used to distinguish different users
    and personalize the communication or actions within the WebSocket connection
    :type user_id: str
    """

    # The code `await websocket.accept()` in the `websocket_endpoint` function is used to accept the
    # WebSocket connection request from a client. When a client establishes a WebSocket connection
    # with the server, the server needs to explicitly accept the connection request.
    await websocket.accept()
    user_data[user_id] = websocket
    
    # The code block `await websocket.send_json({"type": "streaming", "message": "Welcome! How can I
    # assist you today?"})` is sending a welcome message to the client who has just connected to the
    # WebSocket endpoint. This message is in JSON format and contains two key-value pairs:
    # Send welcome message
    await websocket.send_json({
        "type": "streaming", 
        "message": "Welcome! How can I assist you today?"
    })
    
    # The `try-except` block you provided is handling the WebSocket communication within the
    # `websocket_endpoint` function. Here's a breakdown of what it does:
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
        del user_data[user_id]
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {e}")
        del user_data[user_id]
        await websocket.close()

@app.post("/chat")
async def generate_text(user_id: str, user_input: Optional[str] = "How are you doing, today"):
    try:
        # The code snippet `if user_id not in user_data:` is performing a validation check to ensure
        # that the `user_id` provided in the `generate_text` endpoint exists in the `user_data`
        # dictionary.
        # Validate user connection
        if user_id not in user_data:
            return {"status": 404, "message": "User not found"}
        
        # The `messages` list in the `generate_text` endpoint is being used to structure the
        # conversation messages that will be passed to the model for generating a response. Here's a
        # breakdown of what each part of the `messages` list is doing:
        messages = [{"role": "system", 
                "content": "You are working as helpful assistant and your job is to understand aim, gaol and objective of query query and provided response"},
                {"role": "user", "content": user_input}]

        # The code block you provided is generating a response from the model with streaming enabled.
        # Here's a breakdown of what each parameter in the `llm.create_chat_completion` function call
        # is doing:
        # Generate a response from the model with streaming enabled
        response = llm.create_chat_completion(
            messages=messages,
            temperature=1.2,
            repeat_penalty=1.178,
            stop=['<|im_end|>'],
            max_tokens=1024,
            stream=True  # Enable streaming
        )
        
        # This block of code is responsible for processing the response generated by the model in
        # chunks and sending it back to the user in a streaming manner through the WebSocket
        # connection. Here's a breakdown of what each part of the code is doing:
        response_content = ""
        for chunk in response:
            if "choices" in chunk and "delta" in chunk["choices"][0] and "content" in chunk["choices"][0]["delta"]:
                content = chunk["choices"][0]["delta"]["content"]
                response_content += content
                print(content, end="", flush=True)  # Print the response in one line

                # Send streaming content immediately
                if user_id in user_data:
                    await user_data[user_id].send_json({
                        "type": "streaming", 
                        "message": content
                    })
                else:
                    # Handle disconnected user
                    return {"status": 404, "message": "User disconnected"}

        # Send completion message
        if user_id in user_data:
            await user_data[user_id].send_json({
                "type": "complete", 
                "message": "Response complete"
            })

        return {"status": 200, "message": "Completed", "content": response_content}

    # In the provided code snippet, the `except Exception as e:` block is used for exception handling.
    # Here's a breakdown of what this block is doing:
    except Exception as e:
        print(f"Error: {e}")
        # Send error message through WebSocket if possible
        if user_id in user_data:
            await user_data[user_id].send_json({
                "type": "error", 
                "message": f"Generation error: {str(e)}"
            })
        return {"status": 500, "message": f"Internal Server Error: {str(e)}"}
    
# The code block `app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
# allow_methods=["*"], allow_headers=["*"])` is configuring Cross-Origin Resource Sharing (CORS)
# settings for the FastAPI application. Here's a breakdown of what each parameter is doing:
# Allow CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# The `# Run the app` section in the provided Python code is a common pattern used in Python scripts
# to ensure that the script is executed only when it is run directly as the main program, and not when
# it is imported as a module in another script.
# Run the app
if __name__ == "__main__":
    uvicorn.run(app, port=8000)