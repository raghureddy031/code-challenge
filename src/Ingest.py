import ast
import datetime

inputs = []
path = '/Users/Raghu/Desktop/events.txt'
    
with open(path, 'r') as sample:
    for line in sample:
        line = line.replace("},", "}").replace("[", "").replace("]", "")
        inputs.append(ast.literal_eval(line))
        
class Customer(object):
    
    def __init__(self, last_name, adr_city, adr_state, date_join, revenue = 0.0, total_visits = 1, membership_days=0):
        fmt = '%Y-%m-%dT%H:%M:%S.%f'
        self.last_name = last_name
        self.adr_city = adr_city
        self.adr_state = adr_state
        self.date_join = datetime.datetime.strptime(date_join.replace("Z", ""), fmt)
        self.revenue = revenue
        self.total_visits = total_visits
        self.membership_days = membership_days
        
    def add_revenue(self, revenue):
        self.revenue += revenue
        
    def get_revenue(self):
        return self.revenue
        
    def add_visit(self):
        self.total_visits += 1
        
    def get_visits(self):
        return self.total_visits
        
    def days_since_join(self, today=datetime.datetime.now()):
        self.membership_days = today - self.date_join
        return self.membership_days.days
        
    def visits_per_week(self):
        return self.get_visits() / (self.days_since_join() / 7.0)
    
    def revenue_per_visit(self):
        return self.get_revenue() / self.get_visits()
    
    def revenue_per_week(self):
        return self.get_revenue() / (self.days_since_join() / 7.0)
            
    def simple_lifetime_value(self, lifespan=10):
        return 52 * self.revenue_per_week() * lifespan


all_entries = {}

def process_inputs(entry):
    if entry['type'] == 'CUSTOMER':
        all_entries.update({entry['key']: Customer(entry['last_name'], entry['adr_city'], entry['adr_state'], entry['event_time'])})
    elif entry['type'] == 'ORDER':
        all_entries[entry['customer_id']].add_visit()
        all_entries[entry['customer_id']].add_revenue(float(entry['total_amount'].split()[0]))
    else:
        all_entries[entry['customer_id']].add_visit()  

for i in inputs:
    process_inputs(i)
    
    
customers = []
for i in inputs:
    if i['type'] == 'CUSTOMER':
        customers.append(i['key'])


LTV = {}
for i in customers:
     LTV.update({i: all_entries[i].simple_lifetime_value()})


t = sorted(LTV.iteritems(), key=lambda y:-y[1])[:10]

result = []
for y in t:
    result.append("{0}: {1}".format(*y))

print result


