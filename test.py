from tkinter import *
import pymysql


mydb = pymysql.connect("localhost","root","Arunamalladi!","attendance" )
mycursor = mydb.cursor()
mycursor.execute("SELECT distinct COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'class' ORDER BY ORDINAL_POSITION")
myresult = mycursor.fetchall()
myresult=list(myresult)
lis=[]
for i in range(len(myresult)):
	s=''.join(myresult[i])
	lis.append(s)
if 'Dat' in lis:
	lis.remove('Dat')
print(lis)

myc=mydb.cursor()  
myc.execute("SELECT * from class")
res=myc.fetchall()
res=list(res)
li=res[0]
li=list(li)
print(li)

class Table:
    def __init__(self,root):
        j=0
        for i in range(len(lis)-1,-1,-1):
            self.e = Entry(root, width=10,fg='black',font=('Arial',10,'bold'))
            self.e.grid(row=0, column=j)
            self.e.insert(END, lis[i])
            j+=1
        j=0
        for i in range(len(li)-1,-1,-1):
            self.e = Entry(root, width=10, fg='blue',font=('Arial',10,'bold'))
            self.e.grid(row=1, column=j)
            self.e.insert(END, li[i])
            j+=1


root = Tk() 
t = Table(root) 
root.mainloop()
