from tkinter import *
import subprocess
import tkinter.messagebox
import datetime
import xlwt
from xlwt import Workbook
import sys
import mysql.connector as sql
from tkinter import filedialog as fd
import pymysql
from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import json
fr=[]
vr=[]




def dashboard(user):
	def opendna():
		file=fd.askopenfile()
		if file:
			print(file.name)
		db = pymysql.connect("localhost","root",'Arunamalladi!',"attendance" )
		cursor = db.cursor()
		print(user)
		sql="select subject from faculty where username = '%s'" % (user)
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
		subj=cursor.fetchall()
		subj=list(subj)
		sube=subj[0]
		print(sube)
		sub=''.join(sube)
		p=subprocess.Popen('python recognize.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle --image '+file.name+' --subject '+sub,stdin=subprocess.PIPE)
		p.communicate(input=b'y')
		tkinter.messagebox.showinfo('Done', 'Attendance updated successfully')
	def back():
		root.destroy()

	def uattend():
		#top = tk.Toplevel(root)
		for widget in mainframe.winfo_children():
			widget.destroy()
		Label(mainframe,text="Upload Attendance",font=("",16),fg="black").pack(padx=20,pady=20)
		#button=Button(root, text="Upload",command=opendna).place(x=589,y=380)
		button=ttk.Button(mainframe,text="Upload Image", command=opendna)

		button.pack(padx=20,pady=20)


	def vattend():

		def frda():
			def print_sel():
				fr.append(str(cal.selection_get()))
				print(fr)
			top = tk.Toplevel(mainframe)
			cal=Calendar(top, font="Arial 14", selectmode='day', locale='en_US',cursor="hand1", year=2020, month=6, day=5)
			cal.grid(row=2,column=0)
			ttk.Button(top, text="ok", command=print_sel).grid(row=3,column=0)
			#print(fr)
		def vrda():
			def print_sel1():
				vr.append(str(cal.selection_get()))
				print(vr)
			top = tk.Toplevel(mainframe)
			cal=Calendar(top, font="Arial 14", selectmode='day', locale='en_US',cursor="hand1", year=2020, month=6, day=5)
			cal.grid(row=2,column=0)
			ttk.Button(top, text="ok", command=print_sel1).grid(row=3,column=0)
			#print(fr)

		def printtable():
			q="SELECT Date from class where Date>="+"'"+fr[0]+"'"+" and Date<="+"'"+vr[0]+"'"
			print(q)
			for i in range(len(dt)):
				s=''.join(dt[i])
				lis.append(s)
			print(lis)
			myc=db.cursor() 
			myc.execute(q)
			res=myc.fetchall()
			res=list(res)
			print(res)
			bnm=[]
			for j in range(len(res)):
				bhj=[]
				bhj.append(res[j])
				for i in range(len(dt)):
					sql="SELECT JSON_EXTRACT("+sub+", '$."+dt[i]+"') from class where Date="+"'"+res[j][0]+"'"
					print(sql)
					myc.execute(sql)
					vfr=myc.fetchall()
					vfr=list(vfr)
					print(vfr)
					vf=vfr[0]
					v=vf[0]
					v=str(v)
					v=v[1:len(v)-1]
					if v!="yes":
						bhj.append("no")
					else:
						bhj.append(v)
					print(bhj)
				bnm.append(bhj)
				print(bnm)


			#li=res
			#li=list(li)
			#print(li)
			class Table:
				def __init__(self,mainframe):
					j=0
					for i in range(len(lis)):
						#text=Text(mainframe,width=2,height=2)
						#text.insert(INSERT,lis[i])
						self.e = Entry(mainframe, width=15,fg='black',font=('Arial',10,'bold'))
						self.e.grid(row=1, column=j)
						self.e.insert(END, lis[i])
						j+=1    
					#j=0
					#li=res

					for k in range(len(bnm)):
						li=list(bnm[k])
						j=0
						for i in range(len(li)):
							if li[i]=='no':
								self.e = Entry(mainframe, width=15, fg='red',font=('Arial',10,'bold'))
							else:
								self.e = Entry(mainframe, width=15, fg='blue',font=('Arial',10,'bold'))
							self.e.grid(row=k+2, column=j)
							self.e.insert(END, li[i])
							j+=1 
			t = Table(mainframe)


		for widget in mainframe.winfo_children():
			widget.destroy()
		bf=ttk.Button(mainframe,width=15,text="From", command=frda)
		bf.grid(row=0,column=0)
		bv=ttk.Button(mainframe,width=15,text="To", command=vrda)
		bv.grid(row=0,column=1)
		kk=ttk.Button(mainframe,width=15,text="Get Attendance", command=printtable)
		kk.grid(row=0,column=2)
		db = pymysql.connect("localhost","root","Arunamalladi!","attendance" )
		cursor = db.cursor()
		sql="select subject from faculty where username = '%s'" % (user)
		try:
			cursor.execute(sql)
			db.commit()
		except:
			db.rollback()
		subj=cursor.fetchall()
		subj=list(subj)
		sube=subj[0]
		print(sube)
		sub=''.join(sube)
		sql="select "+sub+" from class where Date='2020-07-26'"
		print(sql)
		cursor.execute(sql)
		myresult = cursor.fetchall()
		myresult=list(myresult)
		lk=myresult[0]
		print(lk)
		lk=list(lk)
		kl=lk[0]
		kl=json.loads(kl)
		print(kl)
		dt=list(kl.keys())
		print(dt)
		lis=[]
		lis.append("Date")


		 
		#root.mainloop()



	root = Tk()
	s=ttk.Style(root)
	#root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

	def gotologin():
		root.destroy()
		login()

	root.title('Dashboard')
	user=user
	top_frame = Frame(root, bg="black")
	'''bank_name = Label(top_frame, text="Attendance System", bg="black",fg="white", font=("",13))
	bank_name.pack(side=LEFT)
	quitButton = Button(top_frame, text='X Close', bg="red", command=sys.exit)
	quitButton.pack(side=RIGHT)
	logoutButton = Button(top_frame, text='-> Log Out', bg="black",fg="white", command=gotologin)
	logoutButton.pack(side=RIGHT)
	top_frame.pack(fill=X)'''
	det_frame=Frame(root,height=200,bg="black")
	det_frame.pack(fill=X,side=TOP)
	det_name_label=Label(det_frame,text="\n"+"Welcome "+user+"\n",bg="black",fg="white",font=("times new roman",15))
	det_name_label.pack(side=LEFT)
	func_frame=Frame(root,width=200,bg="black")
	func_frame.pack(fill=Y,side=LEFT)
	mainframe=Frame(root)
	mainframe.pack(side=TOP,fill=BOTH)
	balance_enquiry_button=Button(func_frame,text="Upload Attendance",width=25,command=uattend,bg="black",fg="white")
	balance_enquiry_button.pack(pady=10)
	acc_details_button=Button(func_frame,text="View Attendance",width=25,command=vattend,bg="black",fg="white")
	acc_details_button.pack(pady=10)
	logoutButton = Button(func_frame, text='Log Out', bg="black",fg="white", command=gotologin,width=25)
	logoutButton.pack(pady=10)
	root.mainloop()

def login():    
	def get_pwd():
		db = sql.connect(host = "localhost", user = "root", password = "Arunamalladi!")
		cur = db.cursor()
		
		try :
			db = sql.connect(host = "localhost", user = "root", password = "Arunamalladi!", database = "attendance")
			cur = db.cursor()
		except sql.errors.DatabaseError:
			db = sql.connect(host = "localhost", user = "root", password = "Arunamalladi!", database = "attendance")
			cur = db.cursor()

		while True :
			user = user_name_entry.get()
			passwd = password_entry.get()
			cur.execute("select * from faculty where username = '%s' and password = '%s'" % (user, passwd))
			rud = cur.fetchall()

			if rud:
				root.destroy()
				dashboard(user)
				print("Welcome")

				break
			else:
				tkinter.messagebox.showinfo('Error', 'Invalid Details')
				db.commit()
				break

			cur.close()
			db.close()

	root = Tk()
	s=ttk.Style(root)
	#root.overrideredirect(True)
	root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
	root.title('Attendance System')
	top_frame=Frame(root,bg="black")
	'''bank_name = Label(top_frame,text="Attendance System",bg="black",fg="white",font=("",13))
	bank_name.pack(side=LEFT)
	quitButton=Button(top_frame,text='X Close',bg="red",command=sys.exit)
	quitButton.pack(side=RIGHT)
	top_frame.pack(fill=BOTH)
	LDframe1=Frame(root,height=120)
	LDframe1.pack(fill=X)'''
	Lframe1=Frame(root)
	Lframe1.pack(side=TOP,padx=100,pady=50)
	login_label=Label(Lframe1,text="LOGIN")
	login_label.config(font=("",25))
	login_label.grid(columnspan=2,pady=30)
	user_name_label = Label(Lframe1,text = 'UserID:')
	user_name_label.grid(row=1,column=0,padx=5,pady=20)
	user_name_entry = ttk.Entry(Lframe1, justify = CENTER )
	#entry1 = ttk.Entry(root,  justify = CENTER)
	user_name_entry.grid(row=1,column=1,padx=5,pady=20)
	password_label = Label(Lframe1,text = 'Password:')
	password_label.grid(row=2,column=0,padx=5,pady=20)
	password_entry = ttk.Entry(Lframe1, justify = CENTER, show='*')
	password_entry.grid(row=2,column=1,padx=5,pady=20)
	login_button=ttk.Button(Lframe1,text="Login", command=get_pwd)
	#login_button = Button(Lframe1, text = 'Login',command = get_pwd)
	login_button.grid(row=3,column=1,pady=20)
	LDframe2=Frame(root,height=30,padx=100,pady=50)
	LDframe2.pack(side=BOTTOM)
	Lframe2 = Frame(root,padx=100,pady=50)
	Lframe2.pack(side=BOTTOM, fill=X)
	root.mainloop()

login()





'''p=subprocess.Popen('cacls det.txt /p everyone:f',stdin=subprocess.PIPE)
		p.communicate(input=b'y')

		readdet=open("det.txt","r").readlines()
		balance=readdet[0].split()

		p=subprocess.Popen('cacls det.txt /p everyone:n',stdin=subprocess.PIPE)
		p.communicate(input=b'y')'''