from django.core.mail import EmailMessage
from app_spammy.models import Client, Newsletter, MessageToSend
import sqlite3
import pandas as pd
from datetime import date
from datetime import timedelta


today = date.today()


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
	mail = EmailMessage('test', 'testtest', to=['dchenk@gmail.com'])
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
	change_data_in_db(some_info)  # Отправляем запрос на изменение сроков отправки - в соответствии с периодичностью.
	send_some_mails(some_info)  # Отправляем письма по рассылке

'''
#change date of newsletter using frequency#
def query_big(data):
    return f'UPDATE spammy_newsletter SET posting_date = CURRENT_DATE ' \
           f'+ {adding_periods[data]} {query_part} AND frequency=\'{data}\';'


def make_newsletter(*args, **kwargs):
    df = connect_do_db(query_small) # take data from db

    #need to change next mailing date #
    if len(df):
        #write query to change next mailing date#
        set_date_next_maling = ''
        for i in adding_periods.keys():
            set_date_next_maling += query_big(i)

        #make query to db to change next mailing date #
        connect_do_db(set_date_next_maling)

    # #send emails all addresses from df:#
    for index, row in df.iterrows():
        print(row)
        sub = row[0]
        bod = row[1]
        ema = row[2]
        send_a_message(sub, bod, [ema])
        time.sleep(0.5)



def send_a_message(sub, mes, recip):
    send_mail(
        subject=sub,
        message=mes,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recip, #['ju2ll@ya.ru'],
    )


def connect_do_db(query, *args, **kwargs):
    conn = psycopg2.connect(host='localhost', dbname='mailing', user='oleg', password='12345')
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                try:
                    info_from_db = cur.fetchall()
                except:
                    info_from_db = None
    finally:
        conn.close()
    return pd.DataFrame(info_from_db)
'''
