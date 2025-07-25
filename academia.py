import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import sqlite3
import hashlib
from datetime import datetime

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize database
def init_db():
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Classes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classes (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT,
        instructor TEXT
    )
    ''')

    # Enrollments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        student_id INTEGER,
        class_id INTEGER
    )
    ''')

    # Attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        student_id INTEGER,
        class_id INTEGER,
        date TEXT,
        status TEXT
    )
    ''')

    # Fees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fees (
        student_id INTEGER,
        total_fee INTEGER,
        amount_paid INTEGER
    )
    ''')

    # Payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        student_id INTEGER,
        amount INTEGER,
        date TEXT
    )
    ''')

    # Chat table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        class_id INTEGER,
        student_id INTEGER,
        message TEXT,
        timestamp TEXT
    )
    ''')

    # Timetable table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS timetable (
        class_id INTEGER,
        day TEXT,
        time_slot TEXT,
        subject TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Login/Signup Window
class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login / Signup")
        self.master.geometry("350x220")
        self.master.resizable(False, False)
        self.master.configure(bg="#f0f0f0")

        self.frame = tk.Frame(master, bg="#f0f0f0", padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        self.title_label = tk.Label(self.frame, text="Student Portal Login", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        self.label1 = tk.Label(self.frame, text="Username:", font=("Helvetica", 12), bg="#f0f0f0")
        self.label1.grid(row=1, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, pady=5, sticky='ew')

        self.label2 = tk.Label(self.frame, text="Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.label2.grid(row=2, column=0, sticky='w', pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', font=("Helvetica", 12))
        self.password_entry.grid(row=2, column=1, pady=5, sticky='ew')

        self.btn_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        self.login_btn = tk.Button(self.btn_frame, text="Login", width=12, command=self.login, bg="#4a90e2", fg="white", font=("Helvetica", 12))
        self.login_btn.pack(side='left', padx=10)

        self.signup_btn = tk.Button(self.btn_frame, text="Signup", width=12, command=self.signup, bg="#50c878", fg="white", font=("Helvetica", 12))
        self.signup_btn.pack(side='left', padx=10)

        self.frame.columnconfigure(1, weight=1)

    def login(self):
        username = self.username_entry.get().strip()
        password = hash_password(self.password_entry.get().strip())

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            self.master.destroy()
            root = tk.Tk()
            DashboardWindow(root, result[0], result[1])
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def signup(self):
        username = self.username_entry.get().strip()
        password = hash_password(self.password_entry.get().strip())

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Signup successful. You can now log in.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        conn.close()

# Dashboard Window
class DashboardWindow:
    def __init__(self, master, student_id, username):
        self.master = master
        self.master.title("Student Dashboard")
        self.master.geometry("400x350")
        self.master.resizable(False, False)
        self.master.configure(bg="#f7f7f7")

        self.student_id = student_id
        self.username = username

        self.frame = tk.Frame(master, bg="#f7f7f7", padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        welcome_text = f"Welcome, {username} (ID: {student_id})"
        tk.Label(self.frame, text=welcome_text, font=("Helvetica", 16, "bold"), bg="#f7f7f7").pack(pady=(0,20))

        btn_font = ("Helvetica", 13)
        btn_width = 25
        btn_pad_y = 7

        tk.Button(self.frame, text="Class Management", width=btn_width, font=btn_font,
                  command=self.open_class_manager, bg="#4a90e2", fg="white").pack(pady=btn_pad_y)

        tk.Button(self.frame, text="Attendance", width=btn_width, font=btn_font,
                  command=self.open_attendance, bg="#50c878", fg="white").pack(pady=btn_pad_y)

        tk.Button(self.frame, text="Fee Payment", width=btn_width, font=btn_font,
                  command=self.open_fees, bg="#f39c12", fg="white").pack(pady=btn_pad_y)

        tk.Button(self.frame, text="Group Chat", width=btn_width, font=btn_font,
                  command=self.open_chat, bg="#9b59b6", fg="white").pack(pady=btn_pad_y)

        tk.Button(self.frame, text="Timetable", width=btn_width, font=btn_font,
                  command=self.open_timetable, bg="#e74c3c", fg="white").pack(pady=btn_pad_y)

    def open_class_manager(self):
        ClassManagementWindow(self.master, self.student_id)

    def open_attendance(self):
        AttendanceWindow(self.master, self.student_id)

    def open_fees(self):
        FeesWindow(self.master, self.student_id)

    def open_chat(self):
        ChatWindow(self.master, self.student_id)

    def open_timetable(self):
        TimetableWindow(self.master, self.student_id)

# Class Management Window
class ClassManagementWindow(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.title("Class Management")
        self.geometry("600x400")
        self.configure(bg="#fff")

        self.student_id = student_id

        tk.Label(self, text="Class Management", font=("Helvetica", 16, "bold"), bg="#fff").pack(pady=10)

        # Frame for adding class
        form_frame = tk.Frame(self, bg="#fff")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Class Name:", bg="#fff").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.class_name_entry = tk.Entry(form_frame)
        self.class_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Instructor:", bg="#fff").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.instructor_entry = tk.Entry(form_frame)
        self.instructor_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Add Class", bg="#4a90e2", fg="white", command=self.add_class).grid(row=2, column=0, columnspan=2, pady=10)

        # Classes List
        self.tree = ttk.Treeview(self, columns=("ID", "Class Name", "Instructor"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Class Name", text="Class Name")
        self.tree.heading("Instructor", text="Instructor")
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Class Name", width=200)
        self.tree.column("Instructor", width=150)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_classes()

    def add_class(self):
        name = self.class_name_entry.get().strip()
        instructor = self.instructor_entry.get().strip()
        if not name or not instructor:
            messagebox.showwarning("Input Error", "Please fill both fields.")
            return

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (class_name, instructor) VALUES (?, ?)", (name, instructor))
        conn.commit()
        conn.close()
        self.class_name_entry.delete(0, 'end')
        self.instructor_entry.delete(0, 'end')
        self.load_classes()

    def load_classes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT class_id, class_name, instructor FROM classes")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)

# Attendance Window
class AttendanceWindow(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.title("Attendance")
        self.geometry("600x450")
        self.configure(bg="#fff")

        self.student_id = student_id

        tk.Label(self, text="Attendance", font=("Helvetica", 16, "bold"), bg="#fff").pack(pady=10)

        # Select class
        class_frame = tk.Frame(self, bg="#fff")
        class_frame.pack(pady=5)

        tk.Label(class_frame, text="Select Class:", bg="#fff").pack(side='left', padx=5)
        self.class_combo = ttk.Combobox(class_frame, state="readonly")
        self.class_combo.pack(side='left', padx=5)
        self.load_classes()

        # Date picker
        tk.Label(class_frame, text="Date (YYYY-MM-DD):", bg="#fff").pack(side='left', padx=5)
        self.date_entry = tk.Entry(class_frame)
        self.date_entry.pack(side='left', padx=5)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Status
        tk.Label(class_frame, text="Status:", bg="#fff").pack(side='left', padx=5)
        self.status_combo = ttk.Combobox(class_frame, values=["Present", "Absent"], state="readonly")
        self.status_combo.pack(side='left', padx=5)
        self.status_combo.current(0)

        # Add attendance button
        tk.Button(self, text="Mark Attendance", bg="#4a90e2", fg="white", command=self.mark_attendance).pack(pady=10)

        # Attendance List
        self.tree = ttk.Treeview(self, columns=("Class", "Date", "Status"), show='headings')
        self.tree.heading("Class", text="Class")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.column("Class", width=200)
        self.tree.column("Date", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_attendance()

    def load_classes(self):
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.class_id, c.class_name FROM classes c
            JOIN enrollments e ON c.class_id = e.class_id
            WHERE e.student_id=?
        ''', (self.student_id,))
        classes = cursor.fetchall()
        conn.close()
        self.class_map = {f"{name} (ID: {cid})": cid for cid, name in classes}
        self.class_combo['values'] = list(self.class_map.keys())
        if classes:
            self.class_combo.current(0)

    def mark_attendance(self):
        cls = self.class_combo.get()
        date = self.date_entry.get().strip()
        status = self.status_combo.get()
        if cls == "" or date == "" or status == "":
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Date must be in YYYY-MM-DD format.")
            return

        class_id = self.class_map.get(cls)
        if not class_id:
            messagebox.showerror("Selection Error", "Please select a valid class.")
            return

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (student_id, class_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (self.student_id, class_id, date, status))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Attendance marked.")
        self.load_attendance()

    def load_attendance(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.class_name, a.date, a.status FROM attendance a
            JOIN classes c ON a.class_id = c.class_id
            WHERE a.student_id=?
            ORDER BY a.date DESC
        ''', (self.student_id,))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)

# Fees Window
class FeesWindow(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.title("Fee Payment")
        self.geometry("600x400")
        self.configure(bg="#fff")

        self.student_id = student_id

        tk.Label(self, text="Fee Payment", font=("Helvetica", 16, "bold"), bg="#fff").pack(pady=10)

        self.total_fee_var = tk.StringVar()
        self.amount_paid_var = tk.StringVar()
        self.balance_var = tk.StringVar()

        frame = tk.Frame(self, bg="#fff")
        frame.pack(pady=10, padx=10)

        tk.Label(frame, text="Total Fee:", bg="#fff").grid(row=0, column=0, sticky='w', pady=5)
        tk.Label(frame, textvariable=self.total_fee_var, bg="#fff", fg="blue").grid(row=0, column=1, sticky='w', pady=5)

        tk.Label(frame, text="Amount Paid:", bg="#fff").grid(row=1, column=0, sticky='w', pady=5)
        tk.Label(frame, textvariable=self.amount_paid_var, bg="#fff", fg="green").grid(row=1, column=1, sticky='w', pady=5)

        tk.Label(frame, text="Balance:", bg="#fff").grid(row=2, column=0, sticky='w', pady=5)
        tk.Label(frame, textvariable=self.balance_var, bg="#fff", fg="red").grid(row=2, column=1, sticky='w', pady=5)

        tk.Label(frame, text="Pay Amount:", bg="#fff").grid(row=3, column=0, sticky='w', pady=5)
        self.pay_entry = tk.Entry(frame)
        self.pay_entry.grid(row=3, column=1, pady=5)

        tk.Button(self, text="Make Payment", bg="#4a90e2", fg="white", command=self.make_payment).pack(pady=10)

        # Payments History
        tk.Label(self, text="Payment History", font=("Helvetica", 14), bg="#fff").pack(pady=(15,5))
        self.tree = ttk.Treeview(self, columns=("Amount", "Date"), show='headings')
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.column("Amount", width=100)
        self.tree.column("Date", width=150)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.load_fee_info()
        self.load_payments()

    def load_fee_info(self):
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT total_fee, amount_paid FROM fees WHERE student_id=?", (self.student_id,))
        row = cursor.fetchone()
        if row:
            total_fee, amount_paid = row
        else:
            # If no fee record, set default values
            total_fee, amount_paid = 1000, 0
            cursor.execute("INSERT INTO fees (student_id, total_fee, amount_paid) VALUES (?, ?, ?)",
                           (self.student_id, total_fee, amount_paid))
            conn.commit()
        conn.close()
        balance = total_fee - amount_paid
        self.total_fee_var.set(f"${total_fee}")
        self.amount_paid_var.set(f"${amount_paid}")
        self.balance_var.set(f"${balance}")

    def make_payment(self):
        try:
            amount = int(self.pay_entry.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer amount.")
            return
        if amount <= 0:
            messagebox.showerror("Input Error", "Payment amount must be positive.")
            return

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT total_fee, amount_paid FROM fees WHERE student_id=?", (self.student_id,))
        row = cursor.fetchone()
        if not row:
            messagebox.showerror("Error", "Fee info not found.")
            conn.close()
            return

        total_fee, amount_paid = row
        new_paid = amount_paid + amount
        if new_paid > total_fee:
            messagebox.showerror("Payment Error", "Payment exceeds total fee.")
            conn.close()
            return

        cursor.execute("UPDATE fees SET amount_paid=? WHERE student_id=?", (new_paid, self.student_id))
        cursor.execute("INSERT INTO payments (student_id, amount, date) VALUES (?, ?, ?)",
                       (self.student_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        self.pay_entry.delete(0, 'end')
        messagebox.showinfo("Success", "Payment made successfully.")
        self.load_fee_info()
        self.load_payments()

    def load_payments(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT amount, date FROM payments WHERE student_id=? ORDER BY date DESC", (self.student_id,))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)

# Group Chat Window
class ChatWindow(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.title("Group Chat")
        self.geometry("700x500")
        self.configure(bg="#fff")

        self.student_id = student_id

        tk.Label(self, text="Group Chat", font=("Helvetica", 16, "bold"), bg="#fff").pack(pady=10)

        # Select Class
        class_frame = tk.Frame(self, bg="#fff")
        class_frame.pack(pady=5)

        tk.Label(class_frame, text="Select Class:", bg="#fff").pack(side='left', padx=5)
        self.class_combo = ttk.Combobox(class_frame, state="readonly")
        self.class_combo.pack(side='left', padx=5)
        self.load_classes()
        self.class_combo.bind("<<ComboboxSelected>>", lambda e: self.load_messages())

        # Messages display
        self.msg_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, state='disabled')
        self.msg_display.pack(fill='both', expand=True, padx=10, pady=10)

        # Message entry
        entry_frame = tk.Frame(self, bg="#fff")
        entry_frame.pack(fill='x', padx=10, pady=(0,10))
        self.msg_entry = tk.Entry(entry_frame)
        self.msg_entry.pack(side='left', fill='x', expand=True, padx=(0,10))
        self.msg_entry.bind("<Return>", self.send_message)

        tk.Button(entry_frame, text="Send", bg="#4a90e2", fg="white", command=self.send_message).pack(side='right')

    def load_classes(self):
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.class_id, c.class_name FROM classes c
            JOIN enrollments e ON c.class_id = e.class_id
            WHERE e.student_id=?
        ''', (self.student_id,))
        classes = cursor.fetchall()
        conn.close()
        self.class_map = {f"{name} (ID: {cid})": cid for cid, name in classes}
        self.class_combo['values'] = list(self.class_map.keys())
        if classes:
            self.class_combo.current(0)
            self.load_messages()

    def load_messages(self):
        self.msg_display.configure(state='normal')
        self.msg_display.delete(1.0, 'end')
        cls = self.class_combo.get()
        if not cls:
            self.msg_display.insert('end', "No class selected.\n")
            self.msg_display.configure(state='disabled')
            return
        class_id = self.class_map[cls]

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, ch.message, ch.timestamp FROM chats ch
            JOIN users u ON ch.student_id = u.id
            WHERE ch.class_id=?
            ORDER BY ch.timestamp ASC
        ''', (class_id,))
        messages = cursor.fetchall()
        conn.close()

        for username, message, timestamp in messages:
            time_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%b %d %H:%M")
            self.msg_display.insert('end', f"[{time_str}] {username}: {message}\n")
        self.msg_display.see('end')
        self.msg_display.configure(state='disabled')

    def send_message(self, event=None):
        message = self.msg_entry.get().strip()
        if not message:
            return
        cls = self.class_combo.get()
        if not cls:
            messagebox.showwarning("No Class", "Please select a class to send message.")
            return
        class_id = self.class_map[cls]

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (class_id, student_id, message, timestamp) VALUES (?, ?, ?, ?)",
                       (class_id, self.student_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

        self.msg_entry.delete(0, 'end')
        self.load_messages()

# Timetable Window
class TimetableWindow(tk.Toplevel):
    def __init__(self, master, student_id):
        super().__init__(master)
        self.title("Timetable")
        self.geometry("700x450")
        self.configure(bg="#fff")

        self.student_id = student_id

        tk.Label(self, text="Timetable", font=("Helvetica", 16, "bold"), bg="#fff").pack(pady=10)

        # Select Class
        class_frame = tk.Frame(self, bg="#fff")
        class_frame.pack(pady=5)

        tk.Label(class_frame, text="Select Class:", bg="#fff").pack(side='left', padx=5)
        self.class_combo = ttk.Combobox(class_frame, state="readonly")
        self.class_combo.pack(side='left', padx=5)
        self.load_classes()
        self.class_combo.bind("<<ComboboxSelected>>", lambda e: self.load_timetable())

        # Timetable Treeview
        columns = ("Day", "Time Slot", "Subject")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Add timetable entry form
        form_frame = tk.Frame(self, bg="#fff")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Day:", bg="#fff").grid(row=0, column=0, padx=5, pady=5)
        self.day_entry = ttk.Combobox(form_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], state="readonly")
        self.day_entry.grid(row=0, column=1, padx=5, pady=5)
        self.day_entry.current(0)

        tk.Label(form_frame, text="Time Slot:", bg="#fff").grid(row=0, column=2, padx=5, pady=5)
        self.time_entry = tk.Entry(form_frame)
        self.time_entry.grid(row=0, column=3, padx=5, pady=5)
        self.time_entry.insert(0, "09:00 - 10:00")

        tk.Label(form_frame, text="Subject:", bg="#fff").grid(row=0, column=4, padx=5, pady=5)
        self.subject_entry = tk.Entry(form_frame)
        self.subject_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(form_frame, text="Add Entry", bg="#4a90e2", fg="white", command=self.add_entry).grid(row=0, column=6, padx=5, pady=5)

    def load_classes(self):
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.class_id, c.class_name FROM classes c
            JOIN enrollments e ON c.class_id = e.class_id
            WHERE e.student_id=?
        ''', (self.student_id,))
        classes = cursor.fetchall()
        conn.close()
        self.class_map = {f"{name} (ID: {cid})": cid for cid, name in classes}
        self.class_combo['values'] = list(self.class_map.keys())
        if classes:
            self.class_combo.current(0)
            self.load_timetable()

    def load_timetable(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        cls = self.class_combo.get()
        if not cls:
            return
        class_id = self.class_map[cls]
        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("SELECT day, time_slot, subject FROM timetable WHERE class_id=?", (class_id,))
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_entry(self):
        day = self.day_entry.get()
        time_slot = self.time_entry.get().strip()
        subject = self.subject_entry.get().strip()
        cls = self.class_combo.get()
        if not day or not time_slot or not subject or not cls:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        class_id = self.class_map[cls]

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO timetable (class_id, day, time_slot, subject) VALUES (?, ?, ?, ?)",
                       (class_id, day, time_slot, subject))
        conn.commit()
        conn.close()

        self.time_entry.delete(0, 'end')
        self.subject_entry.delete(0, 'end')
        self.load_timetable()
        messagebox.showinfo("Success", "Timetable entry added.")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
