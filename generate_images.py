import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "app/static/img/workouts"
os.makedirs(output_dir, exist_ok=True)

workouts = [
    {"name": "Dumbbell Flyes", "color": (70, 130, 200), "filename": "chest_fly.jpg"},
    {"name": "Pull-up", "color": (60, 180, 75), "filename": "pullup.jpg"},
    {"name": "Squat", "color": (220, 50, 50), "filename": "squat.jpg"},
    {"name": "Shoulder Press", "color": (255, 165, 0), "filename": "shoulder_press.jpg"},
]

try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

for w in workouts:
    img = Image.new('RGB', (400, 300), color=w["color"])
    draw = ImageDraw.Draw(img)
    text = w["name"]
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (300 - text_height) // 2)
    draw.text(position, text, fill="white", font=font)
    img.save(os.path.join(output_dir, w["filename"]))
    print(f"Created {w['filename']}")