import os
import sys

from services.vision_engine import recognize_students_from_image

def main():
    img_path = r"../전술대회 예시.png"
    with open(img_path, "rb") as f:
        res = recognize_students_from_image(f.read())
        print(res)

if __name__ == "__main__":
    main()
