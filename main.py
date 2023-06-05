import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

files = []  # Global variable to store the list of files


def list_files(directory, sort_order):
    global files  # Declare files as a global variable
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                files.append(file_path)

    if sort_order == "Alphabetical":
        files.sort(key=lambda x: os.path.basename(x))
    elif sort_order == "Date":
        files.sort(key=lambda x: os.path.getmtime(x))

    return files


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        file_list.delete(*file_list.get_children())  # Clear the file list
        files = list_files(directory, sort_var.get())
        if files:
            for file in files:
                file_list.insert("", "end", values=[file])
        else:
            messagebox.showinfo("No Files", "No files found in the selected directory.")


def clear_list():
    file_list.delete(*file_list.get_children())


def search_files(event=None):
    search_text = search_var.get()
    file_list.delete(*file_list.get_children())  # Clear the file list
    found_files = []
    for file in files:
        if search_text.lower() in file.lower():
            file_list.insert("", "end", values=[file])
            found_files.append(file)
    if found_files:
        # Create a new popup window to display the found files
        popup_window = tk.Toplevel(window)
        popup_window.title("Search Results")

        # Create a Listbox widget to display the found files
        file_listbox = tk.Listbox(popup_window)
        file_listbox.pack(fill=tk.BOTH, expand=True)

        # Insert the found files into the Listbox
        for file in found_files:
            file_listbox.insert(tk.END, file)
    else:
        messagebox.showinfo("Search Results", "No files found.")


# Create the main window
window = tk.Tk()
window.title("File List")

# Create the frame
frame = ttk.Frame(window, padding="20")
frame.grid(row=0, column=0, sticky="nsew")

# Create the file list treeview
columns = ("Files",)
file_list = ttk.Treeview(frame, columns=columns, show="headings")
file_list.heading("Files", text="Files")
file_list.column("Files", width=600)
file_list.grid(row=0, column=0, sticky="nsew")

# Create the scrollbar for the file list
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=file_list.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
file_list.configure(yscrollcommand=scrollbar.set)

# Create the browse button
browse_button = ttk.Button(window, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=0, pady=10)

# Create the clear button
clear_button = ttk.Button(window, text="Clear", command=clear_list)
clear_button.grid(row=2, column=0, pady=5)

# Create the sort order options
sort_label = ttk.Label(window, text="Sort Order:")
sort_label.grid(row=3, column=0, pady=5)

sort_var = tk.StringVar()
sort_var.set("Alphabetical")

sort_options = ["Alphabetical", "Date"]
sort_dropdown = ttk.Combobox(window, textvariable=sort_var, values=sort_options, state="readonly")
sort_dropdown.grid(row=4, column=0)

# Create the search bar
search_var = tk.StringVar()
search_entry = ttk.Entry(window, textvariable=search_var)
search_entry.grid(row=5, column=0, pady=5)
search_entry.bind("<Return>", search_files)  # Bind Enter key to search_files function

search_button = ttk.Button(window, text="Search", command=search_files)
search_button.grid(row=6, column=0, pady=5)

# Configure grid weights
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Start the main loop
window.mainloop()
