import sqlite3
import bot_configuration
import datetime
from trade import Trade

class DB:
	def __connect__(self):
		return sqlite3.connect(bot_configuration.DATA_FOLDER + bot_configuration.DATABASE_NAME)

	def __create_table__(self, c):
		c.execute('''CREATE TABLE IF NOT EXISTS trades (create_date REAL PRIMARY KEY, ticker TEXT, entry_date REAL, exit_date REAL, shares REAL, 
			planned_exit_price REAL, planned_entry_price REAL, stop_loss REAL, actual_exit_price REAL, actual_entry_price REAL, status TEXT)''')

	def generate_default_trade(self, ticker, shares, entry, exit):
		return Trade(datetime.timestamp(datetime.now()), ticker, 0.0, 0.0, shares, exit, entry, 0.0, 0.0, 0.0, 'QUEUED')

	def get(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f'SELECT * FROM trades WHERE create_date={create_date}')
		data = c.fetchone()
		conn.close()
		if (data == None):
			return None
		else:
			return Trade(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10])


	def add(self, trade):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f'''INSERT INTO trades VALUES ({trade.create_date}, '{trade.ticker}', {trade.entry_date}, {trade.exit_date}, 
			{trade.shares}, {trade.planned_exit_price}, {trade.planned_entry_price}, {trade.stop_loss}, {trade.actual_exit_price}, {trade.actual_entry_price}, '{trade.status}')''')
		conn.commit()
		conn.close()
		return trade

	def cancel(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET status = 'CANCELLED' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def invalidate(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET status = 'MISSING' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def sell(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET status = 'SELLING' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def buy(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET status = 'BUYING' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def expire(self, create_date):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET status = 'EXPIRED' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def sync(self, create_date, position):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET shares = '{position.shares}', actual_entry_price = '{position.price}' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def update_stop_loss(self, create_date, stop_loss):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		c.execute(f"UPDATE trades SET stop_loss = '{stop_loss}' WHERE create_date = {create_date}")
		conn.commit()
		conn.close()

	def get_all_trades(self):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		trades = []

		for data in c.execute('SELECT * FROM trades ORDER BY create_date'):
			trades.append(Trade(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))

		conn.close()
		return trades

	def get_open_trades(self):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		trades = []

		for data in c.execute("SELECT * FROM trades WHERE status = 'OPEN' ORDER BY create_date ASC"):
			trades.append(Trade(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))

		conn.close()
		return trades

	def get_active_trades(self):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		trades = []

		for data in c.execute("SELECT * FROM trades WHERE status = 'OPEN' OR status = 'BUYING' OR status = 'SELLING' ORDER BY create_date ASC"):
			trades.append(Trade(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))

		conn.close()
		return trades

	def get_queued_trades(self):
		conn = self.__connect__()
		c = conn.cursor()
		self.__create_table__(c)
		trades = []

		for data in c.execute("SELECT * FROM trades WHERE status = 'QUEUED' ORDER BY create_date ASC"):
			trades.append(Trade(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))

		conn.close()
		return trades