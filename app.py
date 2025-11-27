import streamlit as st
from agent import build_agent
from langchain_core.messages import HumanMessage
from history_manager import load_history, add_message
import uuid
import time

if "last_response" not in st.session_state:
    st.session_state.last_response = None

# Streamline effect for AI responses
def typewriter(text):
    placeholder = st.empty()
    displayed = ""

    for char in text:
        displayed += char
        placeholder.markdown(displayed)
        time.sleep(0.005) # typing speed

    return displayed

st.set_page_config(
    page_title="AI Travel Planner",
    layout="wide",
)

st.logo("logo.png", size="large")
st.title("TripSense")
st.caption("Plan trips • Find hotels • Check weather • Calculate distances • Convert currency")

st.sidebar.header("🧭 Navigation")

if st.sidebar.button("🗑 Clear History"):
    open("chat_history.json", "w").write("[]")
    st.session_state.last_response = None
    st.rerun()

st.sidebar.markdown("---")
with st.sidebar.expander("ℹ️ About TripSense"):
    st.markdown("""
**TripSense** helps you with:
-  Trips planning  
-  Hotel recommendations  
-  Weather updates  
-  Distance & route planning  
-  Currency conversions  
-  Packing suggestions  
    """)

@st.cache_resource
def get_agent():
    return build_agent()

agent = get_agent()

history = load_history()

for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

assistant_msgs = [m["content"] for m in history if m["role"] == "assistant"]

if assistant_msgs:
    st.session_state.last_response = assistant_msgs[-1]
else:
    st.session_state.last_response = None


user_input = st.chat_input("Ask anything about travel...")

if user_input:

    # Show user bubble
    with st.chat_message("user"):
        st.markdown(user_input)

    add_message("user", user_input)

    # Loading animation
    with st.spinner("Processing..."):
        try:
            output = agent.invoke({"messages": [HumanMessage(content=user_input)]})
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"⚠️ Something went wrong: {e}")
            st.stop()

    ai_msg = output["messages"][-1]

    # Extract content
    if isinstance(ai_msg.content, list):
        final_text = "".join(
            part["text"] for part in ai_msg.content 
        )
    else:
        final_text = ai_msg.content

    # Display assistant bubble
    with st.chat_message("assistant"):
        typewriter(final_text)

    st.session_state.last_response = final_text
    add_message("assistant", final_text)

# Text file download button
text_file_name = f"response_{uuid.uuid4().hex}.txt"
if st.session_state.last_response:
    st.download_button(
        label="⬇️ Download Last Response",
        data=st.session_state.last_response,
        file_name="travel_plan.txt",
        mime="text/plain",
    )
