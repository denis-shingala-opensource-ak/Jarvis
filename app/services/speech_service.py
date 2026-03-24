"""Speech-to-Text and Text-to-Speech service using free Google services."""
import io
import base64
import asyncio

from app.core.config import settings
from app.core.exceptions import SpeechServiceError, ConfigurationError
from app.core.logging_config import logger


class GoogleFreeSTT:
    """Speech-to-Text using Google's free speech recognition (no API key needed)."""

    async def transcribe(self, audio_bytes: bytes, format: str = "webm") -> str:
        try:
            import speech_recognition as sr
            from pydub import AudioSegment

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._transcribe_sync, audio_bytes, format)
        except Exception as e:
            logger.error(f"Google STT error: {e}")
            raise SpeechServiceError(f"STT failed: {e}")

    def _transcribe_sync(self, audio_bytes: bytes, format: str) -> str:
        import speech_recognition as sr
        from pydub import AudioSegment

        # Convert incoming audio to WAV (speech_recognition requires WAV)
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format)
        wav_buffer = io.BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        return text.strip()


class GoogleFreeTTS:
    """Text-to-Speech using gTTS (Google Translate TTS - free, no API key)."""

    async def synthesize(self, text: str) -> bytes:
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._synthesize_sync, text)
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            raise SpeechServiceError(f"TTS failed: {e}")

    def _synthesize_sync(self, text: str) -> bytes:
        from gtts import gTTS

        tts = gTTS(text=text, lang="en")
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        return mp3_buffer.read()


class OpenAIWhisperSTT:
    """Speech-to-Text using OpenAI Whisper API (requires OpenAI API key)."""

    def __init__(self):
        import openai
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes, format: str = "webm") -> str:
        try:
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = f"audio.{format}"
            transcript = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
            )
            return transcript.strip()
        except Exception as e:
            logger.error(f"Whisper STT error: {e}")
            raise SpeechServiceError(f"STT failed: {e}")


class OpenAITTS:
    """Text-to-Speech using OpenAI TTS API (requires OpenAI API key)."""

    def __init__(self):
        import openai
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def synthesize(self, text: str) -> bytes:
        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice=settings.TTS_VOICE,
                input=text,
                response_format="mp3",
            )
            return response.content
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise SpeechServiceError(f"TTS failed: {e}")


class SpeechService:
    """Unified speech service facade."""

    def __init__(self):
        # STT
        if settings.STT_PROVIDER == "google_free":
            self.stt = GoogleFreeSTT()
        elif settings.STT_PROVIDER == "openai_whisper":
            self.stt = OpenAIWhisperSTT()
        else:
            raise ConfigurationError(f"Unknown STT provider: {settings.STT_PROVIDER}")

        # TTS
        if settings.TTS_PROVIDER == "google_free":
            self.tts = GoogleFreeTTS()
        elif settings.TTS_PROVIDER == "openai_tts":
            self.tts = OpenAITTS()
        else:
            raise ConfigurationError(f"Unknown TTS provider: {settings.TTS_PROVIDER}")

    async def transcribe(self, audio_bytes: bytes, format: str = "webm") -> str:
        return await self.stt.transcribe(audio_bytes, format)

    async def synthesize(self, text: str) -> bytes:
        return await self.tts.synthesize(text)

    async def synthesize_base64(self, text: str) -> str:
        audio_bytes = await self.synthesize(text)
        return base64.b64encode(audio_bytes).decode("utf-8")
