class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.next = None
    
    def insert(self, interval):
        if interval.end < self.start:
            interval.next = self
            return interval
        
        if interval.start > self.end:
            if self.next is None:
                self.next = interval
            else:
                self.next = self.next.insert(interval)
            return self
        
        interval.start = min(self.start, interval.start)
        interval.end = max(self.end, interval.end)
        if self.next is not None:
            n = self.next.insert(interval)
            if n is not interval:
                interval.next = n
        return interval

    def length(self):
        return self.end - self.start

    def total_length(self):
        return self.length() + (0 if self.next is None else self.next.total_length())

    def non_covered_x(self, limit):
        next_bound = limit if self.next is None else self.next.start
        if self.end + 1 < next_bound:
            return self.end + 1
        return None if self.next is None else self.next.non_covered_x(limit)
