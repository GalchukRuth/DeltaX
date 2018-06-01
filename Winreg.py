from _winreg import *
import re
from datetime import *

ENUM_USB = 'SYSTEM\CurrentControlSet\Enum\USB'
ENUM_RUN = 'Software\Microsoft\Windows\CurrentVersion\Run'

# Extracting devices from key by handle
def registryKey(key):
    handle = OpenKey(HKEY_LOCAL_MACHINE, key)
    lst_devices = []
    num_devices = 0
    try:
        while True:
            lst_devices.append(EnumKey(handle, num_devices))
            num_devices += 1
    except WindowsError:
        pass
    return lst_devices, num_devices

#Extracting value from key by handle
def registryValue(key):
    handle = OpenKey(HKEY_LOCAL_MACHINE, key)
    lst = []
    num_values = 0
    try:
        while True:
            lst.append(EnumValue(handle, num_values)[1])
            num_values += 1
    except WindowsError:
        pass
    return lst, num_values

# Read the baseline
def readFromFile(baseline):
    with open(baseline, 'r') as file:
        content = file.read()
    return content

# Compare the entries (value data)
def compare(baseline, current_lst, key):
    baseline_lst = set((readFromFile(baseline).split('\n')[:-1]))
    current_set = set(current_lst)
    new_lst = list(current_set.difference(baseline_lst))
    exist_lst = list(current_set.intersection(baseline_lst))
    handle = OpenKey(HKEY_LOCAL_MACHINE, key)
    return exist_lst, new_lst, calculateDeltaTime(handle)

# Updating baseline
def update(baseline, new_lst):
    for i in new_lst:
        with open(baseline, 'a') as file:
            file.writelines(i + '\n')

# Printing list devices with time delta
def printListDevices():
    lst = registryKey(ENUM_USB)[0]
    for i in lst:
        handle = OpenKey(HKEY_LOCAL_MACHINE, ENUM_USB + "\\" + i)
        time = calculateDeltaTime(handle)
        print '\t', i, '-- time -> ', time

# Extracting vendor from lst_devices to vendors_dic and printing list vendors
def list_VID(lst):
    regex = '(?<=VID_|Vid_)[\w]{4}'
    vendors_dic = {}
    print lst
    for i in lst:
        vid = re.findall(regex, i)
        for v in vid:
            if v in vendors_dic.keys():
                vendors_dic[v] += 1
            else:
                vendors_dic[v] = 1
            print '\t', v, ':', vendors_dic[v], 'devices'

# Calculating the last changed time of the USB keys list
def lst_time(lst):
    delta_lst = []
    for i in lst:
        handle = OpenKey(HKEY_LOCAL_MACHINE, ENUM_USB + "\\" + i)
        delta_lst.append(str(calculateDeltaTime(handle)))
    return delta_lst

# Calculating the last changed time of the USB key
def calculateDeltaTime(handle):
    epoch = datetime(1601, 1, 1)
    reg_time = QueryInfoKey(handle)[2]
    calculated = epoch + timedelta(microseconds=reg_time / 10)
    delta_time = datetime.now() - calculated
    return delta_time

# Create new baseline by value
def baseline_run(baseline, key):
    lst = []
    try:
        num = 0
        while True:
            lst.append(EnumValue(OpenKey(HKEY_LOCAL_MACHINE, key), num))
            num += 1
    except WindowsError:
        pass
    with open(baseline, 'a') as file:
        for i in lst:
            file.writelines(i[1] + '\n')

# Create new baseline by key
def baseline_usb(baseline, key):
    lst = []
    try:
        num = 0
        while True:
            lst.append(EnumKey(OpenKey(HKEY_LOCAL_MACHINE, key), num))
            num += 1
    except WindowsError:
        pass
    with open(baseline, 'a') as file:
        for i in lst:
            file.writelines(i + '\n')