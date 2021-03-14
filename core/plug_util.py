import os, sys, functools, importlib, json

class pm:
 
	def list():
		return [plugin for plugin in os.listdir("plugins/")]
		
	def info(plugin):
		with open(f'plugins/{plugin}/config.json', 'r') as f:
			return json.load(f)
		
	def load(plugin):
		return importlib.import_module(f'plugins.{plugin}.main')