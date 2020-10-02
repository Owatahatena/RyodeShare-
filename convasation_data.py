from DB import DB
import itertools


member_num = 200

member_index = []
for n in range(member_num):
    member_index.append(1000+n)


l = itertools.permutations(member_index,2)

index_score = []
for i in list(l):
    index_score.append((0,i[0],i[1],0.0))


print(index_score[0])
db = DB()
#sql = 'insert into conversation_volume_table ("self_boardernumber","other_boardernumber","conversation_volume") values (%s,%s,%s)'

sql = 'insert into conversation_volume_table values (%s,%s,%s,%s)'

db.insert_many(sql,index_score)


