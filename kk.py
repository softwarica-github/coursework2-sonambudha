import os
import tkinter as tk
from tkinter import filedialog, messagebox

class Inode:
    def __init__(self, inode_number, filename, permissions):
        self.inode_number = inode_number
        self.filename = filename
        self.permissions = permissions

    def get_permissions_str(self):
        perm_str = ""
        perm_str += "r" if self.permissions & 0o400 else "-"
        perm_str += "w" if self.permissions & 0o200 else "-"
        perm_str += "x" if self.permissions & 0o100 else "-"
        return perm_str

class InodeTable:
    def __init__(self):
        self.inodes = []
        self.next_inode_number = 1

    def add_inode(self, filename, permissions):
        inode = Inode(self.next_inode_number, filename, permissions)
        self.inodes.append(inode)
        self.next_inode_number += 1
        return inode

    def list_inodes(self):
        inode_list = []
        for inode in self.inodes:
            perm_str = inode.get_permissions_str()
            inode_list.append(f"Inode {inode.inode_number}: {inode.filename} - Permissions: {perm_str}")
        return inode_list

def create_file(file_name, permissions, content):
    with open(file_name, 'w') as file:
        file.write(content)

    os.chmod(file_name, permissions)

def create_folder(name, permissions):
    os.mkdir(name)
    os.chmod(name, permissions)

def get_permissions_input():
    read = read_var.get()
    write = write_var.get()
    execute = execute_var.get()

    permissions = 0
    if read:
        permissions |= 0o400
    if write:
        permissions |= 0o200
    if execute:
        permissions |= 0o100

    return permissions

def on_create_file():
    file_name = file_name_entry.get()
    permissions = get_permissions_input()
    notes = notes_text.get('1.0', tk.END)
    create_file(file_name, permissions, notes)
    inode = inode_table.add_inode(file_name, permissions)
    status_label.config(text=f"File '{file_name}' created with permissions {oct(permissions)}, inode {inode.inode_number}")

def on_create_folder():
    folder_name = folder_name_entry.get()
    permissions = get_permissions_input()
    create_folder(folder_name, permissions)
    inode = inode_table.add_inode(folder_name, permissions)
    status_label.config(text=f"Folder '{folder_name}' created with permissions {oct(permissions)}, inode {inode.inode_number}")

def on_list_inodes():
    listbox.delete(0, tk.END)
    inode_list = inode_table.list_inodes()
    for item in inode_list:
        listbox.insert(tk.END, item)

def on_read_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        messagebox.showwarning("Warning", "No file selected.")
        return

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text_window = tk.Toplevel(root)
            text_window.title("File Contents")
            text_widget = tk.Text(text_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {str(e)}")

root = tk.Tk()
root.title("File Management System")

inode_table = InodeTable()

# Create a file frame
file_frame = tk.Frame(root, padx=10, pady=10)
file_frame.pack(fill=tk.BOTH, expand=True)

file_name_label = tk.Label(file_frame, text="File Name:")
file_name_label.pack(side=tk.LEFT)

file_name_entry = tk.Entry(file_frame)
file_name_entry.pack(side=tk.LEFT, padx=5)

permission_frame = tk.Frame(file_frame)
permission_frame.pack(side=tk.LEFT)

read_var = tk.BooleanVar()
write_var = tk.BooleanVar()
execute_var = tk.BooleanVar()

read_check = tk.Checkbutton(permission_frame, text="Read", variable=read_var)
write_check = tk.Checkbutton(permission_frame, text="Write", variable=write_var)
execute_check = tk.Checkbutton(permission_frame, text="Execute", variable=execute_var)

read_check.pack(side=tk.LEFT)
write_check.pack(side=tk.LEFT)
execute_check.pack(side=tk.LEFT)

create_file_button = tk.Button(file_frame, text="Create File", command=on_create_file)
create_file_button.pack(side=tk.LEFT, padx=5)

# Create a folder frame
folder_frame = tk.Frame(root, padx=10, pady=10)
folder_frame.pack(fill=tk.BOTH, expand=True)

folder_name_label = tk.Label(folder_frame, text="Folder Name:")
folder_name_label.pack(side=tk.LEFT)

folder_name_entry = tk.Entry(folder_frame)
folder_name_entry.pack(side=tk.LEFT, padx=5)

folder_permission_frame = tk.Frame(folder_frame)
folder_permission_frame.pack(side=tk.LEFT)

folder_read_check = tk.Checkbutton(folder_permission_frame, text="Read", variable=read_var)
folder_write_check = tk.Checkbutton(folder_permission_frame, text="Write", variable=write_var)
folder_execute_check = tk.Checkbutton(folder_permission_frame, text="Execute", variable=execute_var)

folder_read_check.pack(side=tk.LEFT)
folder_write_check.pack(side=tk.LEFT)
folder_execute_check.pack(side=tk.LEFT)

create_folder_button = tk.Button(folder_frame, text="Create Folder", command=on_create_folder)
create_folder_button.pack(side=tk.LEFT, padx=5)

# List inodes button
list_inodes_button = tk.Button(root, text="List Inodes", command=on_list_inodes)
list_inodes_button.pack(pady=10)

# Read file button
read_file_button = tk.Button(root, text="Read File", command=on_read_file)
read_file_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# Inode listbox
listbox_frame = tk.Frame(root)
listbox_frame.pack(fill=tk.BOTH, expand=True)

listbox = tk.Listbox(listbox_frame)
listbox.pack(fill=tk.BOTH, expand=True)

root.mainloop()