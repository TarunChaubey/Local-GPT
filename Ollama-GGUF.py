# The code snippet you provided is utilizing the Llama model for generating a response to a user input
# prompt regarding the importance of AI in education. Here's a breakdown of what each part of the code
# is doing:
# pip install llama-cpp-python 
# huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF qwen2.5-1.5b-instruct-q5_k_m.gguf --local-dir . --local-dir-use-symlinks False

from llama_cpp import Llama

# Initialize the Llama model
# The code snippet you provided is initializing the Llama model for generating responses based on user
# input. Here's a breakdown of the parameters passed to the `Llama` constructor:
llm = Llama(
    model_path='LLM-Quantize-Model/qwen2.5-1.5b-instruct-q5_k_m.gguf',  # Ensure model is optimized for CPU
    n_gpu_layers=4,  # Specify GPU layers or modify based on your setup
    temperature=1.1,
    top_p=0.5,
    n_ctx=32768,
    max_tokens=1500,
    repeat_penalty=1.178,
    stop=['<|im_end|>'],
    verbose=False
)

# Define the user input (prompt)
user_input = "Explain the importance of AI in education."

# Prepare the message
messages = [
    {"role": "user", 
     "content": user_input}]

# Generate a response from the model
response = llm.create_chat_completion(
    messages=messages,
    temperature=1.2,
    repeat_penalty=1.178,
    stop=['<|im_end|>'],
    max_tokens=1500)

# Extract and print the response in one line
response_content = response['choices'][0]['message']['content']
print(response_content)

