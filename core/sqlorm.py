import sqlite3

db_name='auth.db'

class db(object):
	@staticmethod
	def edit(sql_post):
		conn = sqlite3.connect(db_name)
		cursor = conn.cursor()
		cursor.execute(f"{sql_post}")
		conn.commit()
		conn.close()
	def select_all(sql_all):
		conn = sqlite3.connect(db_name)
		cursor = conn.cursor()
		sql=f"{sql_all}"
		cursor.execute(sql)
		test=cursor.fetchall()
		conn.close()
		return test
	def select(sql_select):
		conn = sqlite3.connect(db_name)
		cursor = conn.cursor()
		sql=f"{sql_select}"
		cursor.execute(sql)
		post={}
		for i in cursor.fetchall():
			post=i
		conn.close()
		return post
	def top(sql_top):
		top=[]
		conn = sqlite3.connect(db_name)
		cursor = conn.cursor()
		sql=f"{sql_top}"
		for stay in cursor.execute(sql):
			top.append(stay)
		conn.close()
		return top
		