Equanimity
==========

Back up specified directories across multiple devices, and track those backups.

Set up
------

Step 1
^^^^^^

Clone the repo::

    $ git clone https://github.com/countermeasure/equanimity.git

Step 2
^^^^^^

Install required python packages::

    $ pip install requirements.txt

Step 3
^^^^^^

Set up default config files::

    $ python setup_equanimity.py

Step 4
^^^^^^

Edit the config files which are now in `~/.equanimity` to tell Equanimity what
to backup, where to back it up to, and how to back it up.

Instructions for editing the config files are contained in the files
themselves.

Use
---

Run Equanimity with::

    cd /directory/you/cloned/into && cd equanimity && python equanimity.py
