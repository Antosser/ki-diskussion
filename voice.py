import json
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydub import AudioSegment
from google.cloud import texttospeech
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Function to read dialog from the input file
def read_dialog(file_path):
    try:
        with open(file_path, "r") as f:
            return eval(
                f.read()
            )  # It's better to use safe parsing like JSON, but eval is used as in original code.
    except Exception as e:
        print(f"Error reading dialog from file {file_path}: {e}")
        sys.exit(1)


# Read the dialog from the provided input file
if len(sys.argv) < 2:
    print("Usage: python script.py <dialog_file>")
    sys.exit(1)

dialog_file_path = sys.argv[1]
dialog = read_dialog(dialog_file_path)


# Function to generate speech using Google Cloud Text-to-Speech API
def text_to_speech(text, lang="de-DE", gender="male"):
    try:
        # Initialize Google Cloud TTS client
        client = texttospeech.TextToSpeechClient()

        # Set up the input text to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Choose voice based on gender
        if gender == "male":
            voice_name = "de-DE-Journey-D"  # Male voice
        else:
            voice_name = "de-DE-Journey-O"  # Female voice

        # Set voice parameters (language and specific voice)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            name=voice_name,  # Use specific voice (Journey-D or Journey-F)
        )

        # Set audio configuration (MP3 format)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the Text-to-Speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Generate a random filename using uuid
        audio_file_name = f"{uuid.uuid4().hex}.mp3"
        audio_file_path = os.path.join("generated_audio", audio_file_name)
        os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)

        # Write binary content to file
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(response.audio_content)

        print(f"Saved audio to: {audio_file_path}")
        return audio_file_path

    except Exception as e:
        print(f"Error generating speech for text '{text}': {e}")
        return None


# Create a directory for storing the audio files
output_dir = "generated_audio"
os.makedirs(output_dir, exist_ok=True)

# List to store the generated audio files
audio_files = []

# Use ThreadPoolExecutor to process the dialog in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_audio = {}
    for idx, text in enumerate(dialog):
        if idx % 2 == 0:
            gender = "male"  # First, third, fifth... messages will be male
        else:
            gender = "female"  # Second, fourth, sixth... messages will be female

        # Submit each task to the executor
        future = executor.submit(text_to_speech, text, "de-DE", gender)
        future_to_audio[future] = text

    # Collect the results as they complete
    for future in as_completed(future_to_audio):
        try:
            audio_file_path = future.result()
            if audio_file_path:
                audio_files.append(audio_file_path)
        except Exception as e:
            print(f"Error processing future task: {e}")

# Now combine all the audio files with a 2-second silence between them
print("Combining audio files with 2-second pauses...")

combined = AudioSegment.empty()

for idx, audio_file in enumerate(audio_files):
    print(f"Processing audio file {idx + 1}/{len(audio_files)}: {audio_file}")

    try:
        # Load the generated audio file (assuming MP3 format)
        speech = AudioSegment.from_mp3(audio_file)

        # Append the audio file to the combined output
        combined += speech

        # Add a 2-second silence (2000 milliseconds)
        silence = AudioSegment.silent(duration=2000)  # 2 seconds of silence
        combined += silence

    except Exception as e:
        print(f"Error loading audio file {audio_file}: {e}")

# Export the final combined audio to an output file
output_file = "combined_output.mp3"
try:
    combined.export(output_file, format="mp3")
    print(f"\nFinal combined audio saved to {output_file}")
except Exception as e:
    print(f"Error exporting combined audio: {e}")
