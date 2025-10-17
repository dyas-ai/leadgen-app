import streamlit as st
import pandas as pd
import random
import time
import json

st.set_page_config(page_title="LeadGen AI", page_icon="🚀", layout="wide")

# ----- MOCK LEAD DATABASE -----
def generate_mock_leads(industry, count=10):
    first_names = ["Arjun", "Priya", "Neha", "Ravi", "Karan", "Ananya", "Suresh", "Ishita"]
    last_names = ["Sharma", "Verma", "Singh", "Patel", "Gupta", "Rao", "Mehta", "Bansal"]
    companies = ["Techify", "Designo", "BrandNest", "GrowthHub", "PixelWorks", "CloudIQ", "Finverse", "AI Labs"]
    roles = ["Marketing Manager", "CEO", "CTO", "Designer", "Growth Head", "Analyst", "Sales Lead"]

    leads = []
    for _ in range(count):
        lead = {
            "Name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "Company": random.choice(companies),
            "Role": random.choice(roles),
            "Industry": industry,
            "Email": f"{first_names[random.randint(0, len(first_names)-1)].lower()}@{random.choice(companies).lower()}.com",
            "Score": random.randint(50, 100)
        }
        leads.append(lead)
    return pd.DataFrame(leads)

# ----- APP HEADER -----
st.title("🚀 LeadGen AI")
st.caption("Smart lead generation + scoring assistant")

# ----- SIDEBAR INPUTS -----
st.sidebar.header("🎯 Lead Search Parameters")
industry = st.sidebar.text_input("Target Industry", placeholder="e.g. SaaS, Fitness, E-commerce")
lead_count = st.sidebar.slider("Number of Leads", 5, 50, 10)
scoring_criteria = st.sidebar.multiselect(
    "Scoring Criteria",
    ["Company Size", "Engagement", "Relevance", "Budget Potential"],
    default=["Relevance", "Budget Potential"]
)

if st.sidebar.button("Generate Leads"):
    with st.spinner("Fetching and scoring leads..."):
        time.sleep(2)
        leads_df = generate_mock_leads(industry, lead_count)
        st.session_state["leads"] = leads_df
        st.success("✅ Leads Generated Successfully!")

# ----- MAIN DISPLAY -----
if "leads" in st.session_state:
    st.subheader("📋 Generated Leads")
    st.dataframe(st.session_state["leads"], use_container_width=True)

    # Save leads section
    if st.button("💾 Save This Lead List"):
        saved = st.session_state.get("saved_leads", [])
        saved.append(st.session_state["leads"].to_dict(orient="records"))
        st.session_state["saved_leads"] = saved
        st.success("Leads saved!")

# ----- SAVED LEADS SECTION -----
st.subheader("📂 Saved Lead Data")
if "saved_leads" in st.session_state and len(st.session_state["saved_leads"]) > 0:
    for i, lead_batch in enumerate(st.session_state["saved_leads"]):
        st.markdown(f"**Lead Batch {i+1}:**")
        st.dataframe(pd.DataFrame(lead_batch), use_container_width=True)
else:
    st.info("No leads saved yet. Generate and save to view here.")
