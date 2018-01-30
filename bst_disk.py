# a binary search tree on disk
# TODO: delete node
import json, os

BYTEORDER = 'big'
INT_SIZE = 4
NOT_EXIST = (2 ** 32) - 1

class Node():
    def __init__(self, addr=NOT_EXIST, begin=NOT_EXIST, end=NOT_EXIST, l=NOT_EXIST, r=NOT_EXIST):
        self.addr=addr
        self.begin=begin
        self.end=end
        self.l=l
        self.r=r


class BST():
    def __init__(self, name):
        self.index = open(name + "_index", 'w+b') # open and truncate
        self.data = open(name + "_data", 'w+b')
        self.root = NOT_EXIST

    @staticmethod
    def node_to_bytes(node):
        return (node.addr.to_bytes(4, BYTEORDER) +
                node.begin.to_bytes(4, BYTEORDER) +
                node.end.to_bytes(4, BYTEORDER) +
                node.l.to_bytes(4, BYTEORDER) +
                node.r.to_bytes(4, BYTEORDER))
    
    @staticmethod
    def bytes_to_node(bs):
        node = Node()
        node.addr = node.addr.from_bytes(bs[:INT_SIZE], BYTEORDER)
        node.begin = node.begin.from_bytes(bs[INT_SIZE:2*INT_SIZE], BYTEORDER)
        node.end = node.end.from_bytes(bs[2*INT_SIZE:3*INT_SIZE], BYTEORDER)
        node.l = node.l.from_bytes(bs[3*INT_SIZE:4*INT_SIZE], BYTEORDER)
        node.r = node.r.from_bytes(bs[4*INT_SIZE:], BYTEORDER)
        return node
    
    @staticmethod
    def get_node(f, addr):
        p = f.tell()
        f.seek(addr)
        bs = f.read(INT_SIZE * 5)
        f.seek(p)
        return BST.bytes_to_node(bs)
    
    @staticmethod
    def get_data(f, begin, end):
        p = f.tell()
        f.seek(begin)
        bs = f.read(end - begin)
        f.seek(p)
        return json.loads(bytes.decode(bs))

    @staticmethod
    def update_node(f, node):
        p = f.tell()
        f.seek(node.addr)
        f.write(BST.node_to_bytes(node))
        f.flush()
        f.seek(p)

    def insert(self, v):
        if self.root == NOT_EXIST:
            node = Node(0)
            node.begin = self.data.tell()
            self.data.write(str.encode(json.dumps(v)))
            self.data.flush()
            node.end = self.data.tell()
            self.root = node.addr
            # write index
            self.index.write(self.node_to_bytes(node))
            return
        node = self.get_node(self.index, self.root)
        print('node = ', node.__dict__)
        vv = self.get_data(self.data, node.begin, node.end)
        while True:
            if vv == v:
                return
            elif vv > v:
                # left
                if node.l == NOT_EXIST:
                    # add to left
                    new_node = Node(self.index.tell())
                    new_node.begin = self.data.tell()
                    self.data.write(str.encode(json.dumps(v)))
                    self.data.flush()
                    new_node.end = self.data.tell()
                    # write index
                    print('new_node = ', str(self.node_to_bytes(new_node)))
                    self.index.write(self.node_to_bytes(new_node))
                    self.index.flush()
                    # update node(.l)
                    node.l = new_node.addr
                    self.update_node(self.index, node)
                    return
                node = self.get_node(node.l)
                vv = self.get_data(self.data, node.begin, node.end)
            else:
                # right
                if node.r == NOT_EXIST:
                    # add to right
                    new_node = Node(self.index.tell())
                    new_node.begin = self.data.tell()
                    self.data.write(str.encode(json.dumps(v)))
                    self.data.flush()
                    new_node.end = self.data.tell()
                    # self.root = new_node.addr
                    # write index
                    self.index.write(self.node_to_bytes(new_node))
                    self.index.flush()
                    # update node(.r)
                    node.r = new_node.addr
                    self.update_node(self.index, node)
                    return
                node = self.get_node(node.r)
                vv = self.get_data(self.data, node.begin, node.end)


b = BST('redis')
b.insert('bb')
b.insert('aa')
b.insert('cc')