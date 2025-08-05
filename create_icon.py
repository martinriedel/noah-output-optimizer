#!/usr/bin/env python3
"""
Create PNG icon from SVG for Home Assistant add-on
"""

import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Create a 512x512 image with blue background
    img = Image.new('RGBA', (512, 512), (33, 150, 243, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw battery body (white rectangle with border)
    battery_rect = (160, 180, 352, 300)
    draw.rectangle(battery_rect, fill=(255, 255, 255, 255), outline=(25, 118, 210, 255), width=4)
    
    # Draw battery terminal
    terminal_rect = (352, 220, 376, 260)
    draw.rectangle(terminal_rect, fill=(255, 255, 255, 255), outline=(25, 118, 210, 255), width=4)
    
    # Draw battery charge level (green, 80% full)
    charge_rect = (176, 196, 320, 284)
    draw.rectangle(charge_rect, fill=(76, 175, 80, 255))
    
    # Draw lightning bolt (simplified)
    lightning_points = [(280, 120), (240, 160), (260, 160), (230, 200), (270, 160), (250, 160)]
    draw.polygon(lightning_points, fill=(255, 193, 7, 255), outline=(245, 124, 0, 255))
    
    # Draw optimization arrows (simplified circles)
    draw.ellipse((190, 320, 210, 340), outline=(76, 175, 80, 255), width=6)
    draw.ellipse((302, 320, 322, 340), outline=(76, 175, 80, 255), width=6)
    
    # Add "NOAH" text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    text = "NOAH"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (512 - text_width) // 2
    y = 420 - text_height // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as PNG
    img.save('icon.png', 'PNG')
    print("Icon created successfully as icon.png")

if __name__ == "__main__":
    create_icon()