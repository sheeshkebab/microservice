from flask import Flask, jsonify, make_response
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError

import requests
import os
import simplejson as json

app = Flask(__name__)

database_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print database_path

with open("{}/database/users.json".format(database_path), "r") as f:
    usr = json.load(f)

@app.route("/", methods=['GET'])
def hello():
    ''' Greet the user '''

    return "Hey! The service is up, how about doing something useful"

@app.route('/users', methods=['GET'])
def users():
    ''' Returns the list of users '''

    resp = make_response(json.dumps(usr, sort_keys=True, indent=4))
    resp.headers['Content-Type']="application/json"
    return resp

@app.route('/users/<username>', methods=['GET'])
def user_data(username):
    ''' Returns info about a specific user '''

    if username not in usr:
        return "Not found"

    return jsonify(usr[username])

@app.route('/users/<username>/lists', methods=['GET'])
def user_lists(username):
    ''' Get lists based on username '''

    try:
        req = requests.get("http://127.0.0.1:5001/lists/{}".format(username))
    except requests.exceptions.ConnectionError:
        return "Service unavailable"
    return req.text


@app.route('/users/ldap', methods=['GET'])
def stuff():
  mydict = {}
  mydict['Users'] = []
  server_name = '172.31.19.18'
  domain_name = 'REDHAT'
  user_name = 'administrator'
  password = '7mrfa)Lr@Vy'

  format_string = '{:25} {:>6} {:19} {:19} {}'
  print(format_string.format('User', 'Logins', 'Last Login', 'Expires', 'Description'))

  server = Server(server_name, get_info=ALL)
  conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password, authentication=NTLM, auto_bind=True)
  #conn.search('dc=REDHAT,dc=COM,dc=AU'.format(domain_name), '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
  conn.search('dc=REDHAT,dc=COM,dc=AU', '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
  for e in conn.entries:
      try:
          desc = e.description
          user = {"description":str(desc),"name":str(e.name)}
          mydict['Users'].append(user)
      except LDAPCursorError:
          desc = ""

  resp = make_response(json.dumps(mydict, sort_keys=True, indent=4))
  resp.headers['Content-Type']="application/json"
  return resp

if __name__ == '__main__':
    app.run(port=5000, debug=True)
