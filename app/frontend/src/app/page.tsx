import Image from "next/image";
import Webcam from "@/components/Webcam";
export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col items-center text-center space-y-8 w-full max-w-[90vw]">
        <h1 className="text-4xl font-bold text-gray-800">🎥 Live Webcam Stream</h1>
        <p className="text-base text-gray-600 max-w-2xl">
          Click the button below to capture the current frame and Detect Flames!
        </p>
        <Webcam />
      </main>
    </div>
  );
}