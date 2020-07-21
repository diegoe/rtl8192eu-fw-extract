# rtl8192eu-fw-extract
Extracts firmware from C sources for use in linux-firmware

## Purpose
This is a simple script to easily extract the `*.bin` files used by
`linux-firmware`, specificaly the `rtl8xxxu` driver when used with a
`rtl8192eu` chip.

## Backstory
This particular chip has been published under different brands, and it
seems that each brand has published a different version of the source
code of the out-of-tree driver.

The current in-kernel driver (`rtl8xxxu`) works fine with the card,
provided you have the necessary firmware in `/lib/firmware/rtlwifi`.
However, the current firmware in `linux-firmware` is version 19, from
2016:

```
rtlwifi: v19 firmware for rtl8192eu
This is v19 firmware for the rtl8192u. Support for this device is
currently under development and will be added to the rtl8xxxu driver.
This firmware occurs as data statements in Realtek vendor driver
rtl8192EU_linux_v4.3.1.1_11320.20140505

Signed-off-by: Jes Sorensen <Jes.Sorensen@redhat.com>
Signed-off-by: Kyle McMartin <kyle@kernel.org>
```
https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/commit/rtlwifi/rtl8192eu_nic.bin?id=91d5dd136153e0a199d7bf30fd03763d83586b73

At the time of writing this script, it seems like the latest firmware
version "on the wild" is version 35, from an unknown driver version.

## Requirements
* Python3
* The "official" `rtl8192eu` driver source code

## Where to get the out-of-tree driver

There are a bunch of repos in GitHub that provide a mirror of the
driver, currently I know of two up to date ones:

* https://github.com/clnhub/rtl8192eu-linux/
* https://github.com/Mange/rtl8192eu-linux-driver/

The one by `clnhub` works better on my particular copy of the chip. I
can't offer an explanation for that.

This script should be able to extract the firmware of any of those two
repos.

## Usage
Simply run this script from the root of the driver sources and you'll
get a bunch of `.bin` files created. Example:

```
$ python3 ../rtl8192eu-fw-extract/rtl-fw-extract.py
[BEGIN] Extracting: rtl8192eu_fw_ap.bin
[END] Extracted: rtl8192eu_fw_ap.bin
[BEGIN] Extracting: rtl8192eu_fw_nic.bin
[END] Extracted: rtl8192eu_fw_nic.bin
[BEGIN] Extracting: rtl8192eu_fw_nic_setupbox.bin
[END] Extracted: rtl8192eu_fw_nic_setupbox.bin
[BEGIN] Extracting: rtl8192eu_fw_wowlan.bin
[END] Extracted: rtl8192eu_fw_wowlan.bin

$ md5sum *.bin
df95e5c33e06765208edd4529e8ca6a2  rtl8192eu_fw_ap.bin
ed1fd62b6566a0fed44d46ba1b825a5b  rtl8192eu_fw_nic.bin
84fefbf044d10077758922e1ceda0b14  rtl8192eu_fw_nic_setupbox.bin
3558003e8cb24da617509e09b012a7ae  rtl8192eu_fw_wowlan.bin
```

Note that the above md5sums are simply provided as an example.

Next, just copy the file you need into `/lib/firmware/rtlwifi` and test
your new firmware with a `rmmod rtl8xxxu && modprobe rtl8xxxu`. Make
sure to match the existing filename, and make a backup:

```
$ cp -b rtl8192eu_fw_nic.bin /lib/firmware/rtlwifi/rtl8192eu_nic.bin
$ ls -la /lib/firmware/rtlwifi/rtl8192eu*
-rw-r--r-- 1 root root 32286 jul 21 00:05 /lib/firmware/rtlwifi/rtl8192eu_nic.bin
-rw-r--r-- 1 root root 31818 jul 15 03:41 /lib/firmware/rtlwifi/rtl8192eu_nic.bin~
-rw-r--r-- 1 root root 25878 jul 15 03:41 /lib/firmware/rtlwifi/rtl8192eu_wowlan.bin

$ md5sum /lib/firmware/rtlwifi/rtl8192eu*
ed1fd62b6566a0fed44d46ba1b825a5b  /lib/firmware/rtlwifi/rtl8192eu_nic.bin
c8d25646cbc9efdcb818fc95ad5836a9  /lib/firmware/rtlwifi/rtl8192eu_nic.bin~
28fdfa6f61508752970ced56e20ba9fa  /lib/firmware/rtlwifi/rtl8192eu_wowlan.bin
```

In the above example, I only replaced the `_nic.bin` file because it's
the only one I needed.
