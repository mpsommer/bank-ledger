from __future__ import print_function
import unittest
from const import PREFIX, USER
from bank import bank
bank = bank()


class TestBank(unittest.TestCase):
	redis = bank.redis
	username = 'foo'
	password = 'bar'
	account_key = PREFIX['account'] + username

	def test_signup(self):
		if self.redis.exists(self.account_key):
			self.redis.delete(self.account_key)

		# Test signup
		bank.signup(self.username, self.password)
		value = self.redis.get(self.account_key)
		self.assertEquals(self.password, value)
		try:
			bank.signup(self.username, self.password)
		except SystemExit as error:
			self.assertEquals(error.message, USER['taken_username'])
		
		# Test Login
		self.assertTrue(bank.login(self.username, self.password))
		try:
			bank.login(self.username, 'badpassword')
		except SystemExit as error:
			self.assertEquals(error.message, USER['invalid_password'])
		try:
			bank.login('badusername', 'badpassword')
		except SystemExit as error:
			self.assertEquals(error.message, USER['wrong_username'])

		# Test deposit
		self.assertTrue(bank.deposit(self.username, '3.14'))
		self.assertTrue(bank.deposit(self.username, '3.14'))

		# Test withdraw
		self.assertTrue(bank.withdraw(self.username, '1.03'))
		self.assertTrue(bank.withdraw(self.username, '1.03'))

		# Test balance
		self.assertTrue(bank.balance(self.username))

		# Test transactions:
		for i in range(0, 100):
			self.assertTrue(bank.deposit(self.username, '3.14'))
			self.assertTrue(bank.transactions(self.username))

		# Test logout
		self.assertTrue(bank.logout(self.username))
		try:
			bank.deposit(self.username, '3.14')
		except SystemExit as error:
			self.assertEquals(error.message, USER['instruct_login'])


def main():
	# Reference:
	# https://stackoverflow.com/questions/2090479/valueerror-no-such-test-method-in-class-myapp-tests-sessiontestcase-runtes
	suite = unittest.TestSuite()
	for method in dir(TestBank):
		if method.startswith('test'):
			suite.addTest(TestBank(method))
	unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
	main()