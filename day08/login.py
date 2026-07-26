import pymysql

conn=pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='day07'
)
cur=conn.cursor()
username=input('请输入你的用户名：')
password=input('请输入你的密码：')

sql=''
row=cur.execute(sql)

print(row)

conn.commit()
cur.close()
conn.close()