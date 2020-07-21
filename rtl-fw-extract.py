# rtl8192eu-fw-extract - Extracts firmware from C sources for use in
# linux-firmware
#
# Copyright (C) 2020  Diego Escalante Urrelo <diegoe@gnome.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re


## Regular Expressions to match firmware file

# example: u8 array_mp_8192e_fw_ap[] = {
re_cvar = re.compile(".*_8192e_(\w*)")

# example: 0xE1, 0x92, 0x20, 0x00, 0x23, 0x00, 0x07, 0x00,
re_hexline = re.compile("0x(..)")


## Default firmware file
rtl_fw_file = "hal/rtl8192e/hal8192e_fw.c"


def get_firmware_name_from_cvar(rawstr):
    return "rtl8192eu_%s.bin" % re.match(re_cvar, rawstr)[1]

def get_bytearray_from_hexstr(hexstr):
    return bytearray.fromhex("".join(re.findall(re_hexline, hexstr)))


if __name__ == '__main__':
    with open(rtl_fw_file, "rt") as f:
        for line in f:
            if line.startswith('u8'):
                fw_name = get_firmware_name_from_cvar(line)
                print("[BEGIN] Extracting: %s" % fw_name)

                line = f.readline()
                with open(fw_name, "wb+") as w:
                    while line and not line.startswith('};'):
                        w.write(get_bytearray_from_hexstr(line))
                        line = f.readline()

                print("[END] Extracted: %s" % (fw_name))
