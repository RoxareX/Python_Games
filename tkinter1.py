from tkinter import *

root = Tk()
root.configure(bg='black')

frame1 = LabelFrame(root, padx=10, pady=10, bg='darkblue')
frame1.pack(padx=15, pady=15)

frame2 = LabelFrame(root, padx=10, pady=10, bg='darkblue')
frame2.pack(padx=15, pady=50)

hm1 = Entry(frame1)
hm1.insert(END, "1")
hm1.pack(pady=5)

e1 = Entry(frame1)
e1.pack()

e2 = Entry(frame1)
e2.pack()

master_1 = hm1
master1 = e1
master2 = e2

#------------------------------------------------------------------------------------
hm2 = Entry(frame2)
hm2.insert(END, "1")
hm2.pack(pady=5)

e3 = Entry(frame2)
e3.pack()

e4 = Entry(frame2)
e4.pack()

e5 = Entry(frame2)
e5.pack()

master_2 = hm2
master3 = e3
master4 = e4
master5 = e5

def calculate1(event):
    calc1 = (int(e1.get()) * int(e2.get())) * int(hm1.get())
    calc2 = (int(e1.get()) * int(e2.get()) / 100) * int(hm1.get())
    calc3 = (int(e1.get()) * int(e2.get()) / 1000000) * int(hm1.get())

    global answer1, answer2, answer3

    answer1 = Label(frame1, text=(calc1, "mm2"), bg='darkblue', fg='white')
    answer1.pack()

    answer2 = Label(frame1, text=(calc2, "cm2"), bg='darkblue', fg='white')
    answer2.pack()

    answer3 = Label(frame1, text=(calc3, "m2"), bg='darkblue', fg='white')
    answer3.pack()
    
def clear1(event):
    answer1.destroy()
    answer2.destroy()
    answer3.destroy()

#---------------------------------------------------------------------------------------------------------
def calculate2(event):
    calc4 = (int(e3.get()) * int(e4.get()) * int(e5.get())) * int(hm2.get())
    calc5 = (int(e3.get()) * int(e4.get()) * int(e5.get()) / 1000) * int(hm2.get())
    calc6 = (int(e3.get()) * int(e4.get()) * int(e5.get()) / 1000000000) * int(hm2.get())

    global answer4, answer5, answer6

    answer4 = Label(frame2, text=(calc4, "mm3"), bg='darkblue', fg='white')
    answer4.pack()

    answer5 = Label(frame2, text=(calc5, "cm3"), bg='darkblue', fg='white')
    answer5.pack()

    answer6 = Label(frame2, text=(calc6, "m3"), bg='darkblue', fg='white')
    answer6.pack()

def clear2(event):
    answer4.destroy()
    answer5.destroy()
    answer6.destroy()


calcButton = Button(frame1, text="Calculate", bg='white')
master_1.bind("<Return>", calculate1)
master1.bind("<Return>", calculate1)
master2.bind("<Return>", calculate1)
calcButton.bind("<Return>", calculate1)
calcButton.bind("<Button-1>", calculate1)
calcButton.pack(pady=4)

desButton = Button(frame1, text="Clear", bg='white')
master_1.bind("c", clear1)
master1.bind("c", clear1)
master2.bind("c", clear1)
desButton.bind("c", clear1)
desButton.bind("<Button-1>", clear1)
desButton.pack()

#-------------------------------------------------------------------------------------
calcButton = Button(frame2, text="Calculate", bg='white')
master_2.bind("<Return>", calculate2)
master3.bind("<Return>", calculate2)
master4.bind("<Return>", calculate2)
master5.bind("<Return>", calculate2)
calcButton.bind("<Return>", calculate2)
calcButton.bind("<Button-1>", calculate2)
calcButton.pack(pady=4)

desButton = Button(frame2, text="Clear", bg='white')
master_2.bind("c", clear2)
master3.bind("c", clear2)
master4.bind("c", clear2)
master5.bind("c", clear2)
desButton.bind("c", clear2)
desButton.bind("<Button-1>", clear2)
desButton.pack()


root.mainloop()