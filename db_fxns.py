import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable1(task TEXT,task_status TEXT,task_due_date DATE ,priority TEXT)')


def add_data(task,task_status,task_due_date,priority):
	c.execute('INSERT INTO taskstable1(task,task_status,task_due_date,priority) VALUES (?,?,?,?)',(task,task_status,task_due_date,priority))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM taskstable1')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT task FROM taskstable1')
	data = c.fetchall()
	return data

def get_task(task):
	c.execute('SELECT * FROM taskstable1 WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable1 WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()
	return data


def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	c.execute("UPDATE taskstable1 SET task =?,task_status=?,task_due_date=? ,priority=? ,WHERE task=? and task_status=? and task_due_date=? ,priority=? ",(new_task,new_task_status,new_task_date,new_priority,task,task_status,task_due_date,priority))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(task):
	c.execute('DELETE FROM taskstable1 WHERE task="{}"'.format(task))
	conn.commit()
