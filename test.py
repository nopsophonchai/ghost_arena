import librosa
import soundfile as sf
import numpy as np

# Load the audio file (Librosa defaults to 22050 Hz sample rate)
audio, sr = librosa.load("rew.mp3", sr=4000, mono=True)  # Load as mono and downsample to 11025 Hz

# Quantize the audio to emulate 8-bit
# Normalize audio to -1.0 to 1.0 range
audio = audio / np.max(np.abs(audio))
# Scale and quantize to 8-bit values
audio = np.round(audio * 127) / 127
# Convert back to the 16-bit range to save as a file
audio = (audio * 10000).astype(np.int16)

# Save the modified audio to a WAV file
sf.write("8bit_style_audio.wav", audio, sr)
