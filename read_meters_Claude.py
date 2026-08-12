import anthropic
import base64
import csv
import io
from pathlib import Path
from PIL import Image

client = anthropic.Anthropic()

photos_dir  = r"C:\RaspberryPI\WaterMeterPics"
output_file = r"C:\RaspberryPI\meter_readings.csv"

# -----------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------

# Left 4 digits of the meter - update when they roll over
LEFT_4 = "0165"

# Native capture resolution of the Pi camera
CAMERA_W = 4608
CAMERA_H = 2592

# Digit region corners measured in Paint at 100% zoom at native resolution
# Order: upper-left, upper-right, lower-right, lower-left
DIGIT_REGION = {
    "UL": (2604, 1694),
    "UR": (3242, 1650),
    "LR": (3278, 1898),
    "LL": (2616, 1924),
}

# Upscale factor applied to the crop before sending to Claude
UPSCALE = 3

# -----------------------------------------------------------------------

SYSTEM_PROMPT = "You are a meter reader. Return only digits, nothing else."

PROMPT = """This is a cropped image of a Neptune water meter digit display showing 4 rolling digits.

READING RULES:
- Read the digits left to right
- The rightmost digit is on a BLACK background and is always 0
- If a digit wheel is mid-rotation between two numbers, always take the LOWER number
- The digit 5 on this meter has a distinctive horizontal gap through the middle — this is a physical trait of this meter, not damage or glare. A digit with a flat top, a mid-gap, and a curved lower-right is a 5
- Distinguish 2 from 8: a 2 has an open bottom and a curved top; an 8 has two fully closed loops
- Distinguish 3 from 8: an 8 is two fully closed loops; a 3 is open on the left side
- Distinguish 1 from 7: a 7 has a horizontal top bar; a 1 does not

OUTPUT: Exactly 4 digits, nothing else. If you cannot read with confidence, return 0000."""


def crop_digit_region(img):
    """Perspective-correct crop of the digit strip, scaled up for clarity."""
    stored_w, stored_h = img.size
    sx = stored_w / CAMERA_W
    sy = stored_h / CAMERA_H

    ul_x = int(DIGIT_REGION["UL"][0] * sx)
    ul_y = int(min(DIGIT_REGION["UL"][1], DIGIT_REGION["UR"][1]) * sy)
    lr_x = int(DIGIT_REGION["LR"][0] * sx)
    lr_y = int(max(DIGIT_REGION["LL"][1], DIGIT_REGION["LR"][1]) * sy)

    # Clamp to image bounds
    ul_x = max(0, min(ul_x, stored_w))
    ul_y = max(0, min(ul_y, stored_h))
    lr_x = max(0, min(lr_x, stored_w))
    lr_y = max(0, min(lr_y, stored_h))

    cropped  = img.crop((ul_x, ul_y, lr_x, lr_y))
    upscaled = cropped.resize((cropped.width * UPSCALE, cropped.height * UPSCALE), Image.LANCZOS)
    return upscaled


def image_to_base64(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=95)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def get_meter_reading(jpg_path):
    img        = Image.open(jpg_path)
    cropped    = crop_digit_region(img)
    image_data = image_to_base64(cropped)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=20,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
                {"type": "text", "text": PROMPT}
            ],
        }]
    )
    return message.content[0].text.strip()


def is_valid(raw):
    """4 digits, ends in 0, not 0000."""
    return raw.isdigit() and len(raw) == 4 and raw[-1] == '0' and raw != "0000"


def to_8digit(four):
    return LEFT_4 + four


# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------
results = []

print(f"{'Filename':<40} {'4-digit':>8} {'8-digit':>10}  {'Notes'}")
print("-" * 75)

for date_folder in sorted(Path(photos_dir).iterdir()):
    if not date_folder.is_dir():
        continue
    for jpg_file in sorted(date_folder.glob("*.jpg")):
        raw  = get_meter_reading(jpg_file)
        raw  = ''.join(filter(str.isdigit, raw))

        if is_valid(raw):
            reading_4 = raw
            note      = ""
        else:
            reading_4 = "0000"
            note      = "REVIEW"

        reading_8  = to_8digit(reading_4)
        filename   = jpg_file.stem
        date_part  = filename[:10]
        time_part  = filename[11:].replace("-", ":")

        print(f"{jpg_file.name:<40} {reading_4:>8} {reading_8:>10}  {note}")
        results.append([date_part, time_part, reading_8, reading_4, note])

# Write CSV
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Time", "Meter Reading", "Right 4 Digits", "Notes"])
    writer.writerows(results)

review_count = sum(1 for r in results if r[4] == "REVIEW")
print(f"\nCSV saved to {output_file}")
print(f"Total images: {len(results)}  |  Needs review: {review_count}")
