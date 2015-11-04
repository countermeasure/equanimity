#!/usr/bin/env python

import config
from device import Device
from directory import Directory
from logging import (
    log,
    sync_logs,
    write_log_headers,
)
from output import (
    print_header,
    print_screen_header,
)
from reports import print_devices_comparison
from utils import (
    confirm_continue,
    print_in_color,
)


def backup_directories(directories_to_backup):
    """
    Backs up all the directories which have been selected for backup.
    """
    count = 1

    for d in config.DIRECTORIES:
        directory = Directory(d)

        if directory.name in directories_to_backup:
            print_header('Backing up directory %s of %s: %s' % (
                str(count),
                len(directories_to_backup),
                directory.name
            ))

            if device.has_space:
                directory.backup()
            else:
                print 'Not enough space on %s to update %s.' % (
                    device.name,
                    directory.name
                )
                log('    %s:' % directory.name)
                log('      copied: False')

            count += 1

        else:
            log('    %s:' % directory.name)
            log('      copied: False')

    # Add a blank line below this backup event's log event to seperate it
    # from the next one.
    log('')


if __name__ == "__main__":

    if config.DEVICE:
        device = Device(config.DEVICE)

        print_screen_header()

        device.print_summary()

        device.queue_directories()

        device.print_directory_queue()

        confirm_continue()

        write_log_headers()

        backup_directories(device.directory_queue)

        sync_logs()

        print_devices_comparison()

    else:
        print_in_color('\nNo backup device was found.\n', 'red')
