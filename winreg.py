from _winreg import *
import re
from datetime import *

ENUM_USB = 'SYSTEM\CurrentControlSet\Enum\USB'
ENUM_RUN = 'Software\Microsoft\Windows\CurrentVersion\Run'
BASELINE_RUN = r'C:\Users\Owner\PycharmProjects\DeltaX\reg_run'
BASELINE_USB = r'C:\Users\Owner\PycharmProjects\DeltaX\reg_usb'

def main():
    lst = registryKey(ENUM_USB)[0]
 #   print lst
#    printListDevices()
    list_VID(lst)
 #   menu()
 #   baseline_run(BASELINE_RUN, ENUM_RUN)
  #  compare(BASELINE_RUN, current_lst, ENUM_RUN)
 #   baseline_usb(BASELINE_USB, ENUM_USB)

def menu():
    lst_options = ['Analyze Connected Devices','Run Key Delta']
    for i in range(len(lst_options)):
        print i+1, ' -> ', lst_options[i]
    option = raw_input('Please select action: ')
    if option == '1':
        print '\n***', lst_options[0], '***\n'
        print 'Devices list:'
        printListDevices()
        print 'Total of', registryKey(ENUM_USB)[1], 'devices were connected to this host.'
        print '\nVendors list:'
        list_VID(registryKey(ENUM_USB)[0])
    elif option == '2':
    # key
        current_lst = []
        print '\n***', lst_options[1], '***'
        lst_keys = ['usb', 'run']
        for i in range(len(lst_keys)):
            print i+1, ' -> ', lst_keys[i]
        key = raw_input('Please select key: ')
        if key == '1':
            key = ENUM_USB
            current_lst, time = registryKey(key)
        elif key == '2':
            key = ENUM_RUN
            current_lst, time = registryValue(key)
    # baseline
        lst_baselines = ['reg_usb.txt', 'reg_run.txt']
        for i in range(len(lst_baselines)):
            print i+1, ' -> ', lst_baselines[i]
        baseline = raw_input('Please select baseline: ')
        if baseline == '1':
            baseline = BASELINE_USB
        elif baseline == '2':
            baseline = BASELINE_RUN
    #compare
        exist_list, new_lst, delta_time = compare(baseline, current_lst, key)
        for i in exist_list:
            print '\texist -> ', i
        for i in new_lst:
            print '\tnew -> ', i
        print 'Time changed -> ', delta_time
        baseline_lst = set((readFromFile(baseline).split('\n')[:-1]))
        if (set(current_lst).difference(baseline_lst)):
            action = raw_input('Do you want append to baseline new value? [y / n] ')
            if action == 'y':
                update(baseline, new_lst)
                print '\n', baseline, '-> updated'
            else:
                pass
        else:
            print 'No entries'
    else:
        print 'Error: Invalid Selection'

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

if __name__ == '__main__':
    main()
