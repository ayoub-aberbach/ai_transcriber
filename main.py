import os
import uvicorn
import aiofiles
from groq import Groq
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Response, UploadFile


load_dotenv()
app = FastAPI(debug=True, version="0.0.1", description="Simple REST API that transcribes audio files using AI.")

groq_api = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_api)


@app.get("/", include_in_schema=False)
def Documentation():
    """
    Redirects to the API documentation.

    **Responses:**
    - 307: Temporary redirect to `/docs`.
    """
    return RedirectResponse("/docs")


@app.post("/transcribe/mp3")
async def transcribe_audio(audio_file: UploadFile):
    """
    Transcribes an uploaded MP3 (or other supported audio formats) using Whisper AI.

    **Request Body:**
    - `audio_file`: An uploaded audio file in one of the supported formats (Stored locally).

    **Supported Formats:**
    - flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm, x-m4a

    **Responses:**
    - 200: Successful transcription, returns the transcribed text.
    - 403: Unsupported file type.
    - 404: File not found.
    - 500: Internal server error.
    """
    try:
        file_exts: list = ["flac", "mp3", "mp4", "mpeg", "mpga", "m4a", "ogg", "wav", "webm", "x-m4a"]

        if audio_file.content_type.split("/")[1] not in file_exts:
            return Response("File type not supported", status_code=403)

        async with aiofiles.open(os.path.join("uploads", audio_file.filename), "wb") as local_file:
            file_bytes = await audio_file.read()
            await local_file.write(file_bytes)

        filename = os.path.basename(local_file.name)

        async with aiofiles.open(os.path.join("uploads", filename), "rb") as in_file:
            reading_file = await in_file.read()

            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3", file=(filename, reading_file), language="en"
            )

            return JSONResponse(content=transcription.text.strip(), status_code=200)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except IOError:
        raise HTTPException(status_code=500, detail="IO Error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, reload=True, env_file=".env")
