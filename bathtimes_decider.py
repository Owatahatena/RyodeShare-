#希望時間が1人だけであれば、希望通りの時間にする
#複数人いる場合：
#全体的に希望時間と決定時間の差を詰めるためには
#希望時間と残りの入浴時間をそれぞれソートし、それらに対応したものを
#実際の入浴時間とする。
"""
多くの人は、入浴をはじめ、生活における様々な行動は自分の都合のいい時間もしくは好きな時間に行いたいものである。
そのため、できるだけ多くの人が希望の時間もしくは希望に近い時間に入浴できるように最適化を行う。

最適化の処理は以下の通り。
1.　1つの時間に対して希望者が1人だけであれば、希望通りの時間にする。
2.1　1つの希望時間に対して複数人いる場合は、まず同じ希望時間の人を集めてグループにする。
  2　入浴希望時間が早い方から、希望者1人のみの時間を除く、残りの時間の中で早い時間をグループの中の人数の数に応じて振り分ける。
  3　グループごとに振り分けられた入浴時間をグループ内でランダムに各人に振り分ける。

例
[1, 2, 3, 3, 4, 4, 5, 6, 6, 6]
[1, 2, 3, 4, 6, 7, 5, 8, 9, 10]

"""
import random
class Bath_request_time_data:
    def __init__(self,request_data):
        self.request_data = request_data
        self.request_times = self.__get_request_time()
        self.unique_request_times = self.__get_uniest_request_times()
        self.rest_request_times = self.__get_rest_request_times()
        self.size = len(self.request_data)

    def __get_request_time(self):
        return [request_datum[1] for request_datum in self.request_data]

    def __get_uniest_request_times(self):
        unieuq_request_times = []
        for request_time in self.request_times:
            if self.request_times.count(request_time) == 1:
                unieuq_request_times.append(request_time)
        return unieuq_request_times

    def __get_rest_request_times(self):
        rest_request_times = set(range(1,len(self.request_data)+1)) - set(self.unique_request_times)
        return list(rest_request_times)

    def is_duplication(self):
        duplication_request_times = []
        for request_time in self.request_times:
            if self.request_times.count(request_time) > 1:
                duplication_request_times.append(request_time)

        if duplication_request_times:
            return True
        else:
            return False

class Optimizer:
    def __init__(self,data):
        self.data = data

    def optimize(self):
        if self.data.is_duplication():
            randomized_boarders_info = random.sample(self.data.request_data,self.data.size)
            sorted_boarders_info_list=sorted(randomized_boarders_info,key=lambda boarders_info: boarders_info[1])
            output_boarders_info=[]

            #最終決定した入浴時間をセット
            for request_data in sorted_boarders_info_list:
                if self.data.unique_request_times.count(request_data[1]) > 0:
                    output_boarders_info.append(request_data)
                else:
                    output_boarders_info.append((request_data[0], self.data.rest_request_times.pop(0)))

            print('abbbb',self.data.rest_request_times)

            return output_boarders_info

        else:
            return self.data

def get_real_bathtime(boarders_info_list):
    request_data = Bath_request_time_data(boarders_info_list)
    optimizer = Optimizer(request_data)
    optimized_request_data = optimizer.optimize()
    return optimized_request_data
    a=sorted(optimized_request_data,key=lambda boarders_info: boarders_info[1])
    print(a)

boarders_info_list=[(1,7),(2,1),(3,4),(4,2),(5,1),(6,1),(7,5),(8,2),(9,5),(10,1),
                    (11,17),(12,1),(13,4),(14,12),(15,1),(16,11),(17,5),(18,2),(19,5),(20,1),
                    (21,17),(22,12),(23,55),(24,53),(25,49),(26,19),(27,21),(28,25),(29,12),(30,2),
                    (31,37),(32,15),(33,34),(34,11),(35,28),(36,11),(37,2),(38,20),(39,50),(40,34),
                    (41,57),(42,12),(43,43),(44,61),(45,23),(46,19),(47,18),(48,21),(49,21),(50,17),
                    (51,47),(52,12),(53,62),(54,43),(55,11),(56,20),(57,12),(58,40),(59,42),(60,2),
                    (61,3),(62,2),(63,4),(64,1),(65,1),(66,21),(67,25),(68,39),(69,35),(70,3)]

print(len(boarders_info_list))
request_data = Bath_request_time_data(boarders_info_list)
print(request_data.rest_request_times)
optimizer = Optimizer(request_data)
optimized_request_data = optimizer.optimize()
print('aaa',optimized_request_data)
a=sorted(optimized_request_data,key=lambda boarders_info: boarders_info[1])
print(a)
