from DB import DB
import itertools
import hashlib

member_num = 200

member_index = []
for n in range(member_num):
    member_index.append(1000+n)

member_data = []
grade = 0
classes = ['MI','AC','BC']
import random
for index,i in enumerate(member_index):
    if index < 40:
        grade = 1

    elif index < 80:
        grade = 2

    elif index < 120:
        grade = 3

    elif index < 160:
        grade  = 4

    elif index < 200:
        grade = 5

    c = random.choice(classes)
    member_data.append((0,i,grade,c,hashlib.md5('0'.encode('utf-8')).hexdigest()))

#print(index_score[0])
print(member_data[0])

db = DB()
#sql = 'insert into conversation_volume_table ("self_boardernumber","other_boardernumber","conversation_volume") values (%s,%s,%s)'

sql = 'insert into boarders_table values (%s,%s,%s,%s,%s)'

db.insert_many(sql,member_data)


