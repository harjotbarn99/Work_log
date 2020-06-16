import bottle
import json
import p_database
import other
import eventlet
import eventlet.wsgi
import p_authentication as ath
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode




def get_cypher(key_filename):
  with open(key_filename) as f:
    data = f.read()
  key = RSA.importKey(data,"KEY USED TO GENERATE PEM FILES")
  cipher = PKCS1_OAEP.new(key)
  return cipher

cipher = get_cypher("private-attend-app.pem")
cipher_verify = get_cypher("private-attend-app-token.pem")
cipher_sign = get_cypher("public-attend-app-token.pem")



def decryptt(cyphertext, verify=False):
  content = b64decode(cyphertext)
  if verify:
    content = cipher_verify.decrypt(content).decode()
  else:
    content = cipher.decrypt(content).decode()
  return content


def sign(text):
  cyphertext = cipher_sign.encrypt(text.encode())
  cyphertext = b64encode(cyphertext).decode()
  return cyphertext


def get_username():
  username = bottle.request.get_cookie("token")
  if not username:
    return None
  return decryptt(username, True)



@bottle.route("/")
def login_page():
  return bottle.static_file("frontend/login.html", root=".")


@bottle.route('/key')
def key():
  with open("public-attend-app.pem") as f:
    data = f.read()
  response = {'key': data}
  print(response)
  return json.dumps(response)


@bottle.route("/logJS")
def login_page_js():
  return bottle.static_file("frontend/logJS.js", root=".")


@bottle.post("/login")
def loginAttempt():
  content = bottle.request.body.read().decode()
  content = decryptt(content)
  loginDetails=json.loads(content)
  message = ath.authenticate(loginDetails)
  if message['authenticated']:
    bottle.response.set_cookie("username", loginDetails["username"])
    bottle.response.set_cookie("token", sign(loginDetails["username"]))
  return json.dumps(message)


@bottle.route("/signUpPage")
def signUp_page():
  return bottle.static_file("frontend/signUp.html", root=".")


@bottle.route("/signUpJS")
def signUP_page_js():
  return bottle.static_file("frontend/signUp.js", root=".")


@bottle.post("/signUp")
def reg():
  content = bottle.request.body.read().decode()
  content = decryptt(content)
  cred=json.loads(content)
  message = ath.add_user(cred)
  return message


@bottle.route("/<filename>")
def dashboard_page(filename):
  username = get_username()
  retval = p_database.check_username(username)
  if username and retval:
    return bottle.static_file("frontend/"+filename, root=".")
  return None


@bottle.post("/addWork")
def addwork():
  username = get_username()
  retval = p_database.check_username(username)
  if username and retval:
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    cred['username']=username
    message = p_database.addWork(cred)
    return json.dumps(message)
  return json.dumps({'message':"log not added"})


@bottle.route("/logsToday")
def logsToday():
  username = get_username()
  retval = p_database.check_username(username)
  if username and retval:
    liOfLi = p_database.logsToday()
    return json.dumps(liOfLi)
  return json.dumps({'message':"problem loading log"})



@bottle.post("/logsSpecific")
def logsSpecefic():
  username = get_username()
  retval = p_database.check_username(username)
  if username and retval:
    content = bottle.request.body.read().decode()
    content = decryptt(content)
    cred=json.loads(content)
    Cdate = other.dateCorrect(cred)
    data = p_database.filterLogs(Cdate)
    return json.dumps(data)
  return json.dumps({'message':"problem loading log"})


eventlet.wsgi.server(eventlet.listen(('', 8080)), bottle.default_app())
bottle.run(host='0.0.0.0' , port = '8080' , debug = True)


# ipAddress = bottle.request.environ.get('REMOTE_ADDR')
