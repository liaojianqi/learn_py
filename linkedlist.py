# python实现链表
# python和java一样，只有值传递，每一个对象变量实质上是一个对象的指针
class Node():
    def __init__(self, v, next=None):
        self.v = v
        self.next = next

class List():
    def __init__(self, head=None):
        self.sz = 0
        self.head = head
    
    def append(self, v):
        self.insert(v, self.sz)
    
    def insert(self, v, index):
        if index > self.sz:
            raise ValueError('index out of bounds')
        self.sz += 1
        if index == 0:
            node = Node(v)
            node.next = self.head
            self.head = node
            return
        node = self.head
        for i in range(index - 1):
            node = node.next
        tmp = Node(v)
        tmp.next = node.next
        node.next = tmp

    def out(self):
        node = self.head
        while not node is None:
            print(node.v, end=' ')
            node = node.next
        print('')

a = [1,2,3,4,5]
l = List()
for i in a:
    l.append(i)
l.insert(0, 0)
l.insert(2.5, 3)
# l.insert(10, 30)
l.out()
print(l.sz)