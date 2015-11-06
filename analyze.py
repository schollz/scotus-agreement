
import json
import glob

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


files = glob.glob('./*.wiki')
cases = []
outcomes = {}
dissents = [0,0,0,0,0]
majorityFraction = []
for filem in files:
    inCase = False
    case = {}
    with open(filem,'r') as f:
        for line in f:
            if '|case=' in line:
                try:
                    case = {}
                    case['judges'] = {}
                    case['name'] = line.split('case=')[1].strip()
                    case['majority'] = 0
                    case['dissent'] = 0
                    inCase = True
                except:
                    pass
            if '|justice' in line and inCase:
                if 'majority' in line or 'plurality' in line or 'concurrence' in line:
                    case['judges'][find_between(line,'<!--','-->')] = 'majority'
                    case['majority'] += 1
                elif 'dissent' in line:
                    case['judges'][find_between(line,'<!--','-->')] = 'dissent'
                    case['dissent'] += 1
            if '|justice9' in line:
                inCase = False       
                cases.append(case)
                try:
                    outcome = str(case['majority']) + '-' + str(case['dissent'])
                    if outcome not in outcomes:
                        outcomes[outcome] = 0
                    outcomes[outcome] += 1
                    dissents[case['dissent']] += 1
                    majorityFraction.append(float(100.0*case['majority']/(case['majority']+case['dissent'])))
                except:
                    pass
            

print(json.dumps(outcomes,indent=1))
print(json.dumps(dissents,indent=1))
print(majorityFraction)

'''
a=majorityFraction
[b,i]=hist(a,50:5:100)
area(i,cumsum(b)/max(cumsum(b)))
xlabel('Percent agreement among justices')
ylabel('Cumulative probability of percent agreement')
'''

