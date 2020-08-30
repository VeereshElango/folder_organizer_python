#! /usr/bin/env python3
import sys
import os
sys.path.insert(0, os.getcwd())

from pathlib import Path
import shutil
import logging


logging.basicConfig(filename='folder_organizer.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

from folder_organizer.extensions import extension_paths


def rename_file(source: Path, destination_path: Path):
    """
    Helper function that renames file to reflect new path. If a file of the same
    name already exists in the destination folder, the file name is numbered and
    incremented until the filename is unique (prevents overwriting files).

    :param Path source: source of file to be moved
    :param Path destination_path: path to destination directory
    """
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


def handler(src_path, destination_path):
    try:
        logger.info(f"Folder organzing handler initiate with {src_path} & {destination_path}")
        for child in src_path.iterdir():
            # skips directories and non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = destination_root / extension_paths[child.suffix.lower()]
                destination_path.mkdir(parents=True, exist_ok=True)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)
                logger.info(f"Moved {child} to {destination_path}")
            else:                
                logger.debug(f"Skipped file {child}")
    except Exception as e:
        logger.exception("Exception")


if __name__ == '__main__':
    watch_path = Path.home() / 'Downloads'
    destination_root = Path.home() / 'Downloads/holder of things'
    handler(src_path=watch_path, destination_path=destination_root)

