from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    pkt_size = data["packet_size"]
    pkt_rate = data["packet_rate"]

    attack = False

    if pkt_size > 500:
        attack = True

    if pkt_rate > 20:
        attack = True

    return jsonify({"attack": attack})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
