# CVB/utils/captcha.py

from PIL import Image, ImageDraw, ImageFont
import random
import io

def generate_captcha(text="1234"):
    img = Image.new("RGB", (100, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, fill=(0, 0, 0))
    
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output