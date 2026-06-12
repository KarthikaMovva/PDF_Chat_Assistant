import uuid
import os

def save_file(file) -> str:
    filename = f"{uuid.uuid4()}.pdf"

    with open(filename, "wb") as f:
        f.write(file)

    return filename


def delete_file(filename: str):
    if os.path.exists(filename):
        os.remove(filename)