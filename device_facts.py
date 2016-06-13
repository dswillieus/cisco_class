#!/usr/bin/env python

"""
Gather device facts from devices:
hostname
os_version
management interface data (ip,name,speed, duplex)
device make and model info
last reboot reason
uptime
bootflash
serial numbers for all components
"""
import sys
import xmltodict
import json
from device import Device


def sh_hw(sw):

	gethw = sw.show('show hardware')

	sh_hw_dict = xmltodict.parse(gethw[1])
	
	hardware = sh_hw_dict['ins_api']['outputs']['output']['body']

	hw = {}
	hw['os_version'] = hardware['kickstart_ver_str']
	hw['model'] = hardware['chassis_id']
	hw['bootflash'] = hardware['bootflash_size']
	hw['memory'] = hardware['memory']+hardware['mem_type']
	hw['hostname'] = hardware['host_name']
	hw['uptime'] = '{} day(s) {} hour(s) {} min(s) {} sec(s)'.format(hardware['kern_uptm_days'],\
		hardware['kern_uptm_hrs'],hardware['kern_uptm_mins'],hardware['kern_uptm_secs'])
	hw['last_reboot'] = hardware['rr_reason']

	serials = {}
	ser_num = sh_hw_dict['ins_api']['outputs']['output']['body']['TABLE_slot']['ROW_slot']\
	['TABLE_slot_info']['ROW_slot_info']

	for each in ser_num:
		if 'serial_num' in each.keys():
			key = each['serial_num']
			serials[key] = each['model_num']

	hw['serial_numbers'] = serials

	#print json.dumps(hw, indent=4)

	return hw

def sh_int_mgmt(sw):

	getdata = sw.show('show interface mgmt0')

	sh_int_dict = xmltodict.parse(getdata[1])

	data = sh_int_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']

	ip = data['eth_ip_addr']
	mask = data['eth_ip_mask']
	name = data['interface']
	speed = data['eth_speed']
	duplex = data['eth_duplex']

	mgmt_dict = { 'ip_addr': ip+'/'+mask, 'name': name, 'speed': speed, 'duplex': duplex }

	#print json.dumps(mgmt_dict, indent=4)

	return mgmt_dict

def main():

	switch = Device(ip='172.31.217.135', username='admin', password='cisco123')
	switch.open()

	facts = {}

	intf = sh_int_mgmt(switch)
	facts['mgmt_intf'] = intf

	hw = sh_hw(switch)
	facts.update(hw)

	args = sys.argv

	if len(args) == 1:
		print json.dumps(facts, indent=4)
	else:
		if args[1] in facts.keys():
			print args[1].upper() +': ' + json.dumps(facts[args[1]],indent=4)
		else:
			print 'Invalid Key. Please provide a valid "key" and try again'

if __name__ == "__main__":
	main()
