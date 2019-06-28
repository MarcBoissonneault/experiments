# normal_sequential_implementation.py
# Marc Boissonneault, 2019-05-31
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path
from typing import Iterator
from zipfile import ZipFile

from PIL import Image
from eai.image_loader import ImageLoader

_file_extractor_cli_path = Path(__file__).parent.parent / "utils/file-extractor-cli.jar"


async def execute_async_task(submission_zip_path: str, output_dir: str) -> None:
    submission_zip_file_path = Path(submission_zip_path)
    output_path = Path(output_dir)

    unzipped_data_path = await _unzip(submission_zip_file_path, output_path)
    msg_extract_path = await _extract_msg(unzipped_data_path, output_path)
    await _convert_pdf_files(msg_extract_path, output_path)


async def _unzip(submission_zip_file_path, output_path):
    unzipped_data_path = output_path / f"Step-01-unzip"
    os.makedirs(unzipped_data_path, exist_ok=True)

    with open(submission_zip_file_path, "rb+") as zip_file:
        zip_handle = ZipFile(zip_file)

        for inner_file_name in [x for x in zip_handle.namelist() if not x.startswith("_")]:
            file_path = unzipped_data_path / inner_file_name
            data = zip_handle.read(inner_file_name)

            with open(file_path, "wb") as doc:
                doc.write(data)

    return unzipped_data_path


async def _extract_msg(unzipped_data_path, output_path):
    msg_extract_path = output_path / "Step-02-extract-msg-if-any-msg"
    shutil.copytree(unzipped_data_path, msg_extract_path)
    for dir_path, _, file_names in os.walk(msg_extract_path):
        for file_name in file_names:
            file_stem, extension = os.path.splitext(file_name)
            if "msg" in extension:
                dest_folder = Path(dir_path) / (file_stem + "_msg")
                os.makedirs(dest_folder, exist_ok=True)

                file_path = Path(dir_path) / file_name
                proc = await asyncio.create_subprocess_shell(
                    f'java -jar "{str(_file_extractor_cli_path)}" --split --filename="{file_path}" --out="{dest_folder}"'
                )

                await proc.communicate()
                os.remove(file_path)

    return msg_extract_path


async def _convert_pdf_files(msg_extract_path, output_path):
    converted_data_path = output_path / "Step-03-convert-pdf-files"
    shutil.copytree(msg_extract_path, converted_data_path)

    convert_tasks = []
    for dir_path, dir_names, file_names in os.walk(converted_data_path):
        for file_name in file_names:
            file_stem, extension = os.path.splitext(file_name)
            if "pdf" in extension:
                convert_tasks.append(_convert_pdf_file(dir_path, file_name))

    await asyncio.gather(*convert_tasks)


async def _convert_pdf_file(dir_path, file_name):
    file_stem, extension = os.path.splitext(file_name)
    if "pdf" in extension:
        file_path = Path(dir_path) / file_name
        image_loader = ImageLoader()
        image_iterator: Iterator[Image] = image_loader.from_path(file_path)
        for index, image in enumerate(image_iterator):
            image.save(str(Path(dir_path) / f"{file_stem}_{index+1}.png"))
        os.remove(file_path)
