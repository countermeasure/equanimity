#!/usr/bin/env python

import os
import sys


CONFIG_DIRECTORY = os.path.expanduser('~/.equanimity')


# Create the configuration directory, or exit if it already exists.
if not os.path.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)
else:
    print '\nEquanimity has already been configured.'
    print '\nThis script will not run.\n'
    sys.exit()

# Create the config.yml file.
CONFIG_FILE_PATH = os.path.join(CONFIG_DIRECTORY, 'config.yml')
with open(CONFIG_FILE_PATH, 'w') as f:
    f.write('---\n')
    f.write('# Customise the two lines below, then remove this line.\n')
    f.write('computer_name: name_of_your_computer\n')
    f.write('media_path: /path/to/your/media/directory\n')

# Create the directories.yml file.
DIRECTORIES_FILE_PATH = os.path.join(CONFIG_DIRECTORY, 'directories.yml')
with open(DIRECTORIES_FILE_PATH, 'w') as f:
    f.write('---\n')
    f.write('# This file contains a YAML list of directories which\n')
    f.write('# Equanimity will back up.\n')
    f.write('#\n')
    f.write('# The format for each entry is:\n')
    f.write('#\n')
    f.write('# - name: Short description of the directory\n')
    f.write('#   path: /full/path/to/the/directory\n')
    f.write('#   type: [directory|virtual-machine]\n')
    f.write('#\n')
    f.write('# Here are two examples:\n')
    f.write('#\n')
    f.write('# - name: My Virtual Machine\n')
    f.write('#   path: /home/mycomputer/VMs/my_vm\n')
    f.write('#   type: virtual-machine\n')
    f.write('#\n')
    f.write('# - name: Desktop\n')
    f.write('#   path: /home/mycomputer/Desktop\n')
    f.write('#   type: directory\n')
    f.write('#\n')
    f.write('# Now add yours below.\n')
    f.write('#\n')

# Create the devices.yml file.
DEVICES_FILE_PATH = os.path.join(CONFIG_DIRECTORY, 'devices.yml')
with open(DEVICES_FILE_PATH, 'w') as f:
    f.write('---\n')
    f.write('# This file contains a YAML list of devices which\n')
    f.write('# Equanimity will back up to.\n')
    f.write('#\n')
    f.write('# The format for each device is:\n')
    f.write('#\n')
    f.write('# - name: Short description of the device\n')
    f.write('#   location: The place where you usually keep this device\n')
    f.write('#   path: /full/path/to/the/device\n')
    f.write('#   optional:\n')
    f.write('#   - a directory which will be backed up after prompting\n')
    f.write(
        '#   - another directory which will be backed up after prompting\n'
    )
    f.write('#   exclude:\n')
    f.write('#   - a directory which won\'t be backed up to this device\n')
    f.write(
        '#   - another directory which won\'t be backed up to this device\n'
    )
    f.write('#\n')
    f.write('# NOTE: The `optional` and `exclude` items are optional.\n')
    f.write('#\n')
    f.write('# Here are two examples:\n')
    f.write('#\n')
    f.write('#- name: Backup HDD 1\n')
    f.write('#  location: Office\n')
    f.write('#  path: /media/mycomputer/BackupHDD1\n')
    f.write('#  optional:\n')
    f.write('#    - Photos\n')
    f.write('#    - PersonalVM\n')
    f.write('#\n')
    f.write('#- name: Flash Drive Alpha\n')
    f.write('#  location: Desk drawer\n')
    f.write('#  path: /media/mycomputer/FlashDriveAlpha\n')
    f.write('#  exclude:\n')
    f.write('#    - Photos\n')
    f.write('#\n')
    f.write('# Now add yours below.\n')
    f.write('\n')

# Print a success message with instructions about what to do next.
print '\n***** Equanimity has been configured. *****\n'
print 'Configuration files are in %s.\n' % CONFIG_DIRECTORY
print 'You need to edit them before you start using Equanimity.\n'
print 'The config files themselves contain instructions on how you do that.\n'
