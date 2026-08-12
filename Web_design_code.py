import streamlit as st
from API_code import fetch_jobs
from LLM_file import generate_insights_and_roadmap
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #1E88E5;
        color: white;
        border: none;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1565C0;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

SUGGESTED_ROLES = [
    "Data Analyst",
    "Backend Engineer",
    "Data Engineer",
    "AI/ML Engineer",
    "Frontend Developer",
    "DevOps Engineer",
    "Full Stack Developer",
    "Cloud Architect"
]
SUGGESTED_TOOLS = [
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "Python",
    "Microsoft Excel",
    "Docker",
    "Pandas",
    "Power BI"
]


st.set_page_config(page_title="Career Intelligence Dashboard")
st.markdown("<h1 style='text-align: center;'>🎯Career Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Your assistant to find your best match and master the right skills for your dream role</p>", unsafe_allow_html=True)


# --- USER INPUT FORM ---
with st.form("search_form"):
    col1, col2 = st.columns(2)
    with col1:
        raw_role = st.selectbox(
            label="Target Job/Role Field",
            options=SUGGESTED_ROLES,
            index=None,
            placeholder="e.g.Developer",
            accept_new_options=True
        )
    with col2:
        raw_tool=st.selectbox(
            label="Target Tool",
            options=SUGGESTED_TOOLS,
            placeholder="e.g.Power BI ",
            index=None,
            accept_new_options=True
        )
    
    analyze_button = st.form_submit_button("Analyze Market Demand", type="primary")

# --- PROCESS ON BUTTON CLICK ---
if analyze_button:
    # Clean whitespace directly
    user_role = raw_role.strip()
    user_tool = raw_tool.strip()

    # Strict check
    if len(user_role) == 0 or len(user_tool) == 0:
        st.error("⚠️ Please fill in BOTH input boxes (Job Role AND Tool Name).")
    else:
        st.success(f"Processing query for Role: '{user_role}' | Tool: '{user_tool}'")
        st.markdown("---")
        
        try:
            with st.spinner("Fetching postings & saving to database..."):
                job_descriptions = fetch_jobs(user_role)

            if job_descriptions:
                with st.spinner("Generating AI Analysis..."):
                    analysis, roadmap = generate_insights_and_roadmap(user_role, user_tool, job_descriptions)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("🤖 AI Market Analysis")
                    st.markdown(analysis)
                with col_b:
                    st.subheader("🗺️ Recommended Learning Roadmap")
                    st.markdown(roadmap)
            else:
                st.warning("No job descriptions found for this role.")

        except Exception as e:
            st.error(f"❌ Execution Error: {str(e)}")







            