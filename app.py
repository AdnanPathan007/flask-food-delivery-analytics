from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import requests
from publisher.gcp_publisher import GcpPublisher

app = Flask(__name__)


# ================= LOCATION =================

def get_location(ip):
    try:
        r = requests.get(f'https://ipinfo.io/{ip}/json', timeout=2)
        d = r.json()
        return {
            "ip": ip,
            "city": d.get("city"),
            "region": d.get("region"),
            "country": d.get("country"),
            "loc": d.get("loc")
        }
    except:
        return {}


# ================= ROUTES =================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")


# ================= TRACKING =================

@app.route("/log_click", methods=["POST"])
def log_click():
    data = request.json

    data["server_timestamp"] = datetime.now(timezone.utc).isoformat()
    data["ip"] = request.remote_addr
    data["location"] = get_location(data["ip"])

    print("\n===== EVENT RECEIVED =====")
    print(data)

    publisher = GcpPublisher()
    publisher.add_message_to_queue(data)

    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(debug=True)