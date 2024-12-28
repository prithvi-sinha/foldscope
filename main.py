import os
import time
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from .env
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

if not api_key or not assistant_id:
    raise ValueError("OPENAI_API_KEY or ASSISTANT_ID not set in .env file")

client = OpenAI(api_key=api_key)

# Initialize FastAPI app
app = FastAPI(title="Image Classification API", version="1.0")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://your-frontend-domain.com"],  # Replace with your trusted origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_thread(prompt):
    thread = client.beta.threads.create()
    my_thread_id = thread.id

    message = client.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=assistant_id,
    )

    return run.id, thread.id

def check_status(run_id, thread_id):
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status

@app.get("/")
def read_root():
    """
    Root endpoint for testing the API.
    """
    return {"message": "Welcome to the Image Classification API. Use /classify-image/ to classify images."}

@app.post("/classify-image/")
async def classify_image(image: UploadFile):
    """
    Endpoint to classify an uploaded image using OpenAI API.
    """
    try:
        # Save uploaded file temporarily
        image_path = f"/tmp/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())
        
        # Upload the file to OpenAI
        file = client.files.create(
            file=open(image_path, "rb"),
            purpose="vision"
        )

        # Create content for classification
        content = [
            {
                "type": "text",
                "text": "Please analyze this image and provide a clear description of what type of image this is. Focus on identifying the main subject matter and any key characteristics."
            },
            {
                "type": "image_file",
                "image_file": {
                    "file_id": file.id,
                    "detail": "high"
                }
            }
        ]

        # Create a thread for processing
        my_run_id, my_thread_id = create_thread(content)

        # Poll the status until completion
        while True:
            status = check_status(my_run_id, my_thread_id)
            if status == "completed":
                break
            elif status == "failed":
                raise HTTPException(status_code=500, detail="Image processing failed.")
            time.sleep(2)

        # Retrieve the classification result
        response = client.beta.threads.messages.list(thread_id=my_thread_id)
        if response.data:
            classification = response.data[0].content[0].text.value
            return JSONResponse({"classification": classification})
        else:
            raise HTTPException(status_code=500, detail="No response received from assistant.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
