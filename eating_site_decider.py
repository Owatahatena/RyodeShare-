from heapq import heappush, heappop, heapify

class ESD:
    """
    a: adjacent_matrix
    """
    def __init__(self,A):
        #seated_number = len(A)
        self.seated_number = len(A)
        self.next_A = [] # 隣接管理のリスト
        for index_i,l in enumerate(A):
            self.next_A.append([(cost, index_j, index_i) for index_j, cost in enumerate(l) if cost != -1])

        self.visited = [0] * self.seated_number
        self.v_c = [0] * self.seated_number
        self.connection = 0
        self.que = [(0, 0, '_')] #cost,i,j
        heapify(self.que) 
        self.spanning_tree = {}

    def optimaize(self):
        total_cost = 0
        while len(self.que):
            #cost最小値をヒープから取り出す
            cost, i, j = heappop(self.que)
            #すでに確定済みのノードだったらパス
            if self.visited[i]:
                continue

            #制約：エッジの数が2以下
            if j != '_':
                if self.v_c[i] >= 2 or self.v_c[j] >= 2:
                    continue

            #ノード間の指定があるとき
            if j != '_':
                if not self.spanning_tree:
                    self.spanning_tree[i] = [j]
                    self.spanning_tree[j] = [i]
                    self.v_c[j] += 1
                    self.v_c[i] += 1
                else: 
                    #ノードi の接続先は確定しているか？
                    try:
                        self.spanning_tree[i].append(j)
                        self.v_c[i] += 1

                    except:
                        self.spanning_tree[i] = [j]
                        self.v_c[i] += 1

                    #ノードj の接続先は確定しているか？
                    try:
                        self.spanning_tree[j].append(i)
                        self.v_c[j] += 1

                    except:
                        self.spanning_tree[j] = i
                        self.v_c[j] += 1

            self.visited[i] = 1
            self.connection +=1
            total_cost += cost

            for next_a in self.next_A[i]:
                heappush(self.que,next_a)

            #全てのノード同士の接続が確定したら
            if self.connection == self.seated_number:
                break
              
        return total_cost,self.spanning_tree

#if __name__ == '__main__':
def get_eating_seats(A):
    #A = [[-1,  3,  4,  1, -1],
     #  [ 3, -1, -1,  1, -1],
      # [ 4, -1, -1,  1,  1],
      # [ 1,  1,  1, -1,  3],
      # [-1, -1,  1,  3 ,-1]]

    e = ESD(A)
    a,s = e.optimaize()

    #最小全域木から席順を求めるコード
    print(a,s)
    A = []
    B = []
    for k,v in s.items():
        if len(A) == 0 and len(v) == 1:
            A.append(k)
    output_seats=[]

    print(A[0])
    output_seats.append(A[0])
    B.append(A[0])
    serched = []
    while len(B) != 0:
        k = B.pop()
        serched.append(k)
        for i in s[k]:
            if i not in serched:
                print(i)
                output_seats.append(i)
                B.append(i)
    
    print(output_seats)
    return output_seats
    
