# Web Server
import sys
import argparse
import configparser

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

# Import - Route
from src.route.user import construct_user_blueprint
from src.route.device import construct_device_blueprint
from src.route.sensor import construct_sensor_blueprint
from src.route.data import construct_data_blueprint
from src.route.free_board import construct_free_board_blueprint
from src.route.notice_board import construct_notice_board_blueprint
from src.route.archive import construct_archive_blueprint

from src.utils.file_io import create_dir

parser = argparse.ArgumentParser()
parser.add_argument("-config", default="config.ini")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.config)

stored_data_path = config.get("Path", "stored_data_path")
stored_notice_board_file_path = config.get("Path", "stored_file_path") + "notice_board"
stored_free_board_file_path = config.get("Path", "stored_file_path") + "free_board"
stored_archive_board_file_path = config.get("Path", "stored_file_path") + "archive"

db_name = config.get("Database", "db_name")
db_ip = config.get("Database", "db_ip")
db_port = int(config.get("Database", "db_port"))
db_id = config.get("Database", "db_id")
db_pw = config.get("Database", "db_pw")

ss_port = int(config.get("ServiceServer", "ss_port"))
ss_debug = bool(config.get("ServiceServer", "ss_debug"))

dc_ip = config.get("DataCollectorServer", "dc_ip")
dc_port = config.get("DataCollectorServer", "dc_port")

app = Flask(__name__)

app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{db_id}:{db_pw}@{db_ip}:{db_port}/{db_name}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

create_dir(stored_notice_board_file_path)
create_dir(stored_free_board_file_path)
create_dir(stored_archive_board_file_path)

@app.route("/")
def index():
    return "Welcome iPLAT service server"

app.register_blueprint(construct_user_blueprint(db))  # User
app.register_blueprint(construct_device_blueprint(db))  # Device
app.register_blueprint(construct_sensor_blueprint(db))  # Sensor
app.register_blueprint(construct_data_blueprint(db, stored_data_path))  # Data
app.register_blueprint(construct_free_board_blueprint(db, stored_free_board_file_path))  # Free Board
app.register_blueprint(construct_notice_board_blueprint(db, stored_notice_board_file_path))  # Notice Board
app.register_blueprint(construct_archive_blueprint(db, stored_archive_board_file_path))  # Archive

app.run(host='0.0.0.0', port=ss_port, debug=ss_debug)

