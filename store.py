from __future__ import print_function
import redis
import time
import json
import os
import ConfigParser
from const import PREFIX


class store(object):
	def __init__(self):
		self._redis = None
		self.session_length = 5 * 60
		self.config = self.get_configfile()

	def get_configfile(self):
		"""
		Parse the ledger.cfg file.
		"""
		config_file = ConfigParser.ConfigParser()
		dirname = os.path.dirname(__file__)
		path = os.path.join(dirname, 'ledger.cfg')
		config_file.read(path)
		return config_file

	def redis_connect(self):
		"""
		Establish connection to Redis if there isn't one.
		"""
		if self._redis is None:
			self._redis = redis.StrictRedis(
				host=self.config.get('redis', 'host'),
				port=self.config.get('redis', 'port'),
				db=self.config.get('redis', 'db')
			)
		return self._redis

	def create_account(self, username, password):
		"""
		User account is keyed off of the username and the value is the
		password.
		"""
		rs = self.redis_connect()
		key = PREFIX['account'] + username
		rs.set(key, password)

	def update_session_time(self, username):
		"""
		This resets the session time for a user to current time, which means
		the session will not deactivate until self.session_length has expired.
		"""
		rs = self.redis_connect()
		key = PREFIX['session'] + username
		rs.set(key, time.time())

	def deactivate_session(self, username):
		"""
		Sets the user session time to be longer then self.session_length which
		deactivates the session forcing the user to login again before
		completing any other tasks.
		"""
		rs = self.redis_connect()
		key = PREFIX['session'] + username
		invalid_time = time.time() - self.session_length * 2
		rs.set(key, invalid_time)

	def is_active_session(self, username):
		"""
		Returns true if remaining session time is less than the
		self.session_length. 
		"""
		rs = self.redis_connect()
		is_active = False
		account_key = PREFIX['account'] + username
		session_key = PREFIX['session'] + username
		value = rs.get(session_key)
		if value is None:
			value = 0
		remaining_time = time.time() - float(value)
		if rs.exists(account_key) and remaining_time < self.session_length:
			is_active = True
		return is_active

	def deposit(self, username, value):
		"""
		On successful insertion of value into balance key, record transaction
		and return True.
		"""
		rs = self.redis_connect()
		key = PREFIX['balance'] + username
		deposit = self.dollars_to_cents(value)
		balance = int(rs.get(key))
		new_balance = balance + deposit
		assert new_balance > balance
		result = rs.set(key, new_balance)
		if result == True:
			self.record_transaction(username, 'DEPOSIT', float(value))
		return result

	def withdraw(self, username, value):
		"""
		On successful withdraw of value from balance key, record transaction
		and return True.
		"""
		result = False
		rs = self.redis_connect()
		key = PREFIX['balance'] + username
		balance = int(rs.get(key))
		withdraw = self.dollars_to_cents(value)
		if balance < 0 or balance - withdraw < 0:
			print('Insufficient funds for withdraw.')
		else:
			new_balance = balance - withdraw
			assert new_balance < balance
			result =  rs.set(key, new_balance)
			if result == True:
				self.record_transaction(username, 'WITHDRAW', float(value))
		return result

	def get_balance(self, username):
		"""
		Gets the balance from cache, formats and returns.
		"""
		rs = self.redis_connect()
		key = PREFIX['balance'] + username
		balance = self.cents_to_dollars(rs.get(key))
		return balance

	def record_transaction(self, username, action, value):
		"""
		Records the 100 most recent withdraws and deposit transactions. 
		Returns string of transaction time, action and value. 
		"""
		rs = self.redis_connect()
		key = PREFIX['history'] + username
		assert action is 'WITHDRAW' or action is 'DEPOSIT'
		value = time.strftime(
			'%Y-%m-%d %H:%M:%S', time.gmtime()
		) + ' ' + action +': ' + str(value)

		if rs.exists(key):
			values = json.loads(rs.get(key))
			if len(values) == 100:
				values.pop(0)
			values.append(value)
			rs.set(key, json.dumps(values))
		else:
			values = []
			values.append(value)
			rs.set(key, json.dumps(values))

	def get_transactions(self, username):
		"""
		Returns list of transactions or None
		"""
		rs = self.redis_connect()
		key = PREFIX['history'] + username
		events = rs.get(key)
		if events is None:
			print('There are no recent transactions.')
		else:
			return json.loads(events)

	def dollars_to_cents(self, value):
		"""
		Convert a string representation of dollars and cents to int.
		e.g. 3.14 -> 314
		"""
		return int(float(value)* 100)
	
	def cents_to_dollars(self, value):
		"""
		Converts int to cents to dollars and cents.
		"""
		return float(value) / 100
