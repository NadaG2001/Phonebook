
from argparse import _CountAction
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
#import pymysql
import sqlite3


window = Tk()
window.title("Phonebook")
window.iconbitmap('pho5.ico')
window.geometry('570x400+500+150')
window.configure(bg='#E8EAF6')
window.resizable(width=False, height=False)

######## create database ###########
conn = sqlite3.connect('@@people_con.db')
c = conn.cursor()
c.execute(""" CREATE TABLE IF NOT EXISTS persons(
    namee text,
    email varchar(20),
    id integer,
    phone varchar(20)
    
);
""")

# commit changes
conn.commit()

# close connection
conn.close()

####### Query database ########


def query_database():
    conn = sqlite3.connect('@@people_con.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM persons")
    records = c.fetchall()

    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(
                record[1], record[2], record[0], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(
                record[1], record[2], record[0], record[4]), tags=('oddrow',))
        count += 1

    # commit changes
    conn.commit()

    # close connection
    conn.close()


name = StringVar()
email = StringVar()
id = StringVar()
phone_number = StringVar()

########### Exit Window ########


def iExit():
    iExit = tkinter.messagebox.askyesno(
        "Phonebook", "Confirm if you want to exit?")
    if iExit > 0:
        window.destroy()
        return

########### delete record ############


def Delete():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    conn = sqlite3.connect('@@people_con.db')
    c = conn.cursor()
    # delete from database
    c.execute("DELETE FROM persons WHERE oid =" + entry_id.get())

    # commit changes
    conn.commit()
    # close connection
    conn.close()
    Clear_entries()
    tkinter.messagebox.showinfo("Deleted!", "record has been deleted")

########### search record ###########


def search_record():
    sear = entry_search.get()
    for record in my_tree.get_children():
        my_tree.delete(record)
    conn = sqlite3.connect('@@people_con.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM persons WHERE namee like '%" + sear + "%'")
    records = c.fetchall()

    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(
                record[1], record[2], record[0], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(
                record[1], record[2], record[0], record[4]), tags=('oddrow',))
        count += 1

    # commit changes
    conn.commit()

    # close connection
    conn.close()

############ Read record #############


def read_record(e):
    # clear the boxes
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_id.delete(0, END)
    entry_phoneNumber.delete(0, END)

    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    entry_name.insert(0, values[0])
    entry_email.insert(0, values[1])
    entry_id.insert(0, values[2])
    entry_phoneNumber.insert(0, values[3])

############# Clear entries ###########


def Clear_entries():
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_id.delete(0, END)
    entry_phoneNumber.delete(0, END)


############### Update ###############
def update_record():
    selected = my_tree.focus()
    my_tree.item(selected, text="", values=(entry_name.get(),
                 entry_email.get(), entry_id.get(), entry_phoneNumber.get()))

    # update the database
    conn = sqlite3.connect('@@people_con.db')
    c = conn.cursor()

    c.execute("""UPDATE persons SET
        namee = :nam,
        email = :em,
        phone =:pho

        WHERE oid = :oid""",
              {
                  'nam': entry_name.get(),
                  'em': entry_email.get(),
                  'pho': entry_phoneNumber.get(),
                  'oid': entry_id.get(),

              }
              )
    # commit changes
    conn.commit()
    # close connection
    conn.close()

    # clear the boxes
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_id.delete(0, END)
    entry_phoneNumber.delete(0, END)

######## add record ##########


def add_record():

    conn = sqlite3.connect('@@people_con.db')
    c = conn.cursor()

    c.execute("INSERT INTO persons VALUES(:namee, :email,:id,:phone)",
              {
                  'namee': entry_name.get(),
                  'email': entry_email.get(),
                  'id': entry_id.get(),
                  'phone': entry_phoneNumber.get(),

              }
              )

    # commit changes
    conn.commit()
    # close connection
    conn.close()
    # clear the boxes
    entry_name.delete(0, END)
    entry_phoneNumber.delete(0, END)
    entry_email.delete(0, END)
    entry_id.delete(0, END)

    my_tree.delete(*my_tree.get_children())

    query_database()


# frames
frame_up = Frame(window, width=570, height=51, bg='#1A237E')
frame_up.grid(row=0, column=0, padx=0, pady=0)

frame_down = Frame(window, width=570, height=300, bg='#E8EAF6')
frame_down.grid(row=1, column=0, padx=0, pady=30)


# frame_up widget
app_name = Label(frame_up, text="phonebook", height=1, font=(
    'verdana 17 bold'), bg='#1A237E', fg='#E8EAF6')
app_name.place(x=5, y=5)

# frame_down widget
label_name = Label(frame_down, text='Name *', width=10, height=1,
                   font=('verdana 10'), anchor=NW, bg="#E8EAF6", fg='#424242')
label_name.place(x=8, y=5)
entry_name = Entry(frame_down, width=28, justify='left',
                   highlightthickness=2, relief="solid", textvariable=name)
entry_name.place(x=129, y=5)

label_email = Label(frame_down, text='Email *', width=10, height=1,
                    font=('verdana 10'), anchor=NW, bg="#E8EAF6", fg='#424242')
label_email.place(x=8, y=40)
entry_email = Entry(frame_down, width=28, justify='left',
                    highlightthickness=2, relief="solid", textvariable=email)
entry_email.place(x=129, y=40)

label_id = Label(frame_down, text='ID *', width=10, height=1,
                 font=('verdana 10'), anchor=NW, bg="#E8EAF6", fg='#424242')
label_id.place(x=8, y=75)
entry_id = Entry(frame_down, width=28, justify='left',
                 highlightthickness=2, relief="solid", textvariable=id)
entry_id.place(x=129, y=75)


label_phoneNunber = Label(frame_down, text='Phone Number *', width=13,
                          height=1, font=('verdana 10'), anchor=NW, bg="#E8EAF6", fg='#424242')
label_phoneNunber.place(x=8, y=110)
entry_phoneNumber = Entry(frame_down, width=28, justify='left',
                          highlightthickness=2, relief="solid", textvariable=phone_number)
entry_phoneNumber.place(x=129, y=110)

entry_search = Entry(frame_down, width=22, justify='left',
                     highlightthickness=2, relief="solid")
entry_search.place(x=410, y=0)

######### buttons ###########

button_search = Button(frame_down, text='Search', width=6, font=(
    'verdana 8'), bg="#1A237E", fg='#E8EAF6', command=search_record)
button_search.place(x=355, y=0)

button_clear = Button(frame_down, text='Clear', width=9, fg='#E8EAF6', bg='#1A237E',
                      activebackground='#3F51B5', font=('verdana 8 bold'), command=Clear_entries)
button_clear.place(x=361, y=33)

button_add = Button(frame_down, text='Add', width=10, fg='#E8EAF6', bg='#1A237E',
                    activebackground='#3F51B5', font=('verdana 8 bold'), command=add_record)
button_add.place(x=460, y=32)

button_update = Button(frame_down, text='Update', width=10, fg='#E8EAF6', bg='#1A237E',
                       activebackground='#3F51B5', font=('verdana 8 bold'), command=update_record)
button_update.place(x=460, y=59)

button_delete = Button(frame_down, text='Delete', width=10, fg='#E8EAF6', bg='#1A237E',
                       activebackground='#3F51B5', font=('verdana 8 bold'), command=Delete)
button_delete.place(x=460, y=85)

button_delete = Button(frame_down, text='Exit', width=10, fg='#E8EAF6', bg='#1A237E',
                       activebackground='#3F51B5', font=('verdana 8 bold'), command=iExit)
button_delete.place(x=460, y=112)

#### create TreeView  ####

frame_table = Frame(frame_down, width=530, height=200, bg='#EEE', relief=FLAT)
frame_table.place(x=15, y=150)

#### create TreeView  ####
frame_table = Frame(frame_down, width=530, height=200, bg='#EEE', relief=FLAT)
frame_table.place(x=15, y=150)

style = ttk.Style()
style.theme_use('default')
style.configure("Treeview",
                bg="D3D3D3", fg="black", rowheight=25, fieldbackground="D3D3D3")
style.map('Treeview', bg=[('selected', '#347083')])


tree_frame = Frame(frame_table)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, height=4,
                       yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()
tree_scroll.config(command=my_tree.yview)
my_tree['columns'] = ("Name", "Email", "ID", "phone Number")
my_tree.column("#0", width=0, stretch="No")
my_tree.column("Name", anchor=W, width=150)
my_tree.column("Email", anchor=CENTER, width=153)
my_tree.column("ID", anchor=CENTER, width=40)
my_tree.column("phone Number", anchor=CENTER, width=185)
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Email", text="Email", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("phone Number", text="phone Number", anchor=CENTER)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


#### bind treeview ###
my_tree.bind("<ButtonRelease-1>", read_record)

# run to pull data from database on start
query_database()
window.mainloop()
