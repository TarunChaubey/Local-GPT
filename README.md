# Llama-Cpp Setup and GGUF Model Integration

## Aim
The goal of this project is to set up and integrate the **llama-cpp** library with a GGUF model for natural language processing tasks. This allows users to generate responses using various Python scripts tailored for different use cases (full token generation, streaming, and socket-based responses).

## Goals
- Install the **llama-cpp** library and its dependencies.
- Download a GGUF model and integrate it into the project.
- Run different Python scripts to generate model responses using the downloaded GGUF model.
  - **Ollama-GGUF.py**: Generates and returns a response after all tokens are generated.
  - **Ollama-GGUF-Stream.py**: Generates and streams the response as tokens start generating.
  - **Ollama-GGUF-Socket-FastAPI.py**: Streams the response as tokens are generated and serves it via a socket using FastAPI.

## Objectives
1. **Install llama-cpp** and its dependencies by following the instructions provided in the repository.
   - GitHub Link: [llama.cpp](https://github.com/ggml-org/llama.cpp)

2. **Download GGUF Model**
   - Download the GGUF model from the following link:
     - [Qwen2.5-1.5B-Instruct-GGUF Model](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main)
   - Use the model file `q5_k_m` for testing (though any model can be used).

3. **Python Scripts for Response Generation**
   - `Ollama-GGUF.py`: This script generates a response after generating all tokens.
   - `Ollama-GGUF-Stream.py`: This script generates a response and streams it token by token.
   - `Ollama-GGUF-Socket-FastAPI.py`: This script uses FastAPI to stream the token generation process over a socket connection.

## Demo Video
For a better understanding of the setup and usage, refer to the demo video.

- [Video.wmv](GGUFModelLocal.wmv)

## Requirements
- Python 3.x
- llama-cpp library
- Dependencies as mentioned in the llama-cpp repository
- FastAPI (for socket-based generation)

## Installation

### Step 1: Install llama-cpp and its dependencies
To install the `llama-cpp` library, follow the instructions in the [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp).

### Step 2: Download the GGUF Model
Visit the following link to download the GGUF model:
- [Qwen2.5-1.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main)
- Download the model (`q5_k_m`) or any other compatible model.

### Step 3: Run the Python Scripts
- **Ollama-GGUF.py**: Run the script to generate a full response.
- **Ollama-GGUF-Stream.py**: Run this for token-by-token response streaming.
- **Ollama-GGUF-Socket-FastAPI.py**: Run for FastAPI socket-based response streaming.

## Notes
Ensure that you have all the necessary dependencies installed, and follow the instructions provided in the respective repositories for setting up the environment.

For further questions or issues, feel free to open an issue in the repository.