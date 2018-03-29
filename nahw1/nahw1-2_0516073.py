from prettytable import PrettyTable
from datetime import datetime
import sys

def fun_help():
	print('usage: nahe1-2_0516073.py [-h] [-u] [-after AFTER] [-befor BEFORE] [-n N] [-t T] [-r] filename')
	print('')
	print('Auth log parser.')
	print('')
	print('positional arguments:')
	print('  filename        Log file path.')
	print('')
	print('optional arguments:')
	print('  -h              show this help message and exit')
	print('  -u              Summary failed login log and sort log by user.')
	print('  -after AFTER    Filter log after date. format YYYY-MM-DD-HH:MM:SS')
	print('  -before BEFORE  Filter log before date. format YYYY-MM-DD-HH:MM:SS')
	print('  -n N            Show only the user of most N-th times')
	print('  -t T            Show only the user of attacking equal or more than T times')
	print('  -r              Sort in reverse order')
atime = datetime.strptime('2018-01-01-00:00:00', "%Y-%m-%d-%H:%M:%S")
btime = datetime.strptime('2018-12-31-23:59:59', "%Y-%m-%d-%H:%M:%S")
atimes = 0
btimes = 999999999999
rflag = 1
uflag = 0
ar = sys.argv
flag = 0
filename=''
opt_num = len(ar)
for i in range(1,opt_num):
	if flag == 1:
		flag = 0
		continue

	if ar[i] == '-h':
		fun_help()
	elif ar[i] == '-u':
		uflag = 1
	elif ar[i] == '-after':
		flag = 1
		atime = datetime.strptime(ar[i+1], "%Y-%m-%d-%H:%M:%S")
	elif ar[i] == '-before':
		flag = 1
		btime = datetime.strptime(ar[i+1], "%Y-%m-%d-%H:%M:%S")
	elif ar[i] == '-n':
		btimes = int(ar[i+1])
		flag = 1
	elif ar[i] == '-t':
		atimes = int(ar[i+1])
		flag = 1
	elif ar[i] == '-r':
		rflag = 0
	else:
		filename=ar[i]
f = open(filename, 'r')
li = f.readline()
di = {}
while li:
	if(li.find('sshd') == -1 or li.find('Invalid user') == -1):
		li = f.readline()
		continue
	li = li.split(' ')
	ti = li[0]+'-2018-'+li[2]+'-'+li[3]
	dati = datetime.strptime(ti, "%b-%Y-%d-%H:%M:%S")
	if(atime > dati or dati > btime):
		continue
	
	if li[6] == 'Invalid':
		try:
			di[li[8]] += 1
		except:
			di[li[8]] = 1
	else:	
		try:
			di[li[9]] += 1
		except:
			di[li[9]] = 1
	li = f.readline()
di2 = {}
for k, v in di.items():
	if(atimes <= v and v <= btimes):
		di2[k] = v
di = di2
table = PrettyTable()
table.field_names = ['user','count']
if uflag == 1:
	di = sorted(di.items(), key = lambda d: d[0], reverse = rflag)
else :
	di = sorted(di.items(), key = lambda d: d[1], reverse = rflag)
tt = len(di)
if tt > 10 :
	tt = 10
for i in range(tt):
	table.add_row([di[i][0], di[i][1]])
print(table)















