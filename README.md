DeltaX project by Ruth Galchuk
============================
A customized Windows Security python tool. Tracks changes as indication of compromise.

Files
-----
- Client.py -   presents a menu of analyzing options: "Analyze Connected Devices", "Run Key Delta".
- Winreg.py -
- Reg_Run.txt - a baseline file for the Run key.
- Reg_USB.txt - a baseline file for the USB key.
- Config.txt - contain the list of registry keys that should be scanned for deltas.

Instructions
------------
1.	Write a new python script that presents a menu of analyzing options.
- "Analyze Connected Devices" will go through the relevant registry key (ENUM) and will return::
    a.	A count of total connected devices.
    b.	A list of the devices names with calculating the last changed time of the USB key.
    c.	A count of the devices by their VID (dictionary).
- "Run Key Delta" contains:
	/Reg
	/Scheduled
	/Permissions
    1.	Calculate the last changed time of the USB key and write the results to the file Config.txt.
    2.	Under Reg create a new text file called Run.txt - a baseline file for the Run key.
    3.	Create a new function that can read the baseline file into a list.
    4.	Create a new function that can update the baseline with a new relevant list.
    5.	Create a function that calculated the delta between the file data and the Registry data.
    The function should show which values are new,
    and ask the user whether to update the baseline with new data or not.
    6.	In your Delta X folder, under the Registry folder, create a file named "config.txt".
    7.	This file should contain the list of registry keys that should be scanned for deltas.
    8.	Every time a user runs Delta X, it should be asked to select a key, and a path to save the baseline.