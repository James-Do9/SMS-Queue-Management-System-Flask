class Queue:

    def __init__(self):
        self._queue = [{"name":"John", "phone":"+14074606665"}]
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        self._queue.insert(0, item) #inserts the item at the first position

    def dequeue(self):
        return self._queue.pop() #pops at the end

    def get_queue(self):
        return self._queue #gives back the array itself

    def size(self):
        return len(self._queue) 