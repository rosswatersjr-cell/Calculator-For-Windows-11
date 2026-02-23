import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Tk, ttk, font, messagebox, Menu, colorchooser, Frame, simpledialog
from tkinter import Toplevel, Listbox, StringVar, IntVar, BooleanVar, TclError
from tkinter.ttk import Checkbutton, Label, Button, Scrollbar, Style, Entry
from tkinter.font import families, Font
from pathlib import Path
from datetime import datetime
from re import compile
import mpmath as mp
from mpmath import *
from sympy import *
import time
from datetime import datetime
import os
import sys
import numpy as np
import sympy as sym
import pyperclip# System ClipBoard
import json

version="2026.02.23"
class MyFontChooser(Toplevel):
    def __init__(self, master, font_dict={}, text="Abcd", title="Font Chooser", **kwargs):
        Toplevel.__init__(self, master, **kwargs)
        style=Style()
        style.theme_use('alt')
        style.configure("Vertical.TScrollbar", background="#094983")
        style.configure("Horizontal.TScrollbar", background="#094983")
        style.configure("Vertical.TScrollbar", arrowsize=18, arrowcolor="aqua")
        style.configure("Horizontal.TScrollbar", arrowsize=18, arrowcolor="aqua")
        if Language.get()=="English":title=f"{root_title}  Font Chooser"
        else:title=title=f"{root_title}  Selector de Fuentes"
        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self._validate_family = self.register(self.validate_font_family)
        self._validate_size = self.register(self.validate_font_size)
        self.res = ""# variable storing the chosen font
        style.configure("prev.TLabel", background="white")
        bg = style.lookup("TLabel", "background")
        self.configure(bg=bg)
        self.fonts = list(set(families()))# family list
        self.fonts.append("TkDefaultFont")
        self.fonts.sort()
        for i in range(len(self.fonts)):
            self.fonts[i] = self.fonts[i].replace(" ", r"\ ")
        max_length = int(2.5 * max([len(font) for font in self.fonts])) // 3
        self.sizes = ["%i" % i for i in (list(range(6, 17)) + list(range(18, 32, 2)))]
        # font default
        font_dict["weight"] = font_dict.get("weight", "normal")
        font_dict["slant"] = font_dict.get("slant", "roman")
        font_dict["underline"] = font_dict.get("underline", False)
        font_dict["overstrike"] = font_dict.get("overstrike", False)
        font_dict["family"] = font_dict.get("family", self.fonts[0].replace(r'\ ', ' '))
        font_dict["size"] = font_dict.get("size", 10)
        # style parameters (bold, italic ...)
        if Language.get()=="English":font_props=["Bold","Italic","Underline","Overstrike"]
        else:font_props=["Negrita","Cursiva","Subrayar","Sobreescribir"]
        options_frame = Frame(self, relief='groove', borderwidth=2)
        self.font_family = StringVar(self, " ".join(self.fonts))
        self.font_size = StringVar(self, " ".join(self.sizes))
        self.var_bold = BooleanVar(self, font_dict["weight"] == "bold")
        b_bold = Checkbutton(options_frame, text=[font_props[0]],
                             command=self.toggle_bold,
                             variable=self.var_bold)
        b_bold.grid(row=0, sticky="w", padx=4, pady=(4, 2))
        self.var_italic = BooleanVar(self, font_dict["slant"] == "italic")
        b_italic = Checkbutton(options_frame, text=[font_props[1]],
                               command=self.toggle_italic,
                               variable=self.var_italic)
        b_italic.grid(row=1, sticky="w", padx=4, pady=2)
        self.var_underline = BooleanVar(self, font_dict["underline"])
        b_underline = Checkbutton(options_frame, text=[font_props[2]],
                                  command=self.toggle_underline,
                                  variable=self.var_underline)
        b_underline.grid(row=2, sticky="w", padx=4, pady=2)
        self.var_overstrike = BooleanVar(self, font_dict["overstrike"])
        b_overstrike = Checkbutton(options_frame, text=[font_props[3]],
                                   variable=self.var_overstrike,
                                   command=self.toggle_overstrike)
        b_overstrike.grid(row=3, sticky="w", padx=4, pady=(2, 4))
        # Size and family
        self.var_size = StringVar(self)
        self.entry_family = Entry(self, width=max_length, validate="key",
                                  validatecommand=(self._validate_family, "%d", "%S",
                                                   "%i", "%s", "%V"))
        self.entry_size = Entry(self, width=4, validate="key",
                                textvariable=self.var_size,
                                validatecommand=(self._validate_size, "%d", "%P", "%V"))
        self.list_family = Listbox(self, selectmode="browse",
                                   listvariable=self.font_family,
                                   highlightthickness=0,
                                   exportselection=False,
                                   width=max_length)
        self.list_size = Listbox(self, selectmode="browse",
                                 listvariable=self.font_size,
                                 highlightthickness=0,
                                 exportselection=False,
                                 width=4)
        scroll_family = Scrollbar(self, orient='vertical',
                                  command=self.list_family.yview)
        scroll_size = Scrollbar(self, orient='vertical',
                                command=self.list_size.yview)
        self.preview_font = Font(self, **font_dict)
        if len(text) > 30:
            text = text[:30]
        self.preview = Label(self, relief="groove", style="prev.TLabel", text=text, font=self.preview_font,
                             anchor="center",background=Display_bg.get(),foreground=Display_fg.get())
        # widget configuration
        self.list_family.configure(yscrollcommand=scroll_family.set)
        self.list_size.configure(yscrollcommand=scroll_size.set)
        self.entry_family.insert(0, font_dict["family"])
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        self.entry_size.insert(0, font_dict["size"])
        try:
            i = self.fonts.index(self.entry_family.get().replace(" ", r"\ "))
        except ValueError:# unknown font
            i = 0
        self.list_family.selection_clear(0, "end")
        self.list_family.selection_set(i)
        self.list_family.see(i)
        try:
            i = self.sizes.index(self.entry_size.get())
            self.list_size.selection_clear(0, "end")
            self.list_size.selection_set(i)
            self.list_size.see(i)
        except ValueError:# size not in list
            pass
        self.entry_family.grid(row=0, column=0, sticky="ew", pady=(10, 1), padx=(10, 0))
        self.entry_size.grid(row=0, column=2, sticky="ew", pady=(10, 1), padx=(10, 0))
        self.list_family.grid(row=1, column=0, sticky="nsew", pady=(1, 10), padx=(10, 0))
        self.list_size.grid(row=1, column=2, sticky="nsew", pady=(1, 10), padx=(10, 0))
        scroll_family.grid(row=1, column=1, sticky='ns', pady=(1, 10))
        scroll_size.grid(row=1, column=3, sticky='ns', pady=(1, 10))
        options_frame.grid(row=0, column=4, rowspan=2, padx=10, pady=10, ipadx=10)
        self.preview.grid(row=2, column=0, columnspan=5, sticky="eswn", padx=10, pady=(0, 10), ipadx=4, ipady=4)
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, columnspan=5, pady=(0, 10), padx=10)
        Button(button_frame, text="Ok",
               command=self.ok).grid(row=0, column=0, padx=4, sticky='ew')
        Button(button_frame, text=["Cancel"],
               command=self.quit).grid(row=0, column=1, padx=4, sticky='ew')
        self.list_family.bind('<<ListboxSelect>>', self.update_entry_family)
        self.list_size.bind('<<ListboxSelect>>', self.update_entry_size, add=True)
        self.list_family.bind("<KeyPress>", self.keypress)
        self.entry_family.bind("<Return>", self.change_font_family)
        self.entry_family.bind("<Tab>", self.tab)
        self.entry_size.bind("<Return>", self.change_font_size)
        self.entry_family.bind("<Down>", self.down_family)
        self.entry_size.bind("<Down>", self.down_size)
        self.entry_family.bind("<Up>", self.up_family)
        self.entry_size.bind("<Up>", self.up_size)
        self.bind_class("TEntry", "<Control-a>", self.select_all)
        self.wait_visibility(self)
        self.grab_set()
        self.entry_family.focus_set()
        self.lift()
        hgt=screen_height * 0.4
        wid=screen_width * 0.3
        x=(screen_width/2)-(wid/2)
        y=(screen_height/2)-(hgt/2)
        self.geometry('%dx%d+%d+%d' % (wid, hgt, x, y))
        self.update()
    def select_all(self, event):# Select all entry content.
        event.widget.selection_range(0, "end")
    def keypress(self, event):# Select the first font whose name begin by the key pressed.
        key = event.char.lower()
        _l = [i for i in self.fonts if i[0].lower() == key]
        if _l:
            i = self.fonts.index(_l[0])
            self.list_family.selection_clear(0, "end")
            self.list_family.selection_set(i)
            self.list_family.see(i)
            self.update_entry_family()
    def up_family(self, event):# Navigate in the family listbox with up key.
        try:
            i = self.list_family.curselection()[0]
            self.list_family.selection_clear(0, "end")
            if i <= 0:
                i = len(self.fonts)
            self.list_family.see(i - 1)
            self.list_family.select_set(i - 1)
        except TclError:
            self.list_family.selection_clear(0, "end")
            i = len(self.fonts)
            self.list_family.see(i - 1)
            self.list_family.select_set(i - 1)
        self.list_family.event_generate('<<ListboxSelect>>')
    def up_size(self, event):# Navigate in the size listbox with up key.
        try:
            s = self.var_size.get()
            if s in self.sizes:
                i = self.sizes.index(s)
            elif s:
                sizes = list(self.sizes)
                sizes.append(s)
                sizes.sort(key=lambda x: int(x))
                i = sizes.index(s)
            else:
                i = 0
            self.list_size.selection_clear(0, "end")
            if i <= 0:
                i = len(self.sizes)
            self.list_size.see(i - 1)
            self.list_size.select_set(i - 1)
        except TclError:
            i = len(self.sizes)
            self.list_size.see(i - 1)
            self.list_size.select_set(i - 1)
        self.list_size.event_generate('<<ListboxSelect>>')
    def down_family(self, event):# Navigate in the family listbox with down key.
        try:
            i = self.list_family.curselection()[0]
            self.list_family.selection_clear(0, "end")
            if i >= len(self.fonts):
                i = -1
            self.list_family.see(i + 1)
            self.list_family.select_set(i + 1)
        except TclError:
            self.list_family.selection_clear(0, "end")
            self.list_family.see(0)
            self.list_family.select_set(0)
        self.list_family.event_generate('<<ListboxSelect>>')
    def down_size(self, event):# Navigate in the size listbox with down key.
        try:
            s = self.var_size.get()
            if s in self.sizes:
                i = self.sizes.index(s)
            elif s:
                sizes = list(self.sizes)
                sizes.append(s)
                sizes.sort(key=lambda x: int(x))
                i = sizes.index(s) - 1
            else:
                s = len(self.sizes) - 1
            self.list_size.selection_clear(0, "end")
            if i < len(self.sizes) - 1:
                self.list_size.selection_set(i + 1)
                self.list_size.see(i + 1)
            else:
                self.list_size.see(0)
                self.list_size.select_set(0)
        except TclError:
            self.list_size.selection_set(0)
        self.list_size.event_generate('<<ListboxSelect>>')
    def toggle_bold(self):# Update font preview weight.
        b = self.var_bold.get()
        self.preview_font.configure(weight=["normal", "bold"][b])
    def toggle_italic(self):# Update font preview slant.
        b = self.var_italic.get()
        self.preview_font.configure(slant=["roman", "italic"][b])
    def toggle_underline(self):# Update font preview underline.
        b = self.var_underline.get()
        self.preview_font.configure(underline=b)
    def toggle_overstrike(self):# Update font preview overstrike.
        b = self.var_overstrike.get()
        self.preview_font.configure(overstrike=b)
    def change_font_family(self, event=None):# Update font preview family.
        family = self.entry_family.get()
        if family.replace(" ", r"\ ") in self.fonts:
            self.preview_font.configure(family=family)
    def change_font_size(self, event=None):# Update font preview size.
        size = int(self.var_size.get())
        self.preview_font.configure(size=size)
    def validate_font_size(self, d, ch, V):# Validation of the size entry content.
        l = [i for i in self.sizes if i[:len(ch)] == ch]
        i = None
        if l:
            i = self.sizes.index(l[0])
        elif ch.isdigit():
            sizes = list(self.sizes)
            sizes.append(ch)
            sizes.sort(key=lambda x: int(x))
            i = min(sizes.index(ch), len(self.sizes))
        if i is not None:
            self.list_size.selection_clear(0, "end")
            self.list_size.selection_set(i)
            deb = self.list_size.nearest(0)
            fin = self.list_size.nearest(self.list_size.winfo_height())
            if V != "forced":
                if i < deb or i > fin:
                    self.list_size.see(i)
                return True
        if d == '1':
            return ch.isdigit()
        else:
            return True
    def tab(self, event):# Move at the end of selected text on tab press
        self.entry_family = event.widget
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
    def validate_font_family(self, action, modif, pos, prev_txt, V):# Completion of the text in the entry with existing font names
        if self.entry_family.selection_present():
            sel = self.entry_family.selection_get()
            txt = prev_txt.replace(sel, '')
        else:
            txt = prev_txt
        if action == "0":
            txt = txt[:int(pos)] + txt[int(pos) + 1:]
            return True
        else:
            txt = txt[:int(pos)] + modif + txt[int(pos):]
            ch = txt.replace(" ", r"\ ")
            l = [i for i in self.fonts if i[:len(ch)] == ch]
            if l:
                i = self.fonts.index(l[0])
                self.list_family.selection_clear(0, "end")
                self.list_family.selection_set(i)
                deb = self.list_family.nearest(0)
                fin = self.list_family.nearest(self.list_family.winfo_height())
                index = self.entry_family.index("insert")
                self.entry_family.delete(0, "end")
                self.entry_family.insert(0, l[0].replace(r"\ ", " "))
                self.entry_family.selection_range(index + 1, "end")
                self.entry_family.icursor(index + 1)
                if V != "forced":
                    if i < deb or i > fin:
                        self.list_family.see(i)
                return True
            else:
                return False
    def update_entry_family(self, event=None):# Update family entry when an item is selected in the family listbox.
        #  family = self.list_family.get("@%i,%i" % (event.x , event.y))
        family = self.list_family.get(self.list_family.curselection()[0])
        self.entry_family.delete(0, "end")
        self.entry_family.insert(0, family)
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        self.change_font_family()
    def update_entry_size(self, event):# Update size entry when an item is selected in the size listbox.
        #  size = self.list_size.get("@%i,%i" % (event.x , event.y))
        size = self.list_size.get(self.list_size.curselection()[0])
        self.var_size.set(size)
        self.change_font_size()
    def ok(self):# Validate choice.
        self.res = self.preview_font.actual()
        self.quit()
    def get_res(self):# Return chosen font.
        return self.res
    def quit(self):
        self.destroy()
def askfont(master=None, text="Abcd", title="Font Chooser", **font_args):# Open the font chooser and return the chosen font.
    chooser = MyFontChooser(master, font_args, text, title)
    chooser.wait_window(chooser)
    return chooser.get_res()
def do_ratios():
    ratio=Ratio_Calculator(root)
class Ratio_Calculator(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        root.withdraw()
        self.deiconify()
        if Language.get()=="English":txt="Ratio / Porportion Calculator"
        else:txt="Calculadora de Proporciones / Ratios"
        self.grab_set() # Receive Events And Prevent root Window Interaction
        self.title(f'{root_title}  {txt}')
        hgt=screen_height * 0.6
        wid=screen_width * 0.3
        x=(screen_width/2)-(wid/2)
        y=(screen_height/2)-(hgt/2)
        self.geometry('%dx%d+%d+%d' % (wid, hgt, x, y))
        self.configure(bg='#00FFFF') # Set main backcolor to aqua
        self.bind("<Configure>", self.ratio_resize)
        self.protocol("WM_DELETE_WINDOW", self.ratio_destroy)
        self.txtfont=font.Font(family='Times New Romans', size=16, weight='normal', slant='italic')
        self.formula_font=font.Font(family='Times New Romans', size=9, weight='bold', slant='italic')
        self.btnfont=font.Font(family='Times New Romans', size=10, weight='bold', slant='italic')
        self.ratiofont=font.Font(family='Times New Romans', size=16, weight='bold')
        self.formula=""
        self.focused=tk.StringVar() 
        self.a1=tk.StringVar()
        self.a2=tk.StringVar()
        self.b1=tk.StringVar()
        self.b2=tk.StringVar()
        self.a3=tk.StringVar()
        self.b3=tk.StringVar()
        self.a4=tk.StringVar()
        self.b4=tk.StringVar()
        # Create and position scrolled textbox to display calculation formulas
        global formula_text 
        formula_text=ScrolledText(self, bg='#0c012e', fg='#07f7d8', font=self.formula_font, 
                borderwidth=5, relief="sunken", wrap=tk.WORD)
        formula_text.place(relx=0.015, rely=0.01, relwidth=0.97, relheight=0.22)
        formula_text.bind("<Control-c>", lambda event:copy_to_clipboard(self,formula_text,"selected",event))    
        self.popup_ratio=Menu(formula_text, tearoff=0) # PopUp Menu
        if Language.get()=="English":txt='Copy Displayed Text To Clipboard'
        else:txt='Copiar Texto Mostrado al Portapapeles'
        self.popup_ratio.add_command(label=txt, background='aqua', command=lambda:copy_to_clipboard(self,formula_text,"all"))  
        formula_text.bind("<Button-3>", self.menu_popup2)
        formula_text.focus()
        if Language.get()=="English":txt=['3 Ratio Values Must Be Present To Calculate','The 4th Ratio Value And Porportion Values.',
                                          'All 4 Ratio Values May Be Entered Manually','For Porportion Calculations.',
                                          'Enter At Lease 3 Ratio Values','Find Unknown Porportions','CLEAR','CALCULATE','QUIT','Backspace']
        else:    
            txt=['Deben estar presentes 3 valores de proporción para calcular','el 4º valor de proporción y los valores de proporción.',
                'Los 4 valores de la proporción pueden ingresarse manualmente','para los cálculos de proporción.',
                'Ingrese al menos 3 valores de relación','Encontrar proporciones desconocidas','BORRAR','CALCULAR','SALIR','Retroceso']
        self.formula=f'{txt[0]}\n'
        formula_text.insert(tk.INSERT, self.formula)
        self.formula=f'{txt[1]}\n'
        formula_text.insert(tk.END, self.formula)
        self.formula=f'{txt[2]}\n'
        formula_text.insert(tk.END, self.formula)
        self.formula=f'{txt[3]}\n'
        formula_text.insert(tk.END, self.formula)
        self.default_text=tk.BooleanVar()
        self.default_text.set(True)
       # Create and Position Frame1 and Widgets inside Frame1
        frame1=Frame(self, background='#E5E5E5',  
                highlightbackground="#696969", highlightthickness=5)
        frame1.place(relx=0.015, rely=0.24, relwidth=0.97, relheight=0.295)    
        frame1_lbl=tk.Label(frame1, background='#E5E5E5', font=self.txtfont,
                text=txt[4])
        frame1_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
        a1_lbl=tk.Label(frame1, background='#E5E5E5', font=self.txtfont, text='A1')
        a1_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
        self.a1_txtbx=tk.Entry(frame1, background='#FFFFF0', font=self.txtfont, textvariable=self.a1)
        self.a1_txtbx['validatecommand']=(self.a1_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.a1_txtbx.register(self.on_validate), '%P')
        self.a1_txtbx.config(validate="key", validatecommand=val_cmd)
        self.a1_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
        self.a1_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A1'))
        self.a1_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A2'))
        a2_lbl=tk.Label(frame1, background='#E5E5E5', font=self.txtfont, text='A2')
        a2_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
        self.a2_txtbx=tk.Entry(frame1, background='#FFFFF0', font=self.txtfont, textvariable=self.a2)
        self.a2_txtbx['validatecommand']=(self.a2_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.a2_txtbx.register(self.on_validate), '%P')
        self.a2_txtbx.config(validate="key", validatecommand=val_cmd)
        self.a2_txtbx.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
        self.a2_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A2'))
        self.a2_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B1'))
        ratio_lbl=tk.Label(frame1, background='#E5E5E5', font=self.ratiofont,
                text='________________     :    ________________')
        ratio_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
        b1_lbl=tk.Label(frame1, background='#E5E5E5', font=self.txtfont, text='B1')
        b1_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
        self.b1_txtbx=tk.Entry(frame1, background='#FFFFF0', font=self.txtfont, textvariable=self.b1)
        self.b1_txtbx['validatecommand']=(self.b1_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.b1_txtbx.register(self.on_validate), '%P')
        self.b1_txtbx.config(validate="key", validatecommand=val_cmd)
        self.b1_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
        self.b1_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B1'))
        self.b1_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B2'))
        b2_lbl=tk.Label(frame1, background='#E5E5E5', font=self.txtfont, text='B2')
        b2_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
        self.b2_txtbx=tk.Entry(frame1, background='#FFFFF0', font=self.txtfont, textvariable=self.b2)
        self.b2_txtbx['validatecommand']=(self.b2_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.b2_txtbx.register(self.on_validate), '%P')
        self.b2_txtbx.config(validate="key", validatecommand=val_cmd)
        self.b2_txtbx.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
        self.b2_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B2'))
        self.b2_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A3'))
        # Create and Position Frame2 and Widgets inside Frame2
        kb_frame=Frame(self, background='#00FFFF',borderwidth=2,relief="sunken",  
                highlightbackground="#696969", highlightthickness=4)
        kb_frame.place(relx=0.015, rely=0.524, relwidth=0.97, relheight=0.08)
        keys=['0','1','2','3','4','5','6','7','8','9','-','.',txt[9]]
        key_btn=[]
        for i, item in enumerate(keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
            key_btn.append([num])
            key_btn[i]=tk.Button(kb_frame, text=item,bg="black", fg="white",font=self.txtfont)
            key_btn[i].pack(side='left',fill='both',expand=True,padx=1,pady=2)
            key_btn[i].bind("<Button-1>", self.keyboard)
        # Create and Position Frame2 and Widgets inside Frame2
        frame2=Frame(self, background='#E5E5E5',  
                highlightbackground="#696969", highlightthickness=5)
        frame2.place(relx=0.015, rely=0.596, relwidth=0.97, relheight=0.295)    
        frame2_lbl=tk.Label(frame2, background='#E5E5E5', font=self.txtfont,
                text=txt[5])
        frame2_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
        a_lbl=tk.Label(frame2, background='#E5E5E5', font=self.txtfont, text='A')
        a_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
        self.a3_txtbx=tk.Entry(frame2, background='#FFFFF0', font=self.txtfont, textvariable=self.a3)
        self.a3_txtbx['validatecommand']=(self.a3_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.a3_txtbx.register(self.on_validate), '%P')
        self.a3_txtbx.config(validate="key", validatecommand=val_cmd)
        self.a3_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
        self.a3_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A3'))
        self.a3_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B3'))
        bAnswer_lbl=tk.Label(frame2, background='#E5E5E5', font=self.txtfont, text='B =')
        bAnswer_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
        bAnswer=tk.Label(frame2, background='lightgray', font=self.txtfont, textvariable=self.b4, justify='right',
                anchor='w', borderwidth=1, relief="sunken") 
        bAnswer.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
        porportion_lbl=tk.Label(frame2, background='#E5E5E5', font=self.ratiofont,
                text='________________    ::    ________________')
        porportion_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
        b_lbl=tk.Label(frame2, background='#E5E5E5', font=self.txtfont, text='B')
        b_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
        self.b3_txtbx=tk.Entry(frame2, background='#FFFFF0', font=self.txtfont, textvariable=self.b3)
        self.b3_txtbx['validatecommand']=(self.b3_txtbx.register(self.validate_Entries),'%P','%d')
        val_cmd=(self.b3_txtbx.register(self.on_validate), '%P')
        self.b3_txtbx.config(validate="key", validatecommand=val_cmd)
        self.b3_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
        self.b3_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B3'))
        self.b3_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A1'))
        aAnswer_lbl=tk.Label(frame2, background='#E5E5E5', font=self.txtfont, text='A =')
        aAnswer_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
        aAnswer=tk.Label(frame2, background='lightgray', font=self.txtfont, textvariable=self.a4, justify='right',
                anchor='w', borderwidth=1, relief="sunken") 
        aAnswer.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
        clr_btn=tk.Button(self, font=self.btnfont, text=txt[6], fg="black", command=lambda:self.clear_entries())
        clr_btn.place(relx=0.197, rely=0.912, relwidth=0.16, relheight=0.06)
        calc_btn=tk.Button(self, font=self.btnfont, text=txt[7], fg="red",
                command=lambda:self.calculate_ratio(self.a1.get(),self.a2.get(),self.b1.get(),self.b2.get(),self.a3.get(),self.b3.get()))
        calc_btn.place(relx=0.38, rely=0.912, relwidth=0.25, relheight=0.06)
        quit_btn=tk.Button(self, font=self.btnfont, text=txt[8], fg="black", command=self.ratio_destroy)
        quit_btn.place(relx=0.65, rely=0.912, relwidth=0.16, relheight=0.06)
        self.focus_force()
        self.a1_txtbx.focus_force()
        self.focused.set('A1')
        self.mainloop()
    def menu_popup2(self,event):# display the popup menu
        self.popup_ratio.tk_popup(event.x_root, event.y_root)
        popup.grab_release()#Release the grab
    def ratio_resize(self,event):
        if self.state()=='zoomed':
            self.txtfont.config(size=24)
            self.ratiofont.config(size=30)
            self.formula_font.config(size=18)
            self.btnfont.config(size=20)
        else:    
            self.txtfont.config(size=12)
            self.ratiofont.config(size=16)
            self.formula_font.config(size=9)
            self.btnfont.config(size=10)
    def ratio_destroy(self):# X Icon Was Clicked
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):widget.destroy()
            else:widget.destroy()
        self.withdraw()
        root.deiconify()
        root.grab_set()
        root.focus_force()
        root.update()
    def validate_Entries(self,string):
        regex=compile(r'[-+(0-9.)]*$') # Allowed +- Floats
        result=regex.match(string)
        return (string == "" 
        or (string.count(string)>0 # Prevent duplicates
            and result is not None
            and result.group(0) != ""))       
    def on_validate(self,P):return self.validate_Entries(P)
    def clear_entries(self):# Clears all text from Entry widgets
        self.a1_txtbx.config(state='normal') 
        self.a2_txtbx.config(state='normal') 
        self.b1_txtbx.config(state='normal') 
        self.b2_txtbx.config(state='normal')
        self.a1_txtbx.delete('0',tk.END)
        self.a2_txtbx.delete('0',tk.END)
        self.b1_txtbx.delete('0',tk.END)
        self.b2_txtbx.delete('0',tk.END)
        self.a3_txtbx.delete('0',tk.END)
        self.b3_txtbx.delete('0',tk.END)
        self.a4.set('')
        self.b4.set('')
        formula_text.delete('1.0',tk.END)
        self.focus_force()
        self.a1_txtbx.focus_force()
    def calculate_ratio(self,a_1,a_2,b_1,b_2,a_3,b_3):
        try:
            count=0
            missing_ratio=''
            if len(a_1) != 0:
                a_1=float(a_1)
                count+=1
            else: missing_ratio='a1'
            if len(a_2) != 0:
                a_2=float(a_2)
                count+=1
            else: missing_ratio='a2'
            if len(b_1) != 0:
                b_1=float(b_1)
                count+=1
            else: missing_ratio='b1'
            if len(b_2) != 0:
                b_2=float(b_2)
                count+=1
            else: missing_ratio='b2'
            if count < 3:
                if Language.get()=="English":
                    title='Missing Ratio Value'
                    msg1='A Minimum Of 3 Variables Are Required For\n'
                    msg2=f'Calculations And You Have Only Entered {str(count)}!\n'
                    msg3='Please Enter The Missing Variable/s.'
                else:    
                    title='Valor de Proporción Faltante'
                    msg1='¡Se Requieren al Menos 3 Variables para\n'
                    msg2=f'Cálculos y Solo has Ingresado {str(count)}!\n'
                    msg3='Por favor, ingrese las variables faltantes.'
                msg=msg1+msg2+msg3
                messagebox.showinfo(title, msg)
            if count == 3: # count=3, find & calculate missing ratio value
                if self.default_text.get():
                    formula_text.delete('1.0',tk.END)
                    self.default_text.set(False)
                if missing_ratio == 'a1':
                    zero_exist=self.div_by_zero(self.b2_txtbx, b_2, 'B2') # Prohibit Division by Zero
                    if zero_exist: return
                    tmpstr=(b_1 * a_2) / b_2 #a1=(b1 * a2) / b2, where b2 != 0
                    formula_text.delete('1.0',tk.END)
                    self.formula=(f"A1 = (B1 * A2) / B2 = ({b_1} * {a_2}) / {b_2} = {tmpstr}\n")    
                    formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.a1_txtbx,tmpstr)
                    a_1=tmpstr
                    count+=1
                elif missing_ratio == 'a2':
                    zero_exist=self.div_by_zero(self.b1_txtbx, b_1, 'B1') # Prohibit Division by Zero
                    if zero_exist: return
                    tmpstr=(a_1 / b_1) * b_2 #a2=(a1 / b1) * b2, where b1 != 0
                    formula_text.delete('1.0',tk.END)
                    self.formula=(f"A2 = (A1 / B1) * B2 = ({a_1} / {b_1}) * {b_2} = {tmpstr}\n")    
                    formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.a2_txtbx,tmpstr)
                    a_2=tmpstr
                    count+=1
                elif missing_ratio == 'b1':
                    zero_exist=self.div_by_zero(self.a2_txtbx, a_2, 'A2') # Prohibit Division by Zero
                    if zero_exist: return
                    tmpstr=(a_1 * b_2) / a_2 #b1=(a1 * b2) / a2, where a2 != 0
                    formula_text.delete('1.0',tk.END)
                    self.formula=(f"B1 = (A1 * B2) / A2 = ({a_1} * {b_2}) / {a_2} = {tmpstr}\n")    
                    formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.b1_txtbx,tmpstr)
                    b_1=tmpstr
                    count+=1
                elif missing_ratio == 'b2':
                    zero_exist=self.div_by_zero(self.a1_txtbx, a_1, 'A1') # Prohibit Division by Zero
                    if zero_exist: return
                    tmpstr=(b_1 * a_2) / a_1 #b2=(b1 * a2) / a1, where a1 != 0
                    formula_text.delete('1.0',tk.END)
                    self.formula=(f"B2 = (B1 * A2) / A1 = ({b_1} * {a_2}) / {a_1} = {tmpstr}\n")    
                    formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.b2_txtbx,tmpstr)
                    b_2=tmpstr
                    count+=1
                self.default_text.set(False)
            if count == 4: # All ratio value present, examine for porportion values
                if self.default_text.get():
                    formula_text.delete('1.0',tk.END)
                    self.default_text.set(False)
                if(len(a_3) != 0): a_3=float(a_3)
                if(len(b_3) != 0): b_3=float(b_3)
                # Check for ratio inversions
                if a_1 > a_2: a_inverse=True
                else: a_inverse=False
                if b_1 > b_2: b_inverse=True
                else: b_inverse=False
                # Set inversion true or false for calculations
                if a_inverse and not b_inverse: inverse=True
                if not a_inverse and b_inverse: inverse=True
                if not a_inverse and not b_inverse: inverse=False
                if a_inverse and b_inverse: inverse=False
                # Get the numerical sizes of the ratios for K-Factor calculations
                if(a_1 >= 0) and (a_2 > 0):
                    asize=abs(a_2 - a_1)
                    bsize=abs(b_1 - b_2)
                elif(b_1 > 0) and (b_2 >= 0):
                    asize=abs(a_1 - a_2)
                    bsize=abs(b_2 - b_1)
                else:
                    asize=abs(a_1 - a_2) #0,-100 or -10,-100 Examples
                    bsize=abs(b_1 - b_2) #0,-100 or 10,-100
                # Calculate the K=Factors using the sizes
                if Language.get()=="English":ranges=['A Range','B Range']
                else:ranges=['Rango de A','Rango de B']
                Kfactor_ba=round(abs(bsize / asize),7) #X Amount Of B's Per X Amount Of A's
                KDisplay_ba=f"K = Abs({ranges[1]} / {ranges[0]})"
                Kfactor_ab=round(abs(asize / bsize),7) #X Amount Of A's Per X Amount Of B's
                KDisplay_ab=f"K = Abs({ranges[0]} / {ranges[1]})"
                # Final Calculations
                if not inverse: # Case Not A_Inverse And Not B_Inverse Or A_Inverse And B_Inverse
                    exist=self.a3.get()
                    if len(exist) != 0:# B=B1 - (K * (A1 - A))
                        a_3=float(self.a3.get())
                        self.formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                        formula_text.insert('2.0', self.formula)
                        b_4=round(b_1 - (Kfactor_ba * (a_1 - a_3)), 3)
                        self.formula=(f"B = B1 - (K * (A1 - A)) = {b_1} - ({Kfactor_ba} * ({a_1} - {a_3})) = {b_4}\n")
                        formula_text.insert('3.0', self.formula)
                        self.b4.set(b_4)
                    exist=self.b3.get()
                    if len(exist) != 0:# A=A1 - (K * (B1 - B))
                        b_3=float(self.b3.get())
                        self.formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                        formula_text.insert('4.0', self.formula)
                        a_4=round(a_1 - (Kfactor_ab * (b_1 - b_3)), 3) 
                        self.formula=(f"A = A1 - (K * (B1 - B)) = {a_1} - ({Kfactor_ab} * ({b_1} - {b_3})) = {a_4}\n")
                        formula_text.insert('5.0', self.formula)
                        self.a4.set(a_4)
                else: # Case A_Inverse And Not B_Inverse Or Not A_Inverse And B_Inverse
                    exist=self.a3.get()
                    if len(exist) != 0:# B=B1 - ((A - A1) * K)
                        a_3=float(self.a3.get())
                        self.formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                        formula_text.insert('2.0', self.formula)
                        b_4=round(b_1 - ((a_3 - a_1) * Kfactor_ba), 3)
                        self.formula=(f"B = B1 - ((A - A1) * K) = {b_1} - (({a_3} - {a_1}) * {Kfactor_ba}) = {b_4}\n")
                        formula_text.insert('3.0', self.formula)
                        self.b4.set(b_4)
                    exist=self.b3.get()
                    if len(exist) != 0:# A=A1 - ((B - B1) * K)
                        b_3=float(self.b3.get())
                        self.formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                        formula_text.insert('4.0', self.formula)
                        a_4=round(a_1 - ((b_3 - b_1) * Kfactor_ab), 3) 
                        self.formula=(f"A = A1 - ((B - B1) * K) = {a_1} - (({b_3} - {b_1}) * {Kfactor_ab}) = {a_4}\n")
                        formula_text.insert('5.0', self.formula)
                        self.a4.set(a_4)
        except Exception as e:
            if Language.get()=="English":
                title='Exeption Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error de excepción'
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2=repr(e)
            msg=msg1+msg2    
            messagebox.showerror(title, msg)
    def div_by_zero(self, widget_name, value, focused):
        if value == 0:# Prohibit Division By Zero, Set Focus On Entry Widget
            if Language.get()=="English":
                title='Division By Zero Error'
                msg=f'Division By Zero! Please Change {focused} Value!'
            else:    
                title='Error de División por Cero'
                msg=f'¡División por Cero! ¡Por favor Cambie el Valor de {focused}!'
            messagebox.showerror(title, msg)
            widget_name.delete(0,"end")
            widget_name.focus_set()   
            return True
        else: return False
    def update_ratio(self, widget_name, new_value):
        widget_name.delete(0,"end")
        widget_name.insert(0, new_value)
        widget_name.focus_set()
    def keyboard(self,event):
        f=self.focused.get()
        txt=event.widget["text"]
        if txt!='Backspace' and txt!='Retroceso':
            if f=='A1':
                txt=self.a1.get()+event.widget["text"]
                self.a1.set(txt)
            elif f=='A2':
                txt=self.a2.get()+event.widget["text"]
                self.a2.set(txt)
            elif f=='B1':
                txt=self.b1.get()+event.widget["text"]
                self.b1.set(txt)
            elif f=='B2':
                txt=self.b2.get()+event.widget["text"]
                self.b2.set(txt)
            elif f=='A3':
                txt=self.a3.get()+event.widget["text"]
                self.a3.set(txt)
            elif f=='B3':
                txt=self.b3.get()+event.widget["text"]
                self.b3.set(txt)
        else:        
            if f=='A1':
                txt=self.a1.get()
                txt=txt[:-1]
                self.a1.set(txt)
            elif f=='A2':
                txt=self.a2.get()
                txt=txt[:-1]
                self.a2.set(txt)
            elif f=='B1':
                txt=self.b1.get()
                txt=txt[:-1]
                self.b1.set(txt)
            elif f=='B2':
                txt=self.b2.get()
                txt=txt[:-1]
                self.b2.set(txt)
            elif f=='A3':
                txt=self.a3.get()
                txt=txt[:-1]
                self.a3.set(txt)
            elif f=='B3':
                txt=self.b3.get()
                txt=txt[:-1]
                self.b3.set(txt)
    def keyboard_focus(self,event, widget):
        if widget=='A1':self.a1_txtbx.focus_force()
        elif widget=='A2':self.a2_txtbx.focus_force()
        elif widget=='B1':self.b1_txtbx.focus_force()
        elif widget=='B2':self.b2_txtbx.focus_force()
        elif widget=='A3':self.a3_txtbx.focus_force()
        elif widget=='B3':self.b3_txtbx.focus_force()
        self.focused.set(widget)
class Convert_Base:
    # Class Converts To And From Binary, Octal, Decimal And Hexadecimal, Returned Value Is String Object
    def __init__(self,from_base,to_base,str_val):
        self.f_base=from_base # Integer, Convert From Base
        self.t_base=to_base # Integer, Convert To Base
        self.val=(str_val.split('.')[0])# Remove Any Decimal Values       
        self.r_val='' # String, Returned Converted Value
    def __str__(self):
        def dec_to_bin(val):
            bin_list=list(range(4, 512, 4)) # Good To Hex Length 56 
            value=bin(val & (2**Bit_Size.get() - 1))
            value=value.replace("0b", "")
            bin_len=len(value)
            if bin_len in bin_list:# If In List Then Good To Go
                bin_list=[]
                return str(value)
            else:# Add Extra Zeros
                while bin_len not in bin_list:
                    value=value.rjust(bin_len+1,"0")# Add Zeroes
                    bin_len=len(value)
                    if bin_len in bin_list:
                        bin_list=[]
                        return str(value)
        def dec_to_oct(val):
            if val==0:return'0'
            oct_list=list(range(3, 224, 3))
            value=oct(val & (2**Bit_Size.get() - 1))
            value= value.replace("0o", "")
            oct_len = len(value)
            if oct_len in oct_list:# If In List Then Good To Go
                oct_list=[]
                return str(value)
            else:# Add Extra Zeros
                while oct_len not in oct_list:
                    value=value.rjust(oct_len+1,"0")# Add Zeroes
                    oct_len=len(value)
                    if oct_len in oct_list:
                        oct_list=[]
                        return str(value)
        def dec_to_hex(val):
            if val==0:return'0'
            value=hex(val & (2**Bit_Size.get()-1))
            upper=value.upper() # Uppercase
            value=upper.replace("0X", "")#  Strip 0X
            hex_list=list(range(4, 128, 4))
            hex_len=len(value)
            if hex_len in hex_list:# If In List Then Good To Go
                hex_list=[]
                return str(value)
            else:# Add Extra Zeros
                while hex_len not in hex_list:
                    value=value.rjust(hex_len+1,"0")# Add Zeroes
                    hex_len=len(value)
                    if hex_len in hex_list:
                        hex_list=[]
                        return str(value)
        try:                
            if self.f_base==2:# Binary
                dec_val=int(self.val, 2)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==8:# Octal
                dec_val=int(self.val, 8)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==10:# Decimal
                dec_val=int(self.val, 10)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==16:# Hexadecimal
                dec_val=int(self.val, 16)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
        except Exception as e:
            if Language.get()=="English":
                title='Converting Base Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error de Conversión de Base'
                msg1='Ocurrió una Excepción Durante la Ejecución del Código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            messagebox.showerror(title, msg)
            return 'break'
class Convert_Trig_Units:# Class Converts To And From Degrees, Radians, And Gradians. Returns String
    def __init__(self,from_units,to_units,str_val):
        self.f_units=from_units # String, Convert From Units
        self.t_units=to_units # String, Convert To Units
        self.val=float(str_val) # String, Value To Convert       
        self.r_val='' # String, Returned Converted Value
    def __str__(self):
        if self.f_units==self.t_units:
            self.r_val=str(self.val)
            return self.r_val
        def degrees_to_radians():
            value=self.val*(mp.pi/180)
            return str(value)
        def degrees_to_gradians():
            value=self.val*mpf(400/360)
            return str(value)
        def radians_to_degrees():
            value=self.val*(180/mp.pi)
            return str(value)
        def radians_to_gradians():
            degrees=self.val*(180/mp.pi)
            value=degrees*mpf(400/360)
            return str(value)
        def gradians_to_degrees():
            value=self.val*mpf(360/400)
            return str(value)
        def gradians_to_radians():
            degrees=self.val*mpf(360/400)
            value=degrees*(mp.pi/180)        
            return str(value)
        try:    
            if self.f_units=='Degrees' or self.f_units=='Grados':
                if self.t_units=='Radians' or self.t_units=='Radianes':
                    self.r_val=degrees_to_radians()
                    return self.r_val
                elif self.t_units=='Gradians' or self.t_units=='Gradianos':
                    self.r_val=degrees_to_gradians()
                    return self.r_val
            if self.f_units=='Radians' or self.f_units=='Radianes':
                if self.t_units=='Degrees' or self.t_units=='Grados':
                    self.r_val=radians_to_degrees()
                    return self.r_val
                elif self.t_units=='Gradians' or self.t_units=='Gradianos':
                    self.r_val=radians_to_gradians()
                    return self.r_val
            if self.f_units=='Gradians' or self.f_units=='Gradianos':
                if self.t_units=='Radians' or self.t_units=='Radianes':
                    self.r_val=gradians_to_radians()
                    return self.r_val
                elif self.t_units=='Degrees' or self.t_units=='Grados':
                    self.r_val=gradians_to_degrees()
                    return self.r_val
        except Exception as e:
            if Language.get()=="English":
                title='Converting Trigonometry Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error al Convertir Trigonometría'
                msg1='Ocurrió una Excepción Durante la Ejecución del Código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            messagebox.showerror(title, msg)
            return 'break'
def free_sys_symbols(*args):
    if not D_Memory1 and not  D_Memory2 and not  D_Memory3 and not  D_Memory4:
        if not args:
            for abc in Symbols_Used:
                Symbol(abc).free_symbols
            Symbols_Used.clear()
            Symbol_Names.clear()
            Symbol_Values.clear()
        else:
            for ar in args:
                Symbol(ar).free_symbols
    else:return
class Calculus_Scroll(tk.Frame):
    def __init__(self, parent, hgt, wid):
        super().__init__(parent)
        style=ttk.Style()
        style.theme_use('classic')
        # Pad X And Y Using Percent Of Width And Height 
        pad_10x=int(wid*0.0305)
        pad_20x=int(wid*0.061)
        pad_10y=int(hgt*0.0157)
        pad_20y=int(hgt*0.0313)
        self.canvas = tk.Canvas(self, width=wid, height=hgt, border=2, relief="sunken",bg='#f3f6f4')
        style.configure("Vertical.TScrollbar", background='#048c8c', bordercolor='#444444', arrowcolor='#2986cc')
        self.vbar=ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.vbar.pack(side='right',fill='y',padx=(2,2),pady=(pad_10y,pad_20y))                                        
        style.configure("Horizontal.TScrollbar", background='#048c8c', bordercolor='#444444', arrowcolor='#2986cc')
        self.hbar=ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.hbar.pack(side='bottom',fill='x',padx=(pad_20x,pad_10x),pady=(2,2))                                        
        self.canvas.pack(side='top', anchor='nw', fill='both', expand=True, padx=(pad_10x,0), pady=(0,0))
        self.window=tk.Frame(self.canvas,width=wid, height=hgt, bg='#f3f6f4')
        self.window.pack(side='top',anchor='nw',fill='both', expand=True, padx=(0,0), pady=(0,0))                     
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)                          
        self.canvas_window=self.canvas.create_window((0,0),window=self.window,anchor='nw', tags="self.window") 
        # Bind canvas And Scroll Window To Events                
        self.canvas.bind("<Key-Prior>", self.page_up)
        self.canvas.bind("<Key-Next>", self.page_down)
        self.canvas.bind("<Key-Up>", self.unit_up)
        self.canvas.bind("<Key-Down>", self.unit_down)        
        self.canvas.bind("<Key-Left>", self.unit_left)
        self.canvas.bind("<Key-Right>", self.unit_right)        
        self.window.bind("<Configure>", self.rst_frame)                       
        self.window.bind('<Enter>', self.inside_canvas)                                 
        self.window.bind('<Leave>', self.outside_canvas)                                 
        self.rst_frame(None)
    def rst_frame(self, event):                                              
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def unit_up(self, event):
        self.canvas.yview_scroll(-1, "unit")
        return "break"
    def unit_down(self, event):
        self.canvas.yview_scroll(1, "unit")
        return "break"
    def unit_left(self, event):
        self.canvas.xview_scroll(-1, "unit")
        return "break"
    def unit_right(self, event):
        self.canvas.xview_scroll(1, "unit")
        return "break"
    def page_up(self, event):
        self.canvas.yview_scroll(-1, "page")
        return "break"
    def page_down(self, event):
        self.canvas.yview_scroll(1, "page")
        return "break"
    def scroll_mousey(self, event):
        self.canvas.yview_scroll(int(-1* (event.delta/120)), 'units')
    def inside_canvas(self, event):                                                       
        self.canvas.focus_set()                                                 
        self.canvas.bind_all("<MouseWheel>", self.scroll_mousey)
    def outside_canvas(self, event):                                                       
        self.canvas.unbind_all("<MouseWheel>")
def do_calculus(event):
    if not Disp_List:return
    if Base.get()!='Decimal':return
    Display.set(Expression.get())
    txt=event.widget["text"]
    if txt=="∫":funct="integrate"
    elif txt=="f´(𝓧)":funct="differentiate"
    calc=Calculus(root,funct)
class Calculus(tk.Toplevel):
    def __init__(self, parent, funct):
        super().__init__(parent)
        self.funct=funct
        disp=Display.get()
        root.withdraw()
        self.deiconify()
        self.grab_set() # Receive Events And Prevent root Window Interaction
        hgt=screen_height * 0.6
        wid=screen_width * 0.3
        x=(screen_width/2)-(wid/2)
        y=(screen_height/2)-(hgt/2)
        self.geometry('%dx%d+%d+%d' % (wid, hgt, x, y, ))
        self.configure(bg='#f3f6f4')
        self.protocol("WM_DELETE_WINDOW", self.calculus_destroy)
        self.font=font.Font(family='Times New Romans', size=12, weight='normal', slant='italic')
        self.option_add('*TCombobox*Listbox.font', self.font)
        tk.Frame.scroll = Calculus_Scroll(self, wid, hgt) 
        tk.Frame.scroll.pack(side="top", fill="both", expand=True)
        tk.Frame.scroll.canvas.xview_moveto(0)
        tk.Frame.scroll.canvas.yview_moveto(0)
        tk.Frame.scroll.canvas.bind()
        close_brackets('all')# (Just In Case) Close All Opened Brackets Before Preceding
        if Language.get()=="English":txt="Expression"
        else:txt="Expresión"
        self.display_txt=Display_Text.get("1.0", tk.END).replace("\n","")
        self.expr_txt=f"{txt} = {self.display_txt}"
        disp=Display.get()
        Last_Display.append(f"{txt} = {Expression.get()}\n")
        self.expr=Expression.get().split("=")[0]# If Equation Has Answer, Trim (= and Answer)
        self.expr2=self.expr
        txt1=self.expr_txt
        r=1    
        self.lbl_1=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                text=txt1, anchor='w')
        self.lbl_1.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)        
        val=''
        last=False
        for i, item in enumerate(self.expr):# Populate Names With Values
            if item.isnumeric() or item=='.' or item=='-':
                if item=='-': # Only Populate Negative Numbers And Not Negative Functions 
                    if disp[1].isnumeric(): # Negative Number
                        #Build Value
                        val+=item
                        last=True
                else:#Build Value        
                    val+=item
                    last=True
            else:
                if last==True:
                    xyz=self.get_next_symbol(float(val))
                    self.expr=str(self.expr).replace(str(val),str(xyz),1) #replace value with Symbol_Names
                    last=False
                    val=''
        if last==True:
            xyz=self.get_next_symbol(float(val))
            self.expr=str(self.expr).replace(str(val),str(xyz),1)#replace value with Symbol_Names
            last=False
            val=''
        self.lbl_2=[]
        self.used_symbols=[]
        self.used_txt=[]
        c=0
        for i in range(len(Symbol_Names)):# Place Names And Values into Dictionary And Populate Labels
            txt=''
            sub_dict[Symbol_Names[i]] = Symbol_Values[i]
            if Symbol_Names[i] not in self.used_symbols:# Prevent Duplicate Symbol Population
                if str(Symbol_Names[i])!= "rad_to_deg" and str(Symbol_Names[i])!= "rad_to_grad":
                    txt=str(Symbol_Names[i])+' = '+str(Symbol_Values[i])
                    self.used_txt.append(txt) # Used To Populate These Labels
                    self.used_symbols.append(Symbol_Names[i]) # Used To Polulate symbol_bx 
                    r+=1        
                    self.lbl_2.append([c])
                    self.lbl_2[c]=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                        text=self.used_txt[c], anchor='w', justify='left')
                    self.lbl_2[c].grid(column=0,row=r, sticky=tk.W, padx=5, pady=1)
                    c+=1
        r+=1
        newstr=str(self.expr)
        if newstr[0]=='(' and newstr[-1]==')':newstr=newstr[1:-1] # Remove Extra Brackets
        if Language.get()=="English":txt=[f'Expression Symbolized = {newstr}','With Respect To:','Derivative Work Sheet']
        else:txt=[f'Expresión Simbolizada = {newstr}','Con Respecto a:','Hoja de Trabajo de Derivadas']
        self.lbl_3=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
            text=txt[0], anchor='w')
        self.lbl_3.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
        r+=1
        self.cbo_lbl=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
            text=txt[1], anchor='c', width=20)
        self.cbo_lbl.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
        self.respect=StringVar()
        style= ttk.Style()
        style.theme_use('default')
        r+=1
        style.configure("TCombobox", fieldbackground= '#f0ffff', background= '#f3f6f4')
        self.symbol_bx=ttk.Combobox(tk.Frame.scroll.window, values=self.used_symbols, font=self.font, width=20, 
        textvariable=self.respect, justify=tk.LEFT) 
        self.symbol_bx.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
        self.symbol_bx['state'] = 'readonly'
        if self.funct=='differentiate':
            self.title(f'{root_title}  {txt[2]}')
            r+=1
            if Language.get()=="English":
                multiples=['1st Derivative','2nd Derivative','3rd Derivative','4th Derivative','5th Derivative']
                txt='Number of Derivatives:'
            else:
                multiples=['1ra Derivada','2da Derivada','3ra Derivada','4ta Derivada','5ta Derivada']    
                txt='Número de Derivados:'
            self.multi_lbl=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                text=txt, anchor='c',width=20)
            self.multi_lbl.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
            self.multiple=StringVar()
            r+=1
            style.configure("TCombobox", fieldbackground= '#f0ffff', background= '#f3f6f4')
            self.multi_bx=ttk.Combobox(tk.Frame.scroll.window, values=multiples, font=self.font, width=20, 
            textvariable=self.multiple, justify=tk.LEFT) 
            self.multi_bx.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
            self.multi_bx.bind('<<ComboboxSelected>>', self.do_derivative)
            self.multi_bx['state'] = 'readonly'
            self.symbol_bx.bind('<<ComboboxSelected>>', self.do_derivative)
        elif self.funct=='integrate':
            if Language.get()=="English":txt='Integral Work Sheet'
            else:txt='Hoja de Trabajo de Integrales'
            self.title(f'{root_title}  {txt}')
            self.symbol_bx.bind('<<ComboboxSelected>>', self.do_integral)
        self.lbl_4=[]
        for i in range(0,6):
            r+=1
            self.lbl_4.append([i])
            self.lbl_4[i]=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font,
                text='',anchor='w')
            self.lbl_4[i].grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
        self.update()    
        self.mainloop()
    def get_next_symbol(self,val):
        if val in Symbol_Values:# Value Already Symbolized, return Symbol
            for i, j in enumerate(Symbol_Values):
                if j == val:return Symbol_Names[i]
        for symbol in list(map(chr,range(ord('a'),ord('z')+1))):
            if not symbol in _MyClash and not symbol in Symbols_Used:
                parsed=parse_expr(symbol, evaluate=False)
                symbol=sym.symbols(symbol)
                Symbols_Used.append(str(symbol))
                Symbol_Names.append(parsed)
                Symbol_Values.append(val)
                return symbol
        else: 
            for symbol in list(map(chr,range(ord('A'),ord('Z')+1))):
                if not symbol in _MyClash and not symbol in Symbols_Used:
                    symbol=sym.symbols(symbol)
                    Symbols_Used.append(str(symbol))
                    return symbol
    def do_integral(self,event):
        try:
            resp=parse_expr(self.respect.get(), evaluate=False)
            parsed_integral=parse_expr(self.expr, evaluate=True)
            disp_update('clear')
            integral_expr=Integral(parsed_integral,resp)
            exp=integral_expr.doit()
            newstr=str(self.expr2)
            for i in range(5):# Remove Extra Brackets
                if newstr[0]=='(' and newstr[-1]==')':
                    newstr=newstr[1:-1]
                else:break    
            answer=nround_answer(exp) # Round Answer To User Preference
            Answer_Present.set(True)
            Answer.set(answer)
            if Language.get()=="English":txt=['Equation','"Answer','Invalid Entry!','Get Integral']
            else:txt=['Ecuación','Respuesta','¡Entrada no Válida!','Obtener Integral']
            self.lbl_4[0].config(text=self.expr_txt)
            self.lbl_4[1].config(text=self.lbl_3['text'])
            self.lbl_4[2].config(text=f"{txt[0]} = ∫{resp}({self.display_txt})")
            self.lbl_4[3].config(text=f"= {exp}")
            self.lbl_4[4].config(text = f"{txt[1]} = {answer}")
            self.lbl_4[5].config(text = "--------------------------------------------------------------")
            for d in range(len(self.lbl_4)):
                txt=f"{self.lbl_4[d]["text"]}\n"
                Last_Display.append(txt)
            for d in range(1,len(Last_Display)):# Skip Calculator Expression Display (Last_Display[0])
                disp_update(Last_Display[d])
        except Exception as e:
            Answer.set('')
            Answer_Present.set(False)
            Answer_Err.set(True)
            self.lbl_4[1].config(text = txt[2])
            disp_update(f' = {txt[2]}')
            expr_update(f' = {txt[2]}')
            title= txt[3]
            msg1=f"{txt[2]}\n"
            msg2= repr(e)
            messagebox.showerror(title,msg1+msg2)
            self.calculus_destroy()
    def do_derivative(self,event):
        multiple_derivatives=self.multiple.get()
        resp=self.respect.get()
        if multiple_derivatives=='':return
        if resp=='':return
        try:
            resp=parse_expr(self.respect.get(), evaluate=False)
            parsed_derative=parse_expr(self.expr, evaluate=True)
            disp_update('clear')
            multiple_derivatives=self.multiple.get()
            tmp_str=''
            for i in self.multiple.get(): # Extract Number From String
                if i.isdigit():tmp_str+=i
            multi=parse_expr(tmp_str, evaluate=False)
            if Language.get()=="English":    
                if multiple_derivatives=='1st Derivative':mstr="f '"
                elif multiple_derivatives=='2nd Derivative':mstr="f ''"
                elif multiple_derivatives=='3rd Derivative':mstr="f '''"
                elif multiple_derivatives=='4th Derivative':mstr="f ''''"
                elif multiple_derivatives=='5th Derivative':mstr="f '''''"
            else:    
                if multiple_derivatives=='1ra Derivada':mstr="f '"
                elif multiple_derivatives=='2da Derivada':mstr="f ''"
                elif multiple_derivatives=='3ra Derivada':mstr="f '''"
                elif multiple_derivatives=='4ta Derivada':mstr="f ''''"
                elif multiple_derivatives=='5ta Derivada':mstr="f '''''"
            derative_expr=Derivative(parsed_derative, resp, multi)
            exp=derative_expr.doit()
            newstr=str(self.expr2)
            for i in range(5):# Remove Extra Brackets
                if newstr[0]=='(' and newstr[-1]==')':
                    newstr=newstr[1:-1]
                else:break
            answer=nround_answer(exp)
            Answer_Present.set(True)
            Answer.set(answer)
            if Language.get()=="English":txt=['Equation','"Answer','Invalid Entry!','Get Integral']
            else:txt=['Ecuación','Respuesta','¡Entrada no Válida!','Obtener Integral']
            self.lbl_4[0].config(text=self.expr_txt)
            self.lbl_4[1].config(text=self.lbl_3['text'])
            self.lbl_4[2].config(text=f"{txt[0]} = {mstr}{resp}({self.display_txt})")
            self.lbl_4[3].config(text=f"= {exp}")
            self.lbl_4[4].config(text = f"{txt[1]} = {answer}")
            self.lbl_4[5].config(text = "--------------------------------------------------------------")
            for d in range(len(self.lbl_4)):
                txt=f"{self.lbl_4[d]["text"]}\n"
                Last_Display.append(txt)
            for d in range(1,len(Last_Display)):# Skip Calculator Expression Display (Last_Display[0])
                disp_update(Last_Display[d])
        except Exception as e:
            Answer.set('')
            Answer_Present.set(False)
            Answer_Err.set(True)
            self.lbl_4[1].config(text = txt[2])
            disp_update(f' = {txt[2]}')
            expr_update(f' = {txt[2]}')
            title= txt[3]
            msg1=f"{txt[2]}\n"
            msg2= repr(e)
            messagebox.showerror(title,msg1+msg2)
            self.calculus_destroy()
    def calculus_destroy(self):# X Icon Was Clicked
        Last_Display.clear()
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
            else:
                widget.destroy()
        self.withdraw()
        root.deiconify()
        root.grab_set()
        root.focus_force()
        root.update()
def write_setup():
        temp_dict={}
        sc=json.load(open("Config.json", "r"))
        json.dump(sc,open("Config.json", "w"),indent=4)
        temp_dict[0]=Language.get()
        temp_dict[1]=str(mp.dps)
        temp_dict[2]=str(Round.get())
        temp_dict[3]=str(Exp_Precision.get())
        temp_dict[4]=str(Exp_Digits.get())
        temp_dict[5]=str(Bit_Size.get())
        temp_dict[6]=str(Display_fg.get())
        temp_dict[7]=str(Display_bg.get())
        temp_dict[8]=NewFont.get()
        temp_dict[9]=str(root.winfo_width())
        temp_dict[10]=str(root.winfo_height())
        temp_dict[11]=str(root.winfo_x())
        temp_dict[12]=str(root.winfo_y())
        with open("Config.json", "w") as outfile:json.dump(temp_dict, outfile)
        outfile.close()
        temp_dict.clear()
def read_setup():
    try:
        with open('Config.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        for key, value in data.items():
            if key=="0":Language.set(value)
            elif key=="1":mp.dps=int(value)
            elif key=="2":Round.set(int(value))
            elif key=="3":Exp_Precision.set(int(value))
            elif key=="4":Exp_Digits.set(int(value))
            elif key=="5":Bit_Size.set(int(value))
            elif key=="6":
                Display_fg.set(value)
                Display_Text.focus_force()
                Display_Text.config(fg=Display_fg.get())
            elif key=="7":
                Display_bg.set(value)
                Display_Text.focus_force()
                Display_Text.config(bg=Display_bg.get())
            elif key=="8":
                NewFont.set(value)
                new_font=parse_expr(value, evaluate=False)
                display_font.config(family=new_font['family'], size=new_font['size'], 
                                    weight=new_font['weight'], slant=new_font['slant'])
                NewFont_Size.set(new_font['size'])
                Display_Text.focus_force()
                Display_Text.configure(font=display_font)
            elif key=="9":root_width=int(value)
            elif key=="10":root_height=int(value)
            elif key=="11":root_x=int(value)
            elif key=="12":root_y=int(value)
    except Exception as e:
        if Language.get()=="English":
            title='Error Reading Config.json File'
            msg1=f'Error Reading {item} In Config.json:\n'
        else:
            title='Error al leer el archivo Config.json\n'
            msg1=f'Error al leer {item} en Config.json:'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title,msg)
        pass
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_x, root_y, ))
    root.update()
def convert_script(from_script,to_script,txt):# Convert Between Normal Script, Superscript And Subscript
    new_txt=txt.maketrans(''.join(from_script), ''.join(to_script))
    return txt.translate(new_txt)
def menu_popup(event):# display the popup menu
    popup.tk_popup(event.x_root, event.y_root)
    popup.grab_release()#Release the grab
def precision(which): # Calculator Precision Configuration
    if Language.get()=="English":
        titles=["<Calculator Precision>","<Round Displayed Answer>","<Scientific Notation Digits>",
                "<Exponential Notation Digits>","<Binary Bit Size>"]
        messages=["Enter Number Of Digits For Calculations. Max = 500","Round Answer To nth Decimal Places. 0 = No Rounding, Max = 500",
                    "Total Decimal Digits To Display For Scientific Notation. Max = 500","Exponential Notation Precision. Max = 4",
                    "Choices Are: 8 bits (Byte), 16 bits (Word), 32 bits (Dword), 64 bits (Qword), 128 bits (Double Qword), 256 bits (Yword), 512 (ZWord)"]
    else:
        titles=["<Precisión de la Calculadora>","<Redondear Respuesta Mostrada>","<Dígitos en Notación Científica>",
                "<Dígitos en Notación Exponencial>","<Tamaño de Bit Binario>"]
        messages=["Ingrese el número de dígitos para los cálculos. Máx = 500", "Redondear la respuesta a n lugares decimales. 0 = Sin redondeo, Máx = 500",
                    "Total de dígitos decimales a mostrar para notación científica. Máx = 500", "Precisión de notación exponencial. Máx = 4",
                    "Opciones Son: 8 bits (Byte), 16 bits (Palabra), 32 bits (Dpalabra), 64 bits (Qpalabra), 128 bits (Doble Qpalabra), 256 bits (Ypalabra), 512 bits (Zpalabra)"]
    if which=='dp':
        dpp=simpledialog.askinteger(titles[0],messages[0],parent=root,minvalue=1,maxvalue=500,initialvalue=mp.dps)
        if dpp is not None:
            mp.dps=int(dpp)
            mp.pretty==False
    elif which=='round':        
        rnd=simpledialog.askinteger(titles[1],messages[1],parent=root,minvalue=0,maxvalue=500,initialvalue=Round.get())
        if rnd is not None:Round.set(int(rnd))
    elif which=='exp':        
        snp=simpledialog.askinteger(titles[2],messages[2],parent=root,minvalue=1,maxvalue=500,initialvalue=Exp_Precision.get())
        if snp is not None:Exp_Precision.set(int(snp))
    elif which=='exp_digits':
        enp=simpledialog.askinteger(titles[3],messages[3],parent=root,minvalue=1,maxvalue=4,initialvalue=Exp_Digits.get())
        if enp is not None:Exp_Digits.set(int(enp))
    elif which=='bit_size':
        choices=['8','16','32','64','128','256','512']
        bbs=my_askstring(titles[4],messages[4],choices)
        if bbs is not None:Bit_Size.set(int(bbs))
def choose_font(): # Display Font
    if Language.get()=="English":txt=["Sample text for selected font","Choose Display Font"]
    else:txt=["Texto de Ejemplo para la Fuente Seleccionada","Elegir Fuente de Visualización"]
    default_font=NewFont.get()
    old_font=parse_expr(default_font, evaluate=False)
    if Display.get()!='':sample=Display.get()
    else:sample=txt[0]
    new_font=askfont(root,text=sample,title=txt[1] ,family=old_font['family'],
        size=old_font['size'],weight=old_font['weight'],slant=old_font['slant'])
    if new_font!='':
        NewFont.set(new_font)
        NewFont_Size.set(new_font['size'])
        display_font.config(family=new_font['family'], size=new_font['size'], weight=new_font['weight'], 
            slant=new_font['slant'])
        Display_Text.focus_force()
        Display_Text.configure(font=display_font)
def choose_color(which): # Display fg and bg Colors
    if Language.get()=="English":txt=["Choose Display Background Color","Choose Display ForeColor"]
    else:txt=["Elegir Color de Fondo de la Pantalla","Elegir Color de Primer Plano de la Pantalla"]
    if which=='bg':# Background
        color_code = colorchooser.askcolor(title =txt[0], initialcolor=Display_bg.get())
        if color_code[1]==None:return
        Display_bg.set(color_code[1])
        Display_Text.focus_force()
        Display_Text.config(bg=Display_bg.get())
        Display_Text.config(fg=Display_fg.get())
    elif which=='fg':# Foreground     
        color_code = colorchooser.askcolor(title =txt[1], initialcolor=Display_fg.get())
        if color_code[1]==None:return
        Display_fg.set(color_code[1])
        Display_Text.focus_force()
        Display_Text.config(bg=Display_bg.get())
        Display_Text.config(fg=Display_fg.get())
def about():
    if Language.get()=="English":
        msg1='Creator: Ross Waters\n'
        msg2='Email: RossWatersjr@gmail.com\n'
        msg3=f'Revision: {version}\n'
        msg4='Created For Windows 11'
    else:    
        msg1='Creador: Ross Waters\n'
        msg2='Correo Electrónico: RossWatersjr@gmail.com\n'
        msg3=f'Revisión: {version}\n'
        msg4='Creado para Windows 11'
    msg=msg1+msg2+msg3+msg4
    messagebox.showinfo(root_title, msg)
def calculator_destroy():
    try:# X Icon Was Clicked
        txt=get_greeting("close")
        display_popup(txt)
        time.sleep(2)
        write_setup()
        clear_memories()
        clear_all()
        Symbol_Names.clear()
        Symbol_Values.clear()
        _MyClash.clear()
        _MyConstants.clear()
        Operators.clear()
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):widget.destroy()
            else:widget.destroy()
        os._exit(0)
    except:
        os._exit(0)
def disp_update(txt, b=None):
    if txt!='clear':
        if txt==' = ' or Answer_Present.get():
            disp=Display.get()
            disp+=txt
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp)
            Display.set(disp)
            Disp_List.append(str(txt))
        elif txt=='refresh':    
            Display.set('')
            Display_Text.delete('1.0','end')
            disp=''.join(Disp_List)
            disp2=str(disp).replace('{','').replace('}','')
            Display.set(disp2)
            Display_Text.insert('end',disp2)
        else:     
            Display.set('')
            Display_Text.delete('1.0','end')
            Disp_List.append(str(txt))
            disp=''.join(Disp_List)
            disp2=str(disp).replace('{','').replace('}','')
            Display.set(disp2)
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp2)
            if b==None:
                if txt=='(':bracket_clicked('auto','disp','open')
                elif txt==')':bracket_clicked('auto','disp','close')
            if txt=='{':
                td_open=Temp_Disp_Open.get()
                td_open+=1
                Temp_Disp_Open.set(td_open)
            elif txt=='}':
                td_open=Temp_Disp_Open.get()
                td_open-=1
                Temp_Disp_Open.set(td_open)
    else:
        Display.set('')
        Display_Text.delete('1.0','end')
        Disp_List.clear()
        bracket_clicked('manual','both','clear')
def expr_update(txt, b=None):
    if txt!='clear':
        if txt==' = ' or Answer_Present.get():
            expr=Expression.get()
            expr+=txt
            Expression.set(expr)
            Expr_List.append(str(txt))
        elif txt=='refresh':    
            Expression.set('')
            expr=''.join(Expr_List)
            expr2=str(expr).replace('{','').replace('}','')
            Expression.set(expr2)
        else:     
            Expression.set('')
            Expr_List.append(str(txt))
            expr=''.join(Expr_List)
            expr2=str(expr).replace('{','').replace('}','')
            Expression.set(expr2)
            if b==None: 
                if txt=='(':bracket_clicked('auto','expr','open')
                elif txt==')':bracket_clicked('auto','expr','close')
            if txt=='{':
                te_open=Temp_Expr_Open.get()
                te_open+=1
                Temp_Expr_Open.set(te_open)
            elif txt=='}':
                te_open=Temp_Expr_Open.get()
                te_open-=1
                Temp_Expr_Open.set(te_open)
    else:
        Expression.set('')
        Expr_List.clear()
        bracket_clicked('manual','both','clear')
def numeric_clicked(event):
    try:
        if event.type=='4':text=event.widget["text"] # ButtonPress
        elif event.type=='2':text=event.char # KeyPress
        Display_Text.focus_force()    
        Display_Text.unbind('<period>')
        if text=='??': # Binding event Overrides Disabled State So Check State. If State = 'disabled' return
            if 'disabled' in event.widget.config('state'):return
        elif text=='.' and not Disp_List:
            clear_all()
            return
        elif text=='.'and Disp_List[-1]=='.':
            disp=Display.get()
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp)
            Display.set(disp)
            return    
        if Answer_Present.get() and text=='.':return  
        if Answer_Present.get() or Answer_Err.get():clear_all()
        base=Base.get()
        Display_Text.focus_set()
        if base=='Decimal':
            text=str(text)    
            dec_values=['0','1','2','3','4','5','6','7','8','9']
            if text=='.':# Prevent Multiple Periods From Keyboard Entry
                reverse_value('disp',False)
                value=return_value('disp',False,True) 
                if '.' in value:
                    text=''
                    Display_Text.focus_force()    
                    Display_Text.bind(('<period>'), lambda e: "break")
                    return
                else:    
                    Display_Text.focus_force()    
                    Display_Text.unbind('<period>')
                if Disp_List:
                    if not type_isnumerical(Disp_List[-1]):return       
                    if Disp_List[-1]=='.':return       
                    disp_update(text)
                    expr_update(text)
            elif text in dec_values:     
                if Answer_Present.get() or Answer_Err.get():clear_all()
                disp_update(text)
                expr_update(text)
        else:
            active_values=[]
            text=str(text).upper()
            if base=='Hexadecimal':
                hex_values=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
                if not text in hex_values:return
                active_values=hex_values
            elif base=='Octal':
                octal_values=['0','1','2','3','4','5','6','7']
                if not text in octal_values:return
                active_values=octal_values
            elif base=='Binary' or base=='Binario':
                bin_values=['0','1']
                if not text in bin_values:return
                active_values=bin_values
            if Answer_Present.get() or Answer_Err.get():clear_all()
            disp_update(text)
            Reversed_List.clear()
            opened=0
            closed=0
            if Disp_List:# Reverse Disp_List  But Do Not Pop
                if Disp_List[-1]==')':# Value Inside Brackets
                    for i in list(reversed(Disp_List)):
                        if i=='(':opened+=1
                        if i==')':closed+=1
                        if i in active_values:Reversed_List.append(i)
                        if opened==closed:break
                else:# No Brackets, Only Get Numbers    
                    for i in list(reversed(Disp_List)):
                        if i in active_values:Reversed_List.append(i)
                        else:break
            val2='' # Return Hex Sequence And Get Decimal Equalivent
            for i in list(reversed(Reversed_List)):
                val2+=i
            if base=='Hexadecimal':value=str(Convert_Base(16,10,str(val2)))
            elif base=='Octal':value=str(Convert_Base(8,10,str(val2)))
            elif base=='Binary' or base=='Binario':value=str(Convert_Base(2,10,str(val2)))
            # Update Expr_List With New Value
            if Expr_List:
                reverse_value('expr',True)
                expr_update(value)
            else:expr_update(value)
    except Exception:
        return 'break'
def set_numeric_type(value):
    try:
        float(value)
        status=float(value).is_integer()
        if status and '.' in str(value):return str(value) # Convert xx.0 To Integer xx
        elif status and not '.' in value:return str(int(value))# True Integer
        elif not status and 'e' in value:return str(mpf(value))# Scientific Notation
        elif not status and '.' in value:return str(mpf(value))# True Float
        else:return value   
    except Exception:return 'Invalid Type!'
def type_isnumerical(instr):
    # numeric_list Chars As Part Of Numerical Values
    numeric_list=['-','.',',','!',')','}','^','**']
    try:
        if instr in numeric_list:return True
        elif float(instr): return True
        elif instr.isnumeric():return True
        elif instr.isdigit():return True
        elif instr.isdecimal():return True
        elif instr=='0.0':return True
        else:return False
    except ValueError:
        return False
def clear_memories():
    mem_btn[0]['text']='ms1'
    mem_btn[0].configure(bg='#ffff99')
    D_Memory1.clear()
    E_Memory1.clear()
    mem_btn[1]['text']='ms2'
    mem_btn[1].configure(bg='#ffff99')
    D_Memory2.clear()
    E_Memory2.clear()
    mem_btn[2]['text']='ms3'
    mem_btn[2].configure(bg='#ffff99')
    D_Memory3.clear()
    E_Memory3.clear()
    mem_btn[3]['text']='ms4'
    mem_btn[3].configure(bg='#ffff99')
    D_Memory4.clear()
    E_Memory4.clear()
def memory_clicked(event):
    try:
        allowed=['^','**',', ']
        txt=event.widget["text"]
        if Disp_List and Expr_List:
            if Answer_Present.get():
                display_value=Disp_List[-1]
                expression_value=Expr_List[-1]
            else:
                disp_open=Disp_Bkts_Open.get()
                expr_open=Expr_Bkts_Open.get()
                if disp_open==0 and expr_open>0: # If Display Closed, Close Expression
                    for i in range(expr_open):
                        expr_update(')')
                display_value=''.join(Disp_List)
                expression_value=''.join(Expr_List)
        else:
            display_value=''
            expression_value=''    
        if txt=='ms1':
            D_Memory1.clear()
            E_Memory1.clear()
            if display_value!='':
                for i in display_value:D_Memory1.append(i)
                mem_btn[0]['text']='mr1'
                mem_btn[0].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory1.append(i)
        elif txt=='ms2':
            D_Memory2.clear()
            E_Memory2.clear()
            if display_value!='':
                for i in display_value:D_Memory2.append(i)
                mem_btn[1]['text']='mr2'
                mem_btn[1].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory2.append(i)
        elif txt=='ms3':
            D_Memory3.clear()
            E_Memory3.clear()
            if display_value!='':
                for i in display_value:D_Memory3.append(i)
                mem_btn[2]['text']='mr3'
                mem_btn[2].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory3.append(i)
        elif txt=='ms4':
            D_Memory4.clear()
            E_Memory4.clear()
            if display_value!='':
                for i in display_value:D_Memory4.append(i)
                mem_btn[3]['text']='mr4'
                mem_btn[3].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory4.append(i)
        if txt=='mr1':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory1)): 
                    disp_update(D_Memory1[i])
                for i in range(len(E_Memory1)): 
                    expr_update(E_Memory1[i])
            else:    
                if Disp_List[-1] == D_Memory1[-1] and Expr_List[-1]==E_Memory1[-1]:return
                else:
                    if Disp_List[-1] not in Operators and Disp_List[-1] not in allowed:return
                    else:    
                        for i in range(len(D_Memory1)): 
                            disp_update(D_Memory1[i])
                        for i in range(len(E_Memory1)): 
                            expr_update(E_Memory1[i])
        elif txt=='mr2':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory2)): 
                    disp_update(D_Memory2[i])
                for i in range(len(E_Memory2)): 
                    expr_update(E_Memory2[i])
            else:    
                if Disp_List[-1] == D_Memory2[-1] and Expr_List[-1]==E_Memory2[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory2)): 
                            disp_update(D_Memory2[i])
                        for i in range(len(E_Memory2)): 
                            expr_update(E_Memory2[i])
        elif txt=='mr3':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory3)): 
                    disp_update(D_Memory3[i])
                for i in range(len(E_Memory3)): 
                    expr_update(E_Memory3[i])
            else:    
                if Disp_List[-1] == D_Memory3[-1] and Expr_List[-1]==E_Memory3[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory3)): 
                            disp_update(D_Memory3[i])
                        for i in range(len(E_Memory3)): 
                            expr_update(E_Memory3[i])
        elif txt=='mr4':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory4)): 
                    disp_update(D_Memory4[i])
                for i in range(len(E_Memory4)): 
                    expr_update(E_Memory1[4])
            else:    
                if Disp_List[-1] == D_Memory4[-1] and Expr_List[-1]==E_Memory4[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory4)): 
                            disp_update(D_Memory4[i])
                        for i in range(len(E_Memory4)): 
                            expr_update(E_Memory4[i])
    except Exception as e:
        if Language.get()=="English":
            title= f"{txt} Memory Error"
            msg1='Exception occurred while code execution:\n'
        else:
            title=f"{txt} Error de Memoria"  
            msg1="Ocurrió una excepción durante la ejecución del código:"  
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def sign_clicked(event):
    base=Base.get()
    if Answer_Present.get() or base!='Decimal':return
    if event.widget["text"]!=chr(177) or 'disabled' in event.widget.config('state'):return
    dbo,tdo,ebo,teo=Disp_Bkts_Open.get(),Temp_Disp_Open.get(),Expr_Bkts_Open.get(),Temp_Expr_Open.get() 
    # If Display Closed, Close Expression
    if dbo==0:
        for i in range(ebo):expr_update(')')
    if tdo==0:            
        for i in range(teo):expr_update('}')
    try:
        if Disp_List and Expr_List:
            # Open Brackets With Numeric End ,'-10.3'(10.3' or Is Constant Or % 
            if Disp_List[-1].isdecimal() and Expr_List[-1].isdecimal() or Disp_List[-1] in _MyConstants and \
                Expr_List[-1] in _MyConstants or Disp_List[-1]=='%': # Change Sign For Value Not Enclosed In Brackets
                allowed=['-','.','%']
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10' 
                        if i.isdecimal() or i in allowed or i in _MyConstants:n-=1
                        else:break
                    if active_list[n]!='-':active_list.insert(n,'-')
                    elif active_list[n]=='-':active_list.pop(n)
                    if l==0:disp_update('refresh')        
                    elif l==1:expr_update('refresh')        
                return        
            elif Disp_List[-1]==')' and Expr_List[-1]==')': # Change Sign For Values Inside Parentheses
                bkt_opened,bkt_closed=0,0
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    for i in list(reversed(active_list)): # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                        n-=1
                        if i==')':bkt_closed+=1
                        elif i=='(':bkt_opened+=1
                        if bkt_opened==bkt_closed:
                            if i=='(':
                                if active_list[n-1]!='-':active_list.insert(n,'-')
                                elif active_list[n-1]=='-':active_list.pop(n-1)
                                if l==0:disp_update('refresh')        
                                elif l==1:expr_update('refresh')        
                                break
                return        
            elif Disp_List[-1]=='}' and Expr_List[-1]=='}': # Change Sign For Completed Functions Inside Temp Brackets
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    closed,opened=0,0        
                    for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                        n-=1
                        if i=='}':closed+=1
                        elif i=='{':opened+=1
                        if i=='{' and closed==opened:
                            if active_list[n+1]!='-':active_list.insert(n+1,'-')
                            elif active_list[n+1]=='-':active_list.pop(n+1)
                            if l==0:disp_update('refresh')        
                            elif l==1:expr_update('refresh')        
                            break
                return                
    except:pass
def operator_clicked(event):
    try:
        if event.type=='4':text=event.widget["text"] # ButtonPress
        elif event.type=='2':text=' '+event.char+' ' # KeyPress
        if not Disp_List:return
        if Disp_List[-1] in Operators:return # Prevent Multiple Operators
        disp_open=Disp_Bkts_Open.get()
        expr_open=Expr_Bkts_Open.get()
        if not disp_open and expr_open:bracket_clicked('manual','expr','close')
        if not Answer_Err.get():
            disp_update(text)
            expr_update(text)
            if Answer_Present.get():# Answer Becomes 1st Entry, Operator Becomes Second Entry
                answer=Answer.get()
                clear_all()# Start Fresh
                disp_update(answer)
                disp_update(text)
                base=Base.get() # If Base = Hex, Convert Expression Answer To Decimal
                if base=='Hexadecimal':answer=str(Convert_Base(16,10,str(answer)))
                elif base=='Octal':answer=str(Convert_Base(8,10,str(answer)))
                elif base=='Binary' or base=='Binario':answer=str(Convert_Base(2,10,str(answer)))
                expr_update(answer)
                expr_update(text)
    except Exception as e:
        if Language.get()=="English":
            title=f"Operator Clicked {text}"
            msg1=f'Exception occurred while code execution {Math_Function.get()}:\n'
        else:    
            title=f"Operador hizo clic {text}"
            msg1=f'Ocurrió una excepción durante la ejecución del código {Math_Function.get()}:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def reverse_value(which,pop):
    Reversed_List.clear()
    if not Disp_List:return
    if not Expr_List:return
    try:
        active_list=[]
        if which=='disp':active_list=Disp_List
        elif which=='expr':active_list=Expr_List
        # Populate With Value (Exposed) Not Enclosed In Brackets
        if active_list[-1].isdecimal() or is_float(active_list[-1]) or active_list[-1] in _MyConstants  or active_list[-1]=='%':
            allowed=['-','.','%']
            for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10', ', 10'
                if i.isdecimal() or is_float(i) or i in allowed or i in _MyConstants or i in Hex_List:
                    Reversed_List.append(i)
                    if pop:active_list.pop()
                else:break
            return ''.join(Reversed_List)
        elif active_list[-1]==')': # Values Inside Parentheses (Rounded Brackets).
            bkt_opened,bkt_closed=0,0
            for i in list(reversed(active_list)):  # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                Reversed_List.append(i)
                if pop:active_list.pop()
                if i==')':bkt_closed+=1
                elif i=='(':bkt_opened+=1
                if bkt_opened==bkt_closed:break
            return ''.join(Reversed_List)
        elif active_list[-1]=='}': # Value Is Completed Function Inside Temp Brackets
            bkt_opened,bkt_closed=0,0
            for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                Reversed_List.append(i)
                if pop:active_list.pop()
                if i=='}':bkt_closed+=1
                elif i=='{':bkt_opened+=1
                if bkt_opened==bkt_closed:break
            return ''.join(Reversed_List)
    except:pass
def return_value(which, update, bracket):
    try:
        value=''
        for i in list(reversed(Reversed_List)):value+=i
        if value[0]!='{' and value[-1]!='}': # Value Not Enclosed In {}
            if value[0]!='(' and value[-1]!=')': # Value Not Enclosed In ()
                if bracket:value='('+value+')' # Bracket value With ()
                if update:
                    if which=='disp':
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
            elif value[0]=='(' and value[-1]==')': # Value Enclosed In ()
                if update:
                    if which=='disp':        
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
            else: # Something Else    
                if update:
                    if which=='disp':        
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
        else: # Value Enclosed With {}     
            if update:
                if which=='disp':
                    for element in value:disp_update(element,'Some')
                elif which=='expr':    
                    for element in value:expr_update(element,'Some')
            return value
    except:pass
def open_temp_bracket(which): # Only Used To Increment Unfinished Function Brackets
    if which=='disp':
        td_open=Temp_Disp_Open.get()
        td_open+=1
        Temp_Disp_Open.set(td_open)
    elif which=='expr':
        te_open=Temp_Expr_Open.get()
        te_open+=1
        Temp_Expr_Open.set(te_open)
def close_brackets(which): # Close Unfinished Function Brackets
    if which=='all' or which=='disp':
        disp_open=Disp_Bkts_Open.get()
        if disp_open>0:
            for b in range(0,disp_open):
                disp_update(')')
    if which=='all' or which=='expr':            
        expr_open=Expr_Bkts_Open.get()
        if expr_open>0:
            for b in range(0,expr_open):
                expr_update(')')
    if which=='all' or which=='temp_disp':    
        td_open=Temp_Disp_Open.get()
        if td_open>0:
            for b in range(0,td_open):
                disp_update('}')
    if which=='all' or which=='temp_expr':            
        te_open=Temp_Expr_Open.get()
        if te_open>0:
            for b in range(0,te_open):
                expr_update('}')
def function_check(val):# Prevents Decimal Functions From Trying To Be Converted To Another Base.
    val=str(val)
    list1=['sin','cos','tan','sec','csc','cot','sinh','cosh','tanh','sech','csch','coth']
    list2=['asin','acos','atan','asec','acsc','acot','asinh','acosh','atanh','asech','acsch','acoth']
    list3=['log𝒆','log₁₀','log','1 / ','^','**','ʸ√','²√','³√','n!']
    for item in list1:
        for value in Disp_List:
            if item in value:return True
    for item in list2:
        for value in Disp_List:
            if item in value:return True
    for item in list3:
        for value in Disp_List:
            if item in value:return True
    return False        
def funct_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if event.widget["text"]=='':return
    if Answer_Err.get():return
    try:
        answer_was_present=False
        if Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
            answer=Answer.get()
            clear_all()
            answer_was_present=True
            for i, item in enumerate(answer):
                disp_update(item)
                expr_update(item)
        funct=event.widget["text"]
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        if Disp_List:# Prevent Double Constants
            if event.widget["text"] in _MyConstants and Disp_List[-1] in _MyConstants:return
        # Functions Requiring Data Entry First 
        if funct=='1/𝓧':
            if not Disp_List:return
            if Disp_List[-1] in Operators:return       
            reverse_value('disp',True) # Display 
            disp_update('{')
            disp_update('(')
            disp_update('1')    
            disp_update(' / ')
            value=return_value('disp',True,False) 
            disp_update(')')
            disp_update('}')
            reverse_value('expr',True) # Expression
            expr_update('{')
            expr_update('(')
            expr_update('1')    
            expr_update(' / ')
            value=return_value('expr',True,True)
            expr_update(')')
            expr_update('}')
        elif funct=='𝓧ʸ':# Expression = x**y, Display = x^y
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('(')
                return_value('disp',True,False)
                disp_update('^')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,False)
                expr_update('**')
        elif funct=='𝓧²' or funct=='𝓧³':
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('(')
                value=return_value('disp',True,False)
                disp_update('^')
                if funct=='𝓧²':disp_update('2')
                if funct=='𝓧³':disp_update('3')
                disp_update(')')
                disp_update('}')
                reverse_value('expr',True)
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,False)
                expr_update('**')
                if funct=='𝓧²':expr_update('2')
                if funct=='𝓧³':expr_update('3')
                expr_update(')')
                expr_update('}')
        elif funct=='ʸ√':# mpMath = root(x, y), Simplified = x**(1 / y), Display = ʸ√(x, y)
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                if Disp_List and Disp_List[-1]=='(':bracket=True
                else:bracket=False
                disp_update('{')
                disp_update('ʸ√')
                if not bracket:disp_update('(')
                value=return_value('disp',True,False) 
                disp_update(', ')
                reverse_value('expr',True) # Expression
                if Expr_List and Expr_List[-1]=='(':bracket=True
                else:bracket=False
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,True)
                expr_update('**')
                expr_update('(')
                expr_update('1')
                expr_update(' / ')
        elif funct=='²√'or funct=='³√':#sympify = x**(1 / 2), Display = ²√x, sympify = x**(1 / 3), Display = ³√x
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update(event.widget["text"])
                value=return_value('disp',True,True)
                disp_update('}')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,True)
                expr_update('**') 
                expr_update('(')
                expr_update('1')
                expr_update(' / ')
                if funct=='²√':expr_update(' 2 ')
                if funct=='³√':expr_update(' 3 ')
                expr_update(')')
                expr_update(')')
                expr_update('}')
        elif funct=='n!': # Factorial Of n where n Is Natural Number And Positive, expr=factorial(n)
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('fact')
                value=return_value('disp',True,True)
                disp_update('}')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                expr_update('factorial')
                value=return_value('expr',True,True)
                expr_update(')')
                expr_update('}')
        elif funct=='%':
            if not Disp_List:return
            if Disp_List[-1] in Operators:return
            if not Disp_List[-1].isdecimal() or Disp_List[-1] in _MyConstants:return        
            disp_update('%') # Display
            reverse_value('expr',True) # Expression
            value=return_value('disp',False,True)
            expr=str(value+' * 0.01')    
            expr=parse_expr(expr, evaluate=False)# Change Reversed_List To Percent
            f=str(expr.evalf())
            for i in f:expr_update(i)# Recreate Expr_List With Calculated Percent
        elif funct=='mod':# a % b, remainder, expr = Mod(100, 21)= 16, Display = Mod(100, 21)
            if not Disp_List:return
            reverse_value('disp',True) # Display
            disp_update('{')
            disp_update('mod')
            disp_update('(')
            value=return_value('disp',True,False)
            if value=='break':
                mod_btn.config(state="normal")
                return
            disp_update(', ')
            reverse_value('expr',True) # Expression
            expr_update('{')
            expr_update('Mod')
            expr_update('(')
            value=return_value('expr',True,False)
            expr_update(', ')
        elif funct=='exp':# Scientific Notation
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]):
                reverse_value('disp',True)
                val1=return_value('disp',False,True)# Do Not Update
                val2=str(val1).replace('{','').replace('}','').replace('(','').replace(')','') # Remove Temp Brackets For Examination
                value=np.format_float_scientific(mpf(val2), unique=False, precision=Exp_Precision.get(), exp_digits=Exp_Digits.get())            
                disp_update(value)
                reverse_value('expr',True)
                expr_update(value)
        elif funct in _MyConstants: # Constants
            if not answer_was_present:
                if Disp_List: # End Strip All Brackets For Examination
                    allowed=['^','**',', ']
                    val=''.join(Disp_List)
                    val2 = str(val).replace('{','').replace('}','').replace('(','').replace(')','')
                    if val2!='':
                        if event.widget["text"] in _MyConstants and val2[-1].isdecimal() or \
                            val2[-1] in allowed or Disp_List[-1] in Operators or Disp_List[-1] in allowed:pass
                        else:return
                if funct=='Π₂':
                    disp_update(event.widget["text"])
                    expr_update('Π')
                    parsed=parse_expr('Π')
                else:
                    disp_update(event.widget["text"])
                    expr_update(event.widget["text"])
                    parsed=parse_expr(event.widget["text"], evaluate=False)
                Symbol_Names.append(parsed)
                if funct=='𝓔':Symbol_Values.append(mp.euler)
                elif funct=='π':Symbol_Values.append(mp.pi)
                elif funct=='𝜯':Symbol_Values.append(2*mp.pi)
                elif funct=='𝜱':Symbol_Values.append(mp.phi)
                elif funct=='𝑮':Symbol_Values.append(mp.catalan)
                elif funct=='𝜁3':Symbol_Values.append(mp.apery)
                elif funct=='𝑲':Symbol_Values.append(mp.khinchin)
                elif funct=='𝑨':Symbol_Values.append(mp.glaisher)
                elif funct=='𝑴':Symbol_Values.append(mp.mertens)
                elif funct=='Π₂':Symbol_Values.append(mp.twinprime)
                elif funct=='𝒆':Symbol_Values.append(mp.e)
            else:
                clear_all()
                disp_update(answer)
                expr_update(answer)
    except Exception as e:
        if Language.get()=="English":
            title=f"Function {funct} Error"
            msg1=f'Exception occurred while code execution {funct}:\n'
        else:
            title=f"Error en la Función {funct}"
            msg1=f'Se produjo una excepción durante la ejecución del código {funct}:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def trig_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    if Disp_List[-1]=='^':return
    if Disp_List[-1] in Operators:return
    try:       
        if Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
            answer=Answer.get()
            clear_all()
            disp_update(answer)
            expr_update(answer)
        unit=Trig_Units.get()
        if unit=='Radians' or unit=='Radianes':unit_txt='ʳ'
        elif unit=='Degrees' or unit=='Grados':unit_txt='ᵈ'
        elif unit=='Gradians' or unit=='Gradianos':unit_txt='ᵍ'
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        # Display
        reverse_value('disp',True)
        disp_update('{')
        disp_update(event.widget["text"]+unit_txt)
        disp_value=return_value('disp',False,False)
        bkt=False
        if disp_value[0]=='{' and disp_value[-1]=='}':
            if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
        elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
        if not bkt:disp_update('(')
        disp_update(disp_value)
        if not bkt:disp_update(')')
        disp_update('}')
        # Expression
        reverse_value('expr',True)
        expr_update('{')
        expr_update(event.widget["text"])
        expr_value=return_value('expr',False,True)
        if unit=='Radians' or unit=='Radianes':
            expr_update(expr_value)
            expr_update('}')
            return
        if event.widget["text"][0]!='a': # (No arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
            if unit=='Degrees' or unit=='Grados':# {sin(40 * (pi / 180))}, {sin((20 + 20) * (pi / 180))}
                parsed=parse_expr('rad_to_deg', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(mp.pi/180)
                expr_update('(')
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('rad_to_deg')
                expr_update(')')
            elif unit=='Gradians' or unit=='Gradianos':# {sin(40 * (pi / 200))}, {sin((20 + 20) * (pi / 200))}          
                    parsed=parse_expr('rad_to_grad', evaluate=False)
                    Symbol_Names.append(parsed)
                    Symbol_Values.append(mp.pi/200)
                    expr_update('(')
                    expr_update(expr_value)
                    expr_update(' * ')
                    expr_update('rad_to_grad')
                    expr_update(')')
        elif event.widget["text"][0]=='a': # (arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
            if unit=='Degrees' or unit=='Grados':
                parsed=parse_expr('arc_rad_to_deg', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(180/mp.pi)
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('arc_rad_to_deg')
            elif unit=='Gradians' or unit=='Gradianos':          
                parsed=parse_expr('arc_rad_to_grad', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(200/mp.pi)
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('arc_rad_to_grad')
        expr_update('}')
    except Exception as e:
        if Language.get()=="English":
            title=f"Trigonometry {Math_Function.get()} Error"
            msg1='Exception occurred while code execution:\n'
        else:    
            title=f"Error de Trigonometría {Math_Function.get()}"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def log_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    if Disp_List[-1]=='^' or Disp_List[-1]==', ':return
    if Disp_List[-1] in Operators:return
    try:       
        if Answer_Present.get():# For Only Functions That Require Entry Before Function Click.
            answer=Answer.get()
            clear_all()
            disp_update(answer)
            expr_update(answer)
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        if event.widget["text"]=='log𝒆':text='log𝒆'     
        elif event.widget["text"]=='log10':text='log₁₀'     
        elif event.widget["text"]=='log(x,b)':text='log'
        # Display
        ret=reverse_value('disp',True)
        disp_update('{')
        disp_update(text)
        disp_value=return_value('disp',False,False)# Only Return Value
        bkt=False
        if disp_value[0]=='{' and disp_value[-1]=='}':
            if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
        elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
        # Expression
        reverse_value('expr',True)
        expr_update('{')
        expr_update('log')
        expr_value=return_value('expr',False,True)# Only Return Value
        if text=='log𝒆':    
            if not bkt:disp_update('(')
            disp_update(disp_value)
            if not bkt:disp_update(')')
            disp_update('}')
            expr_update(expr_value)
            expr_update('}')
        elif text=='log₁₀':
            if not bkt:disp_update('(')
            disp_update(disp_value)
            if not bkt:disp_update(')')
            disp_update('}')
            expr_update('(')
            expr_update(expr_value)
            expr_update(', ')
            expr_update('10')
            expr_update(')')
            expr_update('}')
        elif text=='log': #'log(x,b)'
            disp_update('(')
            disp_update(disp_value)
            disp_update(', ')
            expr_update('(')
            expr_update(expr_value)
            expr_update(', ')
    except Exception as e:
        if Language.get()=="English":
            title=f"Logarithmic Function {Math_Function.get()} Error"
            msg1='Exception occurred while code execution:\n'
        else:    
            title=f"Error de Función Logarítmica {Math_Function.get()}"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def temp_clicked(event):# C = K - 273.15, C = (R - 491.67) * (5 / 9), C = (F - 32) * (5/9), F = 32 + (C / (5/9)) 
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    try:
        if Answer_Present.get():
            newval=Answer.get()
            Answer_Present.set(False)
            disp_update('clear')
            expr_update('clear')
            disp_update(str(newval))
            expr_update(str(newval))
        reverse_value('expr',True)
        if event.widget["text"]=='°F→°C':
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' - 32) * (5 / 9')
            expr_update(')')
        elif event.widget["text"]=='°C→°F':
            expr_update('32 + ')
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' / (5 / 9)')
            expr_update(')')
        elif event.widget["text"]=='°K→°C':
            value=return_value('expr',True,True) 
            expr_update(' - ')
            expr_update('273.15')
        elif event.widget["text"]=='°R→°C':
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' - 491.67')
            expr_update(')')
            expr_update(' * (5 / 9)')
        equal_clicked(event)
    except Exception as e:
        if Language.get()=="English":
            title="Temperature Conversion Error"
            msg1='Exception occurred while code execution:\n'
        else:    
            title="Error de Conversión de Temperatura"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def bracket_clicked(how,which,status):
    if Answer_Present.get():return# Brackets Not Allowed If Answer Present
    if Answer_Err.get():return
    if  Disp_List and Disp_List[-1]=='^' and status=='close':return
    if status=='close' and Disp_List[-1]=='(':
        disp=Display.get()
        Display_Text.delete('1.0','end')
        Display_Text.insert('end',disp)
        Display.set(disp)
        return    
    unwanted_list=['-','.',',','!',')']
    disp_open=Disp_Bkts_Open.get()
    expr_open=Expr_Bkts_Open.get()
    try:
        # Avoid Unwanted Brackets
        if status=='open':
            if which=='disp' or which=='both':
                if Disp_List:
                    if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in unwanted_list:
                        if Disp_List[-1]!='^':return
        elif status=='close' and how!='auto':
            if which=='disp' or which=='both':
                if Disp_List:
                    early_list=['(','.',',']
                    if Disp_List[-1]in early_list:return
                    if disp_open==0:return
        elif status=='clear': # Reset Brackets To Zero
            if which=='disp' or which=='both':
                Disp_Bkts_Open.set(0)
                Temp_Disp_Open.set(0)
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,'0'))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                Expr_Bkts_Open.set(0)
                Temp_Expr_Open.set(0)
            return
        if how=='manual': # Brackets Entered Manually By Click. Add Bracket And Increase Or Decrease Count   
            if which=='disp' or which=='both':
                disp_open=Disp_Bkts_Open.get()
                if status=='open':# Create New '('
                    disp_open+=1
                    disp_update('(','Some')
                    Disp_Bkts_Open.set(disp_open)
                elif status=='close':# Create New ')'
                    if disp_open > 0:
                        disp_update(')','Some')
                        disp_open-=1
                        Disp_Bkts_Open.set(disp_open)
                        disp_open=Disp_Bkts_Open.get()
                        td_open=Temp_Disp_Open.get()
                        if td_open>0 and disp_open==0:close_brackets('temp_disp')
                disp_open=Disp_Bkts_Open.get()
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,str(disp_open)))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                expr_open=Expr_Bkts_Open.get()
                if status=='open':# Create New '('
                    expr_open+=1
                    expr_update('(','Some')
                    Expr_Bkts_Open.set(expr_open)
                elif status=='close':# Create New ')'
                    if expr_open > 0:
                        expr_update(')','Some')    
                        expr_open-=1
                        Expr_Bkts_Open.set(expr_open)
                        expr_open=Expr_Bkts_Open.get()
                        disp_open=Disp_Bkts_Open.get()
                        if disp_open==0:
                            for i in range(expr_open):
                                expr=Expression.get()
                                expr_update(')','Some')
                                expr_open-=1
                                Expr_Bkts_Open.set(expr_open)
                            td_open=Temp_Expr_Open.get()
                            if td_open>0 and expr_open==0:close_brackets('temp_expr')
        elif how=='auto': # Brackets Entered Automatically By Expression. Only Increase Or Decrease Count.
            if which=='disp' or which=='both':
                disp_open=Disp_Bkts_Open.get()
                if status=='open':# Increase open count
                    disp_open+=1
                elif status=='close':# Decrease open count 
                    if disp_open > 0:
                        disp_open-=1
                Disp_Bkts_Open.set(disp_open)
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,str(disp_open)))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                expr_open=Expr_Bkts_Open.get()
                if status=='open':expr_open+=1 # Increase open count
                elif status=='close':
                    if expr_open > 0:expr_open-=1 # Decrease open count
                Expr_Bkts_Open.set(expr_open)
    except Exception as e:
        if Language.get()=="English":
            title="Bracket Error"
            msg1='Exception occurred while code execution:\n'
        else:    
            title="Error de Corchete"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def nround_answer(expr):# Use nstr In Conj. With Round.get() To Round Answer
    try:
        expr_answer=expr.evalf(mp.dps, subs=sub_dict)
        answer_str=str(expr_answer)
        rund=Round.get()
        n_str=''
        for i in answer_str:
            n_str=i+n_str
            if i=='.':break
            else:count=len(n_str)
        if '-' in answer_str:count-=1
        n=rund+count
        if rund>0:
            if type_isnumerical(answer_str):
                answer=nstr(mpf(expr_answer), n)
            else:answer=str(expr_answer) # Answer Isn't Numerical   
        else:answer=str(expr_answer) # No Rounding
        return answer # Return Value = n For nstr
    except Exception as e:
        if Language.get()=="English":
            title="Round Answer Error"
            msg1='Exception occurred while code execution:\n'
        else:    
            title="Error de Respuesta Redondeada"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def equal_clicked(event):
    if not Disp_List:return
    if Answer_Err.get():return
    if Disp_List[-1]==' = ':return
    expr=Expression.get()
    close_brackets('all')# (Just In Case) Close All Opened Brackets Before Preceding
    sub_dict={}
    for i in range(len(Symbol_Names)):
        sub_dict[Symbol_Names[i]] = Symbol_Values[i]
    if not Answer_Present.get():
        try:
            constant=False
            expr=Expression.get()
            if expr in _MyConstants: constant=True
            exp=parse_expr(expr, evaluate=True)
            expr_answer=exp.evalf(mp.dps, subs=sub_dict)
            if not constant:answer=nround_answer(expr_answer)
            else:
                answer=str(expr_answer)
            if answer!='' or answer!=None:# Required 2 Entries (= And Answer)
                answer=set_numeric_type(answer) # Test For Valid Answer
                newval=answer
                disp_update(' = ')
                expr_update(' = ')
                if newval!='Invalid Type!'and newval!='Type is Imaginary Literal!':
                    base=Base.get()
                    if base=='Decimal':
                        Answer.set(newval)
                    elif base=='Hexadecimal':
                        hex=str(Convert_Base(10,16,str(newval)))
                        Answer.set(hex)
                    elif base=='Octal':
                        oct=str(Convert_Base(10,8,str(newval)))
                        Answer.set(oct)
                    elif base=='Binary' or base=='Binario':
                        bin=str(Convert_Base(10,2,str(newval)))
                        Answer.set(bin)
                    Answer_Present.set(True)
                    Answer_Err.set(False)
                    disp_update(Answer.get())
                    expr_update(Answer.get())
                else:    
                    Answer.set('')
                    Answer_Present.set(False)
                    Answer_Err.set(True)
                    disp_update(str(newval))
                    expr_update(str(newval))
            Math_Function.set('')
        except Exception:
            Answer.set('')
            Answer_Present.set(False)
            Answer_Err.set(True)
            if Language.get()=="English":
                disp_update(' = Invalid Entry!')
                expr_update(' = Invalid Entry!')
            else:    
                disp_update(' = ¡Entrada no válida!')
                expr_update(' = ¡Entrada no válida!')
            return 'break'
def config_base(base):
    Base.set(base)
    if base=='Binary' or base=='Binario':
        base_btn[0].configure(bg='white', fg='navy')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,2):
            num_btn[num]['state']="normal"
        for num in range(2,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Octal':
        base_btn[3].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        for num in range(0,8):
            num_btn[num]['state']="normal"
        for num in range(8,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Decimal':
        base_btn[1].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,10):
            num_btn[num]['state']="normal"
        for num in range(10,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.unbind('<period>')
        Display_Text.bind('<period>')
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind('<period>')
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Hexadecimal':
        base_btn[2].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,16):
            num_btn[num]['state']="normal"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.unbind(str(item))
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item))
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), numeric_clicked)
def base_clicked(event):
    value=Disp_List
    exist=False
    if not Answer_Present.get():
        exist=function_check(value)
    if exist:return
    if value=='':return
    hex_values=['A','B','C','D','E','F']
    try:
        if Answer_Present.get():from_val=Answer.get()
        else:from_val=Display.get()
        if from_val=='':
            Base.set(event.widget["text"])
            config_base(event.widget["text"])
        elif from_val!='' and Base.get()!= event.widget["text"]:
            f_base=Base.get()# Get Present Base
            if f_base=='Binary' or f_base=='Binario':from_base=2
            elif f_base=='Octal':from_base=8
            elif f_base=='Decimal':from_base=10
            elif f_base=='Hexadecimal':from_base=16
            is_numerical=False
            disp=Display.get()
            for i in disp: # Examine Display String For Only Numerical Value
                if i.isdigit() or i in hex_values:is_numerical=True
                else:
                    is_numerical=False
                    break
            if Answer_Present.get() or is_numerical==True: # If Answer Or Only Numerical Value Exist Then Convert
                Answer_Present.set(False)
                Base.set(event.widget["text"])
                t_base=Base.get()    
                if t_base=='Binary' or t_base=='Binario':to_base=2
                elif t_base=='Octal':to_base=8
                elif t_base=='Decimal':to_base=10
                elif t_base=='Hexadecimal':to_base=16
                config_base(t_base)
                base_val=str(Convert_Base(from_base,to_base,from_val))
            else:return    
            # Pop Last Base Value From Both List And Replace With New Base Value
            disp_update('clear')
            if Answer.get():expr_update('clear')
            for i, item in enumerate(str(base_val)):
                disp_update(item)
            if Answer_Present.get():
                if from_base!=10:
                    answer_val=str(Convert_Base(from_base,10,from_val))
                else:
                    answer_val=from_val   
                for i, item in enumerate(answer_val):
                    expr_update(item)
                Answer_Present.set(False)
                Answer.set('')    
        else: Base.set(event.widget["text"])   
        config_trig(Trig_Units.get())
    except Exception as e:
        if Language.get()=="English":
            title=f"Changing Base {Base.get()}"
            msg1='Exception occurred while code execution:\n'
        else:    
            title=f"Cambiando Base {Base.get()}"
            msg1='Ocurrió una excepción durante la ejecución del código:\n'
        msg2= repr(e)
        msg=msg1+msg2
        messagebox.showerror(title, msg)
        return 'break'
def config_trig(unit):
    base=Base.get()
    Trig_Units.set(unit)
    if base=='Decimal':
        for num in range(0, len(unit_btn)):
            unit_btn[num]['state']="normal"
    else:    
        for num in range(0, len(unit_btn)):
            unit_btn[num]['state']="disabled"
    if unit=='Degrees' or unit=='Grados':
        unit_btn[0].configure(bg='white', fg='green')
        unit_btn[1].configure(bg='green', fg='white')
        unit_btn[2].configure(bg='green', fg='white')
    elif unit=='Radians' or unit=='Radianes':
        unit_btn[1].configure(bg='white', fg='green')
        unit_btn[0].configure(bg='green', fg='white')
        unit_btn[2].configure(bg='green', fg='white')
    elif unit=='Gradians' or unit=='Gradianos':
        unit_btn[2].configure(bg='white', fg='green')
        unit_btn[0].configure(bg='green', fg='white')
        unit_btn[1].configure(bg='green', fg='white')
def trig_unit_clicked(event):
    # Binding event Overrules Disabled State So Check State. If State = 'disabled' return
    base=Base.get() # Only Allow Conversions For Decimal Base
    if 'disabled' in event.widget.config('state') or base!='Decimal':return
    if Answer_Present.get():
        str_val=Answer.get()
    else:
        str_val=Display.get()
    if str_val=='':
        Trig_Units.set(event.widget["text"])
        config_trig(event.widget["text"])    
    from_angle=Trig_Units.get()
    if str_val!='':
        Trig_Units.set(event.widget["text"])
        unit=Trig_Units.get()
        config_trig(unit)
        is_numerical=False
        disp=Display.get()
        is_numerical=type_isnumerical(disp)
        if Answer_Present.get() or is_numerical: # If Answer Or Only Numerical Value Exist Then Convert
            val=str(Convert_Trig_Units(from_angle,unit,str_val))
            Answer_Present.set(False)
        else:return
        rund=Round.get()
        if rund>0:
            expr=val
            exp=parse_expr(expr, evaluate=True)
            expr_answer=exp.evalf(mp.dps, subs=sub_dict)
            answer=nround_answer(expr_answer)
        else:answer=val    
        Display.set(answer)
        Display_Text.delete('1.0','end')
        Display_Text.insert('end',answer)
        Answer_Present.set(True)
        Answer.set(answer)
def config_trig_btns(event):
    arc=Arc.get()
    hyp=Hyp.get()
    if event.widget["text"]=='Hyp':
        if hyp:
            Hyp.set(False)
            hyp=False
        else:
            Hyp.set(True)
            hyp=True
    elif event.widget["text"]=='Arc':        
        if arc:
            Arc.set(False)
            arc=False
        else:
            Arc.set(True)
            arc=True
    if not hyp and not arc:
        trig1=['sin','sec','cos','csc','tan','cot']
        for i, item in enumerate(trig1):
            trig_btn[i]['text']=item
        hyp_btn.configure(bg='green', fg='white')
        arc_btn.configure(bg='green', fg='white')
    elif hyp and not arc:
        trig2=['sinh','sech','cosh','csch','tanh','coth']
        for i, item in enumerate(trig2):
            trig_btn[i]['text']=item
        hyp_btn.configure(bg='white', fg='green')
        arc_btn.configure(bg='green', fg='white')
    elif not hyp and arc:
        trig3=['asin','asec','acos','acsc','atan','acot']
        for i, item in enumerate(trig3):
            trig_btn[i]['text']=item
        arc_btn.configure(bg='white', fg='green')
        hyp_btn.configure(bg='green', fg='white')
    elif hyp and arc:        
        trig4=['asinh','asech','acosh','acsch','atanh','acoth']
        for i, item in enumerate(trig4):
            trig_btn[i]['text']=item
        arc_btn.configure(bg='white', fg='green')
        hyp_btn.configure(bg='white', fg='green')
def clear_entry(event):
    if Answer_Present.get():Answer_Present.set(False)
    if Disp_List and Expr_List:
        if Disp_List[-1]==Expr_List[-1] or Disp_List[-1]=='^' and Expr_List[-1]=='**': 
            last_element = Disp_List[-1]
            if last_element==')':bracket_clicked('auto','both','open')
            if last_element=='(':bracket_clicked('auto','both','close')
            if Disp_List:Disp_List.pop()
            if Expr_List:Expr_List.pop()
            e1=''.join([str(item) for item in Expr_List])
            Expression.set(e1)
            d1=''.join([str(item) for item in Disp_List])
            d2 = str(d1).replace('{','').replace('}','') # Remove Temp Brackets For Examination
            Display.set(d2)
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',d2)
    else:clear_all()
def get_greeting(status):
    current_datetime = datetime.now()
    if Language.get()=="English":
        if current_datetime.hour<12:
            if status=="open":greeting="Good Morning"
            else:greeting="Have a Wonderful Morning"    
        elif current_datetime.hour>=12 and current_datetime.hour<17:
            if status=="open":greeting="Good Afternoon"
            else:greeting="Have a Wonderful Afternoon"    
        elif current_datetime.hour>=17 and current_datetime.hour<=24:
            if status=="open":greeting="Good Evening"
            else:greeting="Have a Wonderful Evening"    
        if status=="open":text = f"Hi {user}. {greeting}."
        else:text = f"Goodbye {user}. {greeting}."
    elif Language.get()=="Spanish":            
        if current_datetime.hour<12:
            if status=="open":greeting="Buenos Días"
            else:greeting="Que Tengas una Mañana Maravillosa"    
        elif current_datetime.hour>=12 and current_datetime.hour<17:
            if status=="open":greeting="Buenas Tardes"
            else:greeting="Que Ttengas una Maravillosa Tarde"    
        elif current_datetime.hour>=17 and current_datetime.hour<=24:
            if status=="open":greeting="Buenas Noches"
            else:greeting="Que Tengas una Noche Maravillosa"    
        if status=="open":text = f"Hola {user}. {greeting}."
        else:text = f"Adiós {user}. {greeting}."
    return text    
def display_popup(display_txt):
    try:# popup menu item Copy Total Display Text To Clip-Board
        text_wid_pixels = copy_font.measure(display_txt)
        display_wid=Display_Text.winfo_width()
        display_center_x=display_wid/2
        text_center_x=display_center_x-(text_wid_pixels/2)
        x=abs(text_center_x/display_wid)
        display_hgt=Display_Text.winfo_height()
        display_center_y=(display_hgt/2)
        y=abs(((display_center_y*display_hgt)/root_height)/100)
        popup_msg=Label(root, text=display_txt,background="#33FFFF", 
            foreground='#000000',font=copy_font,anchor='c')
        popup_msg.place(relx=x, rely=y)
        root.after(3000,popup_msg.destroy)
        root.update()
        root.update_idletasks()
    except Exception as e:
        pass
def menu_popup2(event):# display the popup menu
    btn=event.widget['text']
    trig_btns=['sin','cos','tan','sec','csc','cot','asin','acos','atan','asec','acsc','acot','sinh',
                'cosh','tanh','sech','csch','coth','asinh','acosh','atanh','asech','acsch','acoth']
    if event.type=='4': #<EventType.ButtonPress: '4'>
        if Language.get()=="English":
            en_functions=['Sine','Cosine','Tangent','Secant','Cosecant','Cotangent','ArcSine','ArcCosine',
                            'ArcTangent','ArcSecant','ArcCoscant','ArcCotangent','Hyperbolic Sine','Hyperbolic Cosine',
                            'Hyperbolic Tangent','Hyperbolic Secant','Hyperbolic Cosecant','Hyperbolic Cotangent',
                            'Inverse Hyperbolic Sine','Inverse Hyperbolic Cosine','Inverse Hyperbolic Tangent',
                            'Inverse Hyperbolic Secant','Inverse Hyperbolic Cosecant','Inverse Hyperbolic Cotangent']
            if btn in trig_btns:
                for i, item in enumerate(trig_btns):
                    if btn==item:
                        text=f"Trigonometry {en_functions[i]} Function. Enter Value First Then Click Me."
                        break
            elif btn=="Hyp":text="Trigonometry Hypotenuse Function."
            elif btn=="Arc":text="Trigonometry Inverse Function."
            elif btn=='C':text='Clear Display And Memories. Sets To Default'
            elif btn=='CE':text='Clear Last Entry If Numeric and Base 10.'
            elif btn=='n!':text='Factorial of Positive Natural Number n.'
            elif btn=='𝜯':text='Constant tau (𝜯 = 2*π.'
            elif btn=='𝑮':text="Catalan's Constant (𝑮)."
            elif btn=='𝓔':text="Euler's Constant (𝓔)." 
            elif btn=='π':text="Constant PI (π)." 
            elif btn=='𝜁3':text="Apery's Constant (𝜁3)."
            elif btn=='𝒆':text='Natural Logarithm Base (𝒆).'
            elif btn=='𝜱':text='Golden Ratio (𝜱).'
            elif btn=='𝑲':text="Khinchin's Constant (𝑲)."
            elif btn=='𝑨':text="Glaisher's Constant (𝑨)."
            elif btn=='𝑴':text="Meissel-Mertens Constant (𝑴)."
            elif btn=='Π₂':text="Twin Prime Constant (Π₂)."
            elif btn=='ʸ√':text="Any Root. Enter Value First Then Click Me. Then Enter Root (y) Value."
            elif btn=='²√':text="Square Root. Enter Value First Then Click Me."
            elif btn=='³√':text="Cubed Root. Enter Value First Then Click Me."
            elif btn=='1/𝓧':text="Reciprocal. Enter 𝓧 Value First Then Click Me."
            elif btn=='𝓧ʸ':text="To Any Power. Enter 𝓧 Value First Then Click Me. Then Enter Power (y) Value."
            elif btn=='𝓧³':text="X Cubed. Enter 𝓧 Value First Then Click Me."
            elif btn=='𝓧²':text="X Squared. Enter 𝓧 Value First Then Click Me."
            elif btn=='%':text="Percentage. Enter Value First Then Click Me."
            elif btn=='mod':text="Modulo Returns Division Remainder. Enter Numerator Then Click Me."
            elif btn=='exp':text="Changes Last Numeric Value To Scientific Notation."
            elif btn=='CM':text="Clear All Memories."
            elif btn=='ms1':text="Memory Set 1."
            elif btn=='ms2':text="Memory Set 2."
            elif btn=='ms3':text="Memory Set 3."
            elif btn=='ms4':text="Memory Set 4."
            elif btn=='mr1':text="Memory Recall 1."
            elif btn=='mr2':text="Memory Recall 2."
            elif btn=='mr3':text="Memory Recall 3."
            elif btn=='mr4':text="Memory Recall 4."
            elif btn=='log𝒆':text="Logarithm To The Natural Logarithm Base. Enter Value First Then Click Me."
            elif btn=='log10':text="Logarithm To The Base 10. Enter Value First Then Click Me."
            elif btn=='log(x,b)':text="Logarithm To Any Base. Enter 𝓧 Value First Then Click Me. Then Enter Base."
            elif btn=='A : B':text="Calculate Ratios And Porportions."
            elif btn=='∫':text="Integrate Expression. An Expression Must Be Present To Integrate."
            elif btn=='f´(𝓧)':text="Differentiate Expression. An Expression Must Be Present To Differentiate."
            elif btn=='°F→°C':text="Converts Degrees Fahrenheit To Degrees Celsius."
            elif btn=='°C→°F':text="Converts Degrees Celsius To Degrees Fahrenheit."
        else:    
            es_functions=['Seno','Coseno','Tangente','Secante','Cosecante','Cotangente','ArcoSeno','ArcoCoseno','ArcoTangente',
                        'ArcoSecante','ArcoCosecante','ArcoCotangente','Seno Hiperbólico','Coseno Hiperbólico',
                        'Tangente Hiperbólica','Secante Hiperbólica','Cosecante Hiperbólica','Cotangente Hiperbólica',
                        'Seno Hiperbólico Inverso','Coseno Hiperbólico Inverso','Tangente Hiperbólica Inversa',
                        'Secante Hiperbólica Inversa','Cosecante Hiperbólica Inversa','Cotangente Hiperbólica Inversa']
            if btn in trig_btns:
                for i, item in enumerate(trig_btns):
                    if btn==item:
                        text=f"Función {es_functions[i]} de Trigonometría. Primero Ingrese un Valor y Luego Haga Clic en Mí."
                        break
            elif btn=="Hyp":text="Función de la Hipotenusa en Trigonometría."
            elif btn=="Arc":text="Función Inversa de Trigonometría."
            elif btn=='C':text='Pantalla Clara y Memorias. Restablecer a Valores Predeterminados'
            elif btn=='CE':text='Borrar la última Entrada si es Numérica y en Base 10.'
            elif btn=='n!':text='Factorial de un Número Natural Positivo n.'
            elif btn=='𝜯':text='Constante tau (𝜯 = 2*π.'
            elif btn=='𝑮':text="Constante de Catalan (𝑮)."
            elif btn=='𝓔':text="Constante de Euler (𝓔)." 
            elif btn=='π':text='Constante PI (π).' 
            elif btn=='𝜁3':text="Constante de Apery (𝜁3)."
            elif btn=='𝒆':text='Base del Logaritmo Natural (𝒆).'
            elif btn=='𝜱':text='Proporción Áurea (𝜱).'
            elif btn=='𝑲':text="Constante de Khinchin (𝑲)."
            elif btn=='𝑨':text="Constante de Glaisher (𝑨)."
            elif btn=='𝑴':text="Constante de Meissel-Mertens (𝑴)."
            elif btn=='Π₂':text="Constante de los Primos Gemelos (Π₂)."
            elif btn=='ʸ√':text="Cualquier Raíz. Ingrese un Valor Primero y Luego Haga Clic en Mí. Luego Ingrese el Valor Raíz (y)."
            elif btn=='²√':text="Raíz cuadrada. Ingrese un Valor Primero y Luego Haga Clic en Mí."
            elif btn=='³√':text="Raíz Cúbica. Ingrese un Valor Primero y Luego Haga Clic en Mí."
            elif btn=='1/𝓧':text="Recíproco. Ingrese Primero el Valor de 𝓧 y Luego Haga Clic en Mí."
            elif btn=='𝓧ʸ':text="A Cualquier Poder. Ingrese Primero el Valor de 𝓧 y Luego Haga Clic en Mí. Luego Ingrese el Valor de Potencia (y)."
            elif btn=='𝓧³':text="X al Cubo. Ingrese Primero el Valor de 𝓧 y Luego Haga Clic en Mí."
            elif btn=='𝓧²':text="X al Cuadrado. Ingrese Primero el Valor de 𝓧 y Luego Haga Clic en Mí."
            elif btn=='%':text="Porcentaje. Ingrese un Valor Primero y Luego Haga Clic en Mí."
            elif btn=='mod':text="Módulo Devuelve el Resto de la División. Ingresa el Numerador y Luego Haz Clic en Mí."
            elif btn=='exp':text="Cambia el último Valor Numérico a Notación Científica."
            elif btn=='CM':text="Borrar Todos los Recuerdos."
            elif btn=='ms1':text="Conjunto de Memoria 1."
            elif btn=='ms2':text="Conjunto de Memoria 2."
            elif btn=='ms3':text="Conjunto de Memoria 3."
            elif btn=='ms4':text="Conjunto de Memoria 4."
            elif btn=='mr1':text="Recuerdo de Memoria 1."
            elif btn=='mr2':text="Recuerdo de Memoria 2."
            elif btn=='mr3':text="Recuerdo de Memoria 3."
            elif btn=='mr4':text="Recuerdo de Memoria 4."
            elif btn=='log𝒆':text="Logaritmo a la Base del Logaritmo Natural. Ingrese un Valor Primero y Luego Haga Clic en Mí."
            elif btn=='log10':text="Logaritmo en Base 10. Ingrese un Valor Primero y Luego Haga Clic en Mí."
            elif btn=='log(x,b)':text="Logaritmo a Cualquier Base. Primero Ingresa el Valor 𝓧 y Luego Haz Clic en Mí. Luego Ingresa la Base."
            elif btn=='A : B':text="Calcular Razones y Proporciones."
            elif btn=='∫':text="Integrar Expresión. Debe Estar Ppresente una Expresión para Integrar."
            elif btn=='f´(𝓧)':text="Diferenciar Expresión. Debe Estar Presente una Eexpresión para Diferenciar."
            elif btn=='°F→°C':text="Convierte Grados Fahrenheit a Grados Celsius."
            elif btn=='°C→°F':text="Convierte Grados Celsius a Grados Fahrenheit."
        display_popup(text)
def clear_all():
    Display.set('')
    Display_Text.delete('1.0','end')
    Math_Function.set('')
    Last_Function.set('')
    Disp_List.clear() 
    Disp_Bkts_Open.set(0)
    Temp_Disp_Open.set(0)
    Temp_Expr_Open.set(0)
    Reversed_List.clear()
    Expression.set('')
    Expr_List.clear()
    Expressions_Used.clear()  
    Expr_Bkts_Open.set(0)  
    bracket_clicked('auto','both','clear')
    Answer.set('')
    Answer_Present.set(False)
    Answer_Err.set(False)
    disp_update('clear') 
    expr_update('clear')
    free_sys_symbols()
def set_defaults():
    if not os.path.exists("Config.json"):
        mp.dps=50
        Round.set(10)
        Exp_Precision.set(20)
        Exp_Digits.set(4)
        Bit_Size.set(128)
        Display_fg.set("#ffffff")
        Display_bg.set("#0c012e")
        NewFont.set("{'family': 'Times New Roman', 'size': 16, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}")
        data={}
        with open("Config.json", "w") as json_file:# Create Empty json File
                json.dump(data, json_file, indent=4) # indent=4 for pretty-printing
                json_file.close()
        write_setup()
        root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_x, root_y, ))
    else:
        read_setup()    
    mp.pretty=True
    Hyp.set(False)  
    Arc.set(False)
    config_base('Decimal')     
    config_trig('Degrees')
    clear_all()
    root.deiconify()
    root.update()
def copy_to_clipboard(parent, widget, which, event:tk.Event=None) -> str:
    # Widget Has To Be A Text Object
    try:# Ctrl+c Copy Selected Display Text To Clip-Board
        if which=="selected":
            text=widget.selection_get()
            if Language.get()=="English":txt=" Selected Text Copied To Clipboard! "
            else:txt="¡Texto Seleccionado Copiado al Portapapeles!"
        elif which=="all":
            text=widget.get("1.0", tk.END)
            if text=="\n":text=""
            if Language.get()=="English":txt=" Display Text Copied To Clipboard! "
            else:txt=" ¡Texto Mostrado Copiado al Portapapeles! "
        if text!="":
            pyperclip.copy(text)
            clipboard_msg=Label(parent, text=txt,background="#33FFFF", 
                foreground='#000000',font=copy_font,anchor='c')
            clipboard_msg.place(relx=0.022, rely=0.1, relwidth=0.93)
            root.after(3000, clipboard_msg.destroy)
    except Exception as e:
        pass
def calculate_font_sizes():
    base_font_sizes = [10, 9, 14, 12, 14, 20, 10]
    new_font_sizes=[]
    scaling_factor = min(root.winfo_screenwidth() / 1280, root.winfo_screenheight() / 800)  # Scale relative to 1280x800  
    for s in range(len(base_font_sizes)):
        size=int(base_font_sizes[s] * scaling_factor)
        new_font_sizes.append(size)
    return new_font_sizes
def my_askstring(title, prompt, init_val=None):
    d=My_StringDialog(title, prompt , init_val)
    answer=d.result
    root.update_idletasks()
    return answer  
def my_askstring(title, prompt, init_val=None):
    d=My_StringDialog(title, prompt , init_val)
    answer=d.result
    root.update_idletasks()
    return answer  
class My_StringDialog(tk.simpledialog._QueryString):
    def body(self, master):# initialvalue May Be List, String Or None
        self.attributes("-toolwindow", True)# Remove Min/Max Buttons
        self.bind('<KP_Enter>', self.ok)
        self.bind('<Return>', self.ok)
        pt=tk.Label(master, text=self.prompt, justify="left", font=root.font)
        pad=int((pt.winfo_reqwidth()/2)/2)
        pt.grid(row=2, padx=(5,5),pady=(5,5), sticky= 'we')
        if self.initialvalue is not None:
            wid=len(self.initialvalue)+4
            if type(self.initialvalue)==list:# List
                for item in self.initialvalue:
                    w=len(item)
                    if w>wid:wid=w
                self.entry=ttk.Combobox(master, name="entry", state = "readonly",justify="center",width=wid,font=root.font)
                self.entry['values']=self.initialvalue
                self.entry.current(0)
            else:# String
                self.entry=tk.Entry(master, name="entry", justify='center', bg="#d6ffff",width=wid, font=root.font)
                self.entry.insert(0, self.initialvalue)
                self.entry.select_range(0, 'end')
        else:# None
            self.entry=tk.Entry(master, name="entry", justify='center', bg="#d6ffff", font=root.font)
            self.entry.insert(0, "")
            self.entry.select_range(0, 'end')
        self.entry.grid(row=3, padx=(pad,pad), sticky='we')
        self.entry.bind('<Map>', self.on_map)
        root.update_idletasks()
        return self.entry
    def on_map(self, event):
        self.entry.focus_force()    
def restart_program():
    if Language.get()=="English":display_popup("Restarting Program!")
    else:display_popup("¡Reiniciando el Programa!")
    time.sleep(1)
    try:
        write_setup()
        clear_memories()
        clear_all()
        Symbol_Names.clear()
        Symbol_Values.clear()
        _MyClash.clear()
        _MyConstants.clear()
        Operators.clear()
    except:
        pass
    if os.path.exists('Config.json'):
        Language.set("")
        write_setup()
    try:
        for widget in root.winfo_children():# Destroys Menu Bars, Frame, Canvas And Scroll Bars
            if isinstance(widget, tk.Canvas):widget.destroy()
            else:widget.destroy()
        os.execl(sys.executable, os.path.abspath("pySci_Calculator.exe"), *sys.argv) 
    except:
        pass
        os.execl(sys.executable, os.path.abspath("pySci_Calculator.exe"), *sys.argv)
if __name__ == "__main__":
    root=Tk()
    root.configure(bg='#000000')
    root.font=font.Font(family='Lucida Sans', size=10, weight='normal', slant='italic')
    copy_font=font.Font(family='Lucida Sans', size=12, weight='normal', slant='roman')
    Language=tk.StringVar()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    languages=["English","Spanish"]
    title="Select Language / Seleccionar Idioma"
    msg1="Please Select The Desired Program Language.\n"
    msg2="Por favor, Seleccione el Idioma del Programa Deseado."
    msg=msg1+msg2
    languages=["English","Spanish"]
    if not os.path.exists("Config.json"):
        while Language.get()=="": 
            lang=my_askstring(title, msg, languages)
            if lang=="" or lang==None:Language.set("")
            else:Language.set(lang)
        root_width = screen_width*0.6
        root_height = screen_height*0.5
        root_x = (screen_width // 2) - (root_width // 2)
        root_y = (screen_height // 2) - (root_height // 2)
    else:
        try:
            with open('Config.json', 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
            if data["0"]=="":
                while Language.get()=="": 
                    lang=my_askstring(title, msg, languages)
                    if lang=="" or lang==None:Language.set("")
                    else:Language.set(lang)
                temp_dict={}
                temp_dict[0]=Language.get()
                with open("Config.json", "w") as json_file:
                    data["0"] = Language.get()
                    json.dump(data, json_file)
                    json_file.close()
            else:Language.set(data["0"])        
            root_width=int(data["9"])
            root_height=int(data["10"])
            root_x=int(data["11"])
            root_y=int(data["12"])
        except Exception as e:
            Language.set("English")
            root_width = screen_width*0.55
            root_height = screen_height*0.5
            root_x = (screen_width // 2) - (root_width // 2)
            root_y = (screen_height // 2) - (root_height // 2)
            pass
    dir=Path(__file__).parent.absolute()
    filename='pycal.ico' # Program icon
    ico_path=os.path.join(dir, filename)
    root.iconbitmap(default=ico_path) # root and children
    user=os.getlogin()
    if Language.get()=="English":txt=[f"{user}'s Calculator: ","Right Click Display For Options"]
    else:txt=[f"{user}'s Calculadora: ","Haga Clic Derecho en la Pantalla para Opciones"]
    root_title=txt[0]
    options=txt[1]
    root.title(root_title + options.rjust(40+len(options)))
    sizes = calculate_font_sizes()# Get Font Sizes Depending On Monitor Resolution
    display_font=font.Font(family='Lucida Sans', size=sizes[0], weight='normal', slant='italic')# Display Only
    units_font=font.Font(family='lucidas', size=sizes[1], weight='bold', slant='roman')# Bases, Trig 
    bracket_font=font.Font(family='lucidas', size=sizes[2], weight='normal', slant='roman')# () Only
    memory_font=font.Font(family='lucidas', size=sizes[3], weight='bold', slant='italic')# Memory,Ratio,mod,exp
    symbols_font=font.Font(family='lucidas', size=sizes[4], weight='normal', slant='italic')# Numeric,math symbols,CM
    operator_font=font.Font(family='lucidas', size=sizes[5], weight='normal', slant='roman')# Math Operators,sign
    temp_font=font.Font(family='lucidas', size=sizes[6], weight='bold', slant='italic')# F-C, C-F
    root.configure(bg='#14fafa')
    root.resizable(True,True)
    root.option_add('*TCombobox*Listbox.font', units_font)
    root.protocol("WM_DELETE_WINDOW", calculator_destroy)
    # Bind Keyboard Keys
    root.bind("<Return>", equal_clicked)
    root.bind("<BackSpace>", clear_entry)
    for i in range(10):
        root.bind(str(i), numeric_clicked)
    root.bind("<period>", numeric_clicked)
    Hex_List=['a','A','b','B','c','C','d','D','e','E','f','F']
    for i, item in enumerate(Hex_List):
        root.bind(str(item), numeric_clicked)
    Operators2=['/','*','-','+'] # Bind Keyboard Operator Keys
    for i, item in enumerate(Operators2):
        root.bind(str(item), operator_clicked)
    root.bind("(", lambda event, a='manual', b='both', c='open':bracket_clicked(a,b,c))
    root.bind(")", lambda event, a='manual', b='both', c='close':bracket_clicked(a,b,c))
    # ****Variables And Widgets****
    Display=StringVar()# Text Shown On Display (Advancing Display Update)
    Display.set('')
    Disp_List=[]# Final Display Not Shown
    Reversed_List=[] # Display Or Expression List Reversed
    Disp_Bkts_Open=IntVar()# Number Of Display Brackets Open
    Temp_Disp_Open=IntVar()# Used To Highlight Total Display Function.
    Expression=StringVar()# Advancing Expression Update
    Expr_List=[]# Final Expression Sent To Parser
    Expressions_Used=[]
    Symbol_Names=[]
    Symbol_Values=[]
    Symbols_Used=[]
    sub_dict={}
    Expr_Bkts_Open=IntVar()# Number Of Expression Brackets Open
    Temp_Expr_Open=IntVar()# Used To Highlight Total Expression Function. 
    Math_Function=StringVar()
    Last_Function=StringVar()
    D_Memory1=[]
    D_Memory2=[]
    D_Memory3=[]
    D_Memory4=[]
    E_Memory1=[]
    E_Memory2=[]
    E_Memory3=[]
    E_Memory4=[]
    Exp_Precision=IntVar()
    Round=IntVar()
    Exp_Digits=IntVar()
    Bit_Size=IntVar()
    NewFont=StringVar()
    NewFont_Size=IntVar()
    Last_Display=[]
    Answer=StringVar()# Parsed Answer
    Answer_Err=BooleanVar()
    Answer_Present=BooleanVar()# Answer Received And Present
    Engine_Init=BooleanVar()
    Normal_Script="0123456789"
    Super_Script="⁰¹²³⁴⁵⁶⁷⁸⁹"
    Sub_Script="₀₁₂₃₄₅₆₇₈₉"
    _MyClash=['pi','beta','gamma','zeta','radian','C','O','Q','N','I','E','S']
    _MyConstants=['𝓔','𝑮','𝜱','𝜯','𝑲','𝑨','𝑴','π','𝒆','𝜁3','Π₂','Π','rad_to_deg','rad_to_grad','arc_rad_to_deg','arc_rad_to_grad']
    ####### Widgets #######
    Display_bg=StringVar()
    Display_fg=StringVar()
    Display_bg.set('#0c012e')
    Display_fg.set('#ffffff')
    Display_Text=ScrolledText(root, bg=Display_bg.get(), fg=Display_fg.get(), font=display_font, 
            borderwidth=5, relief="sunken")
    Display_Text.place(relx=0.015, rely=0.01, relwidth=0.97, relheight=0.16)
    Display_Text.bind("<Control-c>", lambda event:copy_to_clipboard(root, Display_Text, "selected", event)) 
    Display_Text.delete('1.0','end')
    Unbound_Keys='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&{[}]|:;",?~`'
    for i, item in enumerate(Unbound_Keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
        if item in Unbound_Keys:
            Display_Text.bind(str(item), lambda e: "break")
    if Language.get()=="English":
        txt=['Calculator Precision',"Round Answer","Scientific Notation Precision","Exponential Notation Precision","Binary Bit Size (8, 16, 32, 64, 128, 256, 512)",
             "Display Font","Display Font Color","Display Background Color","Copy Display Text To Clipboard","Change Language","About My Calculator"]
    else:
        txt=['Precisión de la Calculadora','Redondear Respuesta','Precisión en Notación Científica','Precisión en Notación Exponencial','Tamaño de Bit Binario (8, 16, 32, 64, 128, 256, 512)',
             'Fuente de Visualización','Color de Fuente','Color de Fondo','Copiar Texto de la Pantalla al Portapapeles','Cambiar idioma','Acerca de Mi Calculadora']

    popup=Menu(Display_Text, tearoff=0, font=root.font) # PopUp Menu
    popup.add_command(label=txt[0], background='aqua', command=lambda:precision('dp'))
    popup.add_command(label=txt[1], background='aqua', command=lambda:precision('round'))
    popup.add_command(label=txt[2], background='aqua', command=lambda:precision('exp'))
    popup.add_command(label=txt[3], background='aqua', command=lambda:precision('exp_digits'))
    popup.add_command(label=txt[4], background='aqua', command=lambda:precision('bit_size'))
    popup.add_command(label=txt[5], background='aqua', command=lambda:choose_font())
    popup.add_command(label=txt[6], background='aqua', command=lambda:choose_color('fg'))
    popup.add_command(label=txt[7], background='aqua', command=lambda:choose_color('bg'))
    popup.add_command(label=txt[8], background='aqua', command=lambda:copy_to_clipboard(root,Display_Text,"all")) 
    popup.add_command(label=txt[9], background='aqua', command=lambda:restart_program())
    popup.add_command(label=txt[10], background='aqua', command=lambda:about())
    Display_Text.bind("<Button-3>", menu_popup)
    base_btn=[] 
    Base=StringVar()
    if Language.get()=="English":text=['Binary','Decimal','Hexadecimal','Octal']
    else:text=['Binario','Decimal','Hexadecimal','Octal']
    wid=[0.19,0.21,0.32,0.17]
    x=[0.02,0.23,0.46,0.8]
    hgt=0.82
    y=0.09
    base_frame=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Base Buttons
    base_frame.place(relx=0.015, rely=0.19, relwidth=0.479, relheight=0.095)
    for num in range(0,len(text)):
        base_btn.append([num])
        base_btn[num]=tk.Button(base_frame, text=text[num], background='navy', foreground = '#ffffff', # Base Buttons
            borderwidth=5, relief="raised", font=units_font)
        base_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        base_btn[num].bind("<Button-1>", base_clicked)
    unit_btn=[]
    Trig_Units=StringVar()
    if Language.get()=="English":
        text=['Degrees','Radians','Gradians']
    else:
        text=['Grados','Radianes','Gradianos']
    wid=[0.29,0.29,0.29,0.294]
    x=[0.03,0.35,0.67]
    y=0.09
    hgt=0.82            
    unit_frame=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Trig Units Buttons
    unit_frame.place(relx=0.506, rely=0.19, relwidth=0.36, relheight=0.095)
    for num in range(0,len(text)):
        unit_btn.append([num])
        unit_btn[num]=tk.Button(unit_frame, text=text[num], background="green", foreground = '#ffffff', # Trig Units Buttons
            borderwidth=5, relief="raised", font=units_font)
        unit_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        unit_btn[num].bind("<Button-1>", trig_unit_clicked)
    clrmem_btn=tk.Button(root, text='CM', background="#ffff99", foreground = 'maroon', # Clear Memory Button
            borderwidth=5, relief="raised", font=symbols_font, command=lambda:clear_memories())
    clrmem_btn.place(relx=0.886, rely=0.19, relwidth=0.085, relheight=0.095)
    popup2=Menu(clrmem_btn, tearoff=0)
    clrmem_btn.bind("<Button-3>", menu_popup2)
    pad_fra=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Key Pad
    pad_fra.place(relx=0.015, rely=0.3, relwidth=0.97, relheight=0.68)    
    num_btn=[]
    y,x1,x2=0.015,0.01,0.098
    for num in range(0,10):# Numbers 0 - 9
        num_btn.append([num])
        if (num % 2)==0:x=x1# Even 
        else:x=x2 
        num_btn[num]=tk.Button(pad_fra, text=num, bg='navy', fg = '#ffffff', # Number Buttons
            activebackground='#ffffff', borderwidth=5, relief="raised", font=symbols_font)
        num_btn[num].place(relx=x, rely=y, relwidth=0.08, relheight=0.12)
        num_btn[num].bind("<Button-1>", numeric_clicked) # Bind all the number keys with the callback function
        if (num % 2)!=0:y+=0.14# Odd
    x=[0.01,0.1,0.19,0.28,0.39,0.5]
    wid=[0.08,0.08,0.08,0.1,0.1,0.1]    
    text=['A','B','C','D','E','F'] # Hex Numbers A - F
    for num in range(10,16):
        num_btn.append([num])
        num_btn[num]=tk.Button(pad_fra, text=text[num-10], background='navy', foreground = '#ffffff', # Hex Buttons
            borderwidth=5, relief="raised", font=symbols_font)
        num_btn[num].place(relx=x[num-10], rely=y, relwidth=wid[num-10], relheight=0.12)
        num_btn[num].bind("<Button-1>", numeric_clicked)
    operator_btn=[]
    x=0.19
    y=0.015
    wid=0.08
    hgt=0.12
    Operators=[' / ',' * ',' - ',' + '] # Math Operators
    for num in range(0,len(Operators)):
        operator_btn.append([num])
        operator_btn[num]=tk.Button(pad_fra, text=Operators[num], background="whitesmoke", foreground = 'navy',
            activebackground='#ffe599', borderwidth=5, relief="raised", font=operator_font)
        operator_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        operator_btn[num].bind("<Button-1>", operator_clicked)
        y+=0.14
    equal_btn=tk.Button(pad_fra, text=' = ', background="#14fafa", foreground = 'navy', # Equal Button
        borderwidth=5, relief="raised", font=operator_font)
    equal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    equal_btn.bind("<Button-1>", equal_clicked)
    Logs,log_btn=[],[]
    text=['log𝒆','log10','log(x,b)']
    x=0.28
    y=0.015
    wid=0.1
    hgt=0.12
    for num in range(0,len(text)):
        Logs.append(StringVar(master=None))
        log_btn.append([num])
        log_btn[num]=tk.Button(pad_fra, text=text[num], background="purple", foreground = 'whitesmoke', # Log Buttons
            borderwidth=5, relief="raised", font=units_font)
        log_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        log_btn[num].bind("<Button-1>", log_clicked)
        log_btn[num].bind("<Button-3>", menu_popup2)
        Logs[num].set(num)
        y+=0.14
    sign_btn=tk.Button(pad_fra, text=chr(177), background='navy', foreground = 'whitesmoke', # Sign (Plus Or Minus) 
            borderwidth=5, relief="raised", font=operator_font)
    sign_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    sign_btn.bind("<Button-1>", sign_clicked)
    y+=0.14
    decimal_btn=tk.Button(pad_fra, text=chr(46), background='navy', foreground = 'whitesmoke', # Decimal Point 
            borderwidth=5, relief="raised", font=operator_font)
    decimal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    decimal_btn.bind("<Button-1>", numeric_clicked)
    y+=0.14
    Trig,trig_btn=[],[]
    odd_list=['sec','csc','cot']
    text=['sin','sec','cos','csc','tan','cot']
    x1=0.39
    x2=0.5
    y=0.015
    wid=0.1
    hgt=0.12
    for num in range(0,len(text)):
        Trig.append(StringVar(master=None))
        trig_btn.append([num])
        if text[num] in odd_list:x=x2
        else:x=x1
        trig_btn[num]=tk.Button(pad_fra, text=text[num], background="green", foreground = 'whitesmoke', # Trig Buttons
            borderwidth=5, relief="raised", font=units_font)
        trig_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        trig_btn[num].bind("<Button-1>", trig_clicked)
        trig_btn[num].bind("<Button-3>", menu_popup2)
        Trig[num].set(num)
        if text[num] in odd_list:y+=0.14
    odd_list.clear()    
    Arc=BooleanVar()
    arc_btn=tk.Button(pad_fra, text='Arc', background="green", foreground = 'whitesmoke', # Trig Arc Button
        borderwidth=5, relief="raised", font=units_font)
    arc_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
    arc_btn.bind("<Button-1>", config_trig_btns)
    arc_btn.bind("<Button-3>", menu_popup2)
    Hyp=BooleanVar()
    hyp_btn=tk.Button(pad_fra, text='Hyp', background="green", foreground = 'whitesmoke', # Trig Hyp Button
        borderwidth=5, relief="raised", font=units_font)
    hyp_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
    hyp_btn.bind("<Button-1>", config_trig_btns)
    hyp_btn.bind("<Button-3>", menu_popup2)
    x1=0.39
    x2=0.5
    y+=0.14
    open_btn=tk.Button(pad_fra, text='('+chr(8304), background='whitesmoke', foreground = 'black', # Parenthesis Open Button
        activebackground='#ffe599', borderwidth=5, relief="raised", font=bracket_font)
    open_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
    open_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='open':bracket_clicked(a,b,c))
    closed_btn=tk.Button(pad_fra, text=')', background='whitesmoke', foreground = 'black',  # Parenthesis Close Button
        activebackground='#ffe599', borderwidth=5, relief="raised", font=bracket_font)
    closed_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
    closed_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='close':bracket_clicked(a,b,c))
    x=0.61
    y=0.015
    wid=0.08
    hgt=0.12
    func_btn=[]
    text=['1/𝓧','𝓧ʸ','𝓧³','𝓧²','n!','𝜯','𝑮']
    for num in range(0,len(text)): # Function Buttons Column 1
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[num], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
    func_btn[0].config(font=font.Font(family='lucidas', size=12, weight='normal', slant='italic'))
    clr=tk.Button(pad_fra, text='C', background="whitesmoke", foreground = 'black', # Clear Button
            activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font, command=lambda:clear_all())
    clr.place(relx=0.7, rely=0.015, relwidth=0.09, relheight=0.12)
    popup2=Menu(clr, tearoff=0)
    clr.bind("<Button-3>", menu_popup2)
    x=0.7
    y=0.155
    wid=0.09
    hgt=0.12
    text=['ʸ√','³√','²√','𝓔','π','𝜁3']
    i=0
    for num in range(6,12): # Function Buttons Column 2
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>",lambda event:menu_popup2(event))
        y+=0.14
        i+=1
    func_btn[6]['font']=symbols_font
    ce=tk.Button(pad_fra, text='CE', background="whitesmoke", foreground = 'black', # Clear Entry Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
    ce.place(relx=0.8, rely=0.015, relwidth=0.09, relheight=0.12)
    popup2=Menu(ce, tearoff=0)
    ce.bind("<Button-1>", clear_entry)
    ce.bind("<Button-3>", menu_popup2)
    x=0.8
    y=0.155
    wid=0.09
    hgt=0.12
    text=['%','𝑴','Π₂','𝒆','𝜱','𝑲','𝑨']
    i=0
    for num in range(12,18): # Function Buttons Column 3
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
        i+=1
    func_btn[15]['font'] = bracket_font       
    x=0.9
    y-=0.14
    func_btn.append([num])
    func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
    func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    func_btn[num].bind("<Button-1>", funct_clicked)
    popup2=Menu(func_btn[num], tearoff=0)
    func_btn[num].bind("<Button-3>", menu_popup2)
    mem_btn=[]
    x=0.9
    y=0.015
    wid=0.09
    hgt=0.12
    text=['ms1','ms2','ms3','ms4']
    for num in range(0,len(text)): 
        mem_btn.append([num])
        mem_btn[num]=tk.Button(pad_fra, text=text[num], background="#ffff99", foreground = 'maroon', # Memory Buttons 
                borderwidth=5, relief="raised", font=memory_font)
        mem_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        mem_btn[num].bind("<Button-1>", memory_clicked)
        popup2=Menu(mem_btn[num], tearoff=0)
        mem_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
    mod_btn=tk.Button(pad_fra, text='mod', background="whitesmoke", foreground = 'black', # Modulo Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=memory_font)
    mod_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    mod_btn.bind("<Button-1>", funct_clicked)
    popup2=Menu(mod_btn, tearoff=0)
    mod_btn.bind("<Button-3>", menu_popup2)
    y+=0.14
    exp_btn=tk.Button(pad_fra, text='exp', background="whitesmoke", foreground = 'black', # EXP Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=memory_font)
    exp_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    exp_btn.bind("<Button-1>", funct_clicked)
    popup2=Menu(exp_btn, tearoff=0)
    exp_btn.bind("<Button-3>", menu_popup2)
    ftoc_btn=tk.Button(pad_fra, text='°F→°C', background='#ff9c95', foreground = 'black', # °F→°C Button
        borderwidth=5, relief="raised", font=temp_font)
    ftoc_btn.place(relx=0.01, rely=0.855, relwidth=0.117, relheight=0.12)
    ftoc_btn.bind("<Button-1>", temp_clicked)
    ftoc_btn.bind("<Button-3>", menu_popup2)
    ctof_btn=tk.Button(pad_fra, text='°C→°F', background='#ff9c95', foreground = 'black', # °C→°F Button
        borderwidth=5, relief="raised", font=temp_font)
    ctof_btn.place(relx=0.137, rely=0.855, relwidth=0.117, relheight=0.12)
    ctof_btn.bind("<Button-1>", temp_clicked)
    ctof_btn.bind("<Button-3>", menu_popup2)
    ratio_btn=tk.Button(pad_fra, text='A : B', background='whitesmoke', foreground = 'black', # Ratios
        activebackground='#ffe599', borderwidth=5, relief="raised", font=memory_font, command=lambda:do_ratios())
    ratio_btn.place(relx=0.264, rely=0.855, relwidth=0.117, relheight=0.12)
    ratio_btn.bind("<Button-3>", menu_popup2)
    integrate_btn=tk.Button(pad_fra, text='∫', background='whitesmoke', foreground = 'black', # Integration ∫
        activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font)
    integrate_btn.place(relx=0.39, rely=0.855, relwidth=0.1, relheight=0.12)
    integrate_btn.bind("<Button-1>", do_calculus)
    integrate_btn.bind("<Button-3>", menu_popup2)
    diff_btn=tk.Button(pad_fra, text="f´(𝓧)", background='whitesmoke', foreground = 'black',
        activebackground='#ffe599', borderwidth=5, relief="raised", font=symbols_font) # Differentiation
    diff_btn.place(relx=0.5, rely=0.855, relwidth=0.1, relheight=0.12)
    diff_btn.bind("<Button-1>", do_calculus)
    diff_btn.bind("<Button-3>", menu_popup2)
    text=[]
    set_defaults()
    txt=get_greeting("open")
    display_popup(txt)
    time.sleep(2)
    root.mainloop()

