from flask import Flask
import slf2

application = Flask(__name__)


@application.route("/")
def hello():
    return slf2.main()


if __name__ == "__main__":
    application.run()