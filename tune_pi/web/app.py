import helpers
import forms

import os
import flask
from flask_material import Material
from flask_assets import Environment, Bundle
import subprocess


app = flask.Flask(__name__)
# Material(app)
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('sass/*', filters='pyscss', output='all_compiled.css')
assets.register('scss_all', scss)

app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY']
)

@app.route("/", methods=['GET', 'POST'])
def root():
    form = forms.SimpleForm()
    if flask.request.method == 'GET':
        return flask.render_template('main.html', form=form)
    else:
        return root_post(form)

def root_post(form):
    system_call = helpers.form_to_sys_call(form)
    subprocess.Popen(system_call)

    wait = form.data['seconds']
    return flask.redirect(flask.url_for('results', wait=wait))

@app.route("/results", methods=['GET'])
def results():
    return flask.render_template('results.html')

@app.route("/configure")
def configure():
    # choose obd pids to select from so that the form options aren't
    # overwhelming
    # set names for analog pins
    # set functions for analog pins
    return flask.render_template('configure.html')

@app.route("/download", methods=['GET'])
def download():
    return flask.send_from_directory('static/logs/', 'weblog.json', as_attachment=True)

if __name__ == "__main__":
    app.run()
