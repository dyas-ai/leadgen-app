import streamlit as st
import pandas as pd
import random

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="LeadGen AI", page_icon="🤖", layout="wide")

# ------------------- SIDEBAR (Lead History) -------------------
with st.sidebar:
    st.title("📁 Lead History")
    st.markdown("View your saved and recent lead batches below.")

    # Fix: Always ensure it's a dictionary
    if "saved_leads" not in st.session_state or not isinstance(st.session_state.saved_leads, dict):
        st.session_state.saved_leads = {}

    if st.session_state.saved_leads:
        for batch, df in st.session_state.saved_leads.items():
            with st.expander(f"📄 {batch}"):
                st.dataframe(df, use_container_width=True)
    else:
        st.info("No saved leads yet.")


# ------------------- MAIN CONTAINER -------------------
st.markdown(
    """
    <style>
    .stTextInput textarea, .stTextInput input {
        border-radius: 10px;
        padding: 10px;
    }
    .lead-bubble {
        background-color: #f7f7f8;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .lead-table {
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 LeadGen AI")
st.subheader("Smart lead generation + scoring assistant")

# ------------------- Wizard + Optional Prompt -------------------
st.markdown("### 🧠 Describe your lead requirements or use the quick form")

col1, col2 = st.columns([2, 1])

with col1:
    user_prompt = st.text_area(
        "Prompt (optional):",
        placeholder="e.g., Find SaaS leads in India, target CEOs and Marketing Heads...",
        height=100
    )

with col2:
    industry = st.text_input("Target Industry", placeholder="E-commerce, SaaS, Fintech, etc.")
    lead_count = st.slider("Number of Leads", 5, 50, 10)
    scoring_criteria = st.multiselect(
        "Scoring Criteria",
        ["Relevance", "Revenue", "Engagement", "Seniority"],
        default=["Relevance"]
    )

generate = st.button("🚀 Generate Leads")

# ------------------- Lead Generation Logic -------------------
if generate:
    st.markdown('<div class="lead-bubble">', unsafe_allow_html=True)
    st.success("✅ Leads Generated Successfully!")

    industries = [industry or "E-commerce"]
    first_names = ["Karan", "Ananya", "Priya", "Suresh", "Ishita", "Neha", "Aarav", "Rohit"]
    last_names = ["Singh", "Bansal", "Rao", "Mehta", "Sharma", "Nair", "Patel", "Kumar"]
    companies = ["Techify", "GrowthHub", "CloudIQ", "Designo", "AI Labs", "BrandNest", "PixelWorks"]
    roles = ["Marketing Manager", "CEO", "CTO", "Designer", "Growth Head", "Sales Lead", "Analyst"]

    leads = []
    for _ in range(lead_count):
        lead = {
            "Name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "Company": random.choice(companies),
            "Role": random.choice(roles),
            "Industry": random.choice(industries),
            "Email": f"{random.choice(first_names).lower()}@{random.choice(companies).lower()}.com",
            "Score": random.randint(50, 100)
        }
        leads.append(lead)

    df = pd.DataFrame(leads)
    st.markdown("#### 📋 Generated Leads")
    st.dataframe(df, use_container_width=True, height=300)

    save = st.button("💾 Save This Lead List")
    if save:
        batch_name = f"Lead Batch {len(st.session_state.saved_leads) + 1}"
        st.session_state.saved_leads[batch_name] = df
        st.success(f"✅ Saved as {batch_name}!")

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------- Footer -------------------
st.markdown("---")
st.caption("🚀 LeadGen AI Prototype — Built with Streamlit")


