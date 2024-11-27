import datetime
import subprocess
import dropbox
import environ

env = environ.Env()
env.read_env('.env')

dbx = dropbox.Dropbox(f'{env("DROPBOX_KEY")}')
now = datetime.datetime.now()
db_file_name = f'{now.hour}-{now.minute}-{now.second}.db'
dropbox_path = f'/mydjango/{now.year}/{now.month}/{now.day}/{db_file_name}'
subprocess.run(f'mysqldump -u {env("MYSQL_USER")} {env("MYSQL_DATABASE")} -p{env("MYSQL_PASSWORD")} > {db_file_name}', shell=True)

print(now, 'backup start')
dbx.files_upload(open(db_file_name, 'rb').read(), dropbox_path,  mode=dropbox.files.WriteMode('overwrite'))
print(datetime.datetime.now(), 'backup end')
