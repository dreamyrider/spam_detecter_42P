import requests
import json
import smtplib
from email.mime.text import MIMEText
import time
import logging

spamUserParam=""
timesNN=0

def observing_Spam(spamUserParam,timesN):
	print("Start:");
	# s = requests.session()
	#请求的参数，登录名和密码 username=dreamyrider&password=Wang123456
	# data = {'username':'dreamyrider','password':'Wang123456'}
	#post 登录的地址，
	# res=s.post('http://2p.com/toplayadmin/loginSubmit.in',data);
	# s.connection.close()
	n=30			#2P接口抓取的条数参数
	ntimes=0		#所抓取的n条中出现超过ntimes次，则自动发送邮件
	sleepTime=1	#间隔时间，单位：秒
	timesNRepeat=20	#重复**次抓取到同一个用户，不重复发邮件，避免滥发邮件

	#抓取的地址
	r= requests.post('http://2p.com/forum/section/articles?pageSize=%s&pageNo=1&code=D001288'%n);
	r.connection.close()
	# c= r.content;
	c= str(r.content,'utf-8')
	c= json.loads(c);
	listData=c["data"]["listData"];
	arr=[];
	for z in range(n):
		if listData[z]["status"]==0:
			arr.append(listData[z]["author"]["userName"]);

	#统计重复出现的次数
	m=[]#临时储存所有的异常用户记录
	sendMailDetect=False#默认不触发邮件
	for x in set(arr):
		if arr.count(x)>ntimes:
			#发现异常时执行操作
			ms= str(x)+" has posted "+str(arr.count(x))+" Articles Within a short time. \n";
			m.append(ms);
			spamUser=str(x)#临时储存异常用户名
			if spamUser!=spamUserParam:
				sendMailDetect=True
			elif spamUser==spamUserParam:
				timesN+=1
				if timesN==timesNRepeat:
					sendMailDetect=True
					timesN=0
				elif timesN==(timesNRepeat-1):
					print(spamUser+" detected again. Won't send email till next check.")
				else:
					print(spamUser+" detected again. Won't send email till next "+str(timesNRepeat-timesN)+" times.")
	if sendMailDetect==True:
		mt=''.join(m)#数组合并为字符串
		print(mt)#控制台输出内容
		mt+="\nMaybe there is someone posting spam on our 2P.com. Please go http://2p.com/toplayadmin/artical/index.html check ASAP.\n\nThank you!!!\n\n-- Auto detected by Script\n\nSincerely yours,\nHanson"#添加其他内容
		#发送邮件所需的参数
		msg = MIMEText(mt);
		msg['Subject'] = "WARNING about spams on 2P articles"
		msg['From']    = "noreply@mail.2p.com"
		msg['To']      = "huansongwang@cyou-inc.com"
		s = smtplib.SMTP('smtp.mailgun.org', 587)
		#发送邮件
		# s.login('noreply@mail.2p.com', 'Si6PWuX64LsvGj63Ht')
		# s.sendmail(msg['From'], msg['To'], msg.as_string())
		print("Succeed to send mail.\t\t",time.asctime( time.localtime(time.time()) ))
		s.quit()
	else:
		m=["No Spam detected."]
		print("No Spam detected.\t\t",time.asctime( time.localtime(time.time()) ))
	#记录日志
	log_filename="logtest.log"
	logging.basicConfig(filename=log_filename,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n\t%(message)s \n',
		filemode="a",
		datefmt='%a, %d %b %Y %H:%M:%S',
		level=logging.DEBUG)
	# logging.debug(%(asctime)s %(pathname)s %(filename)s)
	logging.debug(''.join(m))
	print("\nSleep for "+str(sleepTime)+" seconds\n")
	time.sleep(sleepTime);
	observing_Spam(spamUser,timesN);

observing_Spam(spamUserParam,timesNN);

		# msg['From']    = "dreamyrider@163.com"
		# msg['To']      = "hanson@2p.com"
		# s = smtplib.SMTP('smtp.163.com', 25)
		# #发送邮件
		# s.login('dreamyrider', 'Dreamy@123456')