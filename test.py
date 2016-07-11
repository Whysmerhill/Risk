import tkinter as Tk 
 
root = Tk.Tk() 
f1 = Tk.Frame(root) 
s1 = Tk.Scrollbar(f1) 
l1 = Tk.Listbox(f1) 
for i in range(20): l1.insert(i, str(i)) 
s1.config(command = l1.yview) 
l1.config(yscrollcommand = s1.set) 
l1.pack(side = Tk.LEFT, fill = Tk.Y) 
s1.pack(side = Tk.RIGHT, fill = Tk.Y) 
f1.pack() 
root.mainloop()
