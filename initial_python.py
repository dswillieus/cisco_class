router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}

router2 = dict( os_version='3.2.1', hostname='rtp_router2', model='nexus 9396', domain='cisco.com', mgmt_ip='10.1.50.12')

os_version = '3.1.1'
hostname = 'ROUTER3'
model = 'nexus 9396'
domain = 'lab.cisco.com'
mgmt_ip = '10.1.50.13'
router3 = {'os_version':os_version,'hostname':hostname,'model':model,'domain':domain,'mgmt_ip':mgmt_ip}

'''
Used to call object rtr
'''

def getRouter(rtr):
	router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
	router2 = dict( os_version='3.2.1', hostname='rtp_router2', model='nexus 9396', domain='cisco.com', mgmt_ip='10.1.50.12')
	router3 = dict( os_version='3.1.1', hostname='ROUTER3', model='nexus 9504', domain='lab.cisco.com', mgmt_ip='10.1.50.13')
	if rtr == 'router1':
		return router1
	elif rtr == 'router2':
		return router2
	elif rtr == 'router3':
		return router3
	return 'no router found.'

'''
Used for hostname via ip_address input
'''

def getRouter(rtr):
	router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
	router2 = dict(os_version='3.2.1',hostname='rtp_router2',model='nexus 9396',domain='cisco.com',mgmt_ip='10.1.50.12')
	router3 = dict(os_version='3.1.1',hostname='ROUTER3',model='nexus 9504',domain='lab.cisco.com',mgmt_ip='10.1.50.13')
	router_list = [router1,router2,router3]
	for router in router_list:
		if rtr == router['mgmt_ip']:
			return router['hostname']
	return 'No router found.'


'''
Used for hostname via ip_address input
'''

