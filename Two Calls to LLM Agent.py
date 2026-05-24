# ============================================================
# IMPORTS
# ============================================================

from dotenv import load_dotenv
from openai import OpenAI

import json

# Import investigation tools
from tools.customer_tools import (
    get_customer_transactions,
    get_customer_devices,
    get_customer_upi_handles
)

# ============================================================
# LOAD ENV VARIABLES
# ============================================================

load_dotenv()

# Create OpenAI client
client = OpenAI()

# ============================================================
# TOOL DEFINITIONS
# ============================================================
#
# These tool schemas tell the LLM:
# - what tools exist
# - what they do
# - what inputs they need
#
# The model uses these descriptions to decide:
# - which tools to call
# - what arguments to generate
#
# ============================================================

tools = [

    {
        "type": "function",

        "function": {

            "name": "get_customer_transactions",

            "description": "Get all transactions for a customer",

            "parameters": {

                "type": "object",

                "properties": {

                    "customer_id": {
                        "type": "string"
                    }
                },

                "required": ["customer_id"]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "get_customer_devices",

            "description": "Get all devices linked to customer",

            "parameters": {

                "type": "object",

                "properties": {

                    "customer_id": {
                        "type": "string"
                    }
                },

                "required": ["customer_id"]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "get_customer_upi_handles",

            "description": "Get all UPI handles linked to customer",

            "parameters": {

                "type": "object",

                "properties": {

                    "customer_id": {
                        "type": "string"
                    }
                },

                "required": ["customer_id"]
            }
        }
    }
]

# ============================================================
# INITIAL USER MESSAGE
# ============================================================

messages = [

    {
        "role": "user",

        "content": "Investigate customer C001 for suspicious activity."
    }
]

# ============================================================
# FIRST MODEL CALL
# ============================================================
#
# Here model decides:
# - whether tools are needed
# - which tools to call
#
# ============================================================

response = client.chat.completions.create(

    model="gpt-4o-mini",

    messages=messages,

    tools=tools,

    tool_choice="auto"
)

# Extract assistant message
response_message = response.choices[0].message

# ============================================================
# DEBUGGING
# ============================================================

print("\n===== TOOL CALLS =====\n")

print(response_message.tool_calls)

# ============================================================
# APPEND ASSISTANT TOOL REQUEST
# ============================================================
#
# VERY IMPORTANT
#
# We must append assistant tool-call message
# BEFORE tool responses.
#
# ============================================================

messages.append(response_message)

# ============================================================
# EXECUTE ALL TOOL CALLS
# ============================================================

if response_message.tool_calls:

    for tool_call in response_message.tool_calls:

        # Tool/function name
        function_name = tool_call.function.name

        # Parse arguments JSON
        arguments = json.loads(
            tool_call.function.arguments
        )

        print(f"\nExecuting tool: {function_name}")

        print(f"Arguments: {arguments}")

        # ====================================================
        # EXECUTE CORRECT TOOL
        # ====================================================

        if function_name == "get_customer_transactions":

            result = get_customer_transactions(
                arguments["customer_id"]
            )

        elif function_name == "get_customer_devices":

            result = get_customer_devices(
                arguments["customer_id"]
            )

        elif function_name == "get_customer_upi_handles":

            result = get_customer_upi_handles(
                arguments["customer_id"]
            )

        else:

            result = "Unknown tool"

        # ====================================================
        # APPEND TOOL RESPONSE
        # ====================================================

        messages.append({

            "role": "tool",

            "tool_call_id": tool_call.id,

            "content": json.dumps(result)
        })

# ============================================================
# SECOND MODEL CALL
# ============================================================
#
# Now model receives:
# - user request
# - assistant tool requests
# - actual tool outputs
#
# Model can now reason over gathered evidence.
#
# ============================================================

final_response = client.chat.completions.create(

    model="gpt-4o-mini",

    messages=messages
)

# ============================================================
# FINAL REPORT
# ============================================================

print("\n===== INVESTIGATION REPORT =====\n")

print(final_response.choices[0].message.content)