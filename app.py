import streamlit as st
import pandas as pd
import random

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="LeadGen AI", page_icon="🤖", layout="wide")

# ------------------- SIDEBAR (Lead History) -------------------
with st.sidebar:
    st.title("📁 Lead History")
    st.markdown("View your saved and recent lead batches below.")

    # Ensure saved_leads is always a dict
    if "saved_leads" not in st.session_state or not isinstance(st.session_state.saved_leads, dict):
        st.session_state.saved_leads = {}

    if st.session_state.saved_leads:
        for batch, df in st.session_state.saved_leads.items():
            with st.expander(f"📄 {batch}"):
                st.dataframe(df, use_container_width=True)
    else:
        st.info("No saved leads yet.")

# ------------------- STYLES -------------------
st.markdown("""
    <style>
        /* Overall clean look */
        .main {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 12px;
        }

        /* ChatGPT-like input area */
        .chat-input {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 25px;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .chat-input textarea {
            width: 100%;
            border: none;
            outline: none;
            resize: none;
            font-size: 1rem;
            background: transparent;
        }
        .chat-input textarea:focus {
            outline: none !important;
        }

        /* Chat bubbles */
        .user-bubble, .ai-bubble {
            padding: 15px 20px;
            border-radius: 18px;
            margin: 10px 0;
            max-width: 90%;
            line-height: 1.5;
        }
        .user-bubble {
            background-color: #DCF8C6;
            align-self: flex-end;
        }
        .ai-bubble {
            background-color: #ffffff;
            border: 1px solid #e5e5e5;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .bubble-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- MAIN CONTENT -------------------
st.title("🤖 LeadGen AI")
st.subheader("Smart lead generation + scoring assistant")

# Prompt input styled like ChatGPT
st.markdown("### 🧠 Describe your lead requirements")

# Use HTML for a ChatGPT-style input area
with st.container():
    prompt_placeholder = st.empty()
    user_prompt = prompt_placeholder.text_area(
        "Prompt (optional):",
        placeholder="Type your request here (e.g. Find SaaS leads in India targeting CEOs and Marketing Heads)...",
        label_visibility="collapsed",
        height=100
    )

# Lead configuration options
col1, col2 = st.columns([2, 1])
with col1:
    industry = st.text_input("🎯 Target Industry", placeholder="E-commerce, SaaS, Fintech, etc.")
with col2:
    lead_count = st.slider("📊 Number of Leads", 5, 50, 10)
scoring_criteria = st.multiselect(
    "⭐ Scoring Criteria",
    ["Relevance", "Revenue", "Engagement", "Seniority"],
    default=["Relevance"]
)

generate = st.button("🚀 Generate Leads", use_container_width=True)

# ------------------- LEAD GENERATION -------------------
if generate:
    st.markdown('<div class="bubble-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{user_prompt or "Find leads for me."}</div>', unsafe_allow_html=True)

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

    st.markdown(
        f"""
        <div class="ai-bubble">
            ✅ Generated {lead_count} leads in the {industry or "E-commerce"} industry.<br><br>
            Scroll down to view your AI-generated lead table ⬇️
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(df, use_container_width=True, height=300)

    save = st.button("💾 Save This Lead List", use_container_width=True)
    if save:
        batch_name = f"Lead Batch {len(st.session_state.saved_leads) + 1}"
        st.session_state.saved_leads[batch_name] = df
        st.success(f"✅ Saved as {batch_name}!")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("---")
st.caption("🚀 LeadGen AI Prototype — Built with Streamlit")

