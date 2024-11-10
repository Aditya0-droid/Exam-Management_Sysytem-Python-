import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# File paths
students_file = Path("students.json")
results_file = Path("results.json")
admin_file = Path("admin.json")


# Setup the files if not already present
def setup_files():
    if not students_file.exists():
        with open(students_file, "w") as f:
            json.dump([], f)  # Empty list for storing student data
    if not results_file.exists():
        with open(results_file, "w") as f:
            json.dump([], f)  # Empty list for storing results data
    if not admin_file.exists():
        with open(admin_file, "w") as f:
            json.dump({}, f)  # Empty dict for admin credentials


# Function to register a student
def register_student(name, email):
    with open(students_file, "r+") as f:
        students = json.load(f)
        students.append({"name": name, "email": email})
        f.seek(0)
        json.dump(students, f, indent=4)
    messagebox.showinfo("Registration", "Student registered successfully!")


# Function to login student
def login_student(email):
    with open(students_file, "r") as f:
        students = json.load(f)
        for student in students:
            if student["email"] == email:
                return True
    return False


# Function to take the exam and save results
def take_exam(student_email):
    questions = [
        ("What is 2 + 2?", ["3", "4", "5"], 2),
        ("What is the capital of France?", ["Berlin", "Paris", "Rome"], 2),
        ("What is the boiling point of water?", ["90°C", "100°C", "110°C"], 2),
    ]
    score = 0

    # Create a new window to present each question and options
    def ask_question(question, options, correct_option):
        nonlocal score

        # Create a new window for each question
        question_window = tk.Toplevel()
        question_window.title("Exam Question")

        ttk.Label(question_window, text=question).grid(row=0, column=0, padx=10, pady=10)

        # Create buttons for the options
        def on_option_selected(answer):
            nonlocal score
            if answer == correct_option:
                score += 1
            question_window.destroy()  # Close the question window

        for idx, option in enumerate(options, 1):
            ttk.Button(question_window, text=option, command=lambda idx=idx: on_option_selected(idx)).grid(row=idx,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=5)

        # After the last question, show finish button
        if len(options) == 3:
            finish_button = ttk.Button(question_window, text="Finish", command=on_finish)
            finish_button.grid(row=len(options) + 1, column=0, padx=10, pady=10)

    # Finish button logic to save results and show score
    def on_finish():
        with open(results_file, "r+") as f:
            results = json.load(f)
            results.append({"email": student_email, "score": f"{score}/{len(questions)}"})
            f.seek(0)
            json.dump(results, f, indent=4)
        messagebox.showinfo("Result", f"Your total score is {score}/{len(questions)}")

        # Show admin the results
        view_results()  # Automatically display results after exam

    # Ask each question one by one
    for idx, (question, options, correct_option) in enumerate(questions, 1):
        ask_question(question, options, correct_option)


# Function to handle admin registration
def admin_register(username, password):
    with open(admin_file, "w") as f:
        json.dump({"username": username, "password": password}, f)
    messagebox.showinfo("Admin Registration", "Admin registered successfully!")


# Function for admin login
def admin_login(username, password):
    with open(admin_file, "r") as f:
        admin_credentials = json.load(f)
        if admin_credentials["username"] == username and admin_credentials["password"] == password:
            return True
    return False


# Function to view results as admin
def view_results():
    with open(results_file, "r") as f:
        results = json.load(f)
        if results:
            results_text = "\n".join([f"Student: {result['email']}, Score: {result['score']}" for result in results])
            messagebox.showinfo("Results", results_text)
        else:
            messagebox.showinfo("Results", "No results available.")


# GUI setup
def create_gui():
    setup_files()  # Ensure files are set up on startup

    # Create the main window
    root = tk.Tk()
    root.title("Exam Management System")

    # Configure the main frame and components
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky="nsew")

    # Add widgets like labels, buttons, and text fields for user interaction

    def show_register_student_form():
        def on_register():
            name = name_entry.get()
            email = email_entry.get()
            if name and email:
                register_student(name, email)
                name_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Input Error", "Please fill in both fields.")

        register_window = tk.Toplevel(root)
        register_window.title("Register Student")

        ttk.Label(register_window, text="Name").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(register_window, text="Email").grid(row=1, column=0, padx=10, pady=5)

        name_entry = ttk.Entry(register_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        email_entry = ttk.Entry(register_window)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(register_window, text="Register", command=on_register).grid(row=2, column=1, padx=10, pady=5)

    def show_student_login_form():
        def on_login():
            email = email_entry.get()
            if login_student(email):
                messagebox.showinfo("Login Success", f"Welcome {email}!")
                take_exam(email)
            else:
                messagebox.showerror("Login Failed", "Student not found. Please register first.")

        login_window = tk.Toplevel(root)
        login_window.title("Student Login")

        ttk.Label(login_window, text="Email").grid(row=0, column=0, padx=10, pady=5)

        email_entry = ttk.Entry(login_window)
        email_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(login_window, text="Login", command=on_login).grid(row=1, column=1, padx=10, pady=5)

    def show_admin_login_form():
        def on_login():
            username = username_entry.get()
            password = password_entry.get()
            if admin_login(username, password):
                messagebox.showinfo("Admin Login", "Admin login successful!")
                view_results()
            else:
                messagebox.showerror("Login Failed", "Invalid admin credentials.")

        login_window = tk.Toplevel(root)
        login_window.title("Admin Login")

        ttk.Label(login_window, text="Username").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(login_window, text="Password").grid(row=1, column=0, padx=10, pady=5)

        username_entry = ttk.Entry(login_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(login_window, text="Login", command=on_login).grid(row=2, column=1, padx=10, pady=5)

    def show_admin_register_form():
        def on_register():
            username = username_entry.get()
            password = password_entry.get()
            if username and password:
                admin_register(username, password)
            else:
                messagebox.showerror("Input Error", "Please fill in both fields.")

        register_window = tk.Toplevel(root)
        register_window.title("Register Admin")

        ttk.Label(register_window, text="Username").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(register_window, text="Password").grid(row=1, column=0, padx=10, pady=5)

        username_entry = ttk.Entry(register_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        password_entry = ttk.Entry(register_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(register_window, text="Register", command=on_register).grid(row=2, column=1, padx=10, pady=5)

    # Main Menu for the application
    ttk.Button(frame, text="Register Student", command=show_register_student_form).grid(row=0, column=0, padx=10,
                                                                                        pady=10)
    ttk.Button(frame, text="Login Student", command=show_student_login_form).grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(frame, text="Admin Login", command=show_admin_login_form).grid(row=2, column=0, padx=10, pady=10)
    ttk.Button(frame, text="Register Admin", command=show_admin_register_form).grid(row=3, column=0, padx=10, pady=10)

    root.mainloop()



if __name__ == "__main__":
    create_gui()
