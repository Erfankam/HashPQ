#!/usr/bin/python
from threading import Event
import time
import Queue


try:
    from collections import OrderedDict
except:
    # If could not, import it from local directory
    from OrderedDict import OrderedDict

      

DEFAULT_PRIORITY = 0
DEFAULT_QUEUE = 0

class HashPQueue(object):
    __slots__ = [ '__capacity',\
                      '__size',\
                      '__dic',\
                      '__lock',\
                ]

    def __new__(cls, *args, **kwargs):
        return super(HashPQueue, cls).__new__(cls, *args, **kwargs)

    def __str__(self):
        return self.__dic.__str__()

    def __repr__(self):
        return self.__dic.__str__()
    
    def __iter__(self):
        pass

    def __call__(self):
        pass

    def __init__(self, capacity=None, *args, **kwargs):
        self.__capacity = capacity
        self.__size = 0
        self.__dic = {}
        self.__lock = Event()

    def qsize(self):
        return self.__size

    def get(self):
        if not self.__dic:
            self.__lock.wait()
        # sort keys in list
        self.__dic.keys().sort()
        highestPriority = self.__dic.keys()[-1]
        # get high priority list
        highestPriorityList = self.__dic[highestPriority]
        item = highestPriorityList.popitem(last=False)
        self.__size -= 1
        if not self.__size:
            self.__lock.clear()
        else:
            self.__lock.set()
        if not highestPriorityList:
            del self.__dic[highestPriority]
        return item[1]

    def get_by_key(self, key, priority=None):
        if not self.__dic:
            self.__lock.wait()
        value = None
        if priority:
            try:
                value = self.__dic[priority].pop(key)
            except:
                return None
        try:
            for priority in self.__dic.keys():
                if key in self.__dic[priority]:
                    priorityList = self.__dic[priority]
                    value = self.__dic[priority].pop(key)
                    break
        except:
            return None
        self.__size -= 1
        if not self.__size:
            self.__lock.clear()
        else:
            self.__lock.set()
        if not self.__dic[priority]:
            del self.__dic[priority]
        return value

    def pick(self):
        pass

    def pick_nowait(self):
        pass

    def get_as_list(self):
        queue_list = self.__dic.keys()
        queue_list.sort(reverse=True)
        item_list = []
        for queue in queue_list:
            print queue
            for item in self.__dic[queue].items():
                print item
                item_list.append(item)
        return item_list

    def pick_by_key_nowait(self, key, priority=None):
        if not self.__dic:
            return None
        value = None
        if priority:
            try:
                value = self.__dic[priority][key]
            except:
                return None
        try:
            for priority in self.__dic.keys():
                if key in self.__dic[priority]:
                    value = self.__dic[priority][key]
                    break
        except:
            return None
        return value

    def get_dic(self):
        return self.__dic

    def pick_by_key(self, key, priority=None):
        if not self.__dic:
            self.__lock.wait()
        value = None
        if priority:
            try:
                value = self.__dic[priority][key]
            except:
                return None
        try:
            for priority in self.__dic.keys():
                if key in self.__dic[priority]:
                    value = self.__dic[priority][key]
                    break
        except:
            return None
        return value
    def get_by_key_nowait(self, key, priority=None):
        if not self.__dic:
            return None
        value = None
        if priority:
            try:
                value = self.__dic[priority].pop(key)
            except:
                return None
        try:
            for priority in self.__dic.keys():
                if key in self.__dic[priority]:
                    value = self.__dic[priority].pop(key)
                    break
        except:
            return None
        self.__size -= 1
        if not self.__size:
            self.__lock.clear()
        else:
            self.__lock.set()
        if not self.__dic[priority]:
            del self.__dic[priority]
        return value

    def put(self, item):
        if not item:
            return False
        if self.__size == self.__capacity:
            self.__lock.clear()
            self.__lock.wait()
        try:
            priority = item[0]
            key = item[1]
            value = item[2]
        except IndexError:
            try:
                priority = DEFAULT_PRIORITY
                key = item[0]
                value = item[1]
            except IndexError:
                priority = DEFAULT_PRIORITY
                key = DEFAULT_QUEUE
                value = item[0]
        except ValueError:
            return False
        except:
            return False
        if priority not in self.__dic.keys():
            self.__dic[priority] = OrderedDict()
        if key not in self.__dic[priority]:
            self.__size += 1
        self.__dic[priority][key] = value
        self.__lock.set()

    def get_nowait(self):
        if not self.__dic:
            return None
        # sort keys in list
        self.__dic.keys().sort()
        highestPriority = self.__dic.keys()[-1]
        # get high priority list
        highestPriorityList = self.__dic[highestPriority]
        item = highestPriorityList.popitem(last=False)
        self.__size -= 1
        if not self.__size:
            self.__lock.clear()
        else:
            self.__lock.set()
        if not highestPriorityList:
            del self.__dic[highestPriority]
        return item[1]

    def put_nowait_with_kwa(self, **kwargs):
       if not kwargs:
           return False
       if self.__size == self.__capacity:
           return False
       if self.__size == self.__capacity:
           self.__lock.clear()
           self.__lock.wait()
       if 'priority' in kwargs:
           priority = kwargs['priority']
       else:
           priority = DEFAULT_PRIORITY

       if 'key' in kwargs:
           key = kwargs['key']
       else:
           key = DEFAULT_QUEUE

       if 'value' in kwargs:
           value = kwargs['value']
       else:
           raise Exception
           return False

       if priority not in self.__dic.keys():
            self.__dic[priority] = OrderedDict()
       if key not in self.__dic[priority]:
            self.__size += 1
       self.__dic[priority][key] = value
       self.__lock.set()

    def put_nowait(self, item):
        if not item:
            return False
        if self.__size == self.__capacity:
            return False
        if self.__size == self.__capacity:
            self.__lock.clear()
            self.__lock.wait()
        try:
            priority = item[0]
            key = item[1]
            value = item[2]
        except IndexError:
            try:
                priority = DEFAULT_PRIORITY
                key = item[0]
                value = item[1]
            except IndexError:
                priority = DEFAULT_PRIORITY
                key = DEFAULT_QUEUE
                value = item[0]
        except:
            return False
        if priority not in self.__dic.keys():
            self.__dic[priority] = OrderedDict()
        if key not in self.__dic[priority]:
            self.__size += 1
        self.__dic[priority][key] = value
        self.__lock.set()

if __name__ == '__main__':
    pq = HashPQueue()
    pq.put_nowait((1, 3, 4))
    pq.put_nowait((1, 4, 3))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((4, 4, 6))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((3, 4, 6))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((5, 4, 6))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((1, 4, 6))
    pq.put_nowait((5, 4, 6))
    pq.put_nowait((8, 4, 7))
    pq.put_nowait((3, 6))
    pq.put_nowait((2,))
    pq.put_nowait_with_kwa(priority=3, value=3)
    pq.get_dic()
    print "get_as_list:", pq.get_as_list()
    print pq.qsize()

    print pq
    print pq.get_nowait()
    print pq
    #print pq.get_by_key(3)
    #print pq
    print pq.get_nowait()
    print pq
    print pq.get_nowait()
    print pq
    print pq.get_nowait()
    print pq
    print pq.get_nowait()
    print pq
    print pq.get_nowait()
    print pq


