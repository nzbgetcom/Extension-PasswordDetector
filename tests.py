#!/usr/bin/env python3
#
# Copyright (C) 2024 Denis <denis@nzbget.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
from os.path import dirname
import os
import subprocess
import unittest
import shutil
import json

POSTPROCESS_SUCCESS=93
POSTPROCESS_NONE=95
POSTPROCESS_ERROR=94

unrar = os.environ.get('unrar', 'unrar')

root = dirname(__file__)
test_data_dir = root + '/test_data/'
tmp_dir = root + '/tmp/'
with_password_rar = 'with_password_123.rar'
without_password_rar = 'without_password.rar'

host = '127.0.0.1'
username = 'TestUser'
password = 'TestPassword'
port = '6789'

def get_python(): 
	if os.name == 'nt':
		return 'python'
	return 'python3'

def run_script():
	sys.stdout.flush()
	proc = subprocess.Popen([get_python(), root + '/main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())
	out, err = proc.communicate()
	proc.pid
	ret_code = proc.returncode
	return (out.decode(), int(ret_code), err.decode())

def set_defaults_env():
	# NZBGet global options
	os.environ['NZBNA_EVENT'] = 'FILE_DOWNLOADED'
	os.environ['NZBPP_DIRECTORY'] = tmp_dir
	os.environ['NZBOP_ARTICLECACHE'] = '8'
	os.environ['NZBPO_PASSACTION'] = 'PASSACTION'
	os.environ['NZBOP_CONTROLPORT'] = port
	os.environ['NZBOP_CONTROLIP'] = host
	os.environ['NZBOP_CONTROLUSERNAME'] = username
	os.environ['NZBOP_CONTROLPASSWORD'] = password
	os.environ['NZBPR_PASSWORDDETECTOR_HASPASSWORD'] = 'no'

	# script options
	os.environ['NZBNA_CATEGORY'] = 'Movies'
	os.environ['NZBNA_DIRECTORY'] = tmp_dir
	os.environ['NZBNA_NZBNAME'] = 'TestNZB'
	os.environ['NZBPR_FAKEDETECTOR_SORTED'] = 'yes'
	os.environ['NZBOP_TEMPDIR'] = tmp_dir
	os.environ['NZBOP_UNRARCMD'] = unrar

class Tests(unittest.TestCase):

	def test_without_password(self):
		os.mkdir(tmp_dir)
		set_defaults_env()
		shutil.copyfile(test_data_dir + without_password_rar, tmp_dir + without_password_rar)
		os.environ['NZBNA_NZBID'] = without_password_rar
		[out, _, _] = run_script()
		shutil.rmtree(tmp_dir)
		self.assertTrue('Password found in' not in out)

	def test_with_password(self):
		os.mkdir(tmp_dir)
		set_defaults_env()
		shutil.copyfile(test_data_dir + with_password_rar, tmp_dir + with_password_rar)
		os.environ['NZBNA_NZBID'] = with_password_rar
		[out, _, _] = run_script()
		shutil.rmtree(tmp_dir)
		self.assertTrue('Password found in' in out)

	def test_manifest(self):
		with open(root + '/manifest.json', encoding='utf-8') as file:
			try:
				json.loads(file.read())
			except ValueError as e:
				self.fail('manifest.json is not valid.')
		

if __name__ == '__main__':
	unittest.main()
