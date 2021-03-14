from core.utils import utils
from core.sqlorm import db
from flask import render_template, request

def Main(app):
  if not request.args.get('token'):
    utils.templates('security', app)
    return render_template("security.html", net_ip=utils.getNetworkIp())
  else:
    args=[request.args.get(tmp) for tmp in request.args.keys()]
    raw=db.select('SELECT * FROM user')
    if args[0]==raw[0]+raw[1]:
      db.edit(f'UPDATE user SET username="{args[1]}", password="{args[2]}"')
      return "Authentication data updated"
    else:
      return "Wrong username or password!"