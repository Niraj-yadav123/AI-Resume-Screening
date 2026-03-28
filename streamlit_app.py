import streamlit as st
import os
import pandas as pd
from resume_parser import extract_text, extract_name, extract_phone

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Screening Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------- DATABASE ----------------
DB_FILE = "candidates.csv"

if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=[
        "Name",
        "Phone",
        "Role",
        "Score",
        "Eligibility",
        "Interview Decision"
    ])
    df.to_csv(DB_FILE, index=False)

# ---------------- ROLE BASED SKILLS ----------------
ROLE_SKILLS = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "statistics"],
    "Python Developer": ["python", "django", "flask", "api", "git"],
    "Web Developer": ["html", "css", "javascript", "react", "bootstrap"],
    "HR Executive": ["communication", "recruitment", "management", "teamwork"],
    "AI/ML Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pandas"]
}


st.markdown("""
<style>
.main {background:linear-gradient(135deg,#020617,#0f172a);}
h1,h2,h3{color:#38bdf8;}

.stButton>button{
background:linear-gradient(90deg,#38bdf8,#6366f1);
color:white;
border-radius:10px;
height:3em;
width:100%;
font-size:18px;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.title("🚀 AI Resume Screener")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📤 Upload & Analyze", "📞 HR Interview Panel"]
)


if page == "🏠 Home":

    st.title("🚀 AI Resume Screening Platform")
    st.subheader("AI Powered Smart Hiring System")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="padding:2px;background:#0f172a;border-radius:12px;text-align:center">
            <h4>⚡ AI Screening</h4>
            <h2>Automated</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding:10px;background:#0f172a;border-radius:12px;text-align:center">
            <h4>🎯 Skill Matching</h4>
            <h2>Smart Detection</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding:20px;background:#0f172a;border-radius:12px;text-align:center">
            <h4>📈 Hiring Speed</h4>
            <h2>Fast</h2>
        </div>
        """, unsafe_allow_html=True)

    st.success("Upload resumes → AI analyzes → HR decides interview automatically.")


elif page == "📤 Upload & Analyze":

    st.header("📤 Upload Resumes")

    
    if st.button(" Clear Old Data"):
        pd.DataFrame(columns=[
            "Name",
            "Phone",
            "Role",
            "Score",
            "Eligibility",
            "Interview Decision"
        ]).to_csv(DB_FILE, index=False)
        st.success("Old data cleared!")
        st.rerun()

    
    role = st.selectbox("Select Job Role", list(ROLE_SKILLS.keys()))
    skills = ROLE_SKILLS[role]

    st.info(f"✅ Auto Selected Skills: {', '.join(skills)}")

    uploaded_files = st.file_uploader(
        "Upload resumes",
        accept_multiple_files=True
    )

    if st.button("🔍 Analyze Candidates"):

        if not uploaded_files:
            st.warning("Upload resumes first!")
            st.stop()

        data = pd.read_csv(DB_FILE)

        for file in uploaded_files:

            temp_path = f"temp_{file.name}"

            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())

            try:
                text = extract_text(temp_path)
                name = extract_name(text)
                phone = extract_phone(text)

                text_lower = text.lower()

                matched_skills = [s for s in skills if s in text_lower]
                score = int((len(matched_skills) / len(skills)) * 100)

                eligibility = "Eligible" if score >= 50 else "Rejected"
                decision = "Pending Interview" if score >= 50 else "Rejected"

                st.write(f"✅ {name} matched skills: {', '.join(matched_skills)}")

                if not ((data["Name"] == name) & (data["Phone"] == phone)).any():

                    new_row = {
                        "Name": name,
                        "Phone": phone,
                        "Role": role,
                        "Score": score,
                        "Eligibility": eligibility,
                        "Interview Decision": decision
                    }

                    data.loc[len(data)] = new_row

            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        data.to_csv(DB_FILE, index=False)

        st.success("✅ Analysis Completed!")

        updated_df = pd.read_csv(DB_FILE)
        st.dataframe(updated_df, use_container_width=True)


elif page == "📞 HR Interview Panel":

    st.header("📞 HR Interview Management")

    df = pd.read_csv(DB_FILE)

    if df.empty:
        st.info("No candidates analyzed yet.")

    else:
        st.dataframe(df, use_container_width=True)

        st.subheader("✅ Update Interview Decision")

        candidate = st.selectbox(
            "Select Candidate",
            df["Name"].astype(str).unique()
        )

        decision = st.selectbox(
            "Decision",
            ["Accepted for Interview", "Rejected"]
        )

        if st.button("Update Decision"):

            df.loc[df["Name"] == candidate,
                   "Interview Decision"] = decision

            df.to_csv(DB_FILE, index=False)

            st.success("✅ Decision Updated Successfully!")

            st.rerun()

        st.divider()

        st.subheader("📞 Contact Candidate")

        selected = df[df["Name"] == candidate]

        if not selected.empty:

            phone = selected.iloc[0]["Phone"]

            st.markdown(f"### 📱 Phone Number: {phone}")

            if phone != "Not Found":
                clean_phone = str(phone).replace("+", "").replace(" ", "")

                st.markdown(
                    f"[💬 WhatsApp Candidate](https://wa.me/{clean_phone})"
                )