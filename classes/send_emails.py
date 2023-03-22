from django.core.mail import EmailMessage
from app_spammy.models import Client, Newsletter, MessageToSend
import sqlite3
import pandas as pd


def take_data_from_db():
	conn = sqlite3.connect('db.sqlite3')
	query_text ='''
	SELECT
	app_spammy_newsletter.id, letter_subject, body_of_the_letter, email, frequency
	FROM
	app_spammy_newsletter
	INNER JOIN app_spammy_messagetosend
	ON app_spammy_messagetosend.newsletter_id=app_spammy_newsletter.id
	INNER JOIN app_spammy_newsletter_client
	ON app_spammy_newsletter.id=app_spammy_newsletter_client.newsletter_id
	INNER JOIN app_spammy_client
	ON app_spammy_newsletter_client.client_id=app_spammy_client.id
	'''
	query_part ='''
	WHERE(
		posting_date <= CURRENT_DATE
	OR(
		posting_time <= CURRENT_TIME
	AND
	posting_date = CURRENT_DATE
	)
	)
	AND(
		mailing_status='launched'
	)
	'''
	sql_query = pd.read_sql_query(query_text + query_part, conn)
	df = pd.DataFrame(sql_query)  #, columns=['product_id', 'product_name', 'price'])
	return df

def send_some_mails(data_for_emails):
	for index, row in data_for_emails.iterrows():
		what = row['letter_subject']
		why = row['body_of_the_letter']
		where = [row['email']]
		email = EmailMessage(what, why, to=where)
		email.send()
	print('success')

def change_data_in_db(some_info):
	adding_periods = {'once a day': 1, 'once a week': 7, 'once a month': 30}
	change_data = some_info.loc[:]['id']  # Выборка выборки. По ней будем менять отправка письма - планируем следующую отправку
	for i in set(change_data):
		data_frequency = some_info.query('id==@i').loc[0]['frequency']
		data_frequency = adding_periods[data_frequency]
		change_query = f'''
		UPDATE app_spammy_newsletter 
		SET posting_date = date('now','+{data_frequency} day')
		WHERE app_spammy_newsletter.id={i}
		'''
		conn = sqlite3.connect('db.sqlite3')
		cursor = conn.cursor()
		cursor.execute(change_query)
		conn.commit()
		conn.close()


def check_status():
	some_info = take_data_from_db()  # Выборка из бд. По ней будем отправлять письма
	send_some_mails(some_info)  # Отправляем письма по рассылке
	change_data_in_db(some_info)  # Отправляем запрос на изменение сроков отправки - в соответствии с периодичностью.