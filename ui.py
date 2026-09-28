import os
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from openai import OpenAI


from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
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
    base_url="https://api.groq.com/openai/v1",
)

# -----------------------------
# Page
# -----------------------------

st.set_page_config(
    page_title="ProposalMind",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 ProposalMind")
st.caption("AI-powered proposal generation with persistent memory")
if "proposal" not in st.session_state:
    st.session_state.proposal=""
st.markdown("---")

# -----------------------------
# RFP Input
# -----------------------------

rfp = st.text_area(
    "📋 Paste your RFP",
    height=220,
    placeholder="Paste the client's RFP requirements here...",
)

# -----------------------------
# Company / Client Details
# -----------------------------

st.subheader("🏢 Proposal Details")

company_name = st.text_input(
    "Company Name",
    "ProposalMind",
)

contact_name = st.text_input(
    "Contact Name",
    "DataDuo Team",
)

contact_email = st.text_input(
    "Email",
    "demo@proposalmind.example",
)

contact_phone = st.text_input(
    "Phone",
    "+91 00000 00000",
)

client_name = st.text_input(
    "Client Name",
    "Acme Corporation",
)

generate = st.button(
    "🚀 Generate Proposal",
    type="primary",
)

# -----------------------------
# Generate Proposal
# -----------------------------

if generate:

    if not rfp.strip():
        st.warning("Please paste an RFP first.")
        st.stop()

    # -----------------------------
    # Store and Recall Memories
    # -----------------------------

    with st.spinner(
        "🧠 Saving experience and recalling relevant memories..."
    ):

        hindsight.retain(
            bank_id=BANK_ID,
            content=f"New RFP received:\n{rfp}",
            context="current RFP",
        )

        memories = hindsight.recall(
            bank_id=BANK_ID,
            query=rfp,
        )

    # -----------------------------
    # Display Memories
    # -----------------------------

    st.subheader("🧠 Relevant Memories")

    memory_text = str(memories)

    with st.expander(
        "View recalled experience",
        expanded=True,
    ):
        st.write(memory_text)

    # -----------------------------
    # Proposal Prompt
    # -----------------------------

    prompt = f"""
You are ProposalMind, an AI proposal assistant.

Prepare a professional proposal for the client named {client_name}.

COMPANY DETAILS:
Company: {company_name}
Contact Name: {contact_name}
Email: {contact_email}
Phone: {contact_phone}

CLIENT:
{client_name}

NEW RFP:
{rfp}

RELEVANT PAST EXPERIENCE:
{memory_text}

Create the proposal with these sections:

1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Implementation Approach
5. Security
6. Reporting / Integrations
7. Timeline
8. Why Choose Us
9. Closing

At the end, write exactly:

Prepared by: {contact_name}
{company_name}
Email: {contact_email}
Phone: {contact_phone}

Do not use placeholders such as [Contact Name], [Email], or [Phone].
Do not invent contact information.
Do not invent specific past results that are not present in the provided experience.
"""

    # -----------------------------
    # Generate with Groq
    # -----------------------------

    with st.spinner(
        "✍️ Generating tailored proposal..."
    ):

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    proposal = response.choices[0].message.content
    st.session_state.proposal=proposal
    # -----------------------------
    # Display Proposal
    # -----------------------------
if st.session_state.proposal:

    st.subheader("📄 Generated Proposal")

    st.markdown(st.session_state.proposal)


    # -----------------------------
# Requirement Coverage
# -----------------------------

st.subheader("📊 Requirement Coverage")
# -----------------------------
# Requirement Analysis
# -----------------------------

st.subheader("🔍 Understanding of Requirements")

st.info(
    "ProposalMind identified the following key requirements "
    "from the client's RFP:"
)

if "power bi" in rfp.lower():
    st.write("📊 **Power BI Reporting**")

if "security" in rfp.lower():
    st.write("🔐 **Strong Data Security**")

if (
    "fast" in rfp.lower()
    or "rapid" in rfp.lower()
    or "quick" in rfp.lower()
):
    st.write("⚡ **Fast Implementation**")

if (
    "timeline" in rfp.lower()
    or "milestone" in rfp.lower()
    or "schedule" in rfp.lower()
):
    st.write("📅 **Clear Project Timeline**")
proposal_lower = st.session_state.proposal.lower()
rfp_lower = rfp.lower()

requirements = {
    "Power BI / Reporting": [
        "power bi",
        "reporting",
        "dashboard",
    ],
    "Data Security": [
        "security",
        "encryption",
        "access control",
        "rbac",
    ],
    "Fast Implementation": [
        "fast implementation",
        "rapid",
        "quick",
        "agile",
    ],
    "Project Timeline": [
        "timeline",
        "weeks",
        "milestone",
        "implementation",
    ],
}

coverage = {}

for requirement, keywords in requirements.items():
    found = any(
        keyword in proposal_lower
        for keyword in keywords
    )

    coverage[requirement] = found

covered = sum(
    coverage.values()
)

total = len(coverage)

score = int(
    (covered / total) * 100
)

st.metric(
    "Requirement Coverage",
    f"{score}%",
)

for requirement, found in coverage.items():

    if found:
        st.success(
            f"✅ {requirement}"
        )
    else:
        st.warning(
            f"⚠️ {requirement}"
        )
# -----------------------------
# Create Professional PDF
# -----------------------------

if st.session_state.proposal:

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=55,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ProposalTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    subtitle_style = ParagraphStyle(
        "ProposalSubtitle",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=25,
    )

    heading_style = ParagraphStyle(
        "ProposalHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=15,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ProposalBody",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=16,
        spaceAfter=7,
    )

    info_style = ParagraphStyle(
        "ProposalInfo",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "PROPOSAL",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Enterprise Proposal",
            subtitle_style,
        )
    )

    # -----------------------------
    # Proposal Information
    # -----------------------------

    story.append(
        Paragraph(
            f"<b>Prepared for:</b> {client_name}",
            info_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Prepared by:</b> {company_name}",
            info_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Contact:</b> {contact_name}",
            info_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Email:</b> {contact_email}",
            info_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Phone:</b> {contact_phone}",
            info_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d %B %Y')}",
            info_style,
        )
    )

    story.append(Spacer(1, 25))

    # -----------------------------
    # Proposal Content
    # -----------------------------

    for line in st.session_state.proposal.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 7))
            continue

        # Remove Markdown bold
        text = line.replace("**", "")

        # Convert Unicode characters that can cause
        # black squares or strange characters in PDF
        text = (
            text
            .replace("–", "-")
            .replace("—", "-")
            .replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("•", "-")
            .replace("→", "->")
            .replace("←", "<-")
            .replace("≥", ">=")
            .replace("≤", "<=")
            .replace("×", "x")
            .replace("…", "...")
        )

        # Remove any remaining unsupported characters
        text = text.encode(
            "ascii",
            "ignore",
        ).decode("ascii")

        # Escape ReportLab special characters
        text = (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        # -----------------------------
        # Numbered headings
        # -----------------------------

        if (
            text.startswith("1.")
            or text.startswith("2.")
            or text.startswith("3.")
            or text.startswith("4.")
            or text.startswith("5.")
            or text.startswith("6.")
            or text.startswith("7.")
            or text.startswith("8.")
            or text.startswith("9.")
        ):
            story.append(
                Paragraph(
                    text,
                    heading_style,
                )
            )
            continue

        # -----------------------------
        # Markdown headings
        # -----------------------------

        if text.startswith("#"):
            text = text.lstrip("#").strip()

            story.append(
                Paragraph(
                    text,
                    heading_style,
                )
            )
            continue

        # -----------------------------
        # Bullet points
        # -----------------------------

        if text.startswith("-"):
            text = text[1:].strip()

            story.append(
                Paragraph(
                    f"- {text}",
                    body_style,
                )
            )
            continue

        # -----------------------------
        # Normal paragraph
        # -----------------------------

        story.append(
            Paragraph(
                text,
                body_style,
            )
        )

    # -----------------------------
    # Footer / Page Number
    # -----------------------------

    def add_page_number(canvas, doc):
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8,
        )

        canvas.drawCentredString(
            A4[0] / 2,
            25,
            f"ProposalMind - Page {doc.page}",
        )

        canvas.restoreState()

    # -----------------------------
    # Build PDF
    # -----------------------------

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_data = pdf_buffer.getvalue()

    # -----------------------------
    # Download PDF
    # -----------------------------

    st.download_button(
        label="📥 Download Professional Proposal PDF",
        data=pdf_data,
        file_name="ProposalMind_Proposal.pdf",
        mime="application/pdf",
    )