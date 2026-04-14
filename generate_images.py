import os
from PIL import Image, ImageDraw, ImageFont

# Define the output folder
output_dir = "app/static/img/workouts"
os.makedirs(output_dir, exist_ok=True)

# List of workout names and a color for each (you can match with real workouts)
workouts = [
    {"name": "Dumbbell Flyes", "color": (70, 130, 200), "filename": "chest_fly.jpg"},
    {"name": "Pull-up", "color": (60, 180, 75), "filename": "pullup.jpg"},
    {"name": "Squat", "color": (220, 50, 50), "filename": "squat.jpg"},
    {"name": "Shoulder Press", "color": (255, 165, 0), "filename": "shoulder_press.jpg"},
    {"name": "Deadlift", "color": (128, 0, 128), "filename": "deadlift.jpg"},
    {"name": "Leg Press", "color": (0, 150, 150), "filename": "leg_press.jpg"},
    {"name": "Bench Press", "color": (200, 100, 50), "filename": "bench_press.jpg"},
    {"name": "Bicep Curl", "color": (100, 100, 200), "filename": "bicep_curl.jpg"},
]

# Try to load a default font (fallback if none exists)
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

for w in workouts:
    img = Image.new('RGB', (400, 300), color=w["color"])
    draw = ImageDraw.Draw(img)
    # Draw text in the center
    text = w["name"]
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (300 - text_height) // 2)
    draw.text(position, text, fill="white", font=font)
    # Save as JPG
    img.save(os.path.join(output_dir, w["filename"]))
    print(f"Created {w['filename']}")

print("All sample images generated.")