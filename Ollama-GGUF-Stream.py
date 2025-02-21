# pip install llama-cpp-python 
# huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF qwen2.5-1.5b-instruct-q5_k_m.gguf --local-dir . --local-dir-use-symlinks False

from llama_cpp import Llama

# Initialize the Llama model
llm = Llama(
    model_path='LLM-Quantize-Model/qwen2.5-1.5b-instruct-q5_k_m.gguf',  # Ensure model is optimized for CPU
    # n_gpu_layers=None,  # Comment out GPU-related parameters since you're using CPU
    temperature=0.7,  # Lower temperature for less randomness, faster processing
    top_p=0.9,        # More focused sampling (decreases computational complexity)
    n_ctx=32768,       # Reduce context window to save memory and increase speed
    max_tokens=8192,  # Reduce output length for quicker responses
    repeat_penalty=1.1,  # Slightly reduce the penalty for repetition
    stop=['<|im_end|>'],  # Keep the stop token to control output termination
    verbose=False,    # Disable verbose logging for efficiency
)

user_input = ""

while user_input != "exit":
    # Define the user input (prompt)
    print("Enter your query")
    user_input = input()
    print("Query:", user_input)
    # Prepare the message
    messages = [{"role": "system", 
                "content": """You are working as helpful assistant and your job is to understand aim, goal and objective of user query, use chain of thought to break down problem into subproblem, find best optimize solution and while combinting sub-solution check answer relevency with query and give response,

                Instruction:
                    ** Do not try to short the answer, explain as much as you can without thinking token count **

                """},
                {"role": "user", "content": user_input}]

    # Generate a response from the model with streaming enabled
    response = llm.create_chat_completion(
        messages=messages,
        temperature=1.2,
        repeat_penalty=1.178,
        stop=['<|im_end|>'],
        max_tokens=1500,
        stream=True  # Enable streaming
    )

    print("AI response:")
    # Stream the response and print each chunk as it comes
    response_content = ""
    for chunk in response:
        try:
            # Append the content of each chunk to the response
            if "choices" in chunk and "delta" in chunk["choices"][0] and "content" in chunk["choices"][0]["delta"]:
                content = chunk["choices"][0]["delta"]["content"]
                response_content += content
                print(content, end="", flush=True)  # Print the response in one line
        except Exception as e:
            print(f"Error: {e}")
    print("-"*150)  # New line after response