from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
# import pyperclip
import json

window = Tk()
window.title("Password Manager")
window.minsize(width=600, height=600)
window.config(padx=60, pady=60)

letters = ['a', 'b', 'c', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '&', '%', '@', '(', ')', '*', '+']


def generate_password():
    p_letters = [choice(letters) for _ in range(randint(8, 10))]
    p_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    p_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = p_letters + p_symbols + p_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_label.insert(0, password)
    # pyperclip.copy(password)


def save():
    website = web_label.get()
    email = email_label.get()
    password = password_label.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="ohhh!", message="Please fill in the empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            web_label.delete(0, END)
            password_label.delete(0, END)


def find_password():
    website = web_label.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No Details for {website} exist.")


web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
web_label = Entry(width=34)
web_label.grid(column=1, row=1)
web_label.focus()

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
email_label = Entry(width=52)
email_label.insert(0, "kagisele@outlook.com")
email_label.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_label = Entry(width=33)
password_label.grid(column=1, row=3)

general_Button = Button(text="Generate Password", command=generate_password)
general_Button.grid(column=2, row=3)

add_Button = Button(text="Add", width=45, command=save)
add_Button.grid(row=4, column=1, columnspan=2)

search_Button = Button(text="Search", width=14, command=find_password)
search_Button.grid(row=1, column=2)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="lock.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

window.mainloop()
