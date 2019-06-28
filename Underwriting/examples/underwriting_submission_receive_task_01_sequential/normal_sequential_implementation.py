# normal_sequential_implementation.py
# Marc Boissonneault, 2019-05-31
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterator
from zipfile import ZipFile

from PIL import Image
from eai.image_loader import ImageLoader

_file_extractor_cli_path = Path(__file__).parent.parent / "utils/file-extractor-cli.jar"


def execute_task(submission_zip_path: str, output_dir: str) -> None:
    submission_zip_file_path = Path(submission_zip_path)
    output_path = Path(output_dir) / submission_zip_file_path.name

    unzipped_data_path = output_path / f"Step-01-unzip"
    os.makedirs(unzipped_data_path, exist_ok=True)
    unzip(submission_zip_file_path, unzipped_data_path)

    msg_extract_path = output_path / "Step-02-extract-msg-if-any-msg"
    shutil.copytree(unzipped_data_path, msg_extract_path)
    extract_msg_files(msg_extract_path)

    converted_data_path = output_path / "Step-03-convert-pdf-files"
    shutil.copytree(msg_extract_path, converted_data_path)
    convert_pdfs_to_pngs(converted_data_path)


def unzip(submission_zip_file_path, unzipped_data_path):
    with open(submission_zip_file_path, "rb+") as zip_file:
        zip_handle = ZipFile(zip_file)

        for inner_file_name in [x for x in zip_handle.namelist() if not x.startswith("_")]:
            file_path = unzipped_data_path / inner_file_name
            data = zip_handle.read(inner_file_name)

            with open(file_path, "wb") as doc:
                doc.write(data)


def extract_msg_files(path):
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_stem, extension = os.path.splitext(file_name)
            if "msg" in extension:
                dest_folder = Path(dir_path) / (file_stem + "_msg")
                os.makedirs(dest_folder, exist_ok=True)

                file_path = Path(dir_path) / file_name
                proc = subprocess.Popen(
                    [
                        "java",
                        "-jar",
                        str(_file_extractor_cli_path),
                        "--split",
                        f"--filename={file_path}",
                        f"--out={dest_folder}",
                    ]
                )
                proc.communicate()
                proc.wait()
                os.remove(file_path)


def convert_pdfs_to_pngs(path):
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            file_stem, extension = os.path.splitext(file_name)
            if "pdf" in extension:
                file_path = Path(dir_path) / file_name
                image_loader = ImageLoader()
                image_iterator: Iterator[Image] = image_loader.from_path(file_path)
                for index, image in enumerate(image_iterator):
                    image.save(str(Path(dir_path) / f"{file_stem}_{index + 1}.png"))
                os.remove(file_path)
