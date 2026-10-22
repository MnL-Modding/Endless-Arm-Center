import struct
from io import BytesIO

import ndspy.rom
from mnllib.bis import FEventScriptManager

from endless_arm_center.constants import *
from endless_arm_center.mnlscript_misc import arm_center_endless

def main():
    path = "BISROM.nds"
    new_path = "BISMOD.nds"

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
    FEvent_temp.seek(0)
    rom.setFileByName('FEvent/FEvent.dat', FEvent_temp.read())

    overlay_3_temp = BytesIO(overlay_3.data)
    fevent_manager.save_overlay3(overlay_3_temp)
    overlay_3_temp.seek(0)
    overlay_3.data = overlay_3_temp.read()
    rom.files[overlays[3].fileID] = overlay_3.save(compress = True)

    rom.saveToFile(new_path)