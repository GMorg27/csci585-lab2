import re

from flask import Flask, jsonify, render_template, request

from shamir import join_shares, split_shares


app = Flask(__name__)

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/split", methods=["POST"])
def split():
    body = request.get_json()
    d = body.get("d")
    k = body.get("k")
    n = body.get("n")
    if d is None or k is None or n is None:
        return jsonify({"error": "Request body must contain: d, k, n"}), 400
    return split_shares(d, k, n)

@app.route("/join", methods=["POST"])
def join():
    share_strings = request.get_json()
    if not isinstance(share_strings, list):
        return jsonify({"error", "Request body must be a list"}), 400
    if len(share_strings) == 0:
        return jsonify({"error", "List must not be empty"}), 400

    shares = []
    for share_str in share_strings:
        share_str = str(share_str)
        match = re.search(r"\((-?\d+), (-?\d+)\)", share_str)
        if not match:
            return jsonify({"error", f"Could not parse input '{share_str}'"}), 400
        i = int(match.group(1))
        d_i = int(match.group(2))
        shares.append((i, d_i))
    return {"secret": join_shares(shares)}

if __name__ == "__main__":
    app.run(debug=True)
    