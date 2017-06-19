"""Example of using openTypeExtension to store user preference settings."""
import json
import os
import bottle
from bottle import redirect, request, route, view
from requests_oauthlib import OAuth2Session

CLIENT_ID, CLIENT_SECRET = open('auth_settings.txt').read().splitlines()
REDIRECT_URI = 'http://localhost:5000/login/authorized'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # allow HTTP for local dev/test
SCOPES = ['User.Read', 'Directory.AccessAsUser.All']
SESSION = dict()

@route('/')
@view('homepage')
def home():
    """Render the home page."""
    if SESSION.get('msgraph'):
        if request.query.setcolor:
            set_color(request.query.setcolor)
        extension_data = user_extension('com.mahugh.userprefs')
        return dict(displayName=SESSION['displayName'],
                    emaildomain=SESSION['emaildomain'],
                    favcolor=extension_data.get('color'))
    return dict(displayName=None)

@route('/login')
def login():
    """Prompt user to authenticate."""
    msgraph = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
    authorization_url, state = msgraph.authorization_url( \
        'https://login.microsoftonline.com/common/oauth2/v2.0/authorize')
    SESSION['oauth_state'] = state
    return redirect(authorization_url)

@route('/login/authorized')
def authorized():
    """Fetch access token for authenticated user."""
    msgraph = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=SESSION['oauth_state'])
    SESSION['access_token'] = msgraph.fetch_token( \
        'https://login.microsoftonline.com/common/oauth2/v2.0/token', \
        client_secret=CLIENT_SECRET, authorization_response=request.url)
    me_data = msgraph.get('https://graph.microsoft.com/v1.0/me').json()
    SESSION['loggedin'] = True
    SESSION['displayName'] = me_data['displayName']
    SESSION['emaildomain'] = me_data['userPrincipalName'].split('@')[1]
    SESSION['msgraph'] = msgraph
    return redirect('/')

@route('/logout')
def logout():
    """Disconnect."""
    SESSION.clear()
    redirect('/')

def set_color(color):
    """Saves a color selection for the current user."""
    request_body = '''{"@odata.type": "Microsoft.Graph.OpenTypeExtension",
        "extensionName": "com.mahugh.userprefs", "color": "''' + color + '"}'
    request_headers = {'Content-Type' : 'application/json'}
    if user_extension('com.mahugh.userprefs').get('color'):
        # extension exists, so PATCH to update its color setting
        endpoint = 'https://graph.microsoft.com/v1.0/me/extensions/com.mahugh.userprefs'
        SESSION['msgraph'].patch(endpoint, data=request_body, headers=request_headers)
    else:
        # extension doesn't exist, so POST to create it
        endpoint = 'https://graph.microsoft.com/v1.0/me/extensions'
        SESSION['msgraph'].post(endpoint, data=request_body, headers=request_headers)

def user_extension(extension_id):
    """Get a user-node open extension for the current user.
    Returns requested extension as a dictionary (empty if it doesn't exist)."""
    endpoint = 'https://graph.microsoft.com/v1.0/me?$select=id&$expand=extensions'
    jsondata = SESSION['msgraph'].get(endpoint).json()
    for extension in jsondata.get('extensions'):
        if extension['id'] == extension_id:
            return extension
    return dict()

if __name__ == '__main__':
    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server."""
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
        return bottle.static_file(filepath, root=STATIC_ROOT)
    bottle.run(app=bottle.app(), server='wsgiref', host='localhost', port=5000)
