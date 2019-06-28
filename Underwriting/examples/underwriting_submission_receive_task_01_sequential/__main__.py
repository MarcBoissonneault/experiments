# __main__.py
# Marc Boissonneault, 2019-05-31
# Copyright (c) 2019 Element AI. All rights reserved.

from __future__ import annotations

import shutil
import time
from pathlib import Path

from . import normal_sequential_implementation

_examples_path = Path(__file__).parent.parent
_data_path = _examples_path / "Data"
_output_path = _examples_path / "output" / "01_sequential"

if _output_path.exists():
    shutil.rmtree(_output_path)

s = time.perf_counter()

submissions_zip_file_path = _data_path / "submissions"
zips = [
    item
    for item in submissions_zip_file_path.iterdir()
    if item.is_file() and item.suffix == ".zip"
]

for submission in zips:
    output_path = _output_path / submission.name

    normal_sequential_implementation.execute_task(
        submission_zip_path=submission, output_dir=output_path
    )

elapsed = time.perf_counter() - s
print(f"{__file__} executed in {elapsed:0.2f} seconds.")
