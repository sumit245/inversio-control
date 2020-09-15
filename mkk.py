from tkinter import *
from functools import partial
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import email, smtplib, ssl,webbrowser,os,imaplib
import sqlite3 as sq
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header





def Database():
    global conn, cursor
    conn = sq.connect("inversioControl.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def login():
    Database()
    def clr():
        username.set("")
        password.set("")
    def exit_():
        window.destroy()
    try:
        lst=window.grid_slaves()
        for l in lst:
            l.destroy()
    finally:
        password = StringVar()
        username = StringVar()
        
        def validateLogin(username, password):
            if username.get() == "" or password.get() == "":
                emptyMsg="Please Fill Both Fields"
                messagebox.showerror('Fields Required',emptyMsg)
            else:
                cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (username.get(), password.get()))
                if cursor.fetchone() is not None:
                    home()
                    username.set("")
                    password.set("")
                else:
                    errorMsg="Invalid Username or Password"
                    messagebox.showwarning('Warning',errorMsg)
                    username.set("")
                    password.set("")
##            cursor.close()
##            conn.close()

        def changepswd(event):
            print('Hello World')

        lblfrm = LabelFrame(window,height=height, width=width,bd=4,bg='#2057d6',font=('Dubai',16,'bold'),fg='white',text="Login")
        lblfrm.pack(padx=100,pady=150,side=LEFT,expand=0,fill=X)

        entrywidth=lblfrm.winfo_reqwidth()
        entrywidth=entrywidth-513
        
        
        usernameLabel = Label(lblfrm,text="User Name",font=('arial',14,'bold'),bg='#2057d6',fg='white').grid(row=0, column=0,padx=10,pady=10)
        usernameEntry = Entry(lblfrm, textvariable=username,width=entrywidth,bd=4).grid(row=0,columnspan=2, column=1,padx=10,pady=10)  

        
        passwordLabel = Label(lblfrm,text="Password",font=('arial',14,'bold'),bg='#2057d6',fg='white').grid(row=1, column=0,padx=10,pady=10)  
        passwordEntry = Entry(lblfrm, textvariable=password, show='*',width=40,bd=4,highlightcolor='blue').grid(row=1, column=1,columnspan=2,padx=10,pady=10)  

        validateLogin = partial(validateLogin, username, password)

        lblChangepswd=Label(lblfrm,font=('arial',14,'bold'),text='Change Password',fg='#cfcfcf',bg='#2057d6')
        lblChangepswd.bind('<Button-1>',changepswd)
        lblChangepswd.grid(row=3,column=1)
        
        extButton = Button(lblfrm, text='BACK', font=('Courier New',14,'bold'), bg = "#7fff00",fg = "#2057d6",bd = 4,width=8,relief = RAISED,command=exit_).grid(row=5,ipadx=5, column=0,pady=50,padx=10)
        clrButton = Button(lblfrm,text='CLEAR', font=('Courier New',14,'bold'), bg = "#7fff00",fg = "#2057d6",bd = 4,width=8,relief = RAISED,command=clr).grid(row=5, ipadx=5,column=1,pady=50,padx=5)
        loginButton = Button(lblfrm, text='LOGIN' ,font=('Courier New',14,'bold'),bg = "#7fff00",fg = "#2057d6",bd = 4,width=8,relief = RAISED,command=validateLogin).grid(row=5,ipadx=5, column=2,pady=50,padx=10)

        

        
def home():
    fileVar=StringVar()
    notice=StringVar()
    lst=window.pack_slaves()
    msglst=[]
    sentmessage=StringVar()
    for l in lst:
        l.destroy()
    def callback():
        name= fd.askopenfilename() 
        fileVar.set(name)
    def bk():
        lst=window.pack_slaves()
        for l in lst:
            l.destroy()
        login()
    def submit():
        if fileVar.get()=='':
##            messagebox.showerror('Error','Please Upload Before Sending')
            notice.set('Please Attach A File Before Submitting')
        else:
            msglst.append(fileVar.get())
            subject = "Report From XYZ Construction Limited"
            body = "Please Find our report"
            receiver_email = "push9274@gmail.com"
            sender_email = "sumitranjan245@gmail.com"
            password = 'cwwgrczdjmeclfuw'

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message["Bcc"] = receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            filename = fileVar.get()  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                    )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
                notice.set('Report Submitted Successfully')
##                messagebox.showinfo('Success','Report Submitted')
    errmsg = 'Error!'
    
    tabControl=ttk.Notebook(window)
    style=ttk.Style()
    style.theme_create("custom_tabs", parent="alt", settings={
                "TNotebook.Tab": {
                    "configure": {"padding": [10, 10, 10, 10],'margin':10,'font':('arial',14,'bold'),'foreground':'white','background':'#2057d6'}
                    }})
    style.theme_use("custom_tabs")
    
    
    
    lblfrm = LabelFrame(window,height=height, width=400,bd=4,bg='#2057d6',font=('Dubai',16,'bold'),fg='white',text="Send Reports")
    lblfrm.pack(padx=150,pady=150,side=LEFT,expand=0)

    entr=Label(lblfrm,textvariable=fileVar,bd=10,font=('Lucida',10,'bold'),width=36,relief=RIDGE).pack(side=TOP,fill=X,expand=True,padx=10)

    btn2=Button(lblfrm,text='BACK', font=('Courier New',14,'bold'), width=8,bg = "#7fff00",fg = "#2057d6",bd = 4,relief = RAISED, command=bk).pack(side=LEFT,fill=X,padx=10,pady=50,ipadx=2,ipady=2)
    btn1=Button(lblfrm,text='ATTACH', font=('Courier New',14,'bold'), width=8,bg = "#7fff00",fg = "#2057d6",bd = 4,relief = RAISED,command= callback).pack(side=LEFT,fill=X,padx=10,pady=50,ipadx=2,ipady=2)    
    btn3=Button(lblfrm,text='SUBMIT',bg = "#7fff00",fg = "#2057d6",bd = 4,width=8,relief = RAISED,font=('Courier New',14,'bold'),command=submit).pack(side=LEFT,fill=X,padx=10,pady=50,ipadx=2,ipady=2)

    lblnotice=Label(lblfrm,textvariable=notice,font=('Times New Roman',16,'bold'),fg='white',bg = "#2057d6").pack(side=TOP,anchor=SW,after=btn3,fill=X,expand=True,padx=10)
    tab1=tabControl.add(lblfrm,text='Send Report')


    lblfrm1 = LabelFrame(window,height=height, width=400,bd=4,bg='#2057d6',font=('Dubai',16,'bold'),fg='white',text="Outbound Reports")
    lblfrm1.pack(padx=150,pady=150,side=LEFT,expand=0)
    listbox = Listbox(lblfrm1,listvariable=sentmessage) 
    listbox.pack(side = LEFT, fill = BOTH,expand=True) 
    scrollbar = Scrollbar(lblfrm1) 
    scrollbar.pack(side = RIGHT, fill = BOTH) 
    def populate_sentbox():
        for values in msglst:
            if values not in sentmessage.get():
                listbox.insert(END, values)
        lblfrm1.after(1,populate_sentbox)
    populate_sentbox()
    listbox.config(yscrollcommand = scrollbar.set) 
    scrollbar.config(command = listbox.yview) 
    tab2=tabControl.add(lblfrm1,text='View Sent Report')

    lblfrm2 = LabelFrame(window,height=height, width=400,bd=4,bg='#2057d6',font=('Dubai',16,'bold'),fg='white',text="Inbound Reports")
    lblfrm2.pack(padx=150,pady=150,side=LEFT,expand=0)
    listbox1 = Listbox(lblfrm2,listvariable=sentmessage) 
    listbox1.pack(side = LEFT, fill = BOTH,expand=True) 
    scrollbar1 = Scrollbar(lblfrm2) 
    scrollbar1.pack(side = RIGHT, fill = BOTH) 
    def receivemail():

        username = "sumitranjan245@gmail.com"
        password = "cwwgrczdjmeclfuw"
        # create an IMAP4 class with SSL 
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        N = 3
        messages = int(messages[0])
        for i in range(messages, messages-N, -1):
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_ = msg.get("From")
                print("Subject:", subject)
                print("From:", from_)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                subj1='Reports'+str(i)
                                if not os.path.isdir(subj1):
    ##                                # make a folder for this email (named after the subject)
                                    os.mkdir(subj1)
                                filepath = os.path.join(subj1, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
        imap.close()
        imap.logout()


    listbox1.config(yscrollcommand = scrollbar.set) 
    scrollbar1.config(command = listbox.yview) 
    tab3=tabControl.add(lblfrm2,text='View Received Report')


    tabControl.pack(side=LEFT,padx=50,pady=10,expand=0,fill=X)

  
    
if __name__=='__main__':
    window = Tk()
    width = 553
    height = 343
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry("%dx%d+%d+%d" % (1200, 700, 0, 0))
    window.resizable(0, 0)
    window.title('Online Service Solution')
    
    load = Image.open("bgnd.png")
    render = ImageTk.PhotoImage(load)
    img = Label(window, image=render,borderwidth=0)
    img.image = render
    window.iconbitmap('favicon.ico')
    img.place(x=0, y=0)

    ld2 = Image.open("dwmstitle.png")
    rdr2 = ImageTk.PhotoImage(ld2)
    img2 = Label(window, image=rdr2,bd=0)
    img2.image = rdr2
    img2.place(x=800, y=200)
    
    load2 = Image.open("dwmsak.png")
    render2 = ImageTk.PhotoImage(load2)
    img2 = Label(window, image=render2,bd=0)
    img2.image = render2
    img2.place(x=874, y=599)
    
    ld3 = Image.open("invico.png")
    rdr3 = ImageTk.PhotoImage(ld3)
    img3 = Label(window, image=rdr3,bd=0)
    img3.image = rdr3
    img3.place(x=1040, y=25)

   
    
    login()
    window.mainloop()
