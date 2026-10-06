from flask import Flask, jsonify, render_template, request

from cloud import get_shares, save_shares, NUM_SERVERS
from shamir import P_BYTE_LENGTH, join_shares, split_shares


# Config
THRESHOLD = 3

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    body = request.get_json()
    website = body.get("website")
    username = body.get("username")
    password = body.get("password")
    if not website or not username or not password:
        return jsonify({"error": "Request body must contain: website, username, password"}), 400

    # Encode password as number, split into shares, and save
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > P_BYTE_LENGTH:
        return jsonify({"error": "Password too long"}), 400
    secret = int.from_bytes(password_bytes, byteorder="big")

    print(secret)
    shares = split_shares(secret, THRESHOLD, NUM_SERVERS)
    if not save_shares(website, username, shares):
        return jsonify({"error": "Could not save shares to cloud"}), 500
    return jsonify({"message": "Configuration saved"}), 201

@app.route("/autofill", methods=["POST"])
def autofill():
    body = request.get_json()
    website = body.get("website")
    username = body.get("username")
    if not website or not username:
        return jsonify({"error": "Request body must contain: website, username"}), 400

    # Retrieve shares, join, and decode password string
    shares = get_shares(website, username)
    if len(shares) < THRESHOLD:
        return jsonify({"error": "Number of shares available is below threshold"}), 500
    secret = join_shares(shares[:THRESHOLD])
    print(secret)
    password_bytes = int.to_bytes(secret, length=P_BYTE_LENGTH, byteorder="big")
    password = password_bytes.lstrip(b"\x00").decode("utf-8")
    return {"password": password}

if __name__ == "__main__":
    app.run(debug=True)
