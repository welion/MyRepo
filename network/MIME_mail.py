#-*- coding: utf-8 -*-
#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText

HOST = "smtp.163.com"
SUBJECT = u"给你一个招呼"
TO = "353566165@qq.com"
FROM = "welion_zhong@163.com"

def insert_one_line(num, name, start_time, end_time, out_time, result):
     table_one_line = """<tr style='mso-yfti-irow:1;height:44.5pt'>
       <td width=178 style='width:106.75pt;border:solid windowtext 1.0pt;border-top:
       none;background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
       <p>"""+num+"""<o:p></o:p></p>
       </td>
       <td width=134 style='width:80.55pt;border-top:none;border-left:none;
       border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
       background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
       <p>"""+name+"""<o:p></o:p></p>
       </td>
       <td width=135 style='width:81.0pt;border-top:none;border-left:none;
       border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
       background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
       <p>"""+start_time+"-"+end_time+"""<o:p></o:p></p>
       </td>
       <td width=109 style='width:65.25pt;border-top:none;border-left:none;
       border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
       background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
       <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
       7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'>"""+out_time+"""分钟<o:p></o:p></p>
       </td>
       <td width=161 style='width:96.75pt;border-top:none;border-left:none;
       border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
       background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
       <p>"""+result+"""<o:p></o:p></p>
       </td>
      </tr>"""
     return table_one_line

def draw_table():
    table_head = """  <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;height:13.5pt'>
  <td width=178 style='width:106.75pt;border:solid windowtext 1.0pt;background:
  #538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p><b>编号</b><b></b></p>
  </td>
  <td width=134 style='width:80.55pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p><b>变更标题</b><b></b></p>
  </td>
  <td width=135 style='width:81.0pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p><b>实施时间</b><b></b></p>
  </td>
    <td width=109 style='width:65.25pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p><b>影响交易时间</b><b></b></p>
  </td>
  <td width=161 style='width:96.75pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p><b>实施结果</b><b></b></p>
  </td>
 </tr>"""
    
    line = insert_one_line("RMS-150401-0001","发布方案","0:00","0:11","11","成功")
   
    table = """<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0
 style='background:white;border-collapse:collapse;mso-yfti-tbllook:1184;
 mso-padding-alt:0cm 0cm 0cm 0cm'> """ + table_head + line + "</table>" 
    
    return str(table)


msg = MIMEText(draw_table(),"html","utf-8")
msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO

try:
    server = smtplib.SMTP()
    server.connect(HOST,"25")
    server.starttls()
    server.login("welion_zhong@163.com","")
    server.sendmail(FROM,[TO],msg.as_string())
    server.quit()
    print "邮件发送成功"
except Exception,e:
    print "邮件发送失败:"+str(e)

