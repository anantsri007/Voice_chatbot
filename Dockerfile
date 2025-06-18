FROM python:3.10-slim

# Install build tools and all required audio dependencies for TTS and SpeechRecognition
RUN apt-get update && \
    apt-get install -y \
        gcc \
        portaudio19-dev \
        ffmpeg \
        espeak \
        libespeak1 \
        libasound2 \
        libasound2-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["python", "chattbot.py"]
