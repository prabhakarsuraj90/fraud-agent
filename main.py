from dotenv import load_dotenv
from openai import OpenAI

from tools.customer_tools import get_customer_transactions

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Example investigation target
customer_id = "C001"

# Fetch transaction data
transactions = get_customer_transactions(customer_id)

# Investigation prompt
prompt = f"""
You are a senior fraud investigation analyst.

Analyze the following customer transaction history.

Identify:
1. Suspicious patterns
2. Risk indicators
3. Possible fraud hypotheses
4. Overall risk score out of 100

Transaction data:
{transactions}

Be concise but analytical.
"""

# Call LLM
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# Print response
print("\n===== INVESTIGATION REPORT =====\n")
print(response.choices[0].message.content)