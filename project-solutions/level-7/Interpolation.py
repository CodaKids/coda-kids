"""
This module contains methods for automatically 
updating object members between two different values.
"""
# data used to store all lerps
_data = {}

def lerp_iter(start, end, percent):
    """
    Internal lerp helper function.
    """
    return start + percent * (end - start)

class LerpData:
    """Data on lerp"""
    def __init__(self, member, end, duration):
        self.member = member
        self.start = None
        self.end = end
        self.time = 0
        self.duration = duration

    def update(self, obj, delta_time):
        """Update lerp and check if done."""
        if self.time is 0:
            self.start = getattr(obj, self.member)

        self.time += delta_time / self.duration
        setattr(obj, self.member, lerp_iter(self.start, self.end, self.time))
        if self.time >= 1:
            setattr(obj, self.member, self.end)
            return True
        return False

def append(obj, member, end, duration=1):
    """
    Add an object and member to change.

        # move to 0, 0 over 2 seconds
        coda.add(object, "location", coda.Vector2(0, 0), 2);
    """
    if obj in _data.keys():
        _data[obj].append(LerpData(member, end, duration))
    else:
        _data[obj] = [LerpData(member, end, duration)]

def update(delta_time):
    """update all of the lerps. Auto removes lerps when done."""
    to_delete = []
    for (obj, lerp_list) in _data.items():
        if not lerp_list:
            to_delete.append(obj)
        elif lerp_list[0].update(obj, delta_time):
            lerp_list.pop(0)

    for key in to_delete:
        del _data[key]

def clear(obj=None):
    """Clears the list of the given object. If object is None, clear entire list."""
    if obj is None:
        _data.clear()
    else:
        del _data[obj]
