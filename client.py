from winreg import *

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
    baseline_run(BASELINE_RUN, ENUM_RUN)
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

if __name__ == '__main__':
    main()