import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION & API SETUP ---
# Replace the text inside quotes below with the actual API Key you copied from Google
API_KEY = "AIzaSyCweDQ0ny_f4uov2iuV36auuiw-Q__XSTI"
genai.configure(api_key=API_KEY)

# --- 2. LOAD COMPILING DATABASE ---
def load_knowledge_base():
    if os.path.exists("knowledge.txt"):
        with open("knowledge.txt", "r", encoding="utf-8") as file:
            return file.read()
    return "No company data found."

company_data = load_knowledge_base()

# --- 3. STREAMLIT INTERFACE INTERACTION ---
st.set_page_config(page_title="InstruBot - Technical Assistant", page_icon="⚙️", layout="centered")

st.title("⚙️ InstruBot")
st.subheader("Instruworks Internal Technical Assistant")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if user_query := st.chat_input("Ask about Products, Applications, Industry, Brand, or AVL..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    system_instruction = f"""
    You are 'InstruBot', an expert internal technical assistant for the company 'Instruworks'.
    Your primary job is to answer queries strictly structured around these core parameters requested by management:
    - Product
    - Applications
    - Industry
    - Brand
    - AVL (Approved Vendor List)

    Use the following verified company database text to answer the query accurately:
    {company_data}

    Guidelines:
    1. Organize your responses clearly, pointing out relevant Product lines, Applications, Industries, Brands, or AVL status where applicable.
    2. If the user asks something completely unrelated to these categories or outside our data context, politely reply: 'I specialize in our verified Product, Applications, Industry, Brand, and AVL databases. For external queries, please contact menatsales@instruworks.com.'
    """

    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content([system_instruction, user_query])
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error communicating with AI Brain. Please check your API key setup. Details: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})