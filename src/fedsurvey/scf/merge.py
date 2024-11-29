"""Module for merging SCF survey data files."""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Callable

import numpy as np
import pandas as pd

from fedsurvey.config import CHUNK_SIZE, DATA_DIR, MAX_WORKERS
from fedsurvey.models import SCFRecord

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class MergeError(Exception):
    """Custom exception for merge-related errors."""


def process_file(
    data_file: Path,
    read_func: Callable[[str], pd.DataFrame],
) -> pd.DataFrame | None:
    """Process a single SCF data file.

    Args:
    ----
        data_file: Path to the data file
        read_func: Function to read the data file

    Returns:
    -------
        Processed DataFrame or None if processing fails

    """
    try:
        logger.info(f"Processing {data_file.name}")
        df = read_func(str(data_file)).assign(year=data_file.stem[-4:])

        # Validate data
        df_dict = df.to_dict("records")
        validated_records = [SCFRecord(**record).dict() for record in df_dict]
        return pd.DataFrame(validated_records)

    except ValueError as e:
        logger.warning(f"ValueError processing {data_file.name}: {e}")
        try:
            return read_func(str(data_file), convert_categoricals=False).assign(
                year=data_file.stem[-4:],
            )
        except Exception as e:
            logger.exception(f"Failed to process {data_file.name}: {e}")
            return None
    except Exception as e:
        logger.exception(f"Unexpected error processing {data_file.name}: {e}")
        return None


def merge_files(
    from_format: str = "stata",
    to_format: str = "stata",
    input_dir: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Merge SCF data files from multiple years.

    Args:
    ----
        from_format: Input file format
        to_format: Output file format
        input_dir: Directory containing input files
        output_dir: Directory for output file

    Returns:
    -------
        Path to the merged file

    """
    input_dir = input_dir or DATA_DIR
    output_dir = output_dir or DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    data_files = sorted(input_dir.glob(f"*{from_format}*"))

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(process_file, data_file, pd.read_stata)
            for data_file in data_files
        ]
        dfs = [f.result() for f in futures if f.result() is not None]

    # Concatenate results
    merged_df = pd.concat(dfs, ignore_index=True)

    # Save in chunks
    output_path = output_dir / f"scf_merged.{to_format}"
    if to_format == "stata":
        merged_df.to_stata(output_path, write_index=False)
    elif to_format == "csv":
        for i, chunk in enumerate(
            np.array_split(merged_df, len(merged_df) // CHUNK_SIZE + 1),
        ):
            mode = "w" if i == 0 else "a"
            header = i == 0
            chunk.to_csv(output_path, mode=mode, header=header, index=False)

    return output_path


if __name__ == "__main__":
    merge_files()
