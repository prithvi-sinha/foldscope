import os
import time
from openai import OpenAI

# Initialize OpenAI client
os.environ["OPENAI_API_KEY"] = "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"
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Assistant configuration
assistant_id = "asst_QGIJoangFXerAei9NAVTitCA"

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
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status

def process_image(image_path):
    try:
        print("Processing image...")
        file = client.files.create(
                file=open(image_path, "rb"),
                purpose="vision"
                )
        
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

        # Create a new thread
        my_run_id, my_thread_id = create_thread(content)

        # Check the run status
        status = check_status(my_run_id, my_thread_id)
        while (status != "completed"):
            status = check_status(my_run_id, my_thread_id)
            time.sleep(2)

        # Get the response
        response = client.beta.threads.messages.list(
            thread_id=my_thread_id
        )

        if response.data:
            content = response.data[0].content[0].text.value
            return content
        else:
            raise Exception("No response received from assistant")

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Starting image processing...")
    # Replace with your image path
    image_path = "images/IMG_20240523_152537.jpg"
    result = process_image(image_path)
    if result:        
        print("\nImage Classification:")
        print(result)
    else:
        print("Failed to process image")
