everything-efu-gen
======================

Utility for generating file lists (EFU files) for VoidTools' search utility
Everything.

It's useful for allowing an instance of Everything to search remote storage on
non-Windows systems (e.g. Linux), without performing the indexing over the
network.

Requirements
------------
* Python >= 3.4
* ruamel.yaml

Installation
------------

.. code:: shell

  pip install everything-efu-gen

Usage
-----

.. code:: shell

  # generate config
  everything-efu-gen --print-sample-config > myconfig.yaml

  # edit the config, then run
  everything-efu-gen myconfig.yaml

  # this will generate a file '.everything_index.efu' in each of the directories
  # specified in the configuration file.

Then follow `the documentation for adding these to Everything's index <https://www.voidtools.com/support/everything/file_lists/#include_a_file_list_in_the_everything_index>`_ 

To ensure the file lists stay up to date, schedule periodic runs using cron (or
similar).

History
-------
* 0.0.3

  - Support ruamel.yaml >= 0.18.0

* 0.0.2

  - Gracefully handle insufficient permissions to stat

* 0.0.1

  - Gracefully handle stat on non-existant files

* 0.0.0

  - Initial release
