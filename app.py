from flask import Flask, render_template, request, redirect
import json
import threading
from detector import start_detection

app = Flask(__name__)

# Start camera detection in background
threading.Thread(target=start_detection, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_number = request.form["to_number"]
        with open("config.json", "r") as f:
            config = json.load(f)
        config["to_number"] = new_number
        with open("config.json", "w") as f:
            json.dump(config, f)
        return redirect("/")

    with open("config.json") as f:
        config = json.load(f)

    return render_template("index.html", to_number=config["to_number"])

if __name__ == "__main__":
    app.run(debug=True)
