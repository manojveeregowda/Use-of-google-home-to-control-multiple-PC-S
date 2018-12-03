### Dependencies
- Windows (Can run on Linux, but not all commands might work properly.)
- Python 3.6+
- [Ngrok](https://ngrok.com/download)
### How to Run
- Install requirement via pip
  - `pip install -r requirements.txt`
- Export the following environment varibles and register schema with Dialog Flow
  - Windows
    - `$env:DEV_ACCESS_TOKEN = "your-dev-token-here"`
    - `$env:CLIENT_ACCESS_TOKEN = "your-client-token-here"`
  - Linux
    - `export DEV_ACCESS_TOKEN="your-dev-token-here"`
    - `export CLIENT_ACCESS_TOKEN="your-client-token-here"`
  - Then execute the following command
    - `> schema webhook.py`
    - The schema command should come with the flask-assistant package installed with requirements.txt.
- Start ngrok on port 5000 for client port 5001 for proxy server. To control additional PC's just start ngrok on port 5000 on these.
    - `> ngrok http 5000`
    - `> ngrok http 5001`
- Edit `server.py` with the correct addresses from ngrok
  - Line 72, variable `server_address`, is the ngrok server address running on port 5001
  - Line 74, first entry in the dictionary `user_computers_map`, is the info for the client running on the same computer as the proxy server
  - Additional PC's can be added to `user_computers_map`, after the first entry by filling in their respective details
    - url: Should match the ngrok url displayed when ngrok is run on that computer
    - port: Typically 5000 unless changed in webhook.py and when ngrok is started
    - mac: The mac address for the ethernet adapter of that machine
    - word_exe: The location of the word/text editor binary to open when a command to open word or a document is given.
- Start `server.py` and `webhook.py`
  - `> python server.py`
  - `> python webhook.py`
### File Descriptions
- `server.py`
  - This is the proxy server that directs requests to the appropriate client, it has mappings to all the clients based on a name associated with that client (i.e., PC). It also sends the magic packed to the appropriate PC when a wake-up command is issued for that PC, and then asks the default PC to send a response back to Dialogue Flow so as to not break communication chain.
- `webhook.py`
  - This is the client server that sends the responses that communicate with dialogue flow, although all traffic flows through the proxy server this is what is effectively communicating with Dialogue Flow. This also executes commands on the clients computer (i.e., opening a file/Word, editing a file, putting a computer to sleep). Currently it is mainly tailored for Windows, but with few adjustements other OS's should be supported.
- `requirements.txt`
  - List of python package requirements to install via pip (see [How to Run](#how-to-run)).
- `schema` and `templates`
  - These folders contain the intents, training phrases, and commands to be registered with Dialog Flow. They are part of [flask-assistant](https://flask-assistant.readthedocs.io/en/latest/quick_start.html) and modified by the user to fit the current project.
- `Screenshots`
  - This folder contains various screenshots of the project settings in DialogFlow and the Google Assistant preview. It also has a few screenshots showing what the code/ngrok should look like running.
- `test.docx`
  - Sample file used for the demo.
  - Usage: `Open file test on X's computer` or `Open file test`