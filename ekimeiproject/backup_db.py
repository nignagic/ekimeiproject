import datetime
import subprocess
import dropbox

dbx = dropbox.Dropbox('APITOKEN')
now = datetime.datetime.now()
db_file_name = f'{now.hour}-{now.minute}-{now.second}.db'
dropbox_path = f'/mydjango/{now.year}/{now.month}/{now.day}/{db_file_name}'
subprocess.run(f'mysqldump -u username databasename -ppassword > {db_file_name}', shell=True)

print(now, 'backup start')
dbx.files_upload(open(db_file_name, 'rb').read(), dropbox_path,  mode=dropbox.files.WriteMode('overwrite'))
print(datetime.datetime.now(), 'backup end')