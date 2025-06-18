import gradio as gr
import google.generativeai as genai
import os
import pyttsx3
import uuid


genai.configure(api_key="AIzaSyAyflCfV0xGgQjwKHYv_AZaBUQ5qvhkWkA")

model = genai.GenerativeModel('gemini-1.5-flash-latest')

PERSONA_CONTEXT = """
You are Anant Srivastava, a Software Developer with a B.Tech in Electronics & Telecommunication from Bharati Vidyapeeth College of Engineering, Pune (GPA: 7.8). 
You have hands-on experience with C++, JavaScript, Python, Go, and frameworks like Express, Node, Django, and Gin. 
Your expertise includes MySQL, SQLite, MongoDB, Redis, and deploying scalable systems with CI/CD and AWS. 
You interned at Times Network, building AI chatbots, YouTube migration tools, WhatsApp data categorization systems, and Twitter engagement analytics. 
You are known for problem-solving, team collaboration, technical documentation, and time management.
Established in 2019, Home.LLC is dedicated to addressing challenges in the housing market. Our mission is to alleviate
the home ownership crisis in America by streamlining the process of buying, owning, and selling homes for greater efficiency and effectiveness. 
Answer all questions confidently and concisely in first person, as if speaking directly to the CEO.
"""

def text_to_speech(answer):
    # Use a unique filename to avoid overwrite/timing issues
    audio_path = f"bot_response_{uuid.uuid4().hex}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(answer, audio_path)
    engine.runAndWait()
    return audio_path

def chat_with_gemini(audio_file, history=None):
    import speech_recognition as sr

    if audio_file is None:
        return "Please say something!", None, history

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except Exception as e:
            return f"Speech recognition failed: {e}", None, history

    if history is None:
        history = []
    history.append(("User", text))

    prompt = PERSONA_CONTEXT + "\n"
    # Reconstruct conversation from history
    for idx in range(0, len(history) - 1, 2):
        prompt += f"User: {history[idx][1]}\nBot: {history[idx+1][1]}\n"
    if len(history) % 2 == 1:
        prompt += f"User: {history[-1][1]}\nBot:"

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"Gemini API error: {e}"

    history.append(("Bot", answer))

    # Convert answer to speech using offline TTS with unique filename
    audio_path = text_to_speech(answer)

    return answer, audio_path, history

iface = gr.Interface(
    fn=chat_with_gemini,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your interview question"),
        gr.State()
    ],
    outputs=[
        gr.Textbox(label="🤖 Bot's Response"),
        gr.Audio(label="🔊 Bot's Voice Response"),
        gr.State()
    ],
    title="🏠 Home.LLC Interview Voice Bot by Anant Srivastava (Gemini)",
    description="🎤 Speak a question and hear how Anant would respond in the interview. Powered by Google Gemini."
)

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )


























# import gradio as gr
# import google.generativeai as genai
# import os
# import pyttsx3


# genai.configure(api_key="AIzaSyAyflCfV0xGgQjwKHYv_AZaBUQ5qvhkWkA")

# model = genai.GenerativeModel('gemini-1.5-flash-latest')


# PERSONA_CONTEXT = """
# You are Anant Srivastava, a Software Developer with a B.Tech in Electronics & Telecommunication from Bharati Vidyapeeth College of Engineering, Pune (GPA: 7.8). 
# You have hands-on experience with C++, JavaScript, Python, Go, and frameworks like Express, Node, Django, and Gin. 
# Your expertise includes MySQL, SQLite, MongoDB, Redis, and deploying scalable systems with CI/CD and AWS. 
# You interned at Times Network, building AI chatbots, YouTube migration tools, WhatsApp data categorization systems, and Twitter engagement analytics. 
# You are known for problem-solving, team collaboration, technical documentation, and time management.
# Established in 2019, Home.LLC is dedicated to addressing challenges in the housing market. Our mission is to alleviate
# the home ownership crisis in America by streamlining the process of buying, owning, and selling homes for greater efficiency and effectiveness. 
# Answer all questions confidently and concisely in first person, as if speaking directly to the CEO.
# """

# def text_to_speech(answer, audio_path="bot_response.mp3"):
#     engine = pyttsx3.init()
#     engine.save_to_file(answer, audio_path)
#     engine.runAndWait()
#     return audio_path

# def chat_with_gemini(audio_file, history=None):
#     import speech_recognition as sr

#     if audio_file is None:
#         return "Please say something!", None, history

#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data)
#         except Exception as e:
#             return f"Speech recognition failed: {e}", None, history

#     if history is None:
#         history = []
#     history.append(("User", text))

#     prompt = PERSONA_CONTEXT + "\n"
#     # Reconstruct conversation from history
#     for idx in range(0, len(history) - 1, 2):
#         prompt += f"User: {history[idx][1]}\nBot: {history[idx+1][1]}\n"
#     if len(history) % 2 == 1:
#         prompt += f"User: {history[-1][1]}\nBot:"

#     try:
#         response = model.generate_content(prompt)
#         answer = response.text.strip()
#     except Exception as e:
#         answer = f"Gemini API error: {e}"

#     history.append(("Bot", answer))

#     # Convert answer to speech using offline TTS
#     audio_path = text_to_speech(answer)

#     return answer, audio_path, history

# iface = gr.Interface(
#     fn=chat_with_gemini,
#     inputs=[
#         gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak your interview question"),
#         gr.State()
#     ],
#     outputs=[
#         gr.Textbox(label="🤖 Bot's Response"),
#         gr.Audio(label="🔊 Bot's Voice Response"),
#         gr.State()
#     ],
#     title="🏠 Home.LLC Interview Voice Bot by Anant Srivastava (Gemini)",
#     description="🎤 Speak a question and hear how Anant would respond in the interview. Powered by Google Gemini."
# )

# if __name__ == "__main__":
#     iface.launch(
#         server_name="0.0.0.0",
#         server_port=int(os.environ.get("PORT", 7860))
#     )

















