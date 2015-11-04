import os
import subprocess

import config
from logging import log
from utils import (
    checksum_directory,
    print_in_color,
)


class Directory(object):

    def __init__(self, instance):
        self.name = instance['name']
        self.source = instance['path']
        self.type = instance['type']

        self.target = os.path.join(config.DEVICE['path'], self.name)

    def sync_ordinary_directory(self):
        """
        Sync an ordinary directory (not a VM or a git-annex repo) using rsync.
        """
        cmd = 'rsync -r --progress --inplace --no-whole-file --delete ' + \
            '%s/ %s' % (self.source, self.target)

        subprocess.call(cmd, shell=True)

        log('    %s:' % self.name)
        log('      copied: True')

        self.verify_backup()

    def sync_virtual_machine(self):
        """
        Sync a Virtualbox virtual machine using rsync.
        """
        # First, check that the VM isn't running.
        # This command's return code is `0` if it is running, `1` if it isn't.
        vboxmanage_cmd = 'vboxmanage showvminfo "%s" | grep -c "%s"' % (
            os.path.basename(self.source),
            'State:           running'
        )
        return_code = subprocess.call(vboxmanage_cmd, shell=True)

        if return_code == 0:
            vm_running = True
        else:
            vm_running = False

        # Only sync a virtual machine if it isn't running.
        if not vm_running:
            rsync_cmd = 'rsync -r --progress --inplace --no-whole-file ' + \
                '--delete %s/ %s' % (self.source, self.target)

            subprocess.call(rsync_cmd, shell=True)

            log('    %s:' % self.name)
            log('      copied: True')

            self.verify_backup()

        else:
            print_in_color(
                "The '%s' VM is running and WILL NOT be backed up." % self.name,
                'red'
            )
            log('    %s:' % self.name)
            log('      copied: False')

    def sync_git_annex(self):
        """
        Sync a git-annex repository using git-annex.
        """
        subprocess.call(
            'cd %s && git annex sync laptop --content' % self.target,
            shell=True
        )

        log('    %s:' % self.name)
        log('      copied: True')

        self.verify_backup()

    def backup(self):
        """
        Backs up the directory.
        """
        if self.type == 'directory':
            self.sync_ordinary_directory()
        elif self.type == 'virtual-machine':
            self.sync_virtual_machine()
        elif self.type == 'git-annex':
            self.sync_git_annex()

    def verify_backup(self):
        """
        Checksums the source and target directories to make sure the backup
        succeeded.
        """
        source_checksum = checksum_directory(self.source)
        target_checksum = checksum_directory(self.target)

        if source_checksum == target_checksum:
            log('      verified: True')
            log('      checksum: %s' % source_checksum)
        else:
            log('      verified: False')
