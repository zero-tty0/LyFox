import jinja2, os, socket

class utils:
	def templates(modname,app):
		my_loader = jinja2.ChoiceLoader([
			app.jinja_loader,
			jinja2.FileSystemLoader([
	 								f'{os.getcwd()}/plugins/{modname}/templates']),
			])
		app.jinja_loader = my_loader
	def getNetworkIp():
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	    s.connect(('<broadcast>', 0))
	    return s.getsockname()[0]