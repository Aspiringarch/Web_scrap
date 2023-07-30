import bs4
import requests
from matplotlib import pyplot as plt
import xlsxwriter
import xlrd
import sqlite3

url="https://www.worldometers.info/world-population/"
response=requests.get(url)
soup=bs4.BeautifulSoup(response.content,'html.parser')
#print(soup)
table=soup.find('table',{"class":"table table-striped table-bordered table-hover table-condensed table-list"})
tablebody=table.findAll('tr')[1:]
#print(tablebody)

pop1=[]
percent=[]
popchange=[]
age=[]
for tablebodys in tablebody:
    cols=tablebodys.findAll('td')[1:]
    #print(cols)
    cols=[x.text.strip() for x in cols]
    pop1.append(str(cols[0].replace(',','')))
    percent.append(str(cols[1].replace('.','').replace('%','').strip()))
    popchange.append(str(cols[2].replace(',','')))
    age.append(str(cols[3].replace(".","")))
print(pop1)
print(popchange)
print(percent)
print(age)

import xlsxwriter
workbook=xlsxwriter.Workbook("population7.xlsx")
worksheet1=workbook.add_worksheet()
bold=workbook.add_format({'bold':True})
worksheet1.write('A1','age',bold)
worksheet1.write('B1','pop1',bold)
worksheet1.write('C1','percent',bold)
worksheet1.write('D1','popchange',bold)

row=1
col=0

for i in range(len(age)):
    worksheet1.write(row,col,age[i])
    worksheet1.write(row,col+1,pop1[i])
    worksheet1.write(row,col+2,percent[i])
    worksheet1.write(row,col+3,popchange[i])
    row+=1
chart1=workbook.add_chart({'type':'line'})
chart1.add_series(({'categories':'sheet1!$B$2:$B$10','values':'sheet1!$C$2:$C$10'}))
chart1.set_title({'name':'POPULATION'})
worksheet1.insert_chart('H3',chart1)

chart2=workbook.add_chart({'type':'bar'})
chart2.add_series({'categories':'sheet1!$B$2:$B$10','values':'sheet1!$C$2:$C$10'})
chart2.set_title({'name':'POPULATION CHANGE'})
worksheet1.insert_chart('H18',chart2)
chart2.add_series({'categories':'sheet1!$B$2$B$10','values':'sheet1!$D$2:$10'})
workbook.close()

#plt.scatter(age[0:30],popchange[0:30],color='y',label='population')
#plt.title("Population")
#plt.xlabel("Age")
#plt.ylabel("popchange")
#plt.legend()
#plt.show()
#print("done")



wb=xlrd.open_workbook("population.xlsx")
workshhet=wb.sheet_by_name("Sheet1")
num_rows=workshhet.nrows
num_cols=workshhet.ncols
coln_review=[]
for curr_row in range(0,num_rows,1):
    row_review=[]
    for curr_col in range(0,num_cols,1):
        review=workshhet.cell_value(curr_row,curr_col)
        row_review.append(review)

    coln_review.append(row_review)

conn=sqlite3.connect("my_test_db")
print("Database connected successfully ")

conn.execute("CREATE TABLE population6 (age TEXT NOT NULL,pop1 TEXT NOT NULL,popchange TEXT NOT NULL,percent TEXT NOT NULL);")
cursor=conn.cursor()
cursor.executemany('INSERT INTO population6(age,pop1,popchange,percent)VALUES(?,?,?,?)',coln_review)
conn.commit()
conn.close()

print("operation done successfully")
