# Workaround for dynamic scope in Nuitka
if '__compiled__' in globals():
    _dynamicscope_test_variable = False

import os
import struct
import sys
from io import BytesIO

import ndspy.rom
from mnllib.bis import FEventScriptManager
from PySide6 import QtWidgets, QtGui

from endless_arm_center.constants import *
from endless_arm_center.mnlscript_misc import arm_center_endless

def main():
    app = QtWidgets.QApplication(sys.argv)

    if os.name == 'nt':
        app.setStyle('Fusion')

    window = QtWidgets.QMainWindow()
    window.setWindowIcon(QtGui.QIcon(str(FILES_DIR / 'ico_rando.ico')))

    path = import_rom(window)
    if path is None:
        return
    new_path = export_rom(window, path)
    if new_path is None:
        return

    QtWidgets.QMessageBox.information(
        None,
        #: Window title.
        window.tr("Patching ROM"),
        window.tr("Your ROM will now be patched. Please be patient, as this could take several moments."),
    )
    
    mod_files(path, new_path)

    QtWidgets.QMessageBox.information(
        None,
        #: Window title.
        window.tr("Complete"),
        window.tr("ROM has been patched successfully! The program will now exit."),
    )

def mod_files(path, new_path):
    # extracting files
    rom = ndspy.rom.NintendoDSRom.fromFile(path)

    valid = rom.idCode[3] == NA_REGION_CODE # or rom.idCode[3] == EU_REGION_CODE
    if not valid:
        return

    arm9 = BytesIO(ndspy.codeCompression.decompress(rom.arm9))
    overlays = rom.loadArm9Overlays()
    overlay_3 = overlays[3]
    overlay_6 = overlays[6]
    FEvent = rom.getFileByName('FEvent/FEvent.dat')

    # gather appropriate data
    fevent_manager = FEventScriptManager(None)
    fevent_manager.load_overlay3(BytesIO(overlay_3.data))
    fevent_manager.load_overlay6(BytesIO(overlay_6.data))
    fevent_manager.load_fevent(BytesIO(FEvent))

    arm9.seek(0x43D3C)
    test0, test1 = struct.unpack('<II', arm9.read(0x8))
    arm9.seek(-8, 1)
    font_file = arm9.read(test0 + test1)

    coin_string = [None] * 6
    for i in range(6):
        if fevent_manager.fevent_chunks[0x0128][2].text_tables[0x43 + i] is not None:
            coin_string[i] = fevent_manager.fevent_chunks[0x0128][2].text_tables[0x43 + i].entries[0x2D] # "You got 10 coins!"

    # mods go here
    arm_center_endless(
        fevent_manager,
        font_file,
        coin_string
    )

    # inserting files
    FEvent_temp = BytesIO()
    fevent_manager.save_fevent(FEvent_temp)
    rom.setFileByName('FEvent/FEvent.dat', FEvent_temp.getvalue())

    overlay_3_temp = BytesIO(overlay_3.data)
    fevent_manager.save_overlay3(overlay_3_temp)
    overlay_3.data = overlay_3_temp.getvalue()
    rom.files[overlays[3].fileID] = overlay_3.save(compress = True)

    rom.arm9OverlayTable = ndspy.code.saveOverlayTable(overlays)
    rom.saveToFile(new_path)

def import_rom(self):
    QtWidgets.QMessageBox.information(
        None,
        #: Window title.
        self.tr("Choose a ROM"),
        self.tr("Please choose a North American Bowser's Inside Story ROM to open."),
    )
    while True:
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent = None,
            #: Window title.
            caption = self.tr("Open ROM"),
            filter = NDS_ROM_FILENAME_FILTER,
        )

        if path == '':
            return None

        try:
            rom = ndspy.rom.NintendoDSRom.fromFile(path)
        except struct.error:
            QtWidgets.QMessageBox.warning(
                None,
                #: Window title.
                self.tr("Invalid File"),
                self.tr("The chosen file is not a Nintendo DS ROM file."),
            )
            continue

        if rom.name != b"MARIO&LUIGI3":
            QtWidgets.QMessageBox.warning(
                None,
                #: Window title.
                self.tr("Invalid ROM"),
                self.tr("The chosen ROM is not a valid Bowser's Inside Story ROM."),
            )
            continue

        valid = rom.idCode[3] == NA_REGION_CODE
        if valid:
            return path
        else:
            QtWidgets.QMessageBox.warning(
                None,
                #: Window title.
                self.tr("Invalid ROM"),
                self.tr("The chosen ROM is not from a valid region.\n\nOnly a North American Bowser's Inside Story ROM will work."),
            )

def export_rom(self, path):
    QtWidgets.QMessageBox.information(
        None,
        #: Window title.
        self.tr("Choose a New ROM"),
        self.tr("Please choose a file to save the modded ROM to."),
    )

    path, _ = QtWidgets.QFileDialog.getSaveFileName(
        None,
        #: Window title.
        self.tr("Export File"),
        path,
        filter = NDS_ROM_FILENAME_FILTER,
        )

    if path == '':
        return None
    
    return path