from kivy.gesture import GestureDatabase, Gesture

def make(points):
    g = Gesture()
    g.add_stroke(point_list=points)
    g.normalize()
    return g

def build_gesture_db():
    gestures = {
        'swipe_right': make([(i * 10, 0) for i in range(20)]),
        'swipe_left': make([(-i * 10, 0) for i in range(20)]),
        'swipe_up': make([(0, i * 10) for i in range(20)]),
        'swipe_down': make([(0, -i * 10) for i in range(20)]),

        'swipe_v': make([(-10 + i, 20 - i * 2) for i in range(10)] + [(i, i * 2) for i in range(10)]),
        'swipe_caret': make([(i, i * 2) for i in range(10)] + [(10 + i, 20 - i * 2) for i in range(10)]),
        'swipe_greater': make([(i, 10 - i) for i in range(11)] + [(10 - i, -i) for i in range(1, 11)]),
        'swipe_less': make([(10 - i, 10 - i) for i in range(11)] + [(i, -i) for i in range(1, 11)])
    }
    
    gdb = GestureDatabase()
    for g in gestures.values():
        gdb.add_gesture(g)
    return gdb, gestures
