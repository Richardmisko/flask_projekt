from mdblog.app import flask_app
from mdblog.app import init_db    # vid 207, 9:37


import sys      # vid 207 10:45

def start():              # spustac appky, prve vo videu 201, 6:00
    debug = True		  # prepis do tejto podoby (init, start) vid 207, 9:37
    host = "0.0.0.0"
    flask_app.run(host, debug=debug)

def init():
    init_db(flask_app)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        commad = sys.argv[1]
        if commad == "start":
            start()
        elif commad == "init":
            init()
    else:
        print("usage:\n\n\trun.py [ start | init ]")