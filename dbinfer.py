# -*- coding: utf-8 -*-
'''车位信息数据存储接口'''

import json
import os.path as opath
from os import (unlink as erase, rename)
from easydict import EasyDict as edict


class DB(object):
	'''存储车位坐标数据类'''
	def __init__(self, dbfile='parking_part.json'):
		self.db = edict()
		self.dbfile = dbfile
		# if opath.exists(dbfile) and opath.isfile(dbfile):
		# 	with open(dbfile, 'r', encoding='utf-8') as fp:
		# 		try:
		# 			old_data = json.load(fp)
		# 		except:
		# 			old_data = ''
		# 	if len(old_data): 
		# 		if isinstance(old_data, dict):
		# 			self.db.update(old_data)
		# 		else:
		# 			rename(dbfile, dbfile+'.bak')
		# 	if opath.exists(dbfile):
		# 		erase(dbfile)
		# self.dbfile = open(dbfile, 'w+', encoding='utf-8')

	def add(self, keyword, value):
		assert isinstance(keyword, str), '需要"str"类型的参数'
		self.db[keyword] = value

	def update(self, data):
		data.update(self.db)
		self.db = data

	def to_stream(self):
		return json.dumps(self.db)

	def output(self, dirpath):
		dirfile = opath.join(dirpath, self.dbfile)
		json.dump(self.db, dirfile)

	def has(self):
		return not len(self.db) == 0

	def __del__(self):
		# self.dbfile.flush()
		self.dbfile.close()
		del self.dbfile
		del self.db
