from PIL import Image
import pytesseract


def extract_text_from_image(image) -> str:
    """
    Extract text from image.

    :param image: image data.
    :returns text: string representation of the image.
    """
    try:
        image_data = Image.open(image)
        text = pytesseract.image_to_string(image_data)
        return text.strip()
    except Exception:
        raise ValueError("Image processing error.")
