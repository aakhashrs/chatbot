# import gradio as gr
# import requests
# import base64
# import os

# API_ENDPOINT = "http://localhost:8000/chatbot"
# chat_history = []

# # SOLUTION 1: Convert image to base64 (most reliable)
# def get_base64_image(image_path):
#     """Convert image to base64 string"""
#     try:
#         with open(image_path, "rb") as img_file:
#             img_data = base64.b64encode(img_file.read()).decode()
#             return f"data:image/png;base64,{img_data}"
#     except FileNotFoundError:
#         print(f"Image file {image_path} not found!")
#         return None

# # Check if image exists and convert to base64
# background_image = get_base64_image("UTD.png")

# # Backend interaction
# def chat_with_fatima(user_input):
#     global chat_history
#     if not user_input.strip():
#         return chat_history, ""
    
#     try:
#         response = requests.post(API_ENDPOINT, json={"query": user_input}, timeout=10)
#         if response.status_code == 200:
#             result = response.json()
#             answer = result.get("answer", "No response")
#             sources = result.get("sources", [])
            
#             if sources:
#                 answer += "\n\nSources:\n" + "\n".join(f"- {src}" for src in sources)
            
#             contact_info = result.get("contact_info", [])
#             if contact_info:
#                 answer += "\n\nContact Info:"
#                 for contact in contact_info:
#                     answer += f"\n- Email: {contact.get('email', '')}, Phone: {contact.get('phone', '')}, Location: {contact.get('location', '')}"
#         else:
#             answer = f"Server error: {response.status_code}"
#     except Exception as e:
#         answer = f"Exception: {str(e)}"
    
#     chat_history.append(("You", user_input))
#     chat_history.append(("FATIMA", answer))
#     return chat_history, ""

# # Show/Hide toggle
# def toggle_visibility(current):
#     return gr.update(visible=not current), not current

# # Create CSS with background image
# def create_css_with_background():
#     base_css = """
#     /* Float button styling */
#     #float-btn {
#         position: fixed;
#         bottom: 20px;
#         right: 20px;
#         z-index: 1000;
#         width: 48px;
#         height: 48px;
#         border-radius: 24px;
#         font-size: 24px;
#         line-height: 0;
#         text-align: center;
#         background-color: #4a4a4a;
#         color: white;
#         box-shadow: 0 0 6px rgba(0,0,0,0.3);
#         border: none;
#         cursor: pointer;
#     }

#     #float-btn:hover {
#         background-color: #5a5a5a;
#     }

#     /* Chatbox styling */
#     #chatbox {
#         position: fixed;
#         bottom: 80px;
#         right: 20px;
#         width: 320px;
#         height: 420px;
#         z-index: 999;
#         border-radius: 12px;
#         box-shadow: 0 8px 20px rgba(0,0,0,0.4);
#         background: #1c1c1c;
#         padding: 0;
#         font-size: 12px;
#         overflow: hidden;
#     }

#     #chatbox-header {
#         height: 48px;
#         padding: 12px;
#         background-color: #1f1f1f;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         color: white;
#         font-size: 14px;
#         font-weight: bold;
#         border-top-left-radius: 12px;
#         border-top-right-radius: 12px;
#     }

#     /* Chat components styling */
#     .chatbot {
#         background-color: rgba(255, 255, 255, 0.95) !important;
#         border-radius: 8px;
#         margin: 10px;
#         max-height: 280px;
#         overflow-y: auto;
#     }

#     .textbox {
#         background-color: rgba(255, 255, 255, 0.95) !important;
#         margin: 10px;
#         border-radius: 4px;
#     }

#     .button {
#         margin: 5px;
#     }
#     """
    
#     # Add background image if available
#     if background_image:
#         background_css = f"""
#         /* Background image using base64 */
#         .gradio-container {{
#             background-image: url('{background_image}') !important;
#             background-size: cover !important;
#             background-position: center !important;
#             background-repeat: no-repeat !important;
#             background-attachment: fixed !important;
#             min-height: 100vh !important;
#         }}

#         body {{
#             background-image: url('{background_image}') !important;
#             background-size: cover !important;
#             background-position: center !important;
#             background-repeat: no-repeat !important;
#             background-attachment: fixed !important;
#         }}

#         .contain {{
#             background-image: url('{background_image}') !important;
#             background-size: cover !important;
#             background-position: center !important;
#             background-repeat: no-repeat !important;
#         }}
#         """
#     else:
#         # Fallback gradient background
#         background_css = """
#         /* Fallback gradient background */
#         .gradio-container {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
#             min-height: 100vh !important;
#         }

#         body {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
#         }

#         .contain {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
#         }
#         """
    
#     return base_css + background_css

# # Create the Gradio app
# with gr.Blocks(css=create_css_with_background(), title="FATIMA") as demo:
    
#     show_chat = gr.State(False)
#     toggle_btn = gr.Button("💬", elem_id="float-btn")
    
#     # Chat UI
#     with gr.Column(visible=False, elem_id="chatbox") as chatbot_ui:
#         with gr.Row(elem_id="chatbox-header"):
#             gr.Markdown("FATIMA.ai")
#             minimize_btn = gr.Button("⬇", scale=1)
        
#         chatbot = gr.Chatbot()
        
#         with gr.Row():
#             user_input = gr.Textbox(placeholder="Ask FATIMA...", scale=6, show_label=False)
        
#         with gr.Row():
#             send_btn = gr.Button("Send", size="sm", scale=1)
    
#     # Toggle behavior
#     toggle_btn.click(fn=toggle_visibility, inputs=show_chat, outputs=[chatbot_ui, show_chat])
#     minimize_btn.click(fn=toggle_visibility, inputs=show_chat, outputs=[chatbot_ui, show_chat])
    
#     # Chat interactions
#     send_btn.click(fn=chat_with_fatima, inputs=user_input, outputs=[chatbot, user_input])
#     user_input.submit(fn=chat_with_fatima, inputs=user_input, outputs=[chatbot, user_input])

# # Print status
# if background_image:
#     print("✅ Background image loaded successfully!")
# else:
#     print("❌ Background image not found. Using gradient fallback.")
#     print("📁 Make sure 'UTD.png' is in the same directory as this script.")
#     print(f"📂 Current directory: {os.getcwd()}")
#     print(f"📄 Files in directory: {os.listdir('.')}")

# demo.launch()
import gradio as gr
import requests
import base64
import os

API_ENDPOINT = "http://localhost:8000/chatbot"
chat_history = []

# Convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{img_data}"
    except FileNotFoundError:
        print(f"Image file {image_path} not found!")
        return None

background_image = get_base64_image("UTD.png")

# Backend interaction
def chat_with_fatima(user_input):
    global chat_history
    if not user_input.strip():
        return chat_history, ""
    
    try:
        response = requests.post(API_ENDPOINT, json={"query": user_input}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "No response")
            sources = result.get("sources", [])
            if sources:
                answer += "\n\nSources:\n" + "\n".join(f"- {src}" for src in sources)

            contact_info = result.get("contact_info", [])
            if contact_info:
                answer += "\n\nContact Info:"
                for contact in contact_info:
                    answer += f"\n- Email: {contact.get('email', '')}, Phone: {contact.get('phone', '')}, Location: {contact.get('location', '')}"
        else:
            answer = f"Server error: {response.status_code}"
    except Exception as e:
        answer = f"Exception: {str(e)}"

    chat_history.append(("You", user_input))
    chat_history.append(("FATIMA", answer))
    return chat_history, ""

# Toggle visibility
def toggle_visibility(current):
    return gr.update(visible=not current), not current

# CSS styling
def create_css_with_background():
    base_css = """
    #float-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        width: 48px;
        height: 48px;
        border-radius: 24px;
        font-size: 24px;
        text-align: center;
        background-color: #4a4a4a;
        color: white;
        box-shadow: 0 0 6px rgba(0,0,0,0.3);
        border: none;
        cursor: pointer;
    }

    #float-btn:hover {
        background-color: #5a5a5a;
    }

    #chatbox {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 320px;
        height: 440px;
        z-index: 999;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        background: #1c1c1c;
        padding: 0;
        font-size: 12px;
        overflow: hidden;
    }

    #chatbox-header {
        height: 48px;
        padding: 12px;
        background-color: #1f1f1f;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        font-size: 13px;
        font-weight: bold;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
    }

    /* Hide progress timer */
    .wrap.svelte-1ipelgc, .wrap.svelte-13f72ry {
        display: none !important;
    }

    #main-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
        padding: 20px;
    }

    #title-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px 60px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 800px;
        margin: 0 auto;
    }

    #main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
    }

    #subtitle {
        font-size: 1.4rem;
        font-weight: 300;
        color: #e0e0e0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        letter-spacing: 1px;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    """

    if background_image:
        background_css = f"""
        .gradio-container {{
            background-image: url('{background_image}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            min-height: 100vh !important;
        }}
        body {{
            background-image: url('{background_image}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        """
    else:
        background_css = """
        .gradio-container, body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        """
    
    return base_css + background_css

# Launch Gradio
with gr.Blocks(css=create_css_with_background(), title="FATIMA") as demo:
    with gr.Column(elem_id="main-content"):
        gr.HTML("""
        <div id="title-container">
            <h1 id="main-title">UTD-FATIMA.ai</h1>
            <p id="subtitle">Flexible Academic Text Intelligence and Management Assistant</p>
        </div>
        """)

    show_chat = gr.State(False)
    toggle_btn = gr.Button("💬", elem_id="float-btn")

    with gr.Column(visible=False, elem_id="chatbox") as chatbot_ui:
        with gr.Row(elem_id="chatbox-header"):
            gr.Markdown("FATIMA.ai")
            minimize_btn = gr.Button("⬇", scale=1)

        chatbot = gr.Chatbot(label="")

        with gr.Row():
            user_input = gr.Textbox(placeholder="Ask FATIMA...", scale=6, show_label=False)
            send_btn = gr.Button("Send", scale=1)

    toggle_btn.click(fn=toggle_visibility, inputs=show_chat, outputs=[chatbot_ui, show_chat])
    minimize_btn.click(fn=toggle_visibility, inputs=show_chat, outputs=[chatbot_ui, show_chat])
    send_btn.click(fn=chat_with_fatima, inputs=user_input, outputs=[chatbot, user_input])
    user_input.submit(fn=chat_with_fatima, inputs=user_input, outputs=[chatbot, user_input])

if background_image:
    print("✅ Background image loaded successfully.")
else:
    print("⚠️ No background image found. Using gradient fallback.")

demo.launch()
