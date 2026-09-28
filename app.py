import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from openai import OpenAI

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

BANK_ID = "ProposalMind"

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"

)

# -----------------------------
# 1. Store a previous proposal
# -----------------------------

previous_proposal = """
Previous successful proposal for Acme Retail.

Client priorities:
- Strong data security
- Fast implementation
- Power BI integration

Successful approach:
- Phased implementation
- Weekly project milestones
- Clear security and data-protection explanation

Outcome:
The proposal was successful because it clearly connected the
solution to the client's security requirements and implementation timeline.
"""

print("Storing previous proposal in Hindsight...")

hindsight.retain(
    bank_id=BANK_ID,
    content=previous_proposal,
    context="Previous successful enterprise RFP proposal"
)

print("Previous proposal stored.")

# -----------------------------
# 2. New RFP
# -----------------------------

new_rfp = input(
    "\nPaste the new RFP here, then press Enter:\n\n"
)

# -----------------------------
# 3. Recall relevant memories
# -----------------------------

print("\nSearching Hindsight for relevant past experience...")

memory_result = hindsight.recall(
    bank_id=BANK_ID,
    query=(
        "What did previous enterprise clients care about "
        "when evaluating data analytics proposals, especially "
        "security, implementation, reporting and timelines?"
    )
)

memories = "\n".join(
    f"- {memory.text}"
    for memory in memory_result.results
)

print("\nRelevant memories:")
print(memories)

# -----------------------------
# 4. Generate proposal response
# -----------------------------

prompt = f"""
You are ProposalMind, an AI assistant helping a company respond
to Requests for Proposal (RFPs).

NEW RFP:
{new_rfp}

RELEVANT MEMORY FROM PREVIOUS PROPOSALS:
{memories}

Write a concise, professional RFP response.

Use the relevant previous experience when it genuinely helps.
Do not invent facts that are not present in the RFP or memory.

Structure the response with:
1. Implementation approach
2. Security
3. Reporting / Power BI
4. Timeline
"""

print("\nGenerating tailored proposal response...")

response = groq_client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\n==============================")
print("PROPOSALMIND RESPONSE")
print("==============================")
print(response.choices[0].message.content
)

print("\n==============================")
print("PROPOSALMIND RESPONSE")
print("==============================")
print(response.choices[0].message.content)