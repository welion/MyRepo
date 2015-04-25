#/usr/bin/env python
#-*-coding: utf-8 -*-


import os
import sys


def insert_one_line(num, name, start_time, end_time, out_time, result):
     table_one_line = """<tr style='mso-yfti-irow:1;height:44.5pt'>
  <td width=178 style='width:106.75pt;border:solid windowtext 1.0pt;border-top:
  none;background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
  <p class=MsoNormal align=left style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:left;line-height:12.6pt;mso-pagination:widow-orphan'>"""+num+"""<o:p></o:p></p>
  </td>
  <td width=134 style='width:80.55pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
  <p class=MsoNormal align=left style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:left;line-height:12.6pt;mso-pagination:widow-orphan'>"""+name+"""<o:p></o:p></p>
  </td>
  <td width=135 style='width:81.0pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  background:transparent;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:44.5pt'>
  <p class=MsoNormal align=left style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:left;line-height:12.6pt;mso-pagination:widow-orphan'>"""+start_time+"-"+end_time+"""<o:p></o:p></p>
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
  <p class=MsoNormal align=left style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:left;line-height:12.6pt;mso-pagination:widow-orphan'>"""+result+"""<o:p></o:p></p>
  </td>
 </tr>"""
     return table_one_line

def draw_table():
    table_head = """  <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;height:13.5pt'>
  <td width=178 style='width:106.75pt;border:solid windowtext 1.0pt;background:
  #538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'><b>编号</b><b></b></p>
  </td>
  <td width=134 style='width:80.55pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'><b>变更标题</b><b></b></p>
  </td>
  <td width=135 style='width:81.0pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'><b>实施时间</b><b></b></p>
  </td>
    <td width=109 style='width:65.25pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'><b>影响交易时间</b><b></b></p>
  </td>
  <td width=161 style='width:96.75pt;border:solid windowtext 1.0pt;border-left:
  none;background:#538DD5;padding:3.75pt 7.5pt 3.75pt 7.5pt;height:13.5pt'>
  <p class=MsoNormal align=center style='mso-margin-top-alt:auto;margin-bottom:
  7.5pt;text-align:center;line-height:12.6pt;mso-pagination:widow-orphan'><b>实施结果</b><b></b></p>
  </td>
 </tr>"""
    
    line = insert_one_line("RMS-150401-0001","发布方案","0:00","0:11","11","成功")
   
    table = """<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0
 style='background:white;border-collapse:collapse;mso-yfti-tbllook:1184;
 mso-padding-alt:0cm 0cm 0cm 0cm'> """ + table_head + line + "</table>" 
    
    print table
    return table
    

if __name__ == "__main__":
    f1 = draw_table()
    print f1
    with open(r"t.html","w+") as f:
        f.write(draw_table())
