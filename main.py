from flask import Flask, render_template, request, make_response, redirect, jsonify, session, url_for, flash


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=False)


