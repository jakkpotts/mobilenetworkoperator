import os
from flask import Flask, render_template
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


@app.route("/lookup/<number>")
def lookup(number):
    try:
        # Fetch carrier and caller-name information
        lookup_number = client.lookups.v1.phone_numbers(number).fetch(type=['carrier', 'caller-name'])
        carrier_info = lookup_number.carrier or {}
        caller_name_info = lookup_number.caller_name or {}

        # Render the template with the fetched information
        return render_template('lookup.html',
                               carrier_name=carrier_info.get('name'),
                               carrier_type=carrier_info.get('type'),
                               caller_name=caller_name_info.get('caller_name'),
                               caller_type=caller_name_info.get('caller_type'))
    except Exception as e:
        # Handle errors (e.g., invalid number)
        return render_template('error.html', error=str(e))


if __name__ == "__main__":
    app.run()
