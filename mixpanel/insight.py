from datetime import datetime
from isoweek import Week
from itertools import chain
from bitdeli.insight import insight
from bitdeli.widgets import Widget
from discodb.query import Q, Literal, Clause

NUM_WEEKS = 10

class Matrix(Widget):
    defaults = {'size': [3,3]}

def get_latest(model):
    return max(key.split(':', 1)[0] for key in model)

def week_clause(week, event):
    return Clause(Literal('%s:%s' % (week.day(i).strftime('%Y%m%d'), event))
                  for i in range(7))

def cohort(week, mevent, cevent, model):
    mq = week_clause(week, mevent)
    size = float(len(model.query(Q([mq]))))
    for i in range(NUM_WEEKS):
        if size > 0:
            cq = week_clause(week + i + 1, cevent)
            yield len(model.query(Q((mq, cq)))) / size
        else:
            yield 0

def normalize(rows):
    maxval = float(max(chain.from_iterable(rows)))
    if maxval > 0:
        for row in rows:
            for i in range(NUM_WEEKS):
                row[i] /= maxval
    return rows
        
@insight
def view(model, params):
    params = {'events': ['Page View', 'Page View']}
    mevent, cevent = params['events']
    latest = datetime.strptime(get_latest(model), '%Y%m%d')
    week = Week(*latest.isocalendar()[:2])
    rows = [list(cohort(week - i, mevent, cevent, model))
            for i in range(NUM_WEEKS)]
    return [Matrix(size=(12, 12), data=normalize(rows))]
    
    

    