import io
import wave

from fastapi import FastAPI
from starlette.responses import StreamingResponse

from say_neural import NeuralSpeaker

neural_speaker = NeuralSpeaker()
app = FastAPI()


@app.get("/")
async def speak(words: str, speaker: str = 'xenia', sample_rate: int = 48000):
    print(f'speak {words}, {speaker}, {sample_rate}')
    time_elapsed = neural_speaker.speak(words=words, speaker=speaker, save_file=False, sample_rate=sample_rate)
    print(f'Model completed in {time_elapsed} seconds')
    json_response = {'Response': f'Model completed in {time_elapsed} seconds'}
    return json_response


@app.get("/get_audio_file")
async def return_audio_file(words: str, speaker: str = 'xenia', sample_rate: int = 48000):
    print(f'save file {words}, {speaker}, {sample_rate}')
    audio_data = neural_speaker.speak(words=words, speaker=speaker, save_file=True, sample_rate=sample_rate)
    f = io.BytesIO()
    wav_file_in_memory = wave.open(f, 'w')
    wav_file_in_memory.setnchannels(1)  # mono
    wav_file_in_memory.setsampwidth(2)
    wav_file_in_memory.setframerate(sample_rate)
    wav_file_in_memory.writeframes(audio_data)
    wav_file_in_memory.close()
    f.seek(0)
    audio_file_response = StreamingResponse(content=f, media_type="audio/wav")
    audio_file_response.headers["Content-Disposition"] = f"attachment; filename = speech_audio.wav"
    return audio_file_response
