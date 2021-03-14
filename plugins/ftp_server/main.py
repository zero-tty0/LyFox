from flask import render_template, request
from threading import Thread as th
from core.utils import utils
import jinja2, os, time

def backup():
	bp=os.getcwd()+'/plugins/ftp_server/backups'
	fp=os.getcwd()+'/plugins/ftp_server/files'
	if not os.path.isdir(bp): os.mkdir(bp)
	os.system(f'zip -r "{bp}/backup_{time.time()}.zip" "{fp}"')

def Main(app):
	args=[tmp for tmp in request.args.keys()]
	if not args:
		if os.path.exists('/usr/sbin/vsftpd'):
			utils.templates('ftp_server',app)
			
			with open('/etc/vsftpd.conf') as f: config = [i.strip() for i in f.readlines()]
			
			if config[0] != '#.-_':
				with open('plugins/ftp_server/vsftpd.conf', 'a') as f: f.write(f'\nlocal_root={os.getcwd()}/plugins/ftp_server/files')
				os.system('cp plugins/ftp_server/vsftpd.conf /etc/vsftpd.conf; mkdir plugins/ftp_server/files')
				with open('/etc/vsftpd.conf') as f: config = [i.strip() for i in f.readlines()]
			
			templates_tf=''
			for ncon in config:
				if ncon != '#.-_':
					setup=ncon.split('=')
					if setup[1] in ['YES', 'NO']:
						btn=f'''<a type='button' style='float: right;' class='text-light btn btn-rounded btn-sm bg-{"warning" if setup[1]=="YES" else "dark"}' onclick='change_s("{setup[0]}", "{setup[1]}");'>{setup[1]}</a>'''
						templates_tf+=f'''
			<div style='box-shadow: 0 0 10px rgba(0,0,0,0.2); margin-top: 20px;' class="d-inline col-md-4">
				<span class='badge text-light bg-dark'>{setup[0]}</span>
				{btn}
			</div>
						'''
			
			templates_ts=''
			for ncon in config:
				if ncon != '#.-_':
					setup=ncon.split('=')
					if setup[1] not in ['YES', 'NO']:
						templates_ts+=f'''
			<div style='box-shadow: 0 0 10px rgba(0,0,0,0.2); margin-top: 20px;' class="d-inline col-md-4">
				<span class='badge text-light bg-dark'>{setup[0]}</span>
				<div class="form-outline">
					<input type="text" id="{setup[0]}" value='{setup[1]}' class="form-control" />
					<label class="form-label" for="{setup[0]}"></label>
				</div>
				<a type='button' style='float: right;' class='text-light btn btn-rounded btn-sm bg-dark' onclick='change_s("{setup[0]}", "{setup[1]}");'>save</a>
			</div>
						'''
			
			return render_template('ftp_server.html', content_tf=templates_tf, content_ts=templates_ts, net_ip=utils.getNetworkIp(), path=os.getcwd())
		else: return 'Install vsftpd!'
	elif 'def_p' in [tmp for tmp in request.args.keys()]:
		def_p=request.args.get('def_p')
		def_a=request.args.get('def_a')
		new_a=request.args.get('new_a')
		fr=open('/etc/vsftpd.conf', 'r')
		tmp=fr.read()
		fw=open('/etc/vsftpd.conf', 'w') 
		upd=fw.write(tmp.replace(f'{def_p}={def_a}', f'{def_p}={new_a}'))
		fw.close();fr.close()
		return "Configuration changed, plz, restart vsftpd"
	elif 'backup' in [tmp for tmp in request.args.keys()]:
		th(target=backup).start()
		return 'Backup running in background'
	elif 'restore' in [tmp for tmp in request.args.keys()]:
		os.system(f'cp {os.getcwd()}/plugins/ftp_server/vsftpd.conf /etc/')
		return 'Configuration restored'
	elif 'service' in [tmp for tmp in request.args.keys()]:
		mode=request.args.get('service')
		if mode=='start':
			os.system('systemctl enable vsftpd; systemctl start vsdtpd')
			return 'Started ftp service done'
		elif mode=='restart':
			os.system('systemctl restart vsftpd')
			return 'Restarted ftp service done'
		else:
			os.system('systemctl disable vsftpd; systemctl stop vsdtpd')
			return ('Stopped ftp service done')