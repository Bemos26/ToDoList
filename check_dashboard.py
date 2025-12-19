import requests
import re

# Credentials
USERNAME = 'admin'
PASSWORD = 'admin'
LOGIN_URL = 'http://127.0.0.1:8000/login/'
DASHBOARD_URL = 'http://127.0.0.1:8000/dashboard/'

client = requests.Session()

# Get CSRF token
login_page = client.get(LOGIN_URL)
csrf_token = login_page.cookies['csrftoken']

# Login
login_data = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrfmiddlewaretoken': csrf_token,
    'next': '/dashboard/' # Should redirect here
}
headers = {'Referer': LOGIN_URL}

response = client.post(LOGIN_URL, data=login_data, headers=headers)

# Check if login specific text is present
if 'Admin Dashboard' in response.text:
    print("Login successful. Checking users...")
    print(f"Content length: {len(response.text)}")
    
    # Try to find user rows
    if 'mosebemos26' in response.text:
        print("FOUND: mosebemos26")
    else:
        print("MISSING: mosebemos26")
        
    if 'reminder_test_user' in response.text:
        print("FOUND: reminder_test_user")
    else:
        print("MISSING: reminder_test_user")

    # Output a chunk of the HTML for inspection
    # Find the table body
    start = response.text.find('<tbody>')
    end = response.text.find('</tbody>')
    if start != -1 and end != -1:
         print("Table Body Content:")
         print(response.text[start:end+8])
    else:
         print("Could not find table body.")

else:
    print("Login failed or did not redirect to dashboard.")
    print(f"Current URL: {response.url}")
    print(response.text[:500])
