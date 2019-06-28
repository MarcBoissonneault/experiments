# convert.py
# Marc Boissonneault, 2019-04-24
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations

import argparse
import base64
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    with open(args.source_file, "rb") as source_file:
        data = source_file.read()

    b64_data = base64.b64encode(data)

    os.system("echo '%s' | pbcopy" % b64_data.decode())

    with open(args.source_file + ".b64", "w") as destination:
        destination.write(b64_data.decode())

    print("*******************************************************")
    print(f"{args.source_file} base64 encoded copied to clipboard.")
    print("*******************************************************")
