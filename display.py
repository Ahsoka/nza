import os
import tkinter as tk
import automation

from tkinter import filedialog


WIN_W = 370
WIN_H = 300

BTN_W = 20
BTN_H = 2

FONT = ('arial', 10, 'bold')
FILES = {'Input': '', 'Output': ''}

COLOR = {
    'danger': '#F04D43',
    'grey': '#CED4DA',
    'light-grey': '#E9ECEF',
    'mango': '#FB9927',
    'mint': '#5BBD93',
    'success': '#A3DE83',
    'white': '#F8F9FA',
}

# MESSAGE
tip_msg = ("\n"
            "Tips: "
            "\nDon't have tabs overlap the Zoom App"
            "\nPlease do not move the cursor after pressing a button."
        )


class Display(tk.Frame):

    @classmethod
    def main(cls):
        root = tk.Tk()
        root.title("Neato Zoom Automation")
        root.iconbitmap('images/check.ico')
        root.configure(bg=COLOR['grey'])
        root.geometry(f'{WIN_W}x{WIN_H}')

        frame = cls(root, bg=COLOR['grey'])
        frame.grid()
        root.mainloop()


    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        # FILES LABEL
        self.f_in_label = tk.Label(self, text="Roster: EMPTY", font=FONT)
        self.f_out_label = tk.Label(self, text="Results: EMPTY", font=FONT)

        # FILE BUTTONS
        self.f_in_btn = tk.Button(self, text="Student Roster", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: addFile("Input", self.f_in_label, self.f_in_btn, self.f_out_btn))
        self.f_out_btn = tk.Button(self, text="Attendance Sheet", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['mango'], activeforeground='white',
            command=lambda: addFile("Output", self.f_out_label, self.f_in_btn, self.f_out_btn))

        # AUTOMATION BUTTONS
        self.student_btn = tk.Button(self, text="Take Attendance", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: attendance("Student", self.f_in_label, self.f_out_label))
        self.leaders_btn = tk.Button(self, text="Admit Group Leaders", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: attendance("Leader", self.f_in_label, self.f_out_label))

        # HELP LABEL
        self.tip_label = tk.Label(self, text=tip_msg, font=FONT, bg=COLOR['grey'])
        
        # GRID
        self.f_in_label.grid(row=1, column=0, padx=10, pady=(20,0), sticky='WENS')
        self.f_out_label.grid(row=1, column=1, padx=10, pady=(20,0), sticky='WENS')

        self.f_in_btn.grid(row=2, column=0, padx=10, pady=(0,10))
        self.f_out_btn.grid(row=2, column=1, padx=10, pady=(0,10))
        
        self.student_btn.grid(row=3, column=0)
        self.leaders_btn.grid(row=3, column=1)

        self.tip_label.grid(row=5, column=0, pady=(5,0), columnspan=2)
        
        # BINDS
        self.student_btn.bind('<Enter>', self.student_hover)
        self.leaders_btn.bind('<Enter>', self.leaders_hover)

        self.student_btn.bind('<Leave>', self.student_leave)
        self.leaders_btn.bind('<Leave>', self.leaders_leave)

    # HOVER METHODS
    def student_hover(self, e):
        self.student_btn['bg'] = COLOR['mango']
    def leaders_hover(self, e):
        self.leaders_btn['bg'] = COLOR['mango']

    def student_leave(self, e):
        self.student_btn['bg'] = COLOR['mint']
    def leaders_leave(self, e):
        self.leaders_btn['bg'] = COLOR['mint']


def addFile(file, label, in_btn, out_btn):
    file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
    
    if os.path.isfile(file_name):
        FILES[file] = file_name
        f = file_name.split('/')
        
        if file == "Input":
            label.config(text=f[-1])
            in_btn['bg'] = COLOR['success']
        else:
            label.config(text=f[-1])
            out_btn['bg'] = COLOR['success']

    if FILES['Input'] != '' and FILES['Output'] != '':
        automation.setup_df(FILES['Input'], FILES['Output'])


def attendance(student_type, f_in_label, f_out_label):
    if FILES['Input'] != '' and FILES['Output'] != '':
        automation.attendance(FILES['Input'], FILES['Output'], student_type)

           
if __name__ == '__main__':
    Display.main()