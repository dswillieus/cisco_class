#!/usr/bin/env python

import yaml
import xmltodict
import json
from device import Device
#import cli

#using unicodedata module to convert unicode type to string type in main
import unicodedata
'''
verify_code method is from Darren, with few alterations as follows:
* nx variable has been switched to sw,
* show command has been changed to reflect my working OS version,
* and returns MD5sum without printing


def verify_code(sw):

	
	<?xml version="1.0" encoding="UTF-8"?>
	<ins_api>
	<type>cli_show</type>
	<version>1.0</version>
	<sid>eoc</sid>
		<outputs>
			<output>
				<body>
					<file_content_md5sum>e6301b3e6d911fa96c875f970a15759c
					</file_content_md5sum>
				</body>
	<input>show file bootflash:/nxos.7.0.3.I2.2d.bin md5sum</input>
	<msg>Success</msg>
	<code>200</code>
	</output>
	</outputs>
	</ins_api>
	"""

	getcode = sw.conf('show file bootflash:///nxos.7.0.3.I3.1.bin md5sum')
	
	code_dict = xmltodict.parse(getcode[1])
	#print json.dumps(code_dict, indent=4)

	filesum = code_dict['ins_api']['outputs']['output']
	
	md5 = {}
	md5sum = filesum['body']
	#print md5sum
	return md5sum
	
	
def show_hardware(sw):

	getData = sw.show('show hardware')

	show_hw_dict = xmltodict.parse(getData[1])
	
	data = show_hw_dict['ins_api']['outputs']['output']['body']

	hw_dict = {}
	hw_dict['OS Version'] = data['kickstart_ver_str']
	hw_dict['Type'] = data['chassis_id']
	hw_dict['Memory'] = data['memory'] + data['mem_type']
	hw_dict['Hostname'] = data['host_name']
	hw_dict['Bootflash'] = data['bootflash_size']
	hw_dict['Last Reboot Reason'] = data['rr_reason']
	hw_dict['Uptime'] = '{} day(s) {} hour(s) {} minute(s) {} second(s)'.format(data['kern_uptm_days'], \
		data['kern_uptm_hrs'], data['kern_uptm_mins'], data['kern_uptm_secs'])
	
	ser_nums = {}
	ser_nums_data = show_hw_dict['ins_api']['outputs']['output']['body']['TABLE_slot']['ROW_slot']['TABLE_slot_info']['ROW_slot_info']

	for each in ser_nums_data:
		if 'serial_num' in each.keys():
			key = each['serial_num']
			ser_nums[key] = each['model_num']
			hw_dict['Serial Numbers'] = ser_nums
# print json.dumps(hw_dict, indent = 4)

	return hw_dict
'''

def copy_config(sw):
	print 'Copying configuration to running-config... '
	copy = sw.conf('copy bootflash:/testcode/configtest.cfg running-config')
	#print copy
	print 'Copy complete.'

	return copy_config

def set_bootvar(sw):
	boot = sw.conf('config t ; boot nxos bootflash:/imagetest.bin ; end')
	#print boot
	print 'Setting boot variable to NXOS Image.... '
	print 'Saving configuration...'
	save = sw.conf('copy run start')
	#return save
	print 'Save complete.'

	return set_bootvar
'''
main was created with tests in there for checking type, see below
ip address has been changed for my working enviroment.
'''

def main():
	switch = Device(ip = '172.31.217.135', username = 'admin', password = 'cisco123')
	switch.open()

	#verify = verify_code(switch)
	#hw = show_hardware(switch)
	conf = copy_config(switch)
	bootvar = set_bootvar(switch)


	#my_vars = yaml.load(file('codeMapMD5.yml','r'))
	#check OS Version vs. control OS Version in YAML file
	#print 'Does ' + hw['OS Version'] + ' match ' + my_vars['n9kCodeVer']
	#the next four lines are used to check variable types for conversations as needed
	#print 'my_vars type: '
	#print type(my_vars['n9kCodeVer'])
	#print 'hw type: '
	#print type(hw['OS Version'])
	#change unicode to string for hw['OS Version']
	#osVer = unicodedata.normalize('NFKD', hw['OS Version']).encode('ascii','ignore')
	#print osVer type to check if it's a string, which it is
	#print 'osVer type: '
	#print type(osVer)
	'''
	next two lines are a bad attempt to change osVer into an int. Firstly, we
	needs more string manipulation by splitting the osVer string on periods and
	parenthesis, then converting each of those individual strings to ints for
	comparison
	'''
	#osVerI = int("osVer")
	#print osVerI
	#for each in my_vars['NX9000']:
	#	if hw['OS Version'] == my_vars['NX9000.n9kCodeVer']:
	#		print 'Does not need upgrade, checking MD5 Hash'
	#	elif hw['OS Version'] != my_vars['NX9000.n9kCodeVer']:
	#		sw.conf('copy usb0:/'+ my_vars['NX9000.n9kFile'] + 'bootflash:')
	#		print 'Copying files to device...'
	#	else:
	#		print 'Need to upgrade OS version'
	'''
	next else statement would be used to catch all for versions that are not indentical
	to that of the yaml file. An "elif expression:" could be used to tell whether OS
	version is north or south of control version in yaml file, but needs strings to be
	converted to ints for expression comparison first, as commented above
	'''






main()