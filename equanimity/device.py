import os
import subprocess

from datetime import datetime

import config

from output import print_header
from utils import (
    checksum_directory,
    get_directory_size,
    load_yaml,
    print_in_color,
    readable_duration,
)


class Device(object):

    def __init__(self, instance):
        self._location = instance['location']
        self.name = instance['name']
        self.path = instance['path']

        try:
            self.optional = instance['optional']
        except KeyError:
            self.optional = []

        try:
            self.exclude = instance['exclude']
        except KeyError:
            self.exclude = []

        self.log_path = os.path.join(config.LOG_DIR, '%s.log' % self.name)

    @property
    def location(self):
        """
        Gets the device's location.
        """
        return self._location

    def directory_age(self, directory):
        """
        Returns the age in seconds of the backup of the given directory on the
        device.
        """
        # Find the date this copy of the directory was made. Read each log
        # entry, newest first, until one is found which records a copy
        # having been made. If the copy is verified, `dir_date` is its age.
        # If the copy is not verified, `dir_date` is None because it is faulty.
        device_log = load_yaml(self.log_path)
        dir_date = None
        for entry in reversed(device_log):
            try:
                if entry['directories'][directory['name']]['copied']:
                    try:
                        if entry['directories'][directory['name']]['verified']:
                            dir_date = entry['date']
                        else:
                            dir_date = None
                        break
                    except KeyError:
                        break
            except KeyError:
                pass

        # Calculate the time in seconds since the copy was made.
        if dir_date:
            elapsed_time = datetime.now() - \
                datetime.strptime(dir_date, '%d-%b-%Y %H:%M:%S')
            return elapsed_time.total_seconds()
        else:
            return None

    def has_space(self, directory):
        """
        Returns a boolean indicating whether the device has enough space for
        the directory.
        """
        target_dir_size = get_directory_size(directory.target)
        source_dir_size = get_directory_size(directory.source)
        statvfs = os.statvfs(self.path)
        target_spare_space = statvfs.f_frsize * statvfs.f_bavail

        return (target_spare_space + target_dir_size) > source_dir_size

    def print_directory_queue(self):
        """
        Prints the directories to be backed up, and the directories to be
        skipped.
        """
        print '\n\nThese directories will be backed up:'

        for directory_name in self.directory_queue:
            print_in_color('* %s' % directory_name, 'green')

        print '\nThese directories will NOT be backed up:'

        for directory in config.DIRECTORIES:
            if directory['name'] not in self.directory_queue:
                print_in_color('* %s' % directory['name'], 'red')

    def print_summary(self):
        """
        Prints a table with the age of the copy of each directory on the
        device.
        """
        # Print the table heading row.
        print '+{:-<60}+'.format('')
        print '|',
        decorated_device_name = '<<< %s >>>' % self.name
        print_in_color(
            '{:^58}'.format(decorated_device_name),
            'bold',
            line_feed=False
        )
        print '|'

        # Print the column headings row.
        print '+{:-<24}+{:-<35}+'.format('', '')
        print '|{:^24}|{:^35}|'.format(
            '~ Directory ~',
            '~ Approximate backup age ~'
        )
        print '+{:-<24}+{:-<35}+'.format('', '')

        # Print each directory's row.
        for directory in config.DIRECTORIES:
            print '| {:<23}|'.format(directory['name']),
            elapsed_seconds = self.directory_age(directory)
            if elapsed_seconds:
                raw_msg = readable_duration(elapsed_seconds)
                msg = '{:<33}'.format(raw_msg)
                if elapsed_seconds > (60 * 60 * 24 * 3):
                    print_in_color(msg, 'red', line_feed=False)
                elif elapsed_seconds > (60 * 60 * 24 * 1):
                    print_in_color(msg, 'amber', line_feed=False)
                else:
                    print_in_color(msg, 'green', line_feed=False)
            # If there is no record of a verified copy, the directory doesn't
            # exist on this device so enter a dash rather than an age.
            else:
                print '{:<33}'.format('-'),
            print '|'
            print '+{:-<24}+{:-<35}+'.format('', '')

        # Add a blank line after the table.
        print '\n'

    def queue_directories(self):
        """
        Generates a list of the directories selected for backing up.
        """
        self.directory_queue = []

        for directory in config.DIRECTORIES:
            # Determine whether this device is allowed to back up this
            # directory.
            try:
                if directory['name'] in self.exclude:
                    has_permission = False
                else:
                    has_permission = True
            except KeyError:
                # A KeyError means `device` has no `exclude` list, so this
                # directory can't be excluded.
                has_permission = True

            # If this device is allowed to back up which directory, ask
            # the user for confirmation if necessary.
            if has_permission:
                try:
                    # If backing up this directory is optional, ask for user
                    # confirmation.
                    if directory['name'] in self.optional:
                        resp = raw_input(
                            '%s \'%s\'? (y/n): ' % (
                                'Should this backup event include',
                                directory['name']
                            )
                        )
                        if resp.lower() in ['y', 'yes']:
                            self.directory_queue.append(directory['name'])
                    else:
                        # If it's not optional, back it up.
                        self.directory_queue.append(directory['name'])
                except KeyError:
                    # A KeyError means `device` has no `optional` list, so this
                    # directory can't be optional.
                    self.directory_queue.append(directory['name'])

        return self.directory_queue

    def sync_logs_and_config(self):
        """
        Copies all logs and config files to the device and verifies that the
        copy was successful.
        """
        source_dir = config.BASE_PATH
        target_dir = os.path.join(self.path, '.equanimity')

        print_header('Syncing logs to backup device')

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        rsync_cmd = 'rsync -a --delete %s/ %s' % (source_dir, target_dir)
        subprocess.call(rsync_cmd, shell=True)

        if checksum_directory(source_dir) == checksum_directory(target_dir):
            print 'Logs synced successfully.'
        else:
            print_in_color('Logs NOT SYNCED.', 'red')
