# HighLevel CRM Integration

This project integrates with the HighLevel CRM API to manage contacts and update custom fields using OAuth authentication.

## Features
- OAuth authentication with HighLevel CRM.
- Fetching and updating contact details.
- Handling custom fields dynamically.
- Error handling and response validation.

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/AADILNAWAZ786/API_update.git
   cd API_update
# Create a virtual environment (Optional)
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# API Endpoints
- / - Redirects to the OAuth authorization page.
- /callback/ - Handles the OAuth callback and retrieves the access token.
- /update-contact/ - Fetches and updates a contact's custom field.
