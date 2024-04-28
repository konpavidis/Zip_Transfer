import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from threading import Thread
from zipfile import ZipFile
import time

def load_saved_destinations():
    if os.path.exists("saved_destinations.txt"):
        with open("saved_destinations.txt", "r") as file:
            return file.read().splitlines()
    else:
        return []

def save_destinations_to_file(destinations):
    with open("saved_destinations.txt", "w") as file:
        for destination in destinations:
            file.write(destination + "\n")

def cleanup_destinations():
    global saved_destinations
    existing_destinations = [dest for dest in saved_destinations if os.path.exists(dest)]
    if len(existing_destinations) < len(saved_destinations):
        save_destinations_to_file(existing_destinations)
        saved_destinations = existing_destinations

def backup_directory_async(source_path, destination_path, zip_filename_entry, progress_var, remaining_time_label, result_label):
    try:
        zip_filename = zip_filename_entry.get() + ".zip" if zip_filename_entry.get() else os.path.basename(source_path) + ".zip"
        zip_filepath = os.path.join(destination_path, zip_filename)

        def update_progress(current, total, start_time):
            progress_value = int((current / total) * 100)
            progress_var.set(progress_value)

            elapsed_time = time.time() - start_time[0]
            remaining_time = (elapsed_time / current) * (total - current)
            remaining_time_label.config(text=f"Remaining Time: {int(remaining_time)} seconds")

            root.update_idletasks()

        def backup_thread(start_time):
            start_time[0] = time.time()

            with ZipFile(zip_filepath, 'w') as zipf:
                total_files = sum(1 for root, dirs, files in os.walk(source_path) for _ in files)
                current_file = 0

                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        current_file += 1
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname=arcname)

                        update_progress(current_file, total_files, start_time)

                        time.sleep(0.01)

            progress_var.set(100)
            remaining_time_label.config(text="")
            result_label.config(text="Backup completed successfully.")
            clear_fields()

        start_time = [0]
        backup_thread = Thread(target=backup_thread, args=(start_time,))
        backup_thread.start()

    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")

def backup_directory(source_path, destination_path, zip_filename_entry, progress_var, remaining_time_label, result_label):
    root.after(0, backup_directory_async, source_path, destination_path, zip_filename_entry, progress_var, remaining_time_label, result_label)

def browse_destination_directory():
    destination_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_path)
    save_destination(destination_path)

def show_saved_destinations():
    cleanup_destinations()

    saved_destinations_window = tk.Toplevel(root)
    saved_destinations_window.title("Saved Destinations")

    destinations_listbox = tk.Listbox(saved_destinations_window, selectmode=tk.SINGLE, height=10, width=50)
    destinations_listbox.pack(pady=10)

    for destination in saved_destinations:
        destinations_listbox.insert(tk.END, destination)

    def choose_destination():
        selected_index = destinations_listbox.curselection()
        if selected_index:
            selected_destination = destinations_listbox.get(selected_index[0])
            if os.path.exists(selected_destination):
                destination_entry.delete(0, tk.END)
                destination_entry.insert(0, selected_destination)
                saved_destinations_window.destroy()
            else:
                messagebox.showinfo("Error", "Missing Filepath")
                saved_destinations.remove(selected_destination)
                save_destinations_to_file(saved_destinations)
                destinations_listbox.delete(selected_index)

    ok_button = tk.Button(saved_destinations_window, text="OK", command=choose_destination)
    ok_button.pack(pady=10)

saved_destinations = load_saved_destinations()

def save_destination(destination_path):
    if destination_path not in saved_destinations and os.path.exists(destination_path):
        saved_destinations.append(destination_path)
        save_destinations_to_file(saved_destinations)

def browse_source_directory():
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_path)

def clear_fields():
    source_entry.delete(0, tk.END)
    destination_entry.delete(0, tk.END)
    zip_filename_entry.delete(0, tk.END)

def create_gui():
    global root, source_label, source_entry, browse_source_button, destination_label, destination_entry, browse_destination_button, zip_filename_label, zip_filename_entry, show_saved_button, progress_var, progress_bar, remaining_time_label, backup_button, result_label
    root = tk.Tk()
    root.title("Backup Tool")

    source_label = tk.Label(root, text="Source Directory:")
    source_label.pack(pady=5)

    source_entry = tk.Entry(root, width=50)
    source_entry.pack(pady=5)

    browse_source_button = tk.Button(root, text="Browse", command=browse_source_directory)
    browse_source_button.pack(pady=5)

    destination_label = tk.Label(root, text="Destination Directory:")
    destination_label.pack(pady=5)

    destination_entry = tk.Entry(root, width=50)
    destination_entry.pack(pady=5)

    browse_destination_button = tk.Button(root, text="Browse", command=browse_destination_directory)
    browse_destination_button.pack(pady=5)

    zip_filename_label = tk.Label(root, text="Zip Filename:")
    zip_filename_label.pack(pady=5)

    zip_filename_entry = tk.Entry(root, width=50)
    zip_filename_entry.pack(pady=5)

    show_saved_button = tk.Button(root, text="Show Saved Destinations", command=show_saved_destinations)
    show_saved_button.pack(pady=5)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, mode='determinate', variable=progress_var)
    progress_bar.pack(pady=5)

    remaining_time_label = tk.Label(root, text="")
    remaining_time_label.pack(pady=5)

    backup_button = tk.Button(root, text="Backup", command=lambda: backup_directory(source_entry.get(), destination_entry.get(), zip_filename_entry, progress_var, remaining_time_label, result_label))
    backup_button.pack(pady=10)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
