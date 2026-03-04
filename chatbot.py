import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def run_pcos_chatbot(diagnosis_result, user_stats):
    st.write("---")
    st.subheader("💬 Discuss Your Results with AI")
    
    # 1. Fetch API Key from .env
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("Missing API Key! Please ensure GROQ_API_KEY is set in your .env file.")
        return

    # 2. Initialize Groq Client
    client = Groq(api_key=api_key)

    # 3. Initialize Chat History in Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        # System Prompt: Gives the AI context about the specific patient
        system_message = {
            "role": "system",
            "content": f"""You are a helpful, empathetic PCOS health assistant. 
            The user just received a '{diagnosis_result}' screening result.
            Patient Context: Age {user_stats['age']}, BMI {user_stats['bmi']:.1f}.
            Explain the results simply, answer questions about symptoms, and suggest lifestyle improvements (like low GI diets).
            CRITICAL: Always remind the user that you are an AI assistant and this is not a medical diagnosis. 
            Advise them to see a gynecologist for a formal checkup."""
        }
        st.session_state.messages.append(system_message)

    # 4. Display Chat Messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 5. Handle User Input
    if prompt := st.chat_input("Ask me about diet, symptoms, or next steps..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 6. Generate Streaming Response from Groq
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            try:
                completion = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick-17b-128e-instruct", 
                    messages=st.session_state.messages,
                    stream=True,
                )

                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                st.error(f"Chat Error: {e}")