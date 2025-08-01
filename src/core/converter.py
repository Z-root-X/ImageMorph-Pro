# src/core/converter.py
import os

from PIL import Image, UnidentifiedImageError


def convert_image(input_path: str, output_format: str, output_path: str) -> tuple[bool, str]:
    """
    Converts an image from one format to another using Pillow.
    """
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with Image.open(input_path) as img:
            target_format_lower = output_format.lower()

            # Map 'JPG' to 'JPEG' for Pillow compatibility
            if target_format_lower == 'jpg':
                pillow_format = 'jpeg'
            else:
                pillow_format = target_format_lower

            # Crucial step for compatibility with formats that don't support alpha channels
            if img.mode in ['RGBA', 'P'] and pillow_format in ['jpeg', 'bmp']:
                img = img.convert('RGB')

            img.save(output_path, format=pillow_format)
        return True, f"Successfully converted '{os.path.basename(input_path)}' to '{os.path.basename(output_path)}'"
    except FileNotFoundError:
        return False, f"Error: Input file not found at '{input_path}'."
    except UnidentifiedImageError:
        return False, "Error: Cannot identify image file. It may be corrupt or an unsupported format."
    except KeyError:
        return False, f"Error: Unsupported output format '{output_format}'."
    except OSError as e:
        return False, f"Error: Failed to save the image. Reason: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred during conversion: {e}"
