from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"

@app.route('/gitwebhook', methods=['POST'])
def git_post():
	command = "cd /var/www; git reset --hard HEAD; git pull"
	try: 
		result_success = subprocess.check_output( [command_success], shell=True) 
	except subprocess.CalledProcessError as e:
		return "An error occurred while trying to update git repo"
    return "Done!"

@app.route('/gitwebhook', methods=['GET'])
def git_get():
    return "Webhooks work! Now"

if __name__ == "__main__":
    app.run()
