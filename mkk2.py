from tkinter import *
from PIL import Image, ImageTk
window=Tk()
window.title('My Online Quiz')
window.geometry("1300x800+0+0")
window.configure(background="powder blue")
##Tops=Frame(window,width=1350,height=50,bd=8,bg="powder blue")
##Tops.pack(side=TOP)
f1=Frame(window,width=100,height=750,bd=8,bg="powder blue")
f1.pack(side=LEFT,padx=10,pady=10)

f2=Frame(window,width=1200,height=750,bd=8,bg="white")
f2.pack(side=RIGHT,padx=10,pady=10)

loginBtn=Button(f1,font=('arial',16,'bold'),text='Take a Quiz >>',width=15,bd=8,bg='red',fg='white',anchor='w',relief='groove')
loginBtn.grid(row=0,column=1,pady=5)
uploadBtn=Button(f1,font=('arial',16,'bold'),text='Upload Quiz <<',width=15,bd=8,bg='steel blue',fg='white',anchor='w',relief='groove')
uploadBtn.grid(row=1,column=1,pady=5)

load = Image.open("capture.png")
render = ImageTk.PhotoImage(load)
img = Label(f2, image=render)
img.image = render
img.pack(side=TOP)
prevBtn=Button(f2,font=('arial',16,'bold'),text='<< Previous',width=15,bd=8,bg='red',fg='white',anchor='w',relief='groove')
prevBtn.pack(side=LEFT,pady=10)
uploadBtn=Button(f2,font=('arial',16,'bold'),text='Next >>',width=15,bd=8,bg='green',fg='white',anchor='w',relief='groove')
uploadBtn.pack(side=RIGHT,pady=10)


    
window.mainloop()
