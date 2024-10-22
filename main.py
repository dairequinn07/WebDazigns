import os
import re
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse, parse_qs
from flask import Flask, render_template, request, make_response, redirect, jsonify, session, url_for, flash


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


# Step 3: Add HTTPS redirection before any request is processed
# @app.before_request
# def https_redirect():
#     if not request.is_secure and request.headers.get('x-forwarded-proto') != 'https':
#         # Redirect HTTP requests to HTTPS
#         return redirect(request.url.replace('http://', 'https://', 1), code=301)


@app.after_request
def add_response_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET'])
def hello_world():
    response = make_response(render_template('index.html'))
    return response


def get_db_connection():
    db_url = os.environ.get('JAWSDB_URL')

    # Parse the connection string
    parsed_url = urlparse(db_url)

    # Get the query parameters
    query_params = parse_qs(parsed_url.query)

    # Extract the database name
    db_database = parsed_url.path.lstrip("/")  # Remove the leading slash from the path

    # Check if the "reconnect" parameter exists in the query parameters
    if "reconnect" in query_params:
        # Remove the "reconnect" parameter from the database name if present
        db_database = db_database.replace(f"?reconnect={query_params['reconnect'][0]}", "")

    # Extract the individual parts from the URL using regular expressions
    match = re.match(r'mysql://([^:]+):([^@]+)@([^/]+):(\d+)/(.+)', db_url)

    if match:
        db_user = match.group(1)
        db_password = match.group(2)
        db_host = match.group(3)
        db_port = int(match.group(4))
        db_database = db_database

        return mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_database,
            user=db_user,
            password=db_password
        )
    else:
        raise ValueError("Invalid database URL")


@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json() # Get JSON data from the request
    name = data['name']
    company_name = data['company_name']
    email_address = data['email']
    phone_number = data['phone_number']
    comments = data['comments']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert into the database
    cursor.execute(
        """
        INSERT INTO web_dazigns_enquiries (name, company_name, email_address, phone_number, comments)
        VALUES (%s, %s, %s, %s, %s)
        """, (name, company_name, email_address, phone_number, comments)
    )

    conn.commit()
    conn.close()
    # Return success response if no issues
    return jsonify({'success': True}), 200


if __name__ == "__main__":
    app.run(debug=False)


