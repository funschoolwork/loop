# generate_frame.py
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import time

def generate_frame(count: int) -> str:
    for attempt in range(5):  # Retry up to 5 times
        try:
            response = requests.get("https://randomuser.me/api/", timeout=5)
            if response.status_code != 200:
                raise Exception(f"Status code {response.status_code}")
            r = response.json()
            break
        except Exception as e:
            print(f"[ERROR] Failed to fetch user data (attempt {attempt+1}): {e}")
            time.sleep(2)
    else:
        raise RuntimeError("Failed to fetch user data after 5 attempts.")

    user = r["results"][0]
    name = f'{user["name"]["first"]} {user["name"]["last"]}'
    image_url = user["picture"]["large"]

    # Generate background
    bg = Image.new("RGB", (1280, 720), (25, 25, 25))
    draw = ImageDraw.Draw(bg)

    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((50, 600), f"#{count:,} - {name}", fill="white", font=font)

    # Download and paste user image
    try:
        image_response = requests.get(image_url, timeout=5)
        img = Image.open(BytesIO(image_response.content)).resize((400, 400))
        bg.paste(img, (440, 150))
    except Exception as e:
        print(f"[ERROR] Failed to fetch or paste image: {e}")

    # Save frame
    path = "frame.jpg"
    bg.save(path)
    return path
