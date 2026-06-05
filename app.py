import streamlit as st
import os
import sys

# Ensure project root is in path for imports
sys.path.insert(0, os.path.dirname(__file__))
from engine import RAGEngine

# --- Page Configuration ---
st.set_page_config(
    page_title="HDFC Mutual Fund FAQ Assistant",
    page_icon="📈",
    layout="wide"
)

# --- Custom Styling (Groww-like) ---
st.markdown("""
    <style>
    /* Main container styling */
    .main { background-color: #ffffff; color: #44475b; }
    
    /* Chat message bubble refinements */
    .stChatMessage { border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; border: 1px solid #eef2f6; }
    
    /* Groww-style Primary Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        border: 1px solid #00d09c; 
        color: #00d09c; 
        font-weight: 500;
        background-color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #00d09c !important; color: white !important; border-color: #00d09c !important; }
    
    /* Compliance & Disclaimer styling */
    .disclaimer { font-size: 0.85rem; color: #44475b; padding: 12px; border-radius: 8px; background-color: #fceceb; border: 1px solid #f8d7da; margin-top: 20px; }
    .source-chip { background-color: #e8f0fe; color: #1967d2; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

# --- Utility Functions ---
def safe_rerun():
    """Ensures compatibility with different Streamlit versions for rerunning the app."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- Initialize Engine & Session State ---
@st.cache_resource
def get_rag_engine():
    return RAGEngine()

engine = get_rag_engine()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_fund" not in st.session_state:
    st.session_state.selected_fund = None

# --- Sidebar ---
with st.sidebar:
    st.image("https://groww.in/groww-logo-270.png", width=120) # Placeholder logo
    st.title("HDFC FAQ Assistant")
    st.markdown("### Context Settings")
    
    # Fund Selection
    available_funds = engine.get_available_funds()
    selected_fund = st.selectbox(
        "Selected Scheme Scope",
        ["All Funds"] + available_funds,
        index=0, help="Narrow down search results to a specific HDFC mutual fund scheme."
    )
    st.session_state.selected_fund = None if selected_fund == "All Funds" else selected_fund
    
    st.markdown("---")
    st.markdown("### Example Queries")
    examples = [
        "What is the expense ratio?",
        "Who is the fund manager?",
        "What is the exit load?",
        "Should I invest in this fund?"
    ]
    for ex in examples:
        if st.button(ex):
            st.session_state.messages.append({"role": "user", "content": ex})
            safe_rerun()

    st.markdown("---")
    debug_mode = st.checkbox("Debug Mode", help="Show raw context and retrieval scores.")

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        safe_rerun()

    st.markdown('<div class="disclaimer"><b>Disclaimer:</b> Facts-only. No investment advice. This tool provides verified information from official sources.</div>', unsafe_allow_html=True)

# --- Main Chat UI ---
st.title("Mutual Fund FAQ Assistant")
st.markdown("##### Ask factual questions about HDFC Mutual Fund schemes")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a question about HDFC Mutual Funds..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving verified facts..."):
            try:
                # If you want to see debug info, you'd need to modify engine.query 
                # to return scores, but for now we just show the standard response.
                response = engine.query(prompt, filter_fund=st.session_state.selected_fund)
                if debug_mode:
                    st.caption("🔍 Retrieval active with BGE-Large and Metadata Filtering.")
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"I encountered an error while processing your request: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    # We don't need a safe_rerun() here because st.chat_input handles state updates naturally 
    # and we want to see the immediate response.

# --- Footer Information ---
st.markdown("---")
if st.session_state.selected_fund:
    st.info(f"Currently filtering results for: **{st.session_state.selected_fund}**")
else:
    st.caption("Currently searching across all available HDFC Fund documents.")

st.markdown("""
    <center><small>
    Data sourced from HDFC AMC, AMFI, and SEBI. Powered by Groq (Llama-3) & BGE-Large Embeddings.
    </small></center>
    """, unsafe_allow_html=True)