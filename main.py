from flask import Flask, render_template, request, redirect, url_for
import psutil, json
from core.plug_util import pm
from core.utils import utils
from core.sqlorm import db

print(f'''

            |\\__/|   ╭╮╱╱╭━━╮
           /     \\   ┃┃╭┳┫━┳┻┳┳╮
          /_.~ ~,_\\  ┃╰┫┃┃╭┫╋┣┃┫
             \\@/     ╰━╋╮┣╯╰━┻┻╯
           ver 0.1   ╱╱╰━╯

Web panel started, connect to {utils.getNetworkIp()}:1700
Default login: Username 'lyfox'
               Password 'xofyl'
''')

app = Flask(__name__, static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def main():
	token=request.cookies.get('token')
	if token:
		raw=db.select('SELECT * FROM user')
		if token==raw[0]+raw[1]:
			return redirect(url_for('home'))
		else:
			return render_template('auth.html', net_ip=utils.getNetworkIp(), status="<span style='margin-bottom: 5px;' class='badge bg-danger'>Wrong password!</span>")
		
	else:
		return render_template('auth.html', net_ip=utils.getNetworkIp())

@app.route('/home')
def home():
	token=request.cookies.get('token')
	if token:
		raw=db.select('SELECT * FROM user')
		if token!=raw[0]+raw[1]:
			return redirect('/')
	else: return redirect('/')
	templates=''
	for plugin in pm.list():
		plug=pm.info(plugin)
		templates+=f'''
		  <div class="col-md-6">
		    <div style="box-shadow: 0 0 10px rgba(0,0,0,0.2);" class="col-md-12 card text-center">
			  	<div class="card-body">
			    	<h5 class="card-title">{plug['plugname']}</h5>
			   		<p class="card-text">
			    	{plug['plugbanner']}
			    	</p>
			    	<a href="/plugin/{plug['plugloadpath']}" type="button" class="btn btn-warning">open</a>
			    </div>
			  </div>
			</div>'''
	cpu=psutil.virtual_memory().percent
	ram=psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
	hdd = psutil.disk_usage('/')
	hdd_final=int( (hdd.free // (2**30)) * 100 / (hdd.total // (2**30)) )
	return render_template('main.html', cpu_load=int(cpu), ram_load=int(ram), memory=([hdd_final, 100-hdd_final]), modules=templates)

@app.route('/plugin/<plugname>')
def module(plugname):
	token=request.cookies.get('token')
	if token:
		raw=db.select('SELECT * FROM user')
		if token!=raw[0]+raw[1]:
			return redirect('/')
	else: return redirect('/')
	return pm.load(plugname).Main(app)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host=utils.getNetworkIp(), port=1700)