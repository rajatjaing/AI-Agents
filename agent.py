from openai import OpenAI
from tools import *

client = OpenAI(api_key="YOUR_API_KEY")

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current system time",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "name": "log_triage",
        "description": "Analyze error logs",
        "parameters": {
            "type": "object",
            "properties": {
                "log_text": {"type": "string"}
            },
            "required": ["log_text"]
        }
    }
]

def run_agent(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    message = response.choices[0].message

    # If LLM wants to call tool
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = eval(tool_call.function.arguments)

        if function_name == "calculate":
            result = calculate(**arguments)
        elif function_name == "get_current_time":
            result = get_current_time()
        elif function_name == "log_triage":
            result = log_triage(**arguments)

        # Send result back to LLM
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_input},
                message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                }
            ]
        )

        return final_response.choices[0].message.content

    return message.content

while True:
    user_input = input("You: ")
    print("Agent:", run_agent(user_input))
