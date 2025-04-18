from flask import Flask, render_template, request, redirect, make_response, jsonify
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Disable debug mode in production
app.config['DEBUG'] = False
app.config['TESTING'] = False

# File to store the notice text
NOTICE_FILE = 'notice.txt'
# Get redirect URL from environment variable
REDIRECT_URL = os.environ.get('REDIRECT_URL', '')
# Get acknowledgment timeout in days from environment variable, default to 14 days
ACKNOWLEDGMENT_TIMEOUT_DAYS = int(os.environ.get('ACKNOWLEDGMENT_TIMEOUT_DAYS', '14'))
# Get status page URL from environment variable
STATUS_PAGE = os.environ.get('STATUS_PAGE', '')
# Get page title from environment variable
PAGE_TITLE = os.environ.get('PAGE_TITLE', 'Server Notices')

# Cookie types and their descriptions
COOKIE_TYPES = {
    'notice_acknowledged': {
        'name': 'Notice Acknowledgment',
        'description': 'Stores when you last acknowledged the notice to prevent showing it again for a specified period.',
        'default': True
    },
    'cookie_preferences': {
        'name': 'Cookie Preferences',
        'description': 'Stores your cookie preferences to remember your choices.',
        'default': True
    }
}

def is_local_network():
    # Check if the request is coming from a local network
    # This is a simple implementation - in production, you'd want to use proper network detection
    return request.remote_addr.startswith('192.168.') or request.remote_addr.startswith('10.') or request.remote_addr == '127.0.0.1'

def is_reverse_proxy():
    # Check if the request is coming through a reverse proxy
    # This checks for common reverse proxy headers
    return any(header in request.headers for header in ['X-Forwarded-For', 'X-Real-IP', 'X-Forwarded-Proto'])

def save_notice(text):
    with open(NOTICE_FILE, 'w') as f:
        f.write(text)

def load_notice():
    if os.path.exists(NOTICE_FILE):
        with open(NOTICE_FILE, 'r') as f:
            return f.read()
    return ""

def get_cookie_preferences():
    preferences = request.cookies.get('cookie_preferences')
    if preferences:
        try:
            return json.loads(preferences)
        except:
            pass
    return {cookie_type: info['default'] for cookie_type, info in COOKIE_TYPES.items()}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if is_local_network() and not is_reverse_proxy():
            new_text = request.form.get('notice_text', '')
            save_notice(new_text)
    
    notice_text = load_notice()
    is_local = is_local_network()
    is_proxy = is_reverse_proxy()
    cookie_preferences = get_cookie_preferences()
    
    # Check for acknowledgment cookie only if it's enabled
    if cookie_preferences.get('notice_acknowledged', True):
        acknowledged = request.cookies.get('notice_acknowledged')
        if acknowledged:
            try:
                ack_time = datetime.fromisoformat(acknowledged)
                if datetime.now() - ack_time < timedelta(days=ACKNOWLEDGMENT_TIMEOUT_DAYS):
                    return redirect(REDIRECT_URL)
            except:
                pass
    
    return render_template('index.html', 
                         notice_text=notice_text, 
                         is_local=is_local,
                         is_proxy=is_proxy,
                         status_page=STATUS_PAGE,
                         cookie_types=COOKIE_TYPES,
                         cookie_preferences=cookie_preferences,
                         page_title=PAGE_TITLE)

@app.route('/acknowledge', methods=['POST'])
def acknowledge():
    cookie_preferences = get_cookie_preferences()
    if not cookie_preferences.get('notice_acknowledged', True):
        return redirect(REDIRECT_URL)
        
    response = make_response(redirect(REDIRECT_URL))
    # Set cookie with current time
    response.set_cookie('notice_acknowledged', 
                       datetime.now().isoformat(),
                       max_age=timedelta(days=ACKNOWLEDGMENT_TIMEOUT_DAYS).total_seconds())
    return response

@app.route('/update-cookie-preferences', methods=['POST'])
def update_cookie_preferences():
    preferences = request.get_json()
    response = make_response(jsonify({'status': 'success'}))
    
    # Set cookie preferences
    response.set_cookie('cookie_preferences', 
                       json.dumps(preferences),
                       max_age=365*24*60*60)  # 1 year
    
    # If notice acknowledgment is disabled, remove the cookie
    if not preferences.get('notice_acknowledged', True):
        response.delete_cookie('notice_acknowledged')
    
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 