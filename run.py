from __future__ import print_function
import argparse
from bank import bank
from const import HELP, USER
bank = bank()

def get_args():
	parser = argparse.ArgumentParser(
		description='Ledger program',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-s', '--signup', nargs=2, metavar=('USERNAME', 'PASSWORD'), default=argparse.SUPPRESS, help=HELP['signup'])
	parser.add_argument('-l', '--login', nargs=2, metavar=('USERNAME', 'PASSWORD'), default=argparse.SUPPRESS, help=HELP['login'])
	parser.add_argument('-d', '--deposit', nargs=2, metavar=('USERNAME', 'DEPOSIT'), default=argparse.SUPPRESS, help=HELP['deposit'])
	parser.add_argument('-w', '--withdraw', nargs=2, metavar=('USERNAME', 'WITHDRAW'), default=argparse.SUPPRESS, help=HELP['withdraw'])
	parser.add_argument('-b', '--balance', metavar=('USERNAME'), default=argparse.SUPPRESS, help=HELP['balance'])
	parser.add_argument('-t', '--transactions', metavar=('USERNAME'), default=argparse.SUPPRESS, help=HELP['transactions'])
	parser.add_argument('-e', '--logout', metavar=('USERNAME'), default=argparse.SUPPRESS, help=HELP['logout'])
	args = parser.parse_args()
	return args

def main():
	args = get_args()
	if 'signup' in args:
		bank.signup(args.signup[0], args.signup[1])
	if 'login' in args:
		bank.login(args.login[0], args.login[1])
	if 'deposit' in args:
		username = args.deposit[0]
		deposit = args.deposit[1]
		if is_number(deposit) == False or float(deposit) <= 0.0:
			print(USER['invalid_number'])
			return
		bank.deposit(username, deposit)
	if 'withdraw' in args:
		username = args.withdraw[0]
		withdraw = args.withdraw[1]
		if is_number(withdraw) == False or float(withdraw) <= 0.0:
			print(USER['invalid_number'])
			return
		bank.withdraw(username, withdraw)
	if 'balance' in args:
		username = args.balance
		bank.balance(username)
	if 'transactions' in args:
		username = args.transactions
		bank.transactions(username)
	if 'logout' in args:
		username = args.logout
		bank.logout(username)

def is_number(value):
	try:
		float(value)
		return True
	except ValueError:
		pass
	return False

if __name__ == "__main__":
	main()