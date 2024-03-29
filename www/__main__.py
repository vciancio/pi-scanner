from flask import Flask, url_for
from common.config import Config
import common.access_token as access_token
import time

global api_key
api_key = None

app = Flask(__name__)

def get_internal_ip():
    try:
        import socket
        hostname = socket.gethostname()   
        return socket.gethostbyname(hostname+'.local')
    except:
        print("Not connected to network.")
        return None

@app.route("/", methods=['GET'])
def home():
	html = "<h1>Pi-Scanner</h1>"
	html += render_oauth_current_token()
	return html

@app.route("/auth/google-photos")
def auth_google_photos():
    return '''<script type="text/javascript">
            const parsedHash = new URLSearchParams(
  				window.location.hash.substr(1) // skip the first char (#)
			);
            window.location = "/access_token_response/" 
                + parsedHash.get("expires_in") + "/" + parsedHash.get("access_token");
        </script> '''

@app.route("/access_token_response/<expires_in>/<token>", methods=['GET'])
def auth_token(token, expires_in):
	# Offset expires time by a minute just in case we're in the middle of uploading
	expired_time = time.time() + (int(expires_in) - 60)
	access_token.save(token, expired_time)
	return '''<script type="text/javascript">
	window.location = "/";
	</script>'''

@app.route("/deauth/google-photos")
def route_deauth_google_photos():
	if access_token.get_token() == '':
		return '''<script type="text/javascript">
			window.location = "/";
			</script>'''
	revokeTokenEndpoint = 'https://oauth2.googleapis.com/revoke'
	token = access_token.get_token()
	access_token.clear()
	html = "<form method='POST' name='deauth' action='%s'>"%(revokeTokenEndpoint)
	html += "<button name='linkBtn' type='submit'>Unlink to Google Photos</button>"
	html += "<input type='hidden' name='token' value='%s'/>"%(token)
	html += "</form>"
	html += "<script type='text/javascript'>document.forms['deauth'].submit();</script>"
	return html

def render_oauth_current_token():
	api_key = access_token.get_token()
	html = "<div>"
	html += "<p>Current API Key: <i>%s</i></p>"%(api_key)
	if(api_key == None or api_key == ''):
		html += render_oauth_button_auth()
	else:
		html += render_oauth_button_deauth()
	html += "</div>"
	return html

def render_oauth_button_auth():
	oauth2Endpoint = 'https://accounts.google.com/o/oauth2/v2/auth'
	with app.app_context():
		internal_ip = get_internal_ip()
		if internal_ip is None:
			return ""
		redirect_url = 'https://%s.sslip.io%s'%(internal_ip, url_for('auth_google_photos'))
	params = {
		'client_id': Config.GOOGLE_PHOTOS_CLIENT_ID,
		'redirect_uri': redirect_url,
		'response_type': 'token',
		'scope': 'https://www.googleapis.com/auth/photoslibrary.appendonly',
		'include_granted_scopes': 'true',
		'state': 'pass-through value'
	}

	html = "<form method='GET' action='%s'>"%(oauth2Endpoint)
	html += "<button name='linkBtn' type='submit'>Link to Google Photos</button>"
	for p, value in params.items():
		html+= "<input type='hidden' name='%s' value='%s'/>"%(p, value)
	html += "</form>"
	return html

def render_oauth_button_deauth():
	html = "<form method='GET' action='%s'>"%(url_for('route_deauth_google_photos'))
	html += "<button name='linkBtn' type='submit'>Unlink from Google Photos</button>"
	html += "</form>"
	return html


if __name__ == '__main__':
	# app.run(ssl_context=('www/ssl/fullchain.pem', 'www/ssl/privkey.pem'))
	app.run(port=5000, debug=False)
