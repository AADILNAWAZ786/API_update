import requests
from django.shortcuts import redirect, render

# OAuth credentials
CLIENT_ID = '65c0a9a4277b2961322c545a-ls8q934d'
CLIENT_SECRET = '94af4663-c0c7-4340-9ce5-39b38e88c146'
REDIRECT_URI = 'http://127.0.0.1:8000/callback/'  
CUSTOM_FIELD_NAME = 'DFS Booking Zoom Link'

def home(request):
    """
    Redirects the user to the OAuth authorization page to obtain an authorization code.
    """
    auth_url = (
        f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=contacts.write%20contacts.read"
    )
    return redirect(auth_url)

def callback(request):
    """
    Handles the OAuth callback by exchanging the authorization code for an access token.
    Then, it retrieves contacts and updates a custom field for the first contact.
    """
    
    # Get the authorization code from the request
    code = request.GET.get('code')
    if not code:
        return redirect('home') 
    
    # Exchange the authorization code for an access token
    token_url = "https://services.leadconnectorhq.com/oauth/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return redirect('home')  
    
    # Extract access token starts here
    access_token = response.json().get('access_token')
    if not access_token:
        return redirect('home') 
    
    headers = {'Authorization': f'Bearer {access_token}'}
    # Extract access token ends here
    
    # Fetch contacts from API starts here
    contacts_url = "https://services.leadconnectorhq.com/contacts/v1/contacts"
    contacts_response = requests.get(contacts_url, headers=headers)
    if contacts_response.status_code != 200:
        return redirect('home') 

    contacts = contacts_response.json().get('contacts', [])
    if not contacts:
        return redirect('home') 
    # Fetch contacts from API ends here
    
    # Get the first contact
    contact = contacts[0]

    # Fetch custom fields from API starts here
    custom_fields_url = "https://services.leadconnectorhq.com/contacts/v1/custom-fields"
    custom_fields_response = requests.get(custom_fields_url, headers=headers)
    if custom_fields_response.status_code != 200:
        return redirect('home') 
    # Fetch custom fields from API starts here
    
    custom_fields = custom_fields_response.json().get('customFields', [])
    
    # Find the custom field ID by name
    field_id = next((field['id'] for field in custom_fields if field['name'] == CUSTOM_FIELD_NAME), None)
    if not field_id:
        return redirect('home')
    
    # Update the contact's custom field
    update_url = f"https://services.leadconnectorhq.com/contacts/v1/contacts/{contact['id']}"
    payload = {
        'customFields': {
            field_id: "TEST"  #a test value
        }
    }
    
    update_response = requests.patch(update_url, json=payload, headers=headers)
    
    # Render success
    return render(request, 'success.html', {'contact': contact})
