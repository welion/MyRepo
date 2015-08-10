from django.http import HttpResponse
import os,sys
import psutil
from  django.template import Template,Context

def GetCpuInfo():
	return str(os.popen('cat /proc/cpuinfo |grep "model name" |sed "s/model name\t\://"|uniq').read())
	
def GetUserName():
	return str(os.popen('hostname').read())

def GetMemInfo():
	MemTotal = os.popen('free -m|grep Mem|awk \'{print $2 "M"}\'').read()
	MemUsed  = os.popen('free -m|grep Mem|awk \'{print $3 "M"}\'').read()
	MemPer   = os.popen('free -m|grep Mem|awk \'{print ($3-$6-$7)/$2*100 \"%\" }\'').read()
	return {'total':str(MemTotal),
		'used' :str(MemUsed),
		'per'  :str(MemPer),}


def Maketemplate(html,hostname,username,cpuinfo,meminfo):
	with open (html,'r+') as f:
		t=Template(f.read())

#	t=Template('<html><head><title>System Info</title></head><body><p>hostname: {{hostname}}</p><p>username: {{username}}</p><p>CPU Info: {{cpuinfo}}</p><p>Mem Info: {{meminfo}}</p><p></p><p></p><p></p></body></html>')

	c=Context({'hostname':hostname,
		   'username':username,
		   'cpuinfo': cpuinfo,
		   'meminfo': meminfo})
	tempage = t.render(c)
	return tempage

	
def main(request):
	
	# Get system info 
#	message = "It works" + str(cpu) + str(GetUserName()) + GetMemInfo()['total'] + GetMemInfo()['used'] + GetMemInfo()['per']
	pagebase = os.getcwd()
	filepath = pagebase + "/page.html"
	message = Maketemplate(filepath,GetUserName(),GetUserName(),GetCpuInfo(),GetMemInfo())

	return HttpResponse(message)
#	with open(filepath,'r+') as f
	#	return HttpResponse(f)
