from DB import DB
import random
import itertools

db = DB()
sql = 'select boardernumber from boarders_table where grade = 5'

data = db.all_select(sql)
random_boardernumber = random.sample(data,13)

r_b = [i[0] for i in random_boardernumber]

p_r_b = itertools.permutations(r_b,2)

l = list(p_r_b)
print(l[0])

sql2 = "select conversation_volume from conversation_volume_table where self_boardernumber = %s and other_boardernumber = %s"

D = []
for ll in l:
    s = sql2%ll
    D.append(db.all_select(s))

print(D)
