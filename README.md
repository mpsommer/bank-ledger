# bank-ledger
### A bank ledger application built around Redis with python 2.7.
This application allows a user to signup for an account, login to a session deposit values, withdraw values, check the balance, get transaction history, and logout of session.

#### NOTE:
* The username is used as the account identifier and therefore is passed along with all commands.
* Multiple commands can be passed, but multiple commands of the same type are not supported (e.g. ```run.py -d foo 2 -d foo 2``` will not work).
* Transaction history keeps track of only the 100 most recent transactions and only dposit and withdraw are considered transactions.


# Requirements/Installation
### Redis is required. Ensure Redis is installed on system and Redis server is running.
```bash
# Steps for install.
git clone git@github.com:mpsommer/bank-ledger.git
cd bank-ledger
pip install -r requirements.txt
```

# Commands
```python
# For list of commands.
python run.py -h 

# To create account for ledger.
python run.py -s USERNAME PASSWORD

# To login into existing account.
python run.py -l USERNAME PASSWORD

# To deposit into an account.
python run.py -d USERNAME VALUE

# To withdraw from an account.
python run.py -w USERNAME VALUE

# To check the balance of an account.
python run.py -b USERNAME

# To get transaction history.
python run.py -t USERNAME

# To logout of an account.
python run.py -e USERNAME

# To run the test
python test_bank.py
```

# TODO
* Allow for changing of password
* Test store class directly.
* Break up tests into smaller functions.
* Use logger instead of print().
