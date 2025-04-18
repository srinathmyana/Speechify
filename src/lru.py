#!/usr/bin/env python3
from typing import Any, Optional

class Node :
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
class LRUCache:
    def __init__(self, item_limit: int):
        self.capacity = item_limit
        self.cache = {}

        self.head =Node("",0)
        self.tail =Node("",0)
        self.head.next =self.tail
        self.tail.prev =self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _insert_at_front(self, node: Node) :
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node


    def has(self, key = str)-> bool:
        return key in self.cache

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._insert_at_front(node)
        return node.value
       
    def set(self, key: str, value: Any):
        if key in self.cache :
             node = self.cache[key]
             node.value = value
             self.remove(node)
             self._insert_at_front(node)
        else:
             if len(self.cache) >= self.capacity:
                  lru_node = self.tail.prev
                  self._remove(lru_node)
                  del self.cache[lru_node.key]

             new_node = Node(key,value)
             self.cache[key] = new_node
             self._insert_at_front(new_node)

   