import argparse
import os
from base64 import b64encode
import json

import requests

# cluster_url = "http://192.168.128.226"
cluster_url = "http://entity-extraction.eai-whiskey-bear-staging.svc.borgy-k8s.elementai.lan"
# port = 9000
port = 80

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--url", type=str, default=cluster_url)
    parser.add_argument("--port", type=int, default=port)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    with open(args.filename, "rb") as fp:
        res = requests.post(
            f"{args.url}:{args.port}/v1/predict",
            json={"document": b64encode(fp.read()).decode(), "class": "OAF1-page3"},
            timeout=600,
        )

    res.raise_for_status()
    result = res.json()
    result_as_str = json.dumps(result, indent=4, sort_keys=True)
    print(result_as_str)

    os.system(f"echo '%s' | pbcopy" % result_as_str)
    print("*******************************************************")
    print("JSON Result copied to clipboard.")
    print("*******************************************************")
