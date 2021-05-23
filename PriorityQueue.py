class PriorityQueue(object):
    def __init__(self, greatest=False):
        self.queue = []
        self.greatest = greatest

    def __str__(self):
        return ' '.join([str(i[0]) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    def isNotEmpty(self):
        return not self.isEmpty()

    # for inserting an element in the queue
    def add(self, data, priority):
        self.queue.append((data, priority))

    # for popping an element based on Priority
    def pop(self):
        try:
            index = 0
            for i in range(len(self.queue)):
                if self.greatest:
                    if self.queue[i][1] > self.queue[index][1]:
                        index = i
                else:
                    if self.queue[i][1] < self.queue[index][1]:
                        index = i
            item = self.queue[index]
            del self.queue[index]
            return item[0]
        except IndexError:
            print()
            exit()
