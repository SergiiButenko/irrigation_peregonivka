from flask import Flask
from be_template.views.view1 import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)