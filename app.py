import streamlit as st
import pandas as pd
import random

# -------------- CONFIG --------------
st.set_page_config(page_title="LeadGen AI", page_icon="⚡", layout="wide")

# -------------- SIDEBAR --------------
with st.sidebar:
    st.title("📁 Lead History")
    st.markdown("View your saved and recent lead batches below.")
    
    if "saved_leads" not in st.session_state:
        st.session_state.saved_leads = {}

    if st.session_state.saved_leads:
        for batch, df in st.session_state.saved_leads.items():
            with st.expander(f"📄 {batch}"):
                st.dataframe(df)
    else:
        st.info("No saved leads yet.")

# -------------- MAIN UI --------------
st.markdown("<h2 style='text-align:center;'>⚡ LeadGen AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart lead generation & scoring assistant</p>", unsafe_allow_html=True)
st.divider()

# Wizard-like Input
st.markdown("### 💬 Ask LeadGen AI")
user_prompt = st.text_area("Describe the type of leads you want:", 
                           placeholder="e.g. I want SaaS startup leads in India targeting growth managers...")

col1, col2 = st.columns([1, 4])
with col1:
    num_leads = st.slider("Number of leads", 5, 50, 10)
with col2:
    criteria = st.multiselect("Scoring criteria", ["Relevance", "Engagement", "Conversion Potential"], ["Relevance"])

generate_btn = st.button("⚡ Generate Leads")

# Optional Quick Prompts
st.markdown("#### 🧠 Try these prompts:")
sample_prompts = [
    "I want ecommerce founders in India",
    "Generate B2B SaaS leads in US",
    "Find marketing heads in D2C companies"
]
cols = st.columns(len(sample_prompts))
for i, p in enumerate(sample_prompts):
    if cols[i].button(p):
        user_prompt = p
        st.session_state["last_prompt"] = p
        generate_btn = True

# -------------- LEAD GENERATION --------------
def generate_fake_leads(n, industry="General"):
    names = ["Aarav", "Isha", "Karan", "Neha", "Priya", "Suresh", "Ananya", "Rohit"]
    companies = ["Techify", "GrowthHub", "BrandNest", "CloudIQ", "Designo"]
    roles = ["CEO", "Marketing Head", "Growth Lead", "Analyst", "Designer", "Sales Lead"]
    
    leads = []
    for _ in range(n):
        lead = {
            "Name": random.choice(names) + " " + random.choice(["Singh", "Rao", "Bansal"]),
            "Company": random.choice(companies),
            "Role": random.choice(roles),
            "Industry": industry,
            "Email": f"{random.choice(names).lower()}@{random.choice(companies).lower()}.com",
            "Score": random.randint(50, 100)
        }
        leads.append(lead)
    return pd.DataFrame(leads)

# Generate and Display Leads
if generate_btn and user_prompt:
    st.success("✅ Leads Generated Successfully!")
    df = generate_fake_leads(num_leads, user_prompt)
    
    st.markdown("### 🧾 Generated Leads")
    st.dataframe(df, use_container_width=True)
    
    if st.button("💾 Save This Lead List"):
        batch_name = f"Batch {len(st.session_state.saved_leads) + 1}"
        st.session_state.saved_leads[batch_name] = df
        st.toast(f"Saved as {batch_name}")

elif not user_prompt and generate_btn:
    st.warning("⚠️ Please enter a prompt to generate leads.")
