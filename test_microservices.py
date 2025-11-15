import requests
import base64

FLASK_URL = "http://localhost:5001"
DJANGO_URL = "http://127.0.0.1:8000/api/files/upload/"
TEST_IMAGE = "cat.png"

def encode_image_base64(path):
    # Open the file in binary mode (read as bytes)
    with open(path, "rb") as file:
        image_bytes = file.read()

    # Convert bytes to base64 string
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    return base64_string

def test_flask_upload():
    print("\n=== Flask Direct Upload ===")
    image_data = encode_image_base64(TEST_IMAGE)
    payload = {
        "images": [{"filename": TEST_IMAGE, "image_data": image_data}]
    }

    try:
        res = requests.post(f"{FLASK_URL}/upload", json=payload)
        print("Status:", res.status_code)
        print("Response:", res.json())
    except Exception as e:
        print("Flask upload failed:", e)

def test_flask_get():
    print("\n=== Flask Get Image ===")
    payload = {"filenames": [TEST_IMAGE]}

    try:
        res = requests.post(f"{FLASK_URL}/get", json=payload)
        print("Status:", res.status_code)
        data = res.json()
        for img in data.get("images", []):
            print(f"Retrieved: {img['filename']} ({len(img['image_data'])} base64 chars)")
    except Exception as e:
        print("Flask get failed:", e)

def test_django_upload():
    print("\n=== Django Upload (via Flask) ===")
    try:
        with open(TEST_IMAGE, "rb") as f:
            files = {'file': (f.name, f, 'image/png')}
            data = {'description': 'Test from Django'}

            res = requests.post(DJANGO_URL, files=files, data=data)
            print("Status:", res.status_code)
            try:
                print("Response:", res.json())
            except Exception:
                print("Raw response:", res.text)
    except Exception as e:
        print("Django upload failed:", e)

if __name__ == "__main__":
    test_flask_upload()
    test_flask_get()
    test_django_upload()