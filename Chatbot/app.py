# import streamlit as st
# import requests

# # Set page config
# st.set_page_config(
#     page_title="FATIMA.ai | UTD Assistant",
#     page_icon="🤖",
#     layout="wide"
# )

# # Header
# st.title("FATIMA.ai")
# st.subheader("Flexible Academic Text Intelligence and Management Assistant")
# st.write("Your intelligent guide to UTD's academic information")

# # Initialize chat history
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # Display chat history
# for chat in st.session_state.chat_history:
#     st.markdown(f"**You:** {chat['question']}")
#     st.markdown(f"**FATIMA:** {chat['answer']}")
    
#     # Display contact information in a structured way
#     if chat['contact_info']:
#         st.markdown("**Contact Information:**")
#         for contact in chat['contact_info']:
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.markdown(f"📧 {contact['email']}")
#             with col2:
#                 st.markdown(f"📞 {contact['phone']}")
#             with col3:
#                 st.markdown(f" {contact['location']}")
    
#     if chat['sources']:
#         st.markdown("**Sources:** " + ", ".join(chat['sources']))

# # Input area
# user_input = st.text_input("Ask FATIMA about UTD...", key="user_input")
# send_button = st.button("Ask FATIMA")

# # Handle input
# if send_button and user_input:
#     with st.spinner('FATIMA is thinking...'):
#         try:
#             response = requests.post(
#                 "http://localhost:8000/chatbot",
#                 json={"query": user_input},
#                 timeout=10
#             )
            
#             if response.status_code == 200:
#                 result = response.json()
                
#                 # Add to chat history
#                 st.session_state.chat_history.append({
#                     "question": user_input,
#                     "answer": result.get("answer", ""),
#                     "sources": result.get("sources", []),
#                     "contact_info": result.get("contact_info", [])
#                 })
                
#                 # Clear input
#                 st.rerun()
#             else:
#                 st.error(f"Error: Server returned status code {response.status_code}")
                
#         except requests.exceptions.RequestException as e:
#             st.error(f"Error connecting to the server: {str(e)}")
#             st.info("Make sure the chatbot server is running (python chatbot_server.py)")

# # Footer
# st.markdown("---")
# st.write("FATIMA.ai - Powered by advanced language models and UTD's knowledge base")
# st.write("© 2024 UTD Information Systems")
import streamlit as st
import requests
import base64
import time
import hashlib
import random

# Configuration constants
API_ENDPOINT = "http://localhost:8000/chatbot"
API_TIMEOUT = 15
BACKGROUND_IMAGE = "UTD.png"
MAX_MESSAGE_LENGTH = 50

# Widget dimensions
MINIMIZED_WIDTH = '80px'
MINIMIZED_HEIGHT = '40px'
EXPANDED_WIDTH = '180px'
EXPANDED_HEIGHT = '250px'

def get_cache_buster():
    """Generate cache buster for CSS updates"""
    return hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:12]

def get_base64_image(image_file):
    """Convert image to base64 string"""
    try:
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

def get_background_style(image_file=None):
    """Get background style CSS"""
    if image_file and get_base64_image(image_file):
        return f"""
            background-image: url("data:image/png;base64,{get_base64_image(image_file)}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        """
    else:
        return """
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        """

def apply_widget_styling():
    """Apply CSS styling for the floating widget"""
    is_minimized = st.session_state.get('is_minimized', False)
    cache_buster = get_cache_buster()
    
    container_width = MINIMIZED_WIDTH if is_minimized else EXPANDED_WIDTH
    container_height = MINIMIZED_HEIGHT if is_minimized else EXPANDED_HEIGHT
    container_padding = '4px' if is_minimized else '8px'
    
    background_style = get_background_style(BACKGROUND_IMAGE)

    st.markdown(
        f"""
        <style data-cache="{cache_buster}" data-timestamp="{int(time.time())}">
        /* Hide Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        .stDecoration {{display: none;}}
        
        /* Force remove any existing styles */
        .stApp * {{
            box-sizing: border-box !important;
        }}
        
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        .main,
        section[data-testid="stSidebar"] + .main,
        html, body {{
            {background_style}
        }}

        /* Widget container positioning */
        .main .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        section.main .block-container,
        div[data-testid="stAppViewContainer"] .main .block-container,
        .main > .block-container {{
            position: fixed !important;
            bottom: 10% !important;
            right: 10% !important;
            width: {container_width} !important;
            height: {container_height} !important;
            max-width: {container_width} !important;
            max-height: {container_height} !important;
            min-width: {container_width} !important;
            min-height: {container_height} !important;
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
            padding: {container_padding} !important;
            margin: 0 !important;
            z-index: 99999 !important;
            overflow: {'hidden' if is_minimized else 'auto'} !important;
            transition: all 0.3s ease !important;
            transform: translateZ(0) !important;
        }}

        /* Text styling */
        .main .block-container *,
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4,
        .main .block-container p,
        .main .block-container div,
        .main .block-container span,
        .main .block-container .stMarkdown *,
        [data-testid="stMarkdown"] *,
        [data-testid="stMarkdownContainer"] *,
        .element-container * {{
            color: #000000 !important;
            font-family: 'Segoe UI', system-ui, sans-serif !important;
            font-size: 12px !important;
            line-height: 1.2 !important;
        }}
        
        /* Header styling */
        .main .block-container h4 {{
            font-size: 14px !important;
            margin: 2px 0 !important;
        }}
        
        /* Form elements */
        .main .block-container .stTextInput > div > div > input {{
            height: 28px !important;
            font-size: 11px !important;
            padding: 4px 8px !important;
        }}
        
        .main .block-container .stButton > button {{
            height: 28px !important;
            font-size: 11px !important;
            padding: 4px 8px !important;
        }}
        
        /* Spacing */
        .main .block-container .element-container {{
            margin: 2px 0 !important;
        }}
        
        .main .block-container hr {{
            margin: 4px 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def display_chat_message(message_type, content, is_recent=False):
    """Display a chat message with proper formatting"""
    if len(content) > MAX_MESSAGE_LENGTH:
        content = content[:MAX_MESSAGE_LENGTH-3] + "..."
    
    if message_type == "user":
        st.markdown(
            f'<div style="font-size: 10px; margin: 2px 0;"><strong>You:</strong> {content}</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="font-size: 10px; margin: 2px 0;"><strong>AI:</strong> {content}</div>', 
            unsafe_allow_html=True
        )

def make_api_request(query):
    """Make API request to the chatbot backend"""
    try:
        response = requests.post(
            API_ENDPOINT, 
            json={"query": query}, 
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Server error {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "❌ Server not running"
    except requests.exceptions.Timeout:
        return None, "⏰ Timeout"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def initialize_session_state():
    """Initialize session state variables"""
    if 'force_refresh' not in st.session_state:
        st.session_state.clear()
        st.session_state.force_refresh = True

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'is_minimized' not in st.session_state:
        st.session_state.is_minimized = False
    if 'loading' not in st.session_state:
        st.session_state.loading = False

def render_minimized_widget():
    """Render the minimized chat widget"""
    st.markdown('<div style="text-align: center; padding: 8px;">', unsafe_allow_html=True)
    if st.button("💬", key="chat_maximize", help="Open chat"):
        st.session_state.is_minimized = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_expanded_widget():
    """Render the expanded chat widget"""
    # Header with minimize button
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### 🤖 FATIMA")
    with col2:
        if st.button("−", key="minimize", help="Minimize"):
            st.session_state.is_minimized = True
            st.rerun()

    # Show most recent chat
    if st.session_state.chat_history:
        latest_chat = st.session_state.chat_history[-1]
        display_chat_message("user", latest_chat['question'])
        display_chat_message("bot", latest_chat['answer'])
        st.markdown("---")

    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("", key="user_input", placeholder="Ask...")
        submit_button = st.form_submit_button("Send", type="primary", use_container_width=True)

    # Handle form submission
    if submit_button and user_input.strip():
        with st.spinner('Thinking...'):
            result, error = make_api_request(user_input.strip())
            if result:
                st.session_state.chat_history.append({
                    "question": user_input.strip(),
                    "answer": result.get("answer", "No response"),
                    "sources": result.get("sources", []),
                    "contact_info": result.get("contact_info", [])
                })
                st.success("✅")
            else:
                st.session_state.chat_history.append({
                    "question": user_input.strip(),
                    "answer": error,
                    "sources": [],
                    "contact_info": []
                })
                st.error("❌")
        st.rerun()

def main():
    """Main application function"""
    # Page configuration is now handled by config.toml
    st.set_page_config(
        page_title="FATIMA.ai | UTD Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply styling
    apply_widget_styling()
    
    # Render widget based on state
    if st.session_state.is_minimized:
        render_minimized_widget()
    else:
        render_expanded_widget()

if __name__ == "__main__":
    main()