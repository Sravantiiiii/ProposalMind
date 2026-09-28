🧠 ProposalMind

AI-powered enterprise proposal generation with persistent memory

ProposalMind is an AI-powered proposal assistant that helps teams transform client RFPs into professional, tailored proposals.

It combines Hindsight persistent memory, Groq-powered language generation, requirement analysis, and professional PDF generation into one workflow.

---

🎯 Problem

Creating high-quality proposals from RFPs can be time-consuming.

Teams often need to:

- Understand complex client requirements
- Review previous successful proposals
- Reuse relevant project experience
- Address security and implementation requirements
- Create a professional final document

ProposalMind automates this workflow while using previous experience to make new proposals more relevant.

---

💡 Solution

ProposalMind follows this workflow:

Client RFP
    ↓
Requirement Analysis
    ↓
Hindsight Memory
    ↓
Recall Relevant Past Experience
    ↓
AI Proposal Generation
    ↓
Requirement Coverage Check
    ↓
Professional PDF

---

🧠 How Hindsight Memory Is Used

Hindsight provides the persistent memory layer of ProposalMind.

1. Retain

When an RFP is received, ProposalMind stores the RFP as an experience in the Hindsight memory bank.

hindsight.retain(
    bank_id=BANK_ID,
    content=f"New RFP received:\n{rfp}",
    context="current RFP",
)

2. Recall

For a new RFP, ProposalMind searches Hindsight for relevant previous experience.

memories = hindsight.recall(
    bank_id=BANK_ID,
    query=rfp,
)

3. Apply

The recalled memories are provided to the AI model together with the new RFP.

This allows the generated proposal to consider relevant previous experience such as:

- Data security requirements
- Implementation strategies
- Project milestones
- Power BI integration
- Enterprise proposal practices

This makes the system more than a simple one-time text generator.

---

🤖 AI Proposal Generation

ProposalMind uses a Groq-hosted language model to generate the proposal.

The model receives:

- Client requirements
- Company information
- Contact information
- Relevant Hindsight memories

The generated proposal contains:

1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Implementation Approach
5. Security
6. Reporting / Integrations
7. Timeline
8. Why Choose Us
9. Closing

---

📊 Requirement Coverage

ProposalMind analyzes the generated proposal against important RFP requirements.

Currently, it checks areas such as:

- Power BI / Reporting
- Data Security
- Fast Implementation
- Project Timeline

The application displays the resulting requirement coverage visually.

---

📄 Professional PDF Generation

The generated proposal can be downloaded as a professionally formatted PDF.

The PDF includes:

- Client information
- Company information
- Contact details
- Proposal content
- Structured sections
- Page numbers
- Professional formatting

PDF generation is handled using ReportLab.

---

🛠️ Technology Stack

- Python
- Streamlit — Web interface
- Hindsight — Persistent memory
- Groq API — AI proposal generation
- OpenAI Python SDK — API client
- ReportLab — PDF generation
- python-dotenv — Environment configuration

---

⚙️ Setup

Clone the repository and enter the project directory.

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a ".env" file:

HINDSIGHT_BASE_URL=your_hindsight_url
HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key

Never commit ".env" or API keys to GitHub.

---

▶️ Run the Application

Start the Streamlit interface:

streamlit run ui.py

Then open the local Streamlit URL shown in the terminal.

---

🔐 Security

API credentials are stored in environment variables and excluded from Git using ".gitignore".

The repository should never contain:

.env
.venv/
API keys

---

🚀 Key Features

- 🧠 Persistent proposal memory
- 🔎 Relevant experience recall
- 🤖 AI-generated proposals
- 📋 RFP requirement analysis
- 📊 Requirement coverage
- 📄 Professional PDF export
- 🏢 Custom company and client details
- 🔐 Environment-based API key management

---

🏆 Hackathon Demonstration

A typical demonstration flow is:

1. Enter a client RFP.
2. Show the extracted requirements.
3. Show Hindsight's recalled memories.
4. Generate the tailored proposal.
5. Show requirement coverage.
6. Download the professional PDF.

This demonstrates how persistent memory can improve AI-assisted proposal generation.

---

👥 Project

ProposalMind
AI-powered proposal assistant with persistent memory.