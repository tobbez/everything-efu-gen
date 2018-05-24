#!/usr/bin/env python3
#
# Copyright 2017, 2018 Torbjörn Lönnemark <tobbez@ryara.net>
#
# Permission to use, copy, modify, and distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright
# notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import argparse
import csv
import enum
import os
import ruamel.yaml

from itertools import chain
from pathlib import PureWindowsPath


class WindowsFileAttribute(enum.Enum):
  """
  Windows file attribute flags.

  Only useful flags included here.

  Ref: https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117(v=vs.85).aspx
  """
  READONLY = 0x00000001
  HIDDEN = 0x00000002
  DIRECTORY = 0x00000010


def windows_path(path, base):
  """
  Convert a path to a windows path relative to the root `base`.
  """
  return str(PureWindowsPath(path[len(base.rstrip(os.path.sep)):].lstrip(os.path.sep)))


def windows_time(unix_time):
  """
  Convert a UNIX timestamp to a Windows FILETIME.
  """
  # seconds between windows (Jan 1, 1601, 00:00), and unix (Jan 1, 1970, 00:00)
  return int((11644473600 + unix_time) * 10000000)


def windows_attrs(path, name, is_dir):
  """
  Return the windows file attributes for the given path.
  """
  attrs = 0
  if name.startswith('.'):
    attrs |= WindowsFileAttribute.HIDDEN.value

  if not os.access(path, os.W_OK):
    attrs |= WindowsFileAttribute.READONLY.value

  if is_dir:
    attrs |= WindowsFileAttribute.DIRECTORY.value

  return attrs


def generate_config():
  """
  Generate a sample configuration.
  """
  return ruamel.yaml.safe_dump({
      'directories': [
        '/mnt/mydisk',
        '/mnt/myseconddisk',
      ]
  }, default_flow_style=False, indent=4, block_seq_indent=2)


def scan(path):
  """
  Generate a file list for all files stored under `path` and save it to
  `path`/.everything_index.efu.
  """
  outpath_work = os.path.join(path, '.everything_index.efu-scanning')
  outpath = os.path.join(path, '.everything_index.efu')
  with open(outpath_work, 'w') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONE)
    writer.writerow(['Filename', 'Size', 'Date Modified', 'Date Created', 'Attributes'])

    # Doesn't seem to be possible to specify quoting per field number, and
    # writer.dialect.quoting is not writable, so this will have to do (since we
    # want to mirror the format of EFU files created by Everything itself:
    # unquoted fields in the header line, the filename quoted and the rest
    # unqouted for remaining lines).
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)

    for dirpath, dirnames, filenames in os.walk(path):
      for name, is_dir in chain(zip(filenames, [False] * len(filenames)), zip(dirnames, [True] * len(filenames))):
        p = os.path.join(dirpath, name)

        try:
          st = os.lstat(p)
        except FileNotFoundError:
          continue
        except PermissionError:
          writer.writerow([windows_path(p, path), 0, 0, 0, windows_attrs(p, name, is_dir)])
          continue

        try:
          writer.writerow([windows_path(p, path), 0 if is_dir else st.st_size, windows_time(st.st_mtime), windows_time(st.st_ctime), windows_attrs(p, name, is_dir)])
        except UnicodeEncodeError:
          pass

  os.replace(outpath_work, outpath)


def main():
  parser = argparse.ArgumentParser()
  mut_excl_group = parser.add_mutually_exclusive_group(required=True)
  mut_excl_group.add_argument('config', metavar='CONFIG', help="config file", type=open, nargs='*', default=[])
  mut_excl_group.add_argument('--print-sample-config', help="prints a sample config to stdout", required=False, action='store_true')
  args = parser.parse_args()

  if args.print_sample_config:
    print(generate_config(), end='')
    return


  dirs = set()
  for f in args.config:
    config = ruamel.yaml.safe_load(f)
    dirs.update(config['directories'])

  for path in dirs:
    scan(path)


if __name__ == '__main__':
  main()
