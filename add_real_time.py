from DB import DB
import random
import datetime

member_num = 200

member_index = []
for n in range(member_num):
    member_index.append((1000+n,random.randint(1,4),random.randint(1,4),random.randint(1,4),datetime.date(2020,9,24)))

sql = 'insert into time_real_table (boardernumber,bathtime,breakfasttime,dinnertime,answer_date) values (%s,%s,%s,%s,%s)'

print(member_index)
db = DB()
db.insert_many(sql,member_index)
