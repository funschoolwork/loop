# generate_frame.py
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_frame(count: int) -> str:
    # Get a random user with name + image
    r = requests.get("https://randomuser.me/api/").json()
    user = r["results"][0]
    name = f'{user["name"]["first"]} {user["name"]["last"]}'
    image_url = user["picture"]["large"]

    # Create background
    bg = Image.new("RGB", (1280, 720), (25, 25, 25))
    draw = ImageDraw.Draw(bg)

    # Load font (fallback if not found)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((50, 600), f"#{count:,} - {name}", fill="white", font=font)

    # Get and paste user image
    img = Image.open(BytesIO(requests.get(image_url).content)).resize((400, 400))
    bg.paste(img, (440, 150))

    path = "frame.jpg"
    bg.save(path)
    return path
