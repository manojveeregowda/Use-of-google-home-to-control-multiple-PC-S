# ##################################### #
#   CSE 6349-001 Project -- Fall 2018   #
# ##################################### #
# Damian Jimenez             1000584863 #
# Imran Moiz Mohamad         1001535660 #
# Manoj Mysore Veere Gowda   1001547261 #
# ##################################### #

from flask import Flask, request, Response
from wakeonlan import send_magic_packet
import requests
import json


app = Flask(__name__)


def get_user_computer(given_name):
    """
    Find the computer associated with the user name that was given.

    :param given_name: name given in the command query
    :return: computer address associated with the given name
    """
    for k in user_computers_map:
        if k in given_name:
            return user_computers_map[k]

    return user_computers_map["default"]


@app.route("/", methods=["POST"])
def _proxy():
    """
    Source: https://stackoverflow.com/a/36601467
    Forward requests to appropriate computer

    :return: Response from the host computer that was targeted
    """
    data = json.loads(request.get_data())
    given_name = data["result"]["parameters"].get("given-name", "default").lower()
    name_for_comp_used = given_name

    if data["result"]["parameters"].get("command", None) == "wake_up":
        if given_name != "default":
            wake_computer(get_user_computer(name_for_comp_used)["mac"])
            name_for_comp_used = "default"

    data["result"]["parameters"]["given-name"] = given_name.capitalize()

    for k, val in get_user_computer(name_for_comp_used).items():
        data["target_computer_{}".format(k)] = val

    resp = requests.request(
        method=request.method,
        url=request.url.replace(server_address, get_user_computer(name_for_comp_used)["url"]),
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=json.dumps(data),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response


def wake_computer(mac_address=None):
    if mac_address:
        send_magic_packet(mac_address)


if __name__ == '__main__':
    """
    Initialize the program and define the mapping of users to their respective computers.
    """
    server_address = "http://b1b5334b.ngrok.io"  # Runs on port 5001, needs to be http not https
    user_computers_map = {
        "default": {"url": "http://4d2b4e1a.ngrok.io", "port": 5000, "mac": "f8:28:19:c5:98:15", "word_exe": ["/usr/bin/libreoffice", "--writer"]},
        "bob": {"url": "http://643ffc20.ngrok.io", "port": 5000, "mac": "e4.d5.3d.c6.0d.81", "word_exe": ["C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE"]}
    }

    app.run(debug=False, host="localhost", port=5001)
