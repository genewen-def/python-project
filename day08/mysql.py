import pymysql
conn=pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='day07'
)

cur=conn.cursor()
sql='insert into student values (3,"李四",18,140,"2021-01-16")'
print(sql)
row=cur.execute(sql)

print(row)

conn.commit()
cur.close()
conn.close()
