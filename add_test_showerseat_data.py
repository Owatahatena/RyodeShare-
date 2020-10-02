from DB import DB

member_num = 200

member_index = []

for n in range(member_num):
    member_index.append((1000+n,n%20+1))

sql = 'insert into showerseat_table (boardernumber,showerseat) values (%s,%s)'

print(member_index)
db = DB()
db.insert_many(sql,member_index)
