import streamlit as st
import pandas as pd
import io
from Resume_Shortlisting.resume_screener import ResumeScreener
from Employee_Sentiment.sentiment_analyzer import EmployeeSentimentAnalyzer

# Initialize the components
screener = ResumeScreener()
analyzer = EmployeeSentimentAnalyzer()

def main():
    st.set_page_config(page_title="HR Tech Suite", layout="wide")
    
    st.title("HR Technology Suite")
    st.subheader("Streamline your HR processes with AI")
    
    tab1, tab2 = st.tabs(["Resume Screening Dashboard", "Employee Sentiment Analytics"])
    
    # Resume Screening Dashboard
    with tab1:
        st.header("Resume Screening Dashboard")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Job Requisition Section
            st.subheader("Job Requisition")
            job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
            department = st.selectbox("Department", ["Engineering", "Product", "Marketing", "Sales", "HR", "Finance"])
            job_description = st.text_area(
                "Job Description",
                height=200,
                placeholder="Paste the complete job description here..."
            )
        
        with col2:
            # Quick Stats
            st.subheader("Screening Stats")
            st.metric("Resumes in Queue", "0")
            st.metric("Screened Today", "0")
            st.metric("Shortlisted", "0")
        
        # Batch Resume Upload
        st.subheader("Batch Resume Processing")
        uploaded_files = st.file_uploader(
            "Upload multiple resumes (PDF, DOCX)", 
            accept_multiple_files=True,
            type=['pdf', 'docx']
        )
        
        # Or paste resume text
        st.subheader("Quick Resume Screen")
        resume_text = st.text_area(
            "Paste resume text for quick screening",
            height=150,
            placeholder="Paste a single resume text here for quick analysis..."
        )
        
        if st.button("Screen Resumes"):
            if job_description and (uploaded_files or resume_text):
                with st.spinner("Analyzing resumes..."):
                    # Create a table to show results
                    st.subheader("Screening Results")
                    
                    if resume_text:
                        results = screener.score_resume(resume_text, job_description)
                        results_df = pd.DataFrame({
                            'Score': [f"{results['total_score']:.1f}%"],
                            'Skill Match': [f"{results['skill_match']:.1f}%"],
                            'Experience': [f"{results['experience_years']} years"],
                            'Missing Skills': [', '.join(results['missing_skills'])]
                        })
                        st.dataframe(results_df)
                        
                        # Detailed Analysis
                        with st.expander("View Detailed Analysis"):
                            st.write("✅ Matched Skills:", ', '.join(results['matched_skills']))
                            st.write("❌ Missing Skills:", ', '.join(results['missing_skills']))
                            
                        # Quick Actions
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button("Schedule Interview")
                        with col2:
                            st.button("Send Assessment")
                        with col3:
                            st.button("Reject Candidate")
    
    # Employee Sentiment Analytics
    with tab2:
        st.header("Employee Sentiment Analytics Dashboard")
        
        # Upload Feedback Data
        st.subheader("Upload Feedback Data")
        feedback_type = st.selectbox(
            "Select Feedback Type",
            ["Employee Surveys", "Exit Interviews", "Performance Reviews", "1:1 Meeting Notes"]
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            feedback_text = st.text_area(
                "Enter employee feedback for analysis",
                height=150,
                placeholder="Paste employee feedback here..."
            )
            
            department = st.selectbox(
                "Department",
                ["All Departments", "Engineering", "Product", "Marketing", "Sales", "HR", "Finance"]
            )
        
        with col2:
            st.subheader("Department Overview")
            st.metric("Overall Sentiment", "Neutral")
            st.metric("Attrition Risk", "Medium")
            st.metric("Response Rate", "78%")
        
        if st.button("Analyze Feedback"):
            if feedback_text:
                with st.spinner("Analyzing feedback..."):
                    analysis = analyzer.analyze_feedback(feedback_text)
                    
                    # Display Results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Sentiment Analysis")
                        sentiment_score = analysis['sentiment']['score']
                        st.progress(sentiment_score)
                        st.write(f"Sentiment Score: {sentiment_score*100:.1f}%")
                        
                        st.subheader("Key Themes")
                        for theme, present in analysis['themes'].items():
                            if present:
                                st.write(f"🎯 {theme.replace('_', ' ').title()}")
                    
                    with col2:
                        st.subheader("Risk Assessment")
                        risk_score = analysis['risk_score']
                        st.progress(risk_score)
                        st.write(f"Attrition Risk: {risk_score*100:.1f}%")
                        
                        st.subheader("Recommended Actions")
                        if risk_score > 0.7:
                            st.error("High Risk - Immediate Action Required")
                        elif risk_score > 0.4:
                            st.warning("Medium Risk - Monitor Closely")
                        else:
                            st.success("Low Risk - Maintain Engagement")
        
        # HR Analytics Dashboard
        st.subheader("HR Analytics Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Employee Satisfaction", "76%", "2%")
        with col2:
            st.metric("Response Rate", "82%", "5%")
        with col3:
            st.metric("Engagement Score", "7.8", "0.3")

if __name__ == "__main__":
    main()