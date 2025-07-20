# QR Code Generator for wdrive
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont


def generate_qr_code(url, filename="qr_code.png"):
    """Generate a QR code for the server URL."""
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to QR code
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Create a larger image with text
        img_width = 400
        img_height = 500
        final_img = Image.new('RGB', (img_width, img_height), 'white')
        
        # Resize QR code to fit
        qr_img = qr_img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # Paste QR code onto final image
        final_img.paste(qr_img, (50, 50))
        
        # Add text below QR code
        draw = ImageDraw.Draw(final_img)
        
        try:
            # Try to use a nicer font
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except (IOError, OSError):
            # Fallback to default font
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add title
        title = "wdrive Server"
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((img_width - title_width) // 2, 370), title, fill="black", font=font_large)
        
        # Add URL
        url_bbox = draw.textbbox((0, 0), url, font=font_small)
        url_width = url_bbox[2] - url_bbox[0]
        draw.text(((img_width - url_width) // 2, 410), url, fill="blue", font=font_small)
        
        # Add instructions
        instructions = "Scan with your phone camera"
        inst_bbox = draw.textbbox((0, 0), instructions, font=font_small)
        inst_width = inst_bbox[2] - inst_bbox[0]
        draw.text(((img_width - inst_width) // 2, 440), instructions, fill="gray", font=font_small)
        
        # Save the image
        final_img.save(filename)
        
        print(f"📱 QR code saved as {filename}")
        print(f"🔗 Scan to access: {url}")
        
        return filename
        
    except ImportError:
        print("❌ QR code generation requires 'qrcode' and 'Pillow' packages")
        return None
    except Exception as e:
        print(f"❌ Error generating QR code: {str(e)}")
        return None


def generate_simple_qr_code(url, filename="qr_code_simple.png"):
    """Generate a simple QR code without fancy formatting."""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        
        return filename
    except Exception as e:
        print(f"❌ Error generating simple QR code: {str(e)}")
        return None


