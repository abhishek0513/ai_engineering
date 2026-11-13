# standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
import ollama

# Local modules
from tools import Tools, FUNCTION_NAME_TO_FUNCTION

load_dotenv()  # by default looks for .env file
ollama_host = os.getenv("host")
model_name = os.getenv("MODE")

client = ollama.Client(host=ollama_host)
print("Sending request to local model...")

messages = []

# Safety limit: the max number of model rounds for ONE user question
MAX_STEPS = 5

messages.append(
    {
        "role": "system",
        "content": "Always respond in 20 words or less. If you don't know the answer, say 'I don't know'."
    }
)

def stream_chat(history):
    stream = client.chat(
        model=model_name,
        messages=history,
        tools=Tools,
        stream=True,
    )

    full_response = ""
    tool_calls = []
    label_printed = False

    # Streaming started
    try:
        for chunk in stream:
            msg = chunk.message

            # 1. Content Streaming: Stream text chunks in real-time
            if msg.content:
                if not label_printed:
                    print("Assistant: ", end="", flush=True)
                    label_printed = True
                print(msg.content, end="", flush=True)
                full_response += msg.content

            # 2. Capture Tool Calls if requested by the model
            if msg.tool_calls:
                tool_calls = msg.tool_calls

    except KeyboardInterrupt:
        print("\n {Stopped By You}")
        tool_calls = []

    if label_printed:
        print()  # Move to the next line after the assistant's response

    return full_response, tool_calls


def build_tool_calls_payload(tool_calls):
    """
    Converts collected Ollama tool calls into the dict format
    expected inside an assistant history message.
    """
    payload = []
    for tool_call in tool_calls:
        tool_call_dict = {
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }
        payload.append(tool_call_dict)
    return payload


# Chat loop starts from here
while True:
    user_input = input("\nAbhishek: ")
    
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Exiting...")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Chained Tool Calling with MAX_STEPS safety limit
    for step in range(MAX_STEPS):
        full_response, tool_calls = stream_chat(messages)

        if not tool_calls:
            break

        print(f"Model requested {len(tool_calls)} tool call(s) at step {step + 1}")

        # Append assistant message with tool calls request to history
        messages.append({
            "role": "assistant",
            "content": full_response,
            "tool_calls": build_tool_calls_payload(tool_calls)
        })

        # Execute each tool and append the result
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            func_args = tool_call.function.arguments
            
            try:
                print(f" -> Running {func_name}({func_args})")
                fn = FUNCTION_NAME_TO_FUNCTION.get(func_name)
                if fn:
                    result = fn(**func_args)
                else:
                    result = f"Function {func_name} not found"
            except Exception as e:
                result = f"Error while running {func_name} : {e}"
            
            print(f"    ↳ Output: {result}")
            
            messages.append({
                "role": "tool",
                "content": str(result),
            })

    else:
        # Ran out of steps: The model never converged on a final answer
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "assistant",
            "content": fallback
        })
        print("Assistant: " + fallback)
        continue

    # Append final successful assistant response to history
    messages.append({
        "role": "assistant",
        "content": full_response
    })