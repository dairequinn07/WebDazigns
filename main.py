from flask import Flask, render_template, request, make_response, redirect, jsonify, session, url_for, flash


app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    response = make_response(render_template('index.html'))
    return response


if __name__ == "__main__":
    app.run(debug=False)


