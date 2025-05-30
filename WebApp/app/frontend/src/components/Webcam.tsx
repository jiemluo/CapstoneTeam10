'use client';

import { useRef, useState, useEffect } from 'react';

const Webcam = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [uploadedBlobUrl, setUploadedBlobUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [liveMonitoring, setLiveMonitoring] = useState(false);
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string | null>(null);
  const [detectionImageUrl, setDetectionImageUrl] = useState<string | null>(null);
  const [fireDetected, setFireDetected] = useState(false);

  useEffect(() => {
    if (detectionImageUrl) {
      setFireDetected(true);
    } else {
      setFireDetected(false);
    }
  }, [detectionImageUrl]);

  useEffect(() => {
    const startWebcam = async () => {
      console.log(uploadedImage);
      console.log(uploadedBlobUrl);
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Error accessing webcam:', err);
      }
    };

    startWebcam();
  }, []);

  useEffect(() => {
    let isActive = true;
  
    const loopCapture = async () => {
      while (isActive && liveMonitoring) {
        if (canvasRef.current && videoRef.current) {
          const canvas = canvasRef.current;
          const video = videoRef.current;
  
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
  
          const ctx = canvas.getContext('2d');
          if (ctx) ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
          const blob: Blob | null = await new Promise((resolve) =>
            canvas.toBlob((b) => resolve(b), 'image/jpeg')
          );
  
          if (blob) {
            await sendToAPI(blob);
          }
  
          // Optional delay between frames (e.g., 500ms)
          await new Promise((res) => setTimeout(res, 500));
        }
      }
    };
  
    if (liveMonitoring) {
      loopCapture();
    }
  
    return () => {
      isActive = false;
    };
  }, [liveMonitoring]);

  const captureAndSend = async () => {
    if (!canvasRef.current || !videoRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    if (ctx) ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (blob) await sendToAPI(blob);
    }, 'image/jpeg');
  };

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
  
    setUploadedImage(file);
    const imageUrl = URL.createObjectURL(file);
    setUploadedBlobUrl(imageUrl);
  
    const img = new Image();
    img.onload = () => {
      if (canvasRef.current) {
        const canvas = canvasRef.current;
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        if (ctx) ctx.drawImage(img, 0, 0);
      }
    };
    img.src = imageUrl;
  
    sendToAPI(file);
  };


  const sendToAPI = async (imageBlob: Blob | File) => {
    const formData = new FormData();
    formData.append('file', imageBlob);
  
    // const url = "http://localhost:7860/predict";
    const PredictionURL = "https://mcfads1-CapstoneTeamInsomniacs.hf.space/predict";
    const DetectionURL = "https://mcfads1-capstone10-luo.hf.space/predict";

    try {
      const [predictionRes, detectionRes] = await Promise.all([
        fetch(PredictionURL, { method: 'POST', body: formData }),
        fetch(DetectionURL, { method: 'POST', body: formData }),
      ]);
  
      const predictionBlob = await predictionRes.blob();
      setGeneratedImageUrl(URL.createObjectURL(predictionBlob));
  
      const detectionJson = await detectionRes.json();
      setDetectionImageUrl(detectionJson["prediction"]);
    } catch (err) {
      console.error('API call failed:', err);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-6 w-full h-full overflow-hidden">
      {/* Webcam Feed */}
      <div className="w-full bg-black rounded-xl overflow-hidden shadow aspect-video max-h-[40vh]">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-contain"
        />
      </div>
  
      {/* Controls */}
      <div className="flex flex-col md:flex-row w-full items-center gap-2 md:gap-4">
        <button
          onClick={captureAndSend}
          className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl shadow hover:bg-blue-700 text-lg"
        >
          📸 Capture & Send Frame
        </button>
  
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleUpload}
          className="hidden"
        />
  
        <button
          onClick={() => fileInputRef.current?.click()}
          className="px-4 py-3 bg-green-600 text-white font-semibold rounded-xl shadow hover:bg-green-700 text-sm"
        >
          ⬆️ Upload & Send
        </button>
  
        <div className="flex items-center gap-3 mb-2">
          <label className="text-sm font-medium text-gray-700">Live Monitoring</label>
          <input
            type="checkbox"
            checked={liveMonitoring}
            onChange={() => setLiveMonitoring((prev) => !prev)}
            className="w-5 h-5 text-blue-600 bg-gray-100 border-gray-300 rounded"
          />
        </div>
      </div>
  
      {/* Output Comparison */}
      <div className="flex flex-wrap md:flex-nowrap w-full gap-4 flex-grow overflow-hidden">
        {/* Captured Frame */}
        <div className="flex-1 min-w-0 border-2 border-dashed border-gray-300 rounded-xl p-4 shadow-inner bg-white h-[35vh]">
          <p className="text-center text-gray-700 font-medium mb-2 text-sm">📷 Captured Frame</p>
          <canvas
            ref={canvasRef}
            className="w-full h-full object-contain rounded"
          />
        </div>
  
        {/* Prediction Output */}
        {generatedImageUrl && (
          <div
            className={`flex-1 min-w-0 rounded-xl p-4 shadow-lg h-[35vh] transition-all duration-300 ${
              fireDetected
                ? 'border-4 border-red-600 bg-gradient-to-br from-yellow-50 via-red-100 to-yellow-50'
                : 'border bg-white'
            }`}
          >
            <p className={`text-center font-medium mb-2 text-sm ${
              fireDetected ? 'text-red-700' : 'text-gray-700'
            }`}>
              🤖 Prediction {fireDetected && '🔥'}
            </p>
            <img
              src={generatedImageUrl}
              alt="Prediction Result"
              className="w-full h-full object-contain rounded"
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default Webcam;
