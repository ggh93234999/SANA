import requests
import sys
import getpass
import tesserocr
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from PIL import Image
def getIDPW():
	tb = getpass.getpass('Your Password:')
	return tb
def getcode():
	s = requests.Session()
	r = s.get('https://portal.nctu.edu.tw/captcha/pic.php')
	#print (s.headers)
	r = s.get('https://portal.nctu.edu.tw/captcha/pitctest/pic.php')
	#print(r.request.headers)
	with open('tmp.png', 'wb') as f:
		f.write(r.content)
		f.close()

	threshold = 140 
	table = []
	for i in range(256):
		if i < threshold :
			table.append(0)
		else :
			table.append(1)

	image = Image.open('./tmp.png')
	bimage = image.convert('L')
	bimage.save('gtmp.png')
	out = bimage.point(table,'1')
	out.save('btmp.png')

	code1 = tesserocr.image_to_text(image)
	code2 = tesserocr.image_to_text(bimage)
	code3 = tesserocr.image_to_text(out)
	if len(code3) != 6:
		return getcode()
	else:
		if code3.isdigit:
			#print('hello')
			return s, code3
		else:
			return getcode()

def getpost(ID,PW,code):
	payload = {'username':ID, 'password':PW, 'seccode':code, 'Submit2':'登入(Login)', 'pwdtype':'static'}
	return payload
def geturl():
	url = 'https://portal.nctu.edu.tw/portal/chkpas.php?'
	return url
if(sys.argv[1] == '-h'):
	print('usage: main.py [-h] username')
	print('')
	print('Web crawler for NCTU class schedule')
	print('')
	print('positional arguments:')
	print('  username    username of NCTU portal')
	print('')
	print('optional arguments:')
	print('  -h show this help message and exit')
	exit()
ID = sys.argv[1]
PW = getIDPW()

OK = 0
while OK == 0:
	s,code = getcode()
	code = code[:4]
	print(code)
	OK = int(input("OK?(1/0):"))
payload = getpost(ID,PW,code)
url = geturl()
r = s.post(url,payload);
r = s.post('https://portal.nctu.edu.tw/portal/relay.php?D=cos')
f = open('new','w')
f.write(r.text)
f.close()

f = open('new','r')
for i in range(9):
	tmp = f.readline()
def readd(f):
	tmp = f.readline()
	tmp = tmp.strip().lstrip().rstrip(',')
	tmp = tmp.split('"')
	return tmp

need = {}
for i in range(9):
	tmp = readd(f)
	need[tmp[3]] = tmp[7]
tmp = readd(f)
need[tmp[5]] = 'on'
need['Button1'] = '登入'

#print(need)
f.close()
r = s.post('https://course.nctu.edu.tw/index.asp',data=need)
r = s.post('https://course.nctu.edu.tw/index.asp')
r = s.post('https://course.nctu.edu.tw/adSchedule.asp')
r.encoding = 'big5'
f = open('see','w')
f.write(r.text)
f.close()



soup = BeautifulSoup(open('see'),'lxml')

data=[]
i = 0
for table in soup.find_all('table'):
	if (i<1):
		i=i+1
		continue
	for row in table.find_all('tr'):
		cell = row.find_all('td')
		data.append(cell)	

#1 18
l = [] 
for i in range(1,18):
	l.append([])
	l[i-1].append(data[i][0].font.string)
	l[i-1].append(data[i][1].font.string)
	for j in range(2,9):
		for x in data[i][j].font.strings:
			x=x.strip().lstrip().rstrip(',')
			l[i-1].append(x)
			break
#print(l)
table = PrettyTable()
table.field_names = l[0]
for i in range(1,17):
	table.add_row(l[i])
print(table)

