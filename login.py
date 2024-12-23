import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_helper import StarApiPy, Order
import logging
import yaml
import timeit
from flask import Flask, render_template, request, jsonify, redirect, url_for

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)

#start of our program
api = StarApiPy()

#credentials
CRED_FILE = '.\cred.yml'

with open(CRED_FILE) as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)
    print(cred)

# ret = api.login(userid=cred['user'], password=cred['pwd'], twoFA=cred['factor2'], vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
# starttime = timeit.default_timer()
# print("The time difference is :", timeit.default_timer() - starttime)

session_token = None

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    global session_token
    error_message = None  # Variable to store the error message
    if request.method == "POST":
        totp = request.form["totp"]  # 2FA code entered by the user

        try:
            # Attempt to log in
            response = api.login(userid=cred['user'], password=cred['pwd'], twoFA=totp, vendor_code=cred['vc'], api_secret=cred['apikey'], imei=cred['imei'])
            session_token = response.get("susertoken")  # Extract session token from response
            if session_token:
                # Store session_token in a secure location
                try:
                    store_token_to_file(session_token)
                except Exception as e:
                    error_message = f"Failed to store session token: {str(e)}"
                    return render_template("login.html", error_message=error_message)

                # Redirect to dashboard on success
                return redirect(url_for("dashboard", login_success=True))
            else:
                error_message = "Invalid TOTP or API response."

        except Exception as e:
            error_message = f"Login Failed: {str(e )}"

    # Render the login page with error message
    return render_template("login.html", error_message=error_message)



@app.route("/dashboard")
def dashboard():
    global session_token
    if not session_token:
        return redirect(url_for("login"))

    # Fetch and display active positions or other data (placeholder for now)
    login_success = request.args.get("login_success", False)

    return render_template("dashboard.html", login_success=login_success)


def store_token_to_file(token):
    with open(CRED_FILE) as f:
        cred = yaml.load(f, Loader=yaml.FullLoader)
        cred['susertoken'] = token
    with open(CRED_FILE, 'w') as f:
        yaml.dump(cred, f)

if __name__ == "__main__":
    app.run(debug=True)

