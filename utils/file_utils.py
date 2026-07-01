from pathlib import Path
import shutil
from datetime import datetime


def archive_file(file_path):

    archive = Path("data/archive")
    archive.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destination = archive / f"{timestamp}_{Path(file_path).name}"

    shutil.copy(file_path, destination)

    print("File Archived")