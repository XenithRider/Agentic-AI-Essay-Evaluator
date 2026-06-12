import streamlit as st
import requests

st.set_page_config(page_title="AI Essay Evaluator", page_icon="📝", layout="wide")

# UI Header
st.title("📝 AI-Driven Parallel Essay Evaluator")
st.markdown("Submit your essay to receive a comprehensive, multi-dimensional analysis powered by a parallel LangGraph workflow and Gemini 2.5 Flash.")

# Input Area
essay_input = st.text_area("Paste your essay here:", height=300, placeholder="Role of AI in the New World...")

# Submission
if st.button("Evaluate Essay", type="primary"):
    if not essay_input.strip():
        st.warning("Please enter an essay to evaluate.")
    else:
        with st.spinner("Analyzing essay across multiple dimensions (Language, Analysis, Clarity) in parallel..."):
            try:
                # Call the FastAPI backend
                response = requests.post("http://localhost:8000/evaluate", json={"essay": essay_input})
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Evaluation Complete!")

                    # Top Level Metrics
                    st.subheader("🎯 Overall Assessment")
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric(label="Average Score", value=f"{data['avg_score']:.1f} / 10")
                    with col2:
                        st.info(data['overall_feedback'])

                    st.divider()

                    # Detailed Breakdown in Tabs
                    st.subheader("📊 Detailed Breakdown")
                    tab1, tab2, tab3 = st.tabs(["🗣️ Language Quality", "🔍 Depth of Analysis", "💡 Clarity of Thought"])

                    with tab1:
                        st.write(data['language_feedback'])

                    with tab2:
                        st.write(data['analysis_feedback'])

                    with tab3:
                        st.write(data['clarity_feedback'])

                else:
                    st.error(f"Backend Error: {response.json().get('detail', 'Unknown Error')}")

            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is FastAPI running on port 8000?")