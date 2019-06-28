from __future__ import annotations

import argparse

from eai.image_loader import ImageLoader


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("destination")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    img = ImageLoader().from_path(args.filename)

    with open(args.destination, "wb") as dest:
        img.save(dest)
