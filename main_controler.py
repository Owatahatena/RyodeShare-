import mysql.connector
from mysql.connector import errorcode
import datetime
import bathtimes_decider
import eating_times_decider
import eating_site_decider
import itertools

member_num=200;

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'yatsushironct',
            database = 'member_database',
        )

    def get_request_time(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM time_request_table')
        request_times = cur.fetchall()
        output_bath_request_times = []
        output_breakfast_request_times = []
        output_dinner_request_times = []
        for request_time in request_times:
            if(request_time[5] == datetime.date(2020,9,24)):
                output_bath_request_times.append((request_time[1],request_time[2]))
                output_breakfast_request_times.append((request_time[1],request_time[3]))
                output_dinner_request_times.append((request_time[1],request_time[4]))
            else:
                output_bath_request_times.append((request_time[1],100))
                output_breakfast_request_times.append((request_time[1],100))
                output_dinner_request_times.append((request_time[1],100))
        print(request_times)
        print(output_bath_request_times)
        print(output_breakfast_request_times)
        print(output_dinner_request_times)
       
        #入浴時間を決定する
        cur.execute('SELECT * FROM showerseat_table')
        showerseat_info = cur.fetchall()
        sorted_showerseat_info = sorted(showerseat_info,key=lambda seat_info: seat_info[1])
        print(sorted_showerseat_info)
        
        all_real_bathtimes = []

        for seat in range(20):
            cur.execute('SELECT boardernumber FROM showerseat_table WHERE showerseat = %s',(seat+1,))
            one_group_boarders = cur.fetchall()
            print('1グループ',one_group_boarders)
            one_group_request_times = []
            for x in one_group_boarders:
                cur.execute('SELECT bathtime_request FROM time_request_table WHERE boardernumber = %s', (x[0],))
                request_time = cur.fetchall()
                print(request_time)
                one_group_request_times.append((x[0],request_time[0][0]))
            
            real_bathtimes = bathtimes_decider.get_real_bathtime(one_group_request_times)   
            for real_bathtime in real_bathtimes:
                all_real_bathtimes.append(real_bathtime)

        sorted_all_real_bathtimes = sorted(all_real_bathtimes, key = lambda boarder_info : boarder_info[0])
        print(sorted_all_real_bathtimes)
           
        members_num_of_one_grade = []
        members_request_times = []
        all_grade_member=[]
        all_breakfast_times = []
        all_dinner_times = []
        #食事時間を決定する
        for grade in range(5):
            cur.execute('SELECT boardernumber FROM boarders_table WHERE grade = %s',(grade+1,))
            one_grade_member = cur.fetchall()
            one_grade_member = [ boardernumber[0] for boardernumber in one_grade_member]
            all_grade_member.append(one_grade_member)

            members_request_breakfasttimes = []
            members_request_dinnertimes = []
           # all_breakfast_times = []
           # all_dinner_times = []

            for boardernumber in one_grade_member:
                cur.execute('SELECT boardernumber,breakfasttime_request,dinnertime_request FROM time_request_table WHERE boardernumber = %s',(boardernumber,))
                single_request_times = cur.fetchall()
                print(single_request_times)
                members_request_breakfasttimes.append((single_request_times[0][0],single_request_times[0][1]))
                members_request_dinnertimes.append((single_request_times[0][0],single_request_times[0][2]))
            
            output_breakfasttimes = eating_times_decider.get_eating_times(members_request_breakfasttimes)
            all_breakfast_times.append(output_breakfasttimes)
            output_dinnertimes = eating_times_decider.get_eating_times(members_request_dinnertimes)
            all_dinner_times.append(output_dinnertimes)
            print("breakfast",all_breakfast_times,"dinner",all_dinner_times)
        
        single_all_breakfast_times = list(itertools.chain.from_iterable(all_breakfast_times))
        single_all_dinner_times = list(itertools.chain.from_iterable(all_dinner_times))

        sorted_all_breakfast_times = sorted(single_all_breakfast_times,key=lambda boarders_info: boarders_info[0])
        sorted_all_dinner_times = sorted(single_all_dinner_times,key= lambda boarders_info: boarders_info[0])
        
        print("breakfast",sorted_all_breakfast_times,"dinner",sorted_all_dinner_times)
        #print(members_num_of_one_grade)
        for boarder in range(member_num):        
            cur.execute('UPDATE time_real_table SET bathtime=%s,breakfasttime=%s ,dinnertime=%s,answer_date=%s WHERE boardernumber=%s',(sorted_all_real_bathtimes[boarder][1],sorted_all_breakfast_times[boarder][1],sorted_all_dinner_times[boarder][1],datetime.date.today(),sorted_all_real_bathtimes[boarder][0],))
            print(sorted_all_real_bathtimes[boarder][1],sorted_all_breakfast_times[boarder][1],sorted_all_dinner_times[boarder][1],datetime.date.today(),sorted_all_real_bathtimes[boarder][0])
        self.conn.commit()
        group_num = 4

        #食事の席順決定
        
        #同学年・同時間帯グループ抽出
        for grade in range(5):
            same_group_member = [[] for x in range(group_num)]
            sorted_same_group_member = [[] for x in range(group_num)]
            for boarder in all_breakfast_times[grade]:
                same_group_member[boarder[1]-1].append(boarder[0])
                
            for group in range(group_num):
                sorted_same_group_member[group] = sorted(same_group_member[group])
                conversation_table = [[] for x in range(len(sorted_same_group_member[group]))]
                conv_table_line = 0
                print(conversation_table)
                for first_member in sorted_same_group_member[group]:
                    for second_member in sorted_same_group_member[group]:
                        if first_member == second_member:
                            conversation_table[conv_table_line].append(-1.0)
                        else:
                            cur.execute('SELECT conversation_volume FROM conversation_volume_table WHERE self_boardernumber=%s AND other_boardernumber=%s',(first_member,second_member,))
                            conversation_volume = cur.fetchall()
                            conversation_table[conv_table_line].append(conversation_volume[0][0])
                    conv_table_line += 1
                
                deciding_seats = eating_site_decider.get_eating_seats(conversation_table)
                output_group_seats = []
                print("S",sorted_same_group_member)
                for seat in deciding_seats:
                    output_group_seats.append((sorted_same_group_member[group][seat],seat))
                print(output_group_seats)
                for seat in output_group_seats:
                    cur.execute('UPDATE seat_table SET breakfastseat=%s WHERE boardernumber=%s',(seat[1],seat[0],))
                    self.conn.commit()
            print(sorted_same_group_member)
            
        #食事席決定夕食版
        for grade in range(5):
            same_group_member = [[] for x in range(group_num)]
            sorted_same_group_member = [[] for x in range(group_num)]
            for boarder in all_dinner_times[grade]:
                same_group_member[boarder[1]-1].append(boarder[0])

            for group in range(group_num):
                sorted_same_group_member[group] = sorted(same_group_member[group])
                conversation_table = [[] for x in range(len(sorted_same_group_member[group]))]
                conv_table_line = 0
                print(conversation_table)
                for first_member in sorted_same_group_member[group]:
                    for second_member in sorted_same_group_member[group]:
                        if first_member == second_member:
                            conversation_table[conv_table_line].append(-1.0)
                        else:
                            cur.execute('SELECT conversation_volume FROM conversation_volume_table WHERE self_boardernumber=%s AND other_boardernumber=%s',(first_member,second_member,))
                            conversation_volume = cur.fetchall()
                            conversation_table[conv_table_line].append(conversation_volume[0][0])
                    conv_table_line += 1

                deciding_seats = eating_site_decider.get_eating_seats(conversation_table)
                output_group_seats = []
                print("S",sorted_same_group_member)
                for seat in deciding_seats:
                    output_group_seats.append((sorted_same_group_member[group][seat],seat))
                print(output_group_seats)
                for seat in output_group_seats:
                    cur.execute('UPDATE seat_table SET dinnerseat=%s WHERE boardernumber=%s',(seat[1],seat[0],))
                    self.conn.commit()
            print(sorted_same_group_member)

        cur.close()
        self.conn.commit()
    
    def get_bathtime(self):
        cur = self.conn.cursor()
        

db = DB()
db.get_request_time()
