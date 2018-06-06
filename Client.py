from Winreg import *
import sys

ENUM_USB = 'SYSTEM\CurrentControlSet\Enum\USB'
ENUM_RUN = 'Software\Microsoft\Windows\CurrentVersion\Run'
ENUM_RUN_ONCE = 'Software\Microsoft\Windows\CurrentVersion\RunOnce'
BASELINE_RUN = r'C:\Users\Owner\PycharmProjects\DeltaX\Reg_Run.txt'
BASELINE_USB = r'C:\Users\Owner\PycharmProjects\DeltaX\Reg_USB.txt'
BASELINE_RUN_ONCE = r'C:\Users\Owner\PycharmProjects\DeltaX\Reg_RunOnce.txt'
BASELINE_CONFIG = r'C:\Users\Owner\PycharmProjects\DeltaX\Config.txt'

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "quickscan":
            quickScan(BASELINE_RUN, ENUM_RUN)
            raw_input()
        elif sys.argv[1] == "regedit":
            print "Registry Editor opened"
            raw_input("... and what do you think to do???")
    else:
        menu()
        # baseline_run(BASELINE_RUN_ONCE, ENUM_RUN_ONCE)
        # baseline_usb(BASELINE_USB, ENUM_USB)
 
def quickScan(baseline, key):
    current_lst, = registryValue(key)[0]
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
            return 1
        else:
            return 0
    else:
        print 'No entries'

def menu():
    lst_options = ['Analyze Connected Devices','Run Key Delta']
    for i in range(len(lst_options)):
        print i+1, ' -> ', lst_options[i]
    option = raw_input('Please select action: ')
    if option == '1':
        printOptionOne(lst_options[0])
    elif option == '2':
        current_lst, key = getKey(lst_options[1])
        baseline = getBaseline(BASELINE_CONFIG)
        doCompare(baseline, current_lst, key)
    else:
        print 'Error: Invalid Selection'

# Get key and current list of devices or value of key: the user must choose key from the list of keys
def getKey(option):
    current_lst = []
    print '\n***', option, '***'
    lst_keys = ['usb', 'run', 'run once']
    for i in range(len(lst_keys)):
        print i+1, ' -> ', lst_keys[i]
    selected_key = raw_input('\nPlease select key: ')
    key = ""
    if selected_key == '1':
        key = ENUM_USB
        current_lst, num = registryKey(key)
    elif selected_key == '2':
        key = ENUM_RUN
        current_lst, num = registryValue(key)
    elif selected_key == '3':
        key = ENUM_RUN_ONCE
        current_lst, num = registryValue(key)
    return current_lst, key

# Get baseline from Config.txt file: the user must choose baseline
def getBaseline(baseline):
    with open (baseline) as file:
        content = file.read().split('\n')
        for i in range(len(content)):
            print '\t', i+1, "->", content[i]
    selected_baseline = int(raw_input('\nPlease select baseline: '))
    baseline = content[selected_baseline-1]
    return baseline

# Compare between baseline and current list of devices or value of key
def doCompare(baseline, current_lst, key):
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

# Printing of option number one - 'Analyze Connected Devices'
def printOptionOne(option):
    print '\n***', option, '***\n'
    print 'Devices list:'
    printListDevices()
    print 'Total of', registryKey(ENUM_USB)[1], 'devices were connected to this host.'
    print '\nVendors list:'
    list_VID(registryKey(ENUM_USB)[0])

if __name__ == '__main__':
    main()