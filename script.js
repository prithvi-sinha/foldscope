const API_URL = "https://foldscopeapi.onrender.com/classify-image/";

const video = document.getElementById("camera-feed");
const output = document.getElementById("output");
const arResult = document.getElementById("ar-result");

// Access the user's camera
async function startCamera() {
    try {
        console.log("Requesting camera access...");
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Wait for metadata to load
        video.onloadedmetadata = () => {
            console.log("Video feed ready:", video.videoWidth, "x", video.videoHeight);
        };
    } catch (error) {
        console.error("Error accessing camera:", error);
        alert("Error accessing camera: " + error.message);
    }
}

// Capture a frame from the video feed and classify it
async function captureImage() {
    // Wait until the video feed is ready
    if (video.videoWidth === 0 || video.videoHeight === 0) {
        console.log("Video feed not ready. Retrying...");
        setTimeout(captureImage, 500); // Retry after 500ms
        return;
    }

    console.log("Capturing image...");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        if (!blob) {
            console.error("Failed to create Blob from canvas.");
            alert("Failed to capture image. Please try again.");
            return;
        }

        const formData = new FormData();
        formData.append("image", blob, "capture.jpg");

        try {
            output.textContent = "Processing...";
            console.log("Sending image to API...");
            const response = await fetch(API_URL, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            const data = await response.json();
            console.log("API Response:", data);
            output.textContent = data.classification;
            arResult.setAttribute("value", data.classification);
        } catch (error) {
            console.error("Error:", error);
            output.textContent = `Error: ${error.message}`;
        }
    }, "image/jpeg");
}

// Debugging: List available devices
async function listDevices() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        devices.forEach((device) => {
            console.log(`${device.kind}: ${device.label} (id: ${device.deviceId})`);
        });
    } catch (error) {
        console.error("Error listing devices:", error);
    }
}

// Event Listeners
document.getElementById("capture-btn").addEventListener("click", captureImage);
document.getElementById("ar-btn").addEventListener("click", () => {
    alert("Point your camera at a Hiro marker to see AR overlays!");
});

// Initialize the camera and debug utilities
startCamera();
listDevices();
