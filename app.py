from flask import Flask, render_template
import main

app = Flask(__name__)


@app.route("/")
def home():
    rooms, live_data, raspi_data, live_time = main.get_room_status()
    return render_template('index/index.html',
                           rooms=rooms,
                           building=live_data['building'],
                           outside=raspi_data,
                           live_time=live_time)


if __name__ == '__main__':
    app.run(debug=True)
