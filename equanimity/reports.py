import config

from device import Device
from utils import (
    color_text,
    readable_duration,
)


def print_devices_comparison(with_color=True, with_locations=False):
    """
    Prints a table showing when each directory was last backed up on each
    device.
    """
    nominal_table_width = 70

    no_columns = len(config.DEVICES) + 1
    column_width = nominal_table_width / no_columns
    table_width = (column_width * no_columns) + 1

    horizontal_border = (('+' + ('-' * (column_width - 1))) * (no_columns)) + \
        '+'

    # Print the table heading row.
    print '+{:-<{width}}+'.format('', width=(table_width - 2))
    print '|{:^{width}}|'.format('<<< All devices >>>', width=(table_width - 2))

    # Print the subheading row.
    print '+{:-<{width1}}+{:-<{width2}}+'.format(
        '',
        '',
        width1=(column_width - 1),
        width2=((column_width * (no_columns - 1)) - 1)
    )
    print '|{:^{width1}}|{:^{width2}}|'.format(
        '~ Directory ~',
        '~ Approximate backup age ~',
        width1=(column_width - 1),
        width2=((column_width * (no_columns - 1)) - 1)
    )
    print horizontal_border

    # Print the column headings row.
    column_heading_row = '|{:^{width}}' .format('', width=(column_width - 1))
    for device in config.DEVICES:
        column_heading_row += '|{:^{width}}'.format(
            device['name'],
            width=(column_width - 1)
        )
    column_heading_row += '|'
    print column_heading_row
    print horizontal_border

    # Print each directory's row.
    for directory in config.DIRECTORIES:
        directory_row = '| {:<{width}}'.format(
            directory['name'],
            width=(column_width - 2)
        )

        for d in config.DEVICES:
            device = Device(d)
            elapsed_seconds = device.directory_age(directory)

            if elapsed_seconds:
                raw_msg = readable_duration(elapsed_seconds)
                msg = '{:^{width}}'.format(raw_msg, width=(column_width - 2))
            else:
                msg = '{:^{width}}'.format(
                    '-',
                    width=(column_width - 2)
                )

            if with_color and elapsed_seconds > (60 * 60 * 24 * 3):
                msg = color_text(msg, 'red')
            elif with_color and elapsed_seconds > (60 * 60 * 24 * 1):
                msg = color_text(msg, 'amber')
            elif with_color and elapsed_seconds:
                msg = color_text(msg, 'green')

            directory_row += '| {}'.format(msg)
        directory_row += '|'

        print directory_row
        print horizontal_border

    # Print each device's location.
    if with_locations:
        print ''
        print horizontal_border
        location_row = '| {:<{width}}'.format(
            'Location',
            width=(column_width - 2)
        )
        for d in config.DEVICES:
            device = Device(d)
            location_row += '|{:^{width}}'.format(
                '(%s)' % device.location,
                width=(column_width - 1)
            )
        location_row += '|'
        print location_row
        print horizontal_border

    # Add two blank lines at the end for visual clarity.
    print'\n'
