from flask import Flask, jsonify, make_response
import sys
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError

app = Flask(__name__)


@app.route('/ldap', methods=['GET'])
def stuff():
	server_name = 'dc-etgrh.xx.com.au'
	domain_name = 'WORKGROUP'
	user_name = 'administrator'
	password = ''
	 
	format_string = '{:25} {:>6} {:19} {:19} {}'
	print(format_string.format('User', 'Logins', 'Last Login', 'Expires', 'Description'))
	 
	server = Server(server_name, get_info=ALL)
	conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password, authentication=NTLM, auto_bind=True)
	#conn.search('dc=REDHAT,dc=COM,dc=AU'.format(domain_name), '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
	conn.search('dc=REDHAT,dc=COM,dc=AU', '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
	for e in conn.entries:
			try:
					desc = e.description
					print(format_string.format(str(e.name), str(e.logonCount), str(e.lastLogon)[:19], str(e.accountExpires)[:19], desc))
			except LDAPCursorError:
					desc = ""
	 
	print(format_string.format(str(e.name), str(e.logonCount), str(e.lastLogon)[:19], str(e.accountExpires)[:19], desc))
