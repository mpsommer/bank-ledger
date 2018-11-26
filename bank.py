from __future__ import print_function
from const import PREFIX, USER, ACTION
import sys
from store import store
store = store()

class bank(object):
	def __init__(self):
		self.redis = store.redis_connect()

	def signup(self, username, password):
		"""
		If username is not taken, create account with key=username, and
		value=password in Redis, then update session time and set user account
		balance to 0.
		"""
		rs = self.redis
		key = PREFIX['account'] + username
		if rs.exists(key):
			sys.exit(USER['taken_username'])
		else:
			print(USER['create_account'])
			store.create_account(username, password)
			store.update_session_time(username)
			key = PREFIX['balance'] + username
			rs.set(key, store.dollars_to_cents('0'))
			return True

	def login(self, username, password):
		"""
		If username not found, print and exit.
		If wrong password, print and exit.
		If valid credentials, print, update session time, return True.
		"""
		rs = self.redis
		key = PREFIX['account'] + username
		if not rs.exists(key):
			sys.exit(USER['wrong_username'])
		elif rs.get(key) != password:
			sys.exit(USER['invalid_password'])
		else:
			print(USER['login_success'])
			store.update_session_time(username)
			return True

	def deposit(self, username, deposit):
		"""
		On successful deposit, print deposited amount and new balance. Update
		session time. return True.
		"""
		if store.is_active_session(username):
			if store.deposit(username, deposit):
				print(ACTION['deposit'] + deposit)
				print(USER['balance'], store.get_balance(username))
			store.update_session_time(username)
			return True
		else:
			self.instruct_login()

	def withdraw(self, username, withdraw):
		"""
		On successful withdraw, print withdraw amount and new balance.
		Update session time.
		"""
		if store.is_active_session(username):
			if store.withdraw(username, withdraw):
				print(ACTION['withdraw'] + withdraw)
				print(USER['balance'], store.get_balance(username))
			store.update_session_time(username)
			return True
		else:
			self.instruct_login()

	def balance(self, username):
		"""
		Print the current balance.
		"""
		if store.is_active_session(username):
			print(USER['balance'], store.get_balance(username))
			store.update_session_time(username)
			return True
		else:
			self.instruct_login()

	def transactions(self, username):
		"""
		Print the current balance and user history.
		Note: the history only prints the 100 most recent transactions and a 
		transcation is defined as a deposit or withdraw.
		"""
		if store.is_active_session(username):
			print(USER['balance'], store.get_balance(username))
			print(USER['history'])
			events = store.get_transactions(username)
			if events is not None:
				assert len(events) <= 100
				for event in events:
					print(event)
			store.update_session_time(username)
			return True
		else:
			self.instruct_login()

	def logout(self, username):
		"""
		Deactivate user session and print.
		"""
		store.deactivate_session(username)
		print(USER['logout_success'])
		return True

	def instruct_login(self):
		"""
		Instrcucts user to login, and exits the application.
		"""
		sys.exit(USER['instruct_login'])