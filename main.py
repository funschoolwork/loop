# main.py
import subprocess
import time
from generate_frame import generate_frame
import os

# Load your YouTube stream key
STREAM_KEY = os.getenv("STREAM_KEY")
RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"

def stream_loop():
    count = 2_000_000

    while count > 0:
        print(f"[INFO] Generating frame #{count}")
        try:
            frame_path = generate_frame(count)
        except Exception as e:
            print(f"[FATAL] Could not generate frame: {e}")
            break

        print(f"[INFO] Streaming person #{count}")
        ffmpeg_cmd = [
            'ffmpeg',
            '-loop', '1',
            '-i', frame_path,
            '-stream_loop', '-1',
            '-i', 'loop.mp3',
            '-shortest',
            '-vf', 'format=yuv420p',
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-b:v', '3000k',
            '-c:a', 'aac',
            '-b:a', '160k',
            '-f', 'flv',
            f"{RTMP_URL}/{STREAM_KEY}"
        ]

        try:
            subprocess.run(ffmpeg_cmd)
        except Exception as e:
            print(f"[ERROR] Failed to run FFmpeg: {e}")
            break

        count -= 1
        time.sleep(1)

if __name__ == "__main__":
    stream_loop()
