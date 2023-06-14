import tkinter as tk
from tkinter import simpledialog
import string
import secrets

from tkinter.filedialog import asksaveasfilename

#sqlite3 stuff
import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS text_info (id INTEGER PRIMARY KEY, content TEXT NOT NULL)"
cursor.execute(create_table_query)

# import database info
select_query = "SELECT content FROM text_info"
cursor.execute(select_query)

# on the first open of the program there wont be any lists so it's to avoid any error messages
try:
    # converts from list with a tuple to correctly formatted string. Theres probably a better way to do it but who cares as long as I get the result
    results = cursor.fetchall()
    real_results = results[0]
    string_value = ''.join(real_results)
    split_string = string_value.rsplit('\n', 1)
    modified_string = ''.join(split_string)
except:
    pass


def on_closing():
    # save everything for the last time
    save_text_to_database()

    # close the database here I guess
    connection.close()
    root.destroy()


def save_text_to_database():
    # refreshes the text container text that is stored inside local database
    delete_query = "DELETE FROM text_info"
    cursor.execute(delete_query)

    # gets the current text displayed to the user
    text = text_widget.get("1.0", "end")

    # inserts that thext into a datatable
    insert_query = "INSERT INTO text_info (content) VALUES (?)"
    data = (text,)
    cursor.execute(insert_query, data)

    # saves probably?
    connection.commit()

    # just displays a message
    label_instructions.config(text='Text container information saved')



def is_natural_number(value):
    if isinstance(value, int) and value > 0:
        return value
    else:
        return None


def add_to_text_container(event=None):
    entry_value = entry.get()

    if entry_value == '':
        label_instructions.config(text='Please type in your username/gmail')
        return

    number = simpledialog.askinteger("Select password lenght", "Please enter a natural number (meaning you cant enter [-1, 1.2, abc, etc.]):")
    number = is_natural_number(number)

    if number != None:
        if entry_value:
            # generates random password
            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(characters) for _ in range(number))

            # formats the text that is printed to text_widget
            text_widget.insert(tk.END, f'Username/gmail: "{entry_value}" \npassword: "{password}" \nwebsite/app name: "Your Registration Website/App" \n\n')
            entry.delete(0, tk.END)

            # calls the save function so it wont happed that user forgot to click save button and forgets its passwords
            save_text_to_database()
    label_instructions.config(text='Text added and saved to the text container. You can save/rewrite the text to a .txt file by clicking (save to .txt file) button.')
            

def save_to_txt_file():
    # prompts the user for file location
    file_path = asksaveasfilename(title="Save Text File", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    # checks if the file location exists
    if file_path:
        # adds the .txt extention if it doesnt exist already
        if not file_path.endswith(".txt"):
            file_path += ".txt"

        # Open file
        with open(file_path, 'w') as file:
            # gets the text in the current window
            text = text_widget.get("1.0", "end")

            # wrait to the fail
            file.write(text)

    label_instructions.config(text='File saved')



def main():
    global entry, text_widget, root, label_instructions

    root = tk.Tk()
    root.title("Password manager")
    root.geometry("750x650")

    # Frame object
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Guide label
    label_guide = tk.Label(frame, text='Type here your username and or gmail. After pressing enter it will ask you for the lenght of the password and after that it will print it to the text window :)')
    label_guide.configure(justify='left', wraplength=200)
    label_guide.pack()

    # Input field
    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, padx=4)
    entry.bind("<Return>", add_to_text_container)

    # Add Button
    add_button = tk.Button(frame, text='add', command=add_to_text_container)
    add_button.pack(side=tk.LEFT)

    # Instructions Label
    label_instructions = tk.Label(text='Save button is for saving text container so next time you open the program it loads your saved text')
    label_instructions.pack(pady=3)

    # Text Container
    text_widget = tk.Text(root, font='Inter')
    text_widget.pack()

    # Lower Frame for save buttons
    lower_frame = tk.Frame(root)
    lower_frame.pack()

    # save button to save the text
    save_button = tk.Button(lower_frame, text='save', command=save_text_to_database)
    save_button.pack(side=tk.LEFT)
    
    # save button but for a txt file this time
    txt_save_button = tk.Button(lower_frame, text='save to .txt file', command=save_to_txt_file)
    txt_save_button.pack(side=tk.LEFT)

    # on the first open of the program there is no variable modified_string so it's just to avoid error message
    try:
        # writes previous text to the text widget
        text_widget.insert('1.0', modified_string)
    except:
        pass
    #when window closes clear things and close database
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()