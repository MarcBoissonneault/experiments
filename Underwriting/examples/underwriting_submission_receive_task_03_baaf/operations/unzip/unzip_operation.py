# unzip_operation.py
# Marc Boissonneault, 2019-06-03
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
from zipfile import ZipFile

from eai.ai_application_framework.sdk import Operation


def _unzip(zip_file_path: Path, output_path: Path) -> None:
    with open(str(zip_file_path), "rb+") as zip_file:
        zip_handle = ZipFile(zip_file)

        for inner_file_name in zip_handle.namelist():
            file_path = output_path / inner_file_name
            data = zip_handle.read(inner_file_name)

            with open(file_path, "wb") as doc:
                doc.write(data)


class UnzipOperation(Operation):
    def execute(self, context: Dict[str, Any]) -> Any:
        zip_file_path = Path(context.get("zip_file_path"))
        output_path = Path(context.get("output_path"))
        _unzip(zip_file_path, output_path)
