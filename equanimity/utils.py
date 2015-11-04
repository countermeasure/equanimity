import hashlib
import os
import sys
import yaml


def checksum_directory(directory):
    """
    Calculates the checksum of an entire directory.
    Verifies:
        * directory tree structure, including sub-directory names
        * name and location of each file
        * contents of each file
    """
    sha256 = hashlib.sha256()

    chunk_size = 128 * sha256.block_size
    directory_size = get_directory_size(directory)
    progress = 0
    progress_percentage = None

    print 'Calculating checksum for: %s' % directory

    for root, dirs, files in os.walk(directory):
        dirs.sort()
        # Add directory name ot the checksum.
        sha256.update(str(dirs))

        for file_name in sorted(files):
            # Add file name to the checksum.
            sha256.update(file_name)
            file_path = os.path.join(root, file_name)

            with open(file_path, 'r') as f:
                while True:
                    buffer = f.read(chunk_size)
                    if not buffer:
                        break

                    sha256.update(buffer)
                    progress += chunk_size

                    # Only update the display when the progress percentage
                    # changes, otherwise the display can't keep up with all
                    # the updates and it lags the actual state of the script.
                    new_progress_percentage = '{:.0%}'.format(
                        float(progress)/float(directory_size)
                    )
                    if progress_percentage != new_progress_percentage:
                        progress_percentage = new_progress_percentage
                        sys.stdout.write(
                            '\rChecksum progress: {} of {}Mb'.format(
                                progress_percentage,
                                '{:,}'.format(directory_size / 1000000)
                            )
                        )
                        sys.stdout.flush()

    sys.stdout.flush()

    return sha256.hexdigest()


def color_text(message, color):
    """
    Wraps a string in tags for the specified color.
    Available color choices are 'red', 'amber' and 'green'.
    """
    if color == 'red':
        color_code = '\033[91m'
    elif color == 'amber':
        color_code = '\033[93m'
    elif color == 'green':
        color_code = '\033[92m'

    return '%s%s%s' % (color_code, message, '\033[0m')


def confirm_continue():
    """
    Confirms that the user wants to continue.
    Exits if the user doesn't enter a variant of `yes`.
    """
    response = raw_input('\n\nContinue? (y/n): ')
    print ''

    if response.lower() not in ['y', 'yes']:
        sys.exit()


def get_directory_size(directory_path):
    """
    Returns the approximate size of a directory tree in bytes.
    """
    size = 0

    for root, dirs, files in os.walk(directory_path):
        size += os.path.getsize(root)
        for f in files:
            file_path = os.path.join(root, f)
            if not os.path.islink(file_path):
                size += os.path.getsize(file_path)

    return size


def load_yaml(file_path):
    """
    Reads a YAML file and returns a Python object.
    """
    try:
        with open(file_path, 'r') as f:
            object = yaml.load(f.read())
    except:
        print 'Couldn\'t load %s' % file_path
        sys.exit()

    return object


def print_in_color(message, color, line_feed=True):
    """
    Prints the string in the specified color.
    Available color choices are 'red', 'amber', 'green' and 'bold'.
    """
    if color == 'red':
        color_code = '\033[91m'
    elif color == 'amber':
        color_code = '\033[93m'
    elif color == 'green':
        color_code = '\033[92m'
    elif color == 'bold':
        color_code = '\033[1m'

    if line_feed:
        print '%s%s%s' % (color_code, message, '\033[0m')
    else:
        print '%s%s%s' % (color_code, message, '\033[0m'),


def readable_duration(seconds):
    """
    Accepts a duraction in seconds.
    Returns a human-readable duration.
    """
    minutes = int(seconds) / 60
    hours = minutes / 60
    days = hours / 24
    months = int(days / (365.25 / 12))
    years = int(days / 365.25)

    if years:
        if years > 1:
            return '%s years' % years
        else:
            return '1 year'
    elif months:
        if months > 1:
            return '%s months' % months
        else:
            return '1 month'
    elif days:
        if days > 1:
            return '%s days' % days
        else:
            return '1 day'
    elif hours:
        if hours > 1:
            return '%s hours' % hours
        else:
            return '1 hour'
    elif minutes:
        if minutes > 1:
            return '%s mins' % minutes
        else:
            return '1 min'
    else:
        return '<1 min'
