import streamlit as st
import asyncio
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator import CoordinatorAgent
from utils.state_manager import StateManager

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide"
)

if 'state_manager' not in st.session_state:
    st.session_state.state_manager = StateManager()
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'report' not in st.session_state:
    st.session_state.report = None

st.title("Multi-Agent Research & Report Generator")
st.markdown("*AI-powered research with multiple specialized agents*")

with st.sidebar:
    st.header("Configuration")
    
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get free API key at console.groq.com"
    )
    
    if not api_key:
        st.warning("Please enter your Groq API key")
    
    st.markdown("---")
    
    max_search_results = st.slider("Max Search Results", 3, 10, 5)
    temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.7, 0.1)
    
    if st.button("Clear History"):
        st.session_state.logs = []
        st.session_state.report = None
        st.rerun()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Research Topic")
    
    topic = st.text_area(
        "Enter your research topic",
        placeholder="e.g., Benefits of renewable energy",
        height=100
    )
    
    research_depth = st.selectbox(
        "Research Depth",
        ["quick", "standard", "deep"],
        index=1
    )
    
    if st.button("Generate Report", type="primary", disabled=not topic or not api_key):
        st.session_state.logs = []
        st.session_state.report = None
        
        with st.spinner("Working on your research..."):
            try:
                coordinator = CoordinatorAgent(
                    api_key=api_key,
                    max_search_results=max_search_results,
                    temperature=temperature
                )
                
                result = asyncio.run(
                    coordinator.execute_research_pipeline(
                        topic=topic,
                        depth=research_depth
                    )
                )
                
                st.session_state.report = result['report']
                st.session_state.logs = result['logs']
                
                st.success("Report generated successfully!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col2:
    st.subheader("Agent Activity")
    
    if st.session_state.logs:
        for log in st.session_state.logs[-10:]:
            agent = log.get('agent', 'System')
            message = log.get('message', '')
            log_type = log.get('type', 'info')
            
            if log_type == 'error':
                st.error(f"**{agent}**: {message}")
            elif log_type == 'success':
                st.success(f"**{agent}**: {message}")
            else:
                st.info(f"**{agent}**: {message}")
    else:
        st.info("No activity yet. Enter a topic and generate a report!")

if st.session_state.report:
    st.markdown("---")
    st.subheader("Generated Report")
    
    st.download_button(
        label="Download Report",
        data=st.session_state.report,
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )
    
    st.markdown(st.session_state.report)

st.markdown("---")
st.markdown("*Built with Streamlit and Groq AI*")