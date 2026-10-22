from pathlib import Path

from PySide6 import QtCore, QtWidgets

SCRIPT_DIR = Path(__file__).parent
FILES_DIR = SCRIPT_DIR / 'files'

NDS_ROM_FILENAME_FILTER = "NDS ROMs (*.nds);;All Files (*)"

JP_REGION_CODE = ord("J")
TW_REGION_CODE = ord("C")
NA_REGION_CODE = ord("E")
EU_REGION_CODE = ord("P")
KR_REGION_CODE = ord("K")