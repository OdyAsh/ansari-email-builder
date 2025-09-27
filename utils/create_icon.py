#!/usr/bin/env python3
"""
Simple script to create an email-themed icon for the Ansari Email Builder
"""

from PIL import Image, ImageDraw
import os

def create_email_icon():
    """Create a simple email icon with Ansari colors"""

    # Icon size
    size = 64

    # Create new image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background color (the requested teal color)
    bg_color = '#08786b'

    # Draw rounded rectangle background
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=8, fill=bg_color)

    # Email envelope
    envelope_margin = 8
    envelope_height = 32
    envelope_y = (size - envelope_height) // 2

    # Main envelope body
    draw.rounded_rectangle([
        envelope_margin,
        envelope_y,
        size - envelope_margin,
        envelope_y + envelope_height
    ], radius=2, fill='#0a9988', outline='white', width=1)

    # Email flap (triangle)
    flap_points = [
        (envelope_margin, envelope_y),
        (size // 2, envelope_y + 16),
        (size - envelope_margin, envelope_y)
    ]
    draw.polygon(flap_points, fill='#0cb5a3', outline='white')

    # Simple star pattern in center (inspired by Ansari logo)
    center_x, center_y = size // 2, size // 2
    star_size = 8

    # Create 8-pointed star
    star_points = []
    import math
    for i in range(8):
        angle = i * math.pi / 4
        if i % 2 == 0:
            # Outer points
            x = center_x + star_size * math.cos(angle)
            y = center_y + star_size * math.sin(angle)
        else:
            # Inner points
            x = center_x + (star_size * 0.5) * math.cos(angle)
            y = center_y + (star_size * 0.5) * math.sin(angle)
        star_points.extend([x, y])

    draw.polygon(star_points, fill='white', outline=bg_color)

    # Center dot
    draw.ellipse([center_x-2, center_y-2, center_x+2, center_y+2], fill='white')

    return img

if __name__ == "__main__":
    # Create the icon
    icon = create_email_icon()

    # Save as PNG
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    icon_path = os.path.join(assets_dir, "email_icon.png")
    icon.save(icon_path, "PNG")

    # Also save as ICO for favicon
    ico_path = os.path.join(assets_dir, "email_icon.ico")
    icon.save(ico_path, "ICO")

    print(f"Icon saved as: {icon_path}")
    print(f"Favicon saved as: {ico_path}")
    print("You can now use these icons in your Streamlit app!")