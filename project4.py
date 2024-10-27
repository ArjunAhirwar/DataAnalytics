import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class CSVPlotterApp:
    def __init__(self, master):
        global my_img
        self.master = master
        self.master.title("CSV Plotter")
        self.master.iconbitmap('C:/Users/ARJUN/Desktop/Internship Studo/exe/nitlogo.ico')
        self.master.geometry('600x600')

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.my_img = ImageTk.PhotoImage(Image.open('C:/Users/ARJUN/Downloads/nitlogo (1).png'))
        self.my_label = tk.Label(self.frame,image = self.my_img)
        self.my_label.grid(row = 0, column = 0, columnspan= 4)

        self.file_name=tk.StringVar()
        self.file_path=tk.StringVar()

        self.browse = tk.Label(self.frame, text = 'Select File').grid(row = 1, column = 0)
        self.file_entry = tk.Entry(self.frame, textvariable=self.file_name, width=30).grid(row=1, column = 1)
        self.browse_button = tk.Button(self.frame ,text = 'Browse', command = self.browse_file).grid(row = 1, column = 2)

        self.delimeter_label=tk.Label(self.frame, text= 'Select Delimeter').grid(row = 2, column = 0)

        delimeters =['Comma (,)','Semicolon (;)','Colon (:)','Tab (\t)','Space', 'or(|)']

        self.delimeter_combo=ttk.Combobox(self.frame, state='readonly', values=delimeters)
        self.delimeter_combo.grid(row=2,column=1)
        self.delimeter_combo.current(0)

        self.load_button = tk.Button(self.frame, text="Load CSV", command=self.load_file)
        self.load_button.grid(row = 3, column = 0)

        self.column1_label = tk.Label(self.frame, text="Select Column 1:")
        self.column1_label.grid(row = 4, column = 0)

        self.column1_combobox = ttk.Combobox(self.frame, state="readonly")
        self.column1_combobox.grid(row=4, column=1)

        self.column2_label = tk.Label(self.frame, text="Select Column 2:")
        self.column2_label.grid(row = 4, column = 2)

        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=4, column =3)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row = 4, column = 4)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.select_plot_label = tk.Label(self.frame, text ='Select The Type of Plot ')
        self.select_plot_label.grid(row=5, column =0)

        plot=['Line','Scatter','Histogram','2D Histogram','Pie Chart']

        self.select_plot = ttk.Combobox(self.frame, state= "readonly", values = plot)
        self.select_plot.grid(row = 5, column= 1)

        self.select_plot.current(0)

        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_graph)
        self.plot_button.grid(row = 6, column = 0, columnspan = 4)


    def browse_file(self):
        file_path = filedialog.askopenfilename(title = 'Select a file',filetypes=[("Log files", "*.*"),("csv files", "*.csv")])
        if file_path:
            self.file_name.set(file_path.split('/')[-1])
            self.file_path.set(file_path)

    def load_file(self):
        
        file_path = self.file_path.get()
        
        deli = self.delimeter_combo.get()
        
        delimeters =['Comma (,)','Semicolon (;)','Colon (:)','Tab (\t)','Space', 'or(|)']

        index = delimeters.index(deli)

        deli_lst = [",", ";", ":","\t", " ", "|"]

        deli = deli_lst[index]
        
        if not file_path or not deli:
            messagebox.showerror("Error", "Please select a file and delimiter")
                    
        try:
            self.df = pd.read_csv(file_path, delimiter = deli )
            self.column_names = self.df.columns.tolist()

            self.listbox.delete(0, tk.END)

            for item in self.column_names:

                self.listbox.insert(tk.END, item)  
                self.column1_combobox["values"] = self.column_names      

                self.column1_combobox.current(0)

        except Exception as e:

            messagebox.showerror("Error", f"Failed to load file: {e}")



    def plot_graph(self):
        
        column1 = self.column1_combobox.get()

        selected_indices = self.listbox.curselection()
        selected_items = [self.column_names[index] for index in selected_indices]

        fig, ax = plt.subplots(figsize = (10,8))

        if not column1 or not selected_items:
            messagebox.showerror("Error", "please select column1 and column2 ")

        if self.select_plot.get() == 'Line':

            try:
                for i in range(len(selected_items)):
            
                    ax.plot(self.df[column1],self.df[selected_items[i]], label = selected_items[i] ) 


            except Exception as e:
                
                messagebox.showerror("Error", f"Failed to plot_graph: {e}")
                    
        if self.select_plot.get() == 'Scatter':

            try:
                for i in range(len(selected_items)):
                    ax.scatter(self.df[column1],self.df[selected_items[i]], label = selected_items[i] )

            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot_graph: {e}")
            
        if self.select_plot.get() == 'Histogram':

            try:
                for i in range(len(selected_items)):
                    ax.hist(self.df[column1],self.df[selected_items[i]], label = selected_items[i] )

            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot_graph: {e}")
            
        if self.select_plot.get() == '2D Histogram':

            try:
                for i in range(len(selected_items)):
                    ax.hist2d(self.df[column1],self.df[selected_items[i]], label = selected_items[i] )

            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot_graph: {e}")
            
            
        if self.select_plot.get() == 'Pie Chart':

            try:
                for i in range(len(selected_items)):
                    ax.pie(self.df[column1],self.df[selected_items[i]], label = selected_items[i] )

            except Exception as e:
                messagebox.showerror("Error", f"Failed to plot_graph: {e}")

        ax.grid(True)
        ax.legend()

        top_window = tk.Toplevel(self.frame)
        canvas = FigureCanvasTkAgg(fig, master = top_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, top_window).pack()
        toolbar.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVPlotterApp(root)
    root.mainloop()
