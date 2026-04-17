import customtkinter as ctk
from CTkColorPicker import AskColor
from CTkListbox import *
from sympy import Integral, Derivative, Symbol, parse_expr, symbols
from mpmath import mp, mpf, nstr
from win32api import GetMonitorInfo, MonitorFromPoint
from pathlib import Path
from datetime import datetime
from re import compile
from typing import Literal
from PIL import Image
from time import sleep
from pyperclip import copy
from datetime import datetime
import ctypes
import os
import sys
import numpy as np
import json

class MyFontChooser(ctk.CTkToplevel):
    def __init__(self, parent, font_dict={}, text="Sample text for selected font", **kwargs):
        super().__init__(parent)
        self.withdraw()
        if os.path.exists("Font_Families.json"):# Windows Font Family Names are stored in json file. Not reliant on tk families.
            with open("Font_Families.json", 'r') as json_file:
                self.fonts = json.load(json_file)
                json_file.close()
            self.deiconify()
            self.font_dict=font_dict
            self.sample_txt = text
            self.after(300, self.wm_iconbitmap, parent.ico_path)
            if parent.Language.get()=="English":title=f"{parent.root_title}  Font Chooser"
            else:title=title=f"{parent.root_title}  Selector de Fuentes"
            self.title(title)
            primary_monitor=MonitorFromPoint((0, 0))
            monitor_info=GetMonitorInfo(primary_monitor)
            work_area=monitor_info.get("Work")
            self.screen_width=work_area[2]
            self.screen_height=(work_area[3])
            self.width = int(self.screen_width*0.3)
            self.height = int(self.screen_height*0.45)
            self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
            self.x = int(((self.screen_width // 2) - (self.width // 2)) / self.scale_factor)
            self.y = int(((self.screen_height // 2) - (self.height // 2)) / self.scale_factor)
            self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y))
            self.chooser_font = ctk.CTkFont(family="Arial", size=14, weight="normal", slant="roman")
            self.update()
            self.protocol("WM_DELETE_WINDOW", self.quit)
            self.new_font = ""#  (return value)
            try:
                self.sizes = ["%i" % i for i in (list(range(6, 17)) + list(range(18, 32, 2)))]
                max_length = int(max([len(font) for font in self.fonts]))
                fake_txt=["X" * max_length, "XXXX"]# Font Family ListBox Width And Font Weight ListBox
                req_width=[]
                for w in range(len(fake_txt)):
                    fake_lbl= ctk.CTkLabel(master=self, text=fake_txt[w], font=self.chooser_font)# Just To Get Required Width And Height
                    self.update()
                    req_width.append(w)
                    req_width[w]=fake_lbl.winfo_reqwidth() / self.scale_factor
                    req_height=(fake_lbl.winfo_reqheight() * 7)  / self.scale_factor# Show 7 Selections
                fake_lbl.destroy()
                self.font_dict["weight"] = self.font_dict.get("weight", "normal")
                self.font_dict["slant"] = self.font_dict.get("slant", "roman")
                self.font_dict["underline"] = self.font_dict.get("underline", False)
                self.font_dict["overstrike"] = self.font_dict.get("overstrike", False)
                self.font_dict["family"] = self.font_dict.get("family", self.fonts[0].replace(r'\ ', ' '))
                self.font_dict["size"] = self.font_dict.get("size", 10)
                # style parameters (bold, italic ...)
                if parent.Language.get()=="English":font_props=["Bold","Italic","Underline","Overstrike"]
                else:font_props=["Negrita","Cursiva","Subrayar","Sobreescribir"]
                options_frame=ctk.CTkFrame(self, fg_color='#99ffff', border_width=2, border_color="black", corner_radius=10) 
                self.font_size = ctk.StringVar(self, " ".join(self.sizes))
                self.var_bold = ctk.BooleanVar(self, self.font_dict["weight"] == "bold")
                b_bold = ctk.CTkCheckBox(options_frame, text=[font_props[0]], font=self.chooser_font, border_width=2, border_color=("black","black"),
                                        text_color=("#000080","#000080"), command=self.toggle_bold, variable=self.var_bold)
                b_bold.grid(row=0, sticky="w", padx=4, pady=(4, 2))
                self.var_italic = ctk.BooleanVar(self, self.font_dict["slant"] == "italic")
                b_italic = ctk.CTkCheckBox(options_frame, text=[font_props[1]], font=self.chooser_font, border_width=2, border_color=("black","black"), 
                                    text_color=("#000080","#000080"), command=self.toggle_italic, variable=self.var_italic)
                b_italic.grid(row=1, sticky="w", padx=4, pady=2)
                self.var_underline = ctk.BooleanVar(self, self.font_dict["underline"])
                b_underline = ctk.CTkCheckBox(options_frame, text=[font_props[2]], font=self.chooser_font, border_width=2, border_color=("black","black"),
                                        text_color=("#000080","#000080"), command=self.toggle_underline, variable=self.var_underline)
                b_underline.grid(row=2, sticky="w", padx=4, pady=2)
                self.var_overstrike = ctk.BooleanVar(self, self.font_dict["overstrike"])
                b_overstrike = ctk.CTkCheckBox(options_frame, text=[font_props[3]], font=self.chooser_font, border_width=2, border_color=("black","black"),
                                        text_color=("#000080","#000080"), variable=self.var_overstrike, command=self.toggle_overstrike)
                b_overstrike.grid(row=3, sticky="w", padx=4, pady=(2, 4))
                # Size and family
                self.var_size = ctk.StringVar(self)
                self.var_family= ctk.StringVar(self)
                self.entry_family = ctk.CTkEntry(self, placeholder_text="Enter Name", width=max_length, font=self.chooser_font, textvariable=self.var_family,
                                            corner_radius=10, state="normal")
                self.entry_size = ctk.CTkEntry(self, placeholder_text="Enter Size", width=5, font=self.chooser_font, textvariable=self.var_size, 
                                            corner_radius=10, state="normal")
                self.list_family = CTkListbox(self, height= req_height, width=req_width[0], font=self.chooser_font,
                                                fg_color="#99ffff", text_color="#000000", border_width=2, justify="left", hover_color="#ff8080", corner_radius=10)
                self.list_size = CTkListbox(self, height= req_height, width=req_width[1], font=self.chooser_font, fg_color="#99ffff", text_color="#000000",
                                    border_width=2, justify="left", hover_color="#ff8080", corner_radius=10)
                self.preview_font = ctk.CTkFont(self.font_dict["family"], self.font_dict["size"],self.font_dict["weight"],
                                                self.font_dict["slant"],self.font_dict["underline"],self.font_dict["overstrike"])
                preview_width = self.width - 20 # Prevent Label from expanding X, Wrap text 
                self.preview = ctk.CTkLabel(self, width=preview_width, wraplength=preview_width, text=self.sample_txt, font=self.preview_font, anchor="w",
                                            corner_radius=10, fg_color=parent.Display_bg.get(),text_color=parent.Display_fg.get())
                # Populate The Family And Size CTkListboxes 
                for f in range(0, len(self.fonts)):
                    self.list_family.insert(f, self.fonts[f])
                for s in range(0, len(self.sizes)):    
                    self.list_size.insert(s, self.sizes[s])
                # widget configuration
                self.entry_family.configure(state="normal")
                self.entry_size.configure(state="normal")
                self.entry_family.insert(0, self.font_dict["family"])
                self.entry_family.selection_clear()
                self.entry_family.icursor("end")
                self.entry_size.insert(0, self.font_dict["size"])
                self.entry_family.configure(state="readonly")
                self.entry_size.configure(state="readonly")
                try:
                    if self.entry_family.get() in self.fonts:
                        i = self.fonts.index(self.entry_family.get())
                    else: i=0     
                except ValueError:# unknown font
                    i = 0
                self.list_family.selection_clear()
                self.list_family.activate(i)
                self.list_family.see(i)
                try:
                    i = self.sizes.index(self.entry_size.get())
                    self.list_size.selection_clear()
                    self.list_size.activate(i)
                    self.list_size.see(i)
                except ValueError:# size not in list
                    pass
                self.entry_family.grid(row=0, column=0, sticky="ew", rowspan=1, pady=(10, 2), padx=(10, 0))
                self.entry_size.grid(row=0, column=1, sticky="ew", rowspan=1, pady=(10, 2), padx=(10, 0))
                pad_y2=int(req_height* 0.7)
                options_frame.grid(row=1, column=2, sticky="nsew", pady=(0, pad_y2), padx=(10, 0))
                self.list_family.grid(row=1, column=0, sticky="nsew", pady=(0, 0), padx=(10, 0))
                self.list_size.grid(row=1, column=1, sticky="nsew", pady=(0, 0), padx=(10, 0))
                self.preview.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=(10, 10), pady=(10, 10))
                button_frame=ctk.CTkFrame(self) 
                button_frame.grid(row=3, column=0, columnspan=5, padx=(0, 0), pady=(10, 0))
                self.ok_btn = ctk.CTkButton(button_frame, text="OK", border_width=2, corner_radius=5, font=self.chooser_font,
                                border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                                command=self.ok).grid(row=0, column=0, padx=(0, 20), sticky='ew')  
                self.cancel_btn = ctk.CTkButton(button_frame, text="Cancel", border_width=2, corner_radius=5, font=self.chooser_font,
                                border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                                command=self.quit).grid(row=0, column=1, padx=(20, 0), sticky='ew') 
                self.list_family.bind('<<ListboxSelect>>', self.update_entry_family)
                self.list_size.bind('<<ListboxSelect>>', self.update_entry_size, add=True)
                self.entry_family.bind("<Tab>", self.tab)
                self.entry_family.bind("<Down>", self.down_family)
                self.entry_size.bind("<Down>", self.down_size)
                self.entry_family.bind("<Up>", self.up_family)
                self.entry_size.bind("<Up>", self.up_size)
                self.entry_family.focus_set()
                self.lift()
                self.update()
                self.grab_set()
                parent.wait_window(self)
            except Exception as e:
                self.quit()  
        else:
            self.fonts=[]
            title="< Retrieving Windows Font Family Names >"
            msg1="Font_Families.json File Doesn't Exist!\n"
            msg2=f"Closing Window"
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            self.quit()
    def select_all(self, event):# Select all entry content.
        event.widget.selection_range(0, "end")
    def up_family(self, event):# Navigate in the family listbox with up key.
        try:
            f = self.var_family.get()
            if f in self.fonts:
                i = self.fonts.index(f)
            else:i=0    
            self.list_family.selection_clear()
            if i <= 0:
                i = len(self.fonts)
            self.list_family.see(i - 1)
            self.list_family.activate(i - 1)
        except Exception as e:
            self.list_family.selection_clear()
            i = len(self.fonts)
            self.list_family.see(i - 1)
            self.list_family.activate(i - 1)
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
            self.list_size.selection_clear()
            if i <= 0:
                i = len(self.sizes)
            self.list_size.see(i - 1)
            self.list_size.activate(i - 1)
        except Exception:
            i = len(self.sizes)
            self.list_size.see(i - 1)
            self.list_size.activate(i - 1)
        self.list_size.event_generate('<<ListboxSelect>>')
    def down_family(self, event):# Navigate in the family listbox with down key.
        try:
            f = self.var_family.get()
            if f in self.fonts:
                i = self.fonts.index(f)
            else:i=0    
            self.list_family.selection_clear()
            if i >= len(self.fonts):
                i = -1
            self.list_family.see(i + 1)
            self.list_family.activate(i + 1)
        except Exception:
            self.list_family.selection_clear()
            self.list_family.see(0)
            self.list_family.activate(0)
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
            self.list_size.selection_clear()
            if i < len(self.sizes) - 1:
                self.list_size.activate(i + 1)
                self.list_size.see(i + 1)
            else:
                self.list_size.see(0)
                self.list_size.activate(0)
        except Exception:
            self.list_size.activate(0)
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
        family.replace(" ", r"\ ") in self.fonts
        self.preview_font.configure(family=family)
    def change_font_size(self, event=None):# Update font preview size.
        size = int(self.var_size.get())
        self.preview_font.configure(size=size)
    def tab(self, event):# Move at the end of selected text on tab press
        self.entry_family = event.widget
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
    def update_entry_family(self, event=None):# Update family entry when an item is selected in the family listbox.
        self.entry_family.configure(state="normal")
        index = self.list_family.curselection()
        if index >=0:family = self.list_family.get(index) 
        self.entry_family.delete(0, "end")
        self.entry_family.insert(0, family)
        self.entry_family.selection_clear()
        self.entry_family.icursor("end")
        self.entry_family.configure(state="readonly")
        self.change_font_family()
    def update_entry_size(self, event):# Update size entry when an item is selected in the size listbox.
        self.entry_size.configure(state="normal")
        index = self.list_size.curselection()
        if index >=0:
            size = self.list_size.get(index) 
            self.var_size.set(size)
            self.change_font_size()
        self.entry_size.configure(state="readonly")
    def ok(self):
        family_new=self.preview_font.cget("family")
        size_new=self.preview_font.cget("size")
        weight_new=self.preview_font.cget("weight")
        slant_new=self.preview_font.cget("slant")
        self.new_font_dict={'family': family_new, 'size': size_new, 'weight': weight_new, 'slant': slant_new}
        self.new_font = self.new_font_dict
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):widget.destroy()
            else:widget.destroy()
        self.grab_release()
        self.destroy()    
    def quit(self):
        self.new_font = ""
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):widget.destroy()
            else:widget.destroy()
        self.grab_release()
        self.destroy()    
class Ratio_Calculator(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)
        try:
            app.withdraw()
            self.after(250, self.wm_iconbitmap, app.ico_path)
            if app.Language.get()=="English":txt="Ratio / Porportion Calculator"
            else:txt="Calculadora de Proporciones / Ratios"
            self.title(f'{app.root_title}  {txt}')
            _width = int(app.screen_width*0.3)
            _height = int(app.screen_height*0.5)
            _x = int(((app.screen_width // 2) - (_width // 2)) / app.scale_factor)
            _y = int(((app.screen_height // 2) - (_height // 2)) / app.scale_factor)
            self.geometry('%dx%d+%d+%d' % (_width, _height, _x, _y))
            self.transient(app)  # Set the dialog to be on top of the app
            self.grab_set()        # Freeze interaction with the main window
            self.configure(bg='#00FFFF') # Set main backcolor to aqua
            self.protocol("WM_DELETE_WINDOW", self.ratio_destroy)
            self.ratio_font=ctk.CTkFont(family='Arial', size=14, weight='normal', slant='italic')# Ratio Formulas
            self.formula=""
            self.focused=ctk.StringVar() 
            self.a1=ctk.StringVar()
            self.a2=ctk.StringVar()
            self.b1=ctk.StringVar()
            self.b2=ctk.StringVar()
            self.a3=ctk.StringVar()
            self.b3=ctk.StringVar()
            self.a4=ctk.StringVar()
            self.b4=ctk.StringVar()
            self.formula_text=ctk.CTkTextbox(self, fg_color=('#0c012e','#0c012e'), text_color='#07f7d8', font=self.ratio_font, 
                    border_width=5, wrap="word", scrollbar_button_hover_color='#07f7d8', corner_radius=10)
            self.formula_text.place(relx=0.015, rely=0.01, relwidth=0.97, relheight=0.22)
            self.formula_text.bind("<Control-c>", lambda event:app.copy_to_clipboard(self.formula_text,"selected"))    
            self.formula_text.bind("<Button-3>", lambda event:self.copy_display())
            self.formula_text.focus()
            if app.Language.get()=="English":txt=['3 Ratio Values Must Be Present To Calculate','The 4th Ratio Value And Porportion Values.',
                                            'All 4 Ratio Values May Be Entered Manually','For Porportion Calculations.',
                                            'Enter At Lease 3 Ratio Values','Find Unknown Porportions','CLEAR','CALCULATE','QUIT','Backspace']
            else:    
                txt=['Deben estar presentes 3 valores de proporción para calcular','el 4º valor de proporción y los valores de proporción.',
                    'Los 4 valores de la proporción pueden ingresarse manualmente','para los cálculos de proporción.',
                    'Ingrese al menos 3 valores de relación','Encontrar proporciones desconocidas','BORRAR','CALCULAR','SALIR','Retroceso']
            self.formula=f'{txt[0]}\n'
            self.formula_text.insert("insert", self.formula)
            self.formula=f'{txt[1]}\n'
            self.formula_text.insert("end", self.formula)
            self.formula=f'{txt[2]}\n'
            self.formula_text.insert("end", self.formula)
            self.formula=f'{txt[3]}\n'
            self.formula_text.insert("end", self.formula)
            self.default_text=ctk.BooleanVar()
            self.default_text.set(True)
            frame1=ctk.CTkFrame(self, fg_color='#E5E5E5', border_width=2, border_color="black", corner_radius=10) 
            frame1.place(relx=0.015, rely=0.24, relwidth=0.97, relheight=0.275)    
            frame1_lbl = ctk.CTkLabel(frame1, text=txt[4], font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            frame1_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
            a1_lbl = ctk.CTkLabel(frame1, text='A1', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            a1_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
            self.a1_txtbx = ctk.CTkEntry(frame1, textvariable=self.a1, font=self.ratio_font, border_color=("black","black"), 
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.a1_txtbx.register(self.on_validate), '%P')
            self.a1_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.a1_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
            self.a1_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A1'))
            self.a1_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A2'))
            a2_lbl = ctk.CTkLabel(frame1, text='A2', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            a2_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
            self.a2_txtbx = ctk.CTkEntry(frame1, textvariable=self.a2, font=self.ratio_font, border_color=("black","black"),  
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.a2_txtbx.register(self.on_validate), '%P')
            self.a2_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.a2_txtbx.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
            self.a2_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A2'))
            self.a2_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B1'))
            ratio_lbl = ctk.CTkLabel(frame1, font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"),
                                        text='__________________________     :    __________________________')
            ratio_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
            b1_lbl = ctk.CTkLabel(frame1, text='B1', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            b1_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
            self.b1_txtbx = ctk.CTkEntry(frame1, textvariable=self.b1, font=self.ratio_font, border_color=("black","black"),  
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.b1_txtbx.register(self.on_validate), '%P')
            self.b1_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.b1_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
            self.b1_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B1'))
            self.b1_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B2'))
            b2_lbl = ctk.CTkLabel(frame1, text='B2', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            b2_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
            self.b2_txtbx = ctk.CTkEntry(frame1, textvariable=self.b2, font=self.ratio_font, border_color=("black","black"),  
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.b2_txtbx.register(self.on_validate), '%P')
            self.b2_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.b2_txtbx.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
            self.b2_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B2'))
            self.b2_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A3'))
            kb_frame=ctk.CTkFrame(self, fg_color='#00FFFF', border_width=0, border_color="black", corner_radius=0) 
            kb_frame.place(relx=0.015, rely=0.524, relwidth=0.97, relheight=0.08)
            keys=['0','1','2','3','4','5','6','7','8','9','-','.',txt[9]]
            key_btn=[]
            for i, item in enumerate(keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
                key_btn.append([i])
                key_btn[i] = ctk.CTkButton(kb_frame, text=item, anchor="c", border_width=2, corner_radius=5, font=self.ratio_font,
                                width=1, border_color=("black", "black"), fg_color=("black", "black"), hover_color="#00FFFF",
                                text_color=("white","white"), command=lambda i=item: self.keyboard(i))
                key_btn[i].pack(side='left',fill='both',expand=True,padx=1,pady=2)
            frame2=ctk.CTkFrame(self, fg_color='#E5E5E5', border_width=0, border_color="black", corner_radius=10) 
            frame2.place(relx=0.015, rely=0.617, relwidth=0.97, relheight=0.275)    
            frame2_lbl = ctk.CTkLabel(frame2, text=txt[5], font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            frame2_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
            a_lbl = ctk.CTkLabel(frame2, text='A', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            a_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
            self.a3_txtbx = ctk.CTkEntry(frame2, textvariable=self.a3, font=self.ratio_font, border_color=("black","black"), 
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.a3_txtbx.register(self.on_validate), '%P')
            self.a3_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.a3_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
            self.a3_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'A3'))
            self.a3_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'B3'))
            bAnswer_lbl = ctk.CTkLabel(frame2, text='B =', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            bAnswer_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
    
            bAnswer = ctk.CTkEntry(frame2, textvariable=self.b4, font=self.ratio_font, border_width=2, state="disabled", corner_radius=5, 
                                        border_color=("black","black"), text_color=("black","black"), fg_color=("#99ffff","#99ffff"))
            bAnswer.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
            porportion_lbl = ctk.CTkLabel(frame2, font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"),
                                        text='__________________________     :    __________________________')
            porportion_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
            b_lbl = ctk.CTkLabel(frame2, text='B', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            b_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
            self.b3_txtbx = ctk.CTkEntry(frame2, textvariable=self.b3, font=self.ratio_font, border_color=("black","black"), 
                                        border_width=2, text_color=("black","black"), fg_color=("#99ffff","#99ffff"), corner_radius=5,
                                        state="normal", validatecommand=((self.validate_Entries),'%P','%d'))
            val_cmd=(self.b3_txtbx.register(self.on_validate), '%P')
            self.b3_txtbx.configure(validate="key", validatecommand=val_cmd)
            self.b3_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
            self.b3_txtbx.bind("<Button-1>", lambda event:self.keyboard_focus(event,'B3'))
            self.b3_txtbx.bind("<Tab>", lambda event:self.keyboard_focus(event,'A1'))
            aAnswer_lbl = ctk.CTkLabel(frame2, text='A =', font=self.ratio_font, anchor="center",
                                        fg_color=('#E5E5E5','#E5E5E5'),text_color=("black","black"))
            aAnswer_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
            aAnswer = ctk.CTkEntry(frame2, textvariable=self.a4, font=self.ratio_font, border_width=2, state="disabled", corner_radius=5, 
                                        border_color=("black","black"), text_color=("black","black"), fg_color=("#99ffff","#99ffff"))
            aAnswer.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
            clr_btn = ctk.CTkButton(self, text=txt[6], border_width=2, corner_radius=5, font=self.ratio_font,
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                            command=lambda:self.clear_entries())  
            clr_btn.place(relx=0.197, rely=0.912, relwidth=0.16, relheight=0.06)
            calc_btn = ctk.CTkButton(self, text=txt[7], border_width=2, corner_radius=5, font=self.ratio_font,
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                            command=lambda:self.calculate_ratio(self.a1.get(),self.a2.get(),self.b1.get(),self.b2.get(),self.a3.get(),self.b3.get()))
            calc_btn.place(relx=0.38, rely=0.912, relwidth=0.25, relheight=0.06)
            quit_btn = ctk.CTkButton(self, text=txt[8], border_width=2, corner_radius=5, font=self.ratio_font,
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                            command=self.ratio_destroy)  
            quit_btn.place(relx=0.65, rely=0.912, relwidth=0.16, relheight=0.06)
            self.focus_force()
            self.a1_txtbx.focus_force()
            self.focused.set('A1')
            self.mainloop()
        except Exception as e:
            self.destroy    
    def copy_destroy(self, event):
        self.popup_btn.destroy()
        app.copy_to_clipboard(self.formula_text,"all")    
    def copy_display(self):
        if hasattr(self, "popup_btn") and self.popup_btn.winfo_exists():
            self.popup_btn.destroy()
            return
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        parent_wid=self.formula_text.winfo_width()
        parent_hgt=self.formula_text.winfo_height()
        popup_width = int(parent_wid * 0.5)
        popup_height = int(parent_hgt * 0.3)
        x_pos = int(((parent_wid // 2) - (popup_width // 2)) / scale_factor)
        y_pos = int(((parent_hgt // 2) - (popup_height // 2)) / scale_factor)
        if app.Language.get()=="English":msg="Copy Display Text To Clipboard"
        else:msg="Copiar Texto Mostrado al Portapapeles"
        self.popup_btn=ctk.CTkButton(self.formula_text, text=msg, font=self.ratio_font, border_width=2, corner_radius=15, anchor="center",  
                        border_color="black", fg_color=("#00ced1", "#00ced1"), hover_color="#ff9999", text_color="#000000",
                        width=popup_width, height=popup_height)
        self.popup_btn.place(x=x_pos, y=y_pos)
        self.popup_btn.bind("<Button-1>", lambda event:self.copy_destroy(event))    
        self.popup_btn.bind("<FocusOut>", lambda event: self.destroy_popup(event))
        self.popup_btn.update()
        self.popup_btn.focus_force()
    def destroy_popup(self, event):
        self.popup_btn.destroy()
    def ratio_destroy(self):# X Icon Was Clicked
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):widget.destroy()
            else:widget.destroy()
        self.withdraw()
        app.deiconify()
        app.grab_set()
        app.focus_force()
        app.update()
    def validate_Entries(self,string):
        regex=compile(r'[-+(0-9.)]*$') # Allowed +- Floats
        result=regex.match(string)
        return (string == "" 
        or (string.count(string)>0 # Prevent duplicates
            and result is not None
            and result.group(0) != ""))       
    def on_validate(self,P):return self.validate_Entries(P)
    def clear_entries(self):# Clears all text from Entry widgets
        self.a1_txtbx.configure(state='normal') 
        self.a2_txtbx.configure(state='normal') 
        self.b1_txtbx.configure(state='normal') 
        self.b2_txtbx.configure(state='normal')
        self.a1_txtbx.delete('0','end')
        self.a2_txtbx.delete('0','end')
        self.b1_txtbx.delete('0','end')
        self.b2_txtbx.delete('0','end')
        self.a3_txtbx.delete('0','end')
        self.b3_txtbx.delete('0','end')
        self.a4.set('')
        self.b4.set('')
        self.formula_text.delete('1.0','end')
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
                if app.Language.get()=="English":
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
                info_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="info")
            if count == 3: # count=3, find & calculate missing ratio value
                if self.default_text.get():
                    self.formula_text.delete('1.0','end')
                    self.default_text.set(False)
                if missing_ratio == 'a1':
                    zero_exist=self.div_by_zero(self.b2_txtbx, b_2, 'B2') # Prohibit Division by Zero
                    if zero_exist: return
                    tmp=float((b_1 * a_2) / b_2) #a1=(b1 * a2) / b2, where b2 != 0
                    s = nstr(tmp, n=6, force_type=True)
                    if 'e' in s.lower(): # Scientific Notation Exist
                        result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                        mantissa, exponent = s.split('e')
                        if mpf(exponent) < 0:# Small Decimal Numbers
                            exp=abs(int(exponent)) + len(str(result))
                            val = mpf(f"{tmp:.{exp}f}")
                        else:val = float(f"{tmp:.10f}")
                    else:val = float(f"{tmp:.10f}")        
                    self.formula_text.delete('1.0','end')
                    self.formula=(f"A1 = (B1 * A2) / B2 = ({b_1} * {a_2}) / {b_2} = {tmp}\n")    
                    self.formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.a1_txtbx, val)
                    a_1 = val
                    count+=1
                elif missing_ratio == 'a2':
                    zero_exist=self.div_by_zero(self.b1_txtbx, b_1, 'B1') # Prohibit Division by Zero
                    if zero_exist: return
                    tmp=float((a_1 / b_1) * b_2) #a2=(a1 / b1) * b2, where b1 != 0
                    s = nstr(tmp, n=6, force_type=True)
                    if 'e' in s.lower(): # Scientific Notation Exist
                        result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                        mantissa, exponent = s.split('e')
                        if float(exponent) < 0:# Small Decimal Numbers
                            exp=abs(int(exponent)) + len(str(result))
                            val = mpf(f"{tmp:.{exp}f}")
                        else:val = float(f"{tmp:.10f}")
                    else:val = float(f"{tmp:.10f}")        
                    self.formula_text.delete('1.0','end')
                    self.formula=(f"A2 = (A1 / B1) * B2 = ({a_1} / {b_1}) * {b_2} = {tmp}\n")    
                    self.formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.a2_txtbx, val)
                    a_2 = val
                    count+=1
                elif missing_ratio == 'b1':
                    zero_exist=self.div_by_zero(self.a2_txtbx, a_2, 'A2') # Prohibit Division by Zero
                    if zero_exist: return
                    tmp=float((a_1 * b_2) / a_2) #b1=(a1 * b2) / a2, where a2 != 0
                    s = nstr(tmp, n=6, force_type=True)
                    if 'e' in s.lower(): # Scientific Notation Exist
                        result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                        mantissa, exponent = s.split('e')
                        if float(exponent) < 0:# Small Decimal Numbers
                            exp=abs(int(exponent)) + len(str(result))
                            val = mpf(f"{tmp:.{exp}f}")
                        else:val = float(f"{tmp:.10f}")
                    else:val = float(f"{tmp:.10f}")        
                    self.formula_text.delete('1.0','end')
                    self.formula=(f"B1 = (A1 * B2) / A2 = ({a_1} * {b_2}) / {a_2} = {tmp}\n")    
                    self.formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.b1_txtbx, val)
                    b_1 = val
                    count+=1
                elif missing_ratio == 'b2':
                    zero_exist=self.div_by_zero(self.a1_txtbx, a_1, 'A1') # Prohibit Division by Zero
                    if zero_exist: return
                    tmp=float((b_1 * a_2) / a_1) #b2=(b1 * a2) / a1, where a1 != 0
                    s = nstr(tmp, n=6, force_type=True)
                    if 'e' in s.lower(): # Scientific Notation Exist
                        result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                        mantissa, exponent = s.split('e')
                        if float(exponent) < 0:# Small Decimal Numbers
                            exp=abs(int(exponent)) + len(str(result))
                            val = mpf(f"{tmp:.{exp}f}")
                        else:val = float(f"{tmp:.10f}")
                    else:val = float(f"{tmp:.10f}")        
                    self.formula_text.delete('1.0','end')
                    self.formula=(f"B2 = (B1 * A2) / A1 = ({b_1} * {a_2}) / {a_1} = {tmp}\n")    
                    self.formula_text.insert('1.0', self.formula)
                    self.update_ratio(self.b2_txtbx, val)
                    b_2 = val
                    count+=1
                self.default_text.set(False)
            if count == 4: # All ratio value present, examine for porportion values
                if self.default_text.get():
                    self.formula_text.delete('1.0','end')
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
                    asize=float(abs(a_2 - a_1))
                    bsize=float(abs(b_1 - b_2))
                elif(b_1 > 0) and (b_2 >= 0):
                    asize=float(abs(a_1 - a_2))
                    bsize=float(abs(b_2 - b_1))
                else:
                    asize=float(abs(a_1 - a_2)) #0,-100 or -10,-100 Examples
                    bsize=float(abs(b_1 - b_2)) #0,-100 or 10,-100
                # Calculate the K=Factors using the sizes
                if app.Language.get()=="English":ranges=['A Range','B Range']
                else:ranges=['Rango de A','Rango de B']
                Kfactor_ba=abs(bsize / asize) #X Amount Of B's Per X Amount Of A's
                KDisplay_ba=f"K = Abs({ranges[1]} / {ranges[0]})"
                Kfactor_ab=abs(asize / bsize) #X Amount Of A's Per X Amount Of B's
                KDisplay_ab=f"K = Abs({ranges[0]} / {ranges[1]})"
                # Final Calculations
                if not inverse: # Case Not A_Inverse And Not B_Inverse Or A_Inverse And B_Inverse
                    exist=self.a3.get()
                    if len(exist) != 0:# B=B1 - (K * (A1 - A))
                        a_3 = mpf(self.a3.get())
                        self.formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                        self.formula_text.insert('2.0', self.formula)
                        b_4 = float(b_1 - (Kfactor_ba * (a_1 - a_3)))
                        s = nstr(b_4, n=6, force_type=True)
                        if 'e' in s.lower(): # Scientific Notation Exist
                            result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                            mantissa, exponent = s.split('e')
                            if float(exponent) < 0:# Small Decimal Numbers
                                exp=abs(int(exponent)) + len(str(result))
                                val = mpf(f"{b_4:.{exp}f}")
                            else:val = float(f"{b_4:.10f}")
                        else:val = float(f"{b_4:.10f}")        
                        self.formula=(f"B = B1 - (K * (A1 - A)) = {b_1} - ({Kfactor_ba} * ({a_1} - {a_3})) = {b_4}\n")
                        self.formula_text.insert('3.0', self.formula)
                        self.b4.set(val)
                    exist=self.b3.get()
                    if len(exist) != 0:# A=A1 - (K * (B1 - B))
                        b_3=mpf(self.b3.get())
                        self.formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                        self.formula_text.insert('4.0', self.formula)
                        a_4 = float(a_1 - (Kfactor_ab * (b_1 - b_3)))
                        s = nstr(a_4, n=6, force_type=True)
                        if 'e' in s.lower(): # Scientific Notation Exist
                            result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                            mantissa, exponent = s.split('e')
                            if float(exponent) < 0:# Small Decimal Numbers
                                exp=abs(int(exponent)) + len(str(result))
                                val = mpf(f"{a_4:.{exp}f}")
                            else:val = float(f"{a_4:.10f}")
                        else:val = float(f"{a_4:.10f}")        
                        self.formula=(f"A = A1 - (K * (B1 - B)) = {a_1} - ({Kfactor_ab} * ({b_1} - {b_3})) = {a_4}\n")
                        self.formula_text.insert('5.0', self.formula)
                        self.a4.set(val)
                else: # Case A_Inverse And Not B_Inverse Or Not A_Inverse And B_Inverse
                    exist=self.a3.get()
                    if len(exist) != 0:# B=B1 - ((A - A1) * K)
                        a_3=mpf(self.a3.get())
                        self.formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                        self.formula_text.insert('2.0', self.formula)
                        b_4 = float(b_1 - ((a_3 - a_1) * Kfactor_ba))
                        s = nstr(b_4, n=6, force_type=True)
                        if 'e' in s.lower(): # Scientific Notation Exist
                            result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                            mantissa, exponent = s.split('e')
                            if float(exponent) < 0:# Small Decimal Numbers
                                exp=abs(int(exponent)) + len(str(result))
                                val = mpf(f"{b_4:.{exp}f}")
                            else:val = float(f"{b_4:.10f}")
                        else:val = float(f"{b_4:.10f}")        
                        self.formula=(f"B = B1 - ((A - A1) * K) = {b_1} - (({a_3} - {a_1}) * {Kfactor_ba}) = {b_4}\n")
                        self.formula_text.insert('3.0', self.formula)
                        self.b4.set(val)
                    exist=self.b3.get()
                    if len(exist) != 0:# A=A1 - ((B - B1) * K)
                        b_3=mpf(self.b3.get())
                        self.formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                        self.formula_text.insert('4.0', self.formula)
                        a_4 = float(a_1 - ((b_3 - b_1) * Kfactor_ab))
                        s = nstr(a_4, n=6, force_type=True)
                        if 'e' in s.lower(): # Scientific Notation Exist
                            result = s.partition('00')[0]# Remove All After First 2 Sequential Zeros
                            mantissa, exponent = s.split('e')
                            if float(exponent) < 0:# Small Decimal Numbers
                                exp=abs(int(exponent)) + len(str(result))
                                val = mpf(f"{a_4:.{exp}f}")
                            else:val = float(f"{a_4:.10f}")
                        else:val = float(f"{a_4:.10f}")        
                        self.formula=(f"A = A1 - ((B - B1) * K) = {a_1} - (({b_3} - {b_1}) * {Kfactor_ab}) = {a_4}\n")
                        self.formula_text.insert('5.0', self.formula)
                        self.a4.set(val)
        except Exception as e:
            if app.Language.get()=="English":
                title='Exeption Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error de excepción'
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2=repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")    
    def div_by_zero(self, widget_name, value, focused):
        if value == 0:# Prohibit Division By Zero, Set Focus On Entry Widget
            if app.Language.get()=="English":
                title='Division By Zero Error'
                msg=f'Division By Zero! Please Change {focused} Value!'
            else:    
                title='Error de División por Cero'
                msg=f'¡División por Cero! ¡Por favor Cambie el Valor de {focused}!'
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            widget_name.delete(0,"end")
            widget_name.focus_set()   
            return True
        else: return False
    def update_ratio(self, widget_name, new_value):
        widget_name.delete(0,"end")
        widget_name.insert(0, new_value)
        widget_name.focus_set()
    def keyboard(self, txt):
        f=self.focused.get()
        if txt!='Backspace' and txt!='Retroceso':
            if f=='A1':
                txt=self.a1.get()+txt
                self.a1.set(txt)
            elif f=='A2':
                txt=self.a2.get()+txt
                self.a2.set(txt)
            elif f=='B1':
                txt=self.b1.get()+txt
                self.b1.set(txt)
            elif f=='B2':
                txt=self.b2.get()+txt
                self.b2.set(txt)
            elif f=='A3':
                txt=self.a3.get()+txt
                self.a3.set(txt)
            elif f=='B3':
                txt=self.b3.get()+txt
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
            value=bin(val & (2**app.Bit_Size.get() - 1))
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
            value=oct(val & (2**app.Bit_Size.get() - 1))
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
            value=hex(val & (2**app.Bit_Size.get()-1))
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
                if dec_val>2**(app.Bit_Size.get())-1:
                    dec_val=2**(app.Bit_Size.get())-1
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
                if dec_val>2**(app.Bit_Size.get())-1:
                    dec_val=2**(app.Bit_Size.get())-1
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
                if dec_val>2**(app.Bit_Size.get())-1:
                    dec_val=2**(app.Bit_Size.get())-1
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
                if dec_val>2**(app.Bit_Size.get())-1:
                    dec_val=2**(app.Bit_Size.get())-1
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
            if app.Language.get()=="English":
                title='Converting Base Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error de Conversión de Base'
                msg1='Ocurrió una Excepción Durante la Ejecución del Código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
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
            if app.Language.get()=="English":
                title='Converting Trigonometry Error'
                msg1='Exception occurred while code execution:\n'
            else:    
                title='Error al Convertir Trigonometría'
                msg1='Ocurrió una Excepción Durante la Ejecución del Código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
class Calculus_Scroll(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app)
        try:
            self.canvas = ctk.CTkCanvas(self, highlightthickness=0,bg='#f3f6f4', borderwidth=5, relief="sunken")
            self.v_scrollbar = ctk.CTkScrollbar(self, orientation="vertical", corner_radius=10, 
                                                button_hover_color="#00cccc", command=self.canvas.yview)
            self.h_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", corner_radius=10, 
                                                button_hover_color="#00cccc", command=self.canvas.xview)
            self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
            self.v_scrollbar.pack(side='right',fill='y',padx=(0, 5),pady=(30, 60))                                        
            self.canvas.pack(side='top', anchor='nw', fill='both', expand=True, padx=(20, 5), pady=(10, 5))
            self.h_scrollbar.pack(side='bottom',fill='x',padx=(20, 20),pady=(0, 5))                                        
            #self.scrollable_frame = ctk.CTkFrame(self.canvas)
            self.window=ctk.CTkFrame(self.canvas, bg_color="#f3f6f4", fg_color='#f3f6f4')
            self.window.pack(side='top',anchor='nw',fill='both', expand=True, padx=(0, 0), pady=(0, 0))                     
            self.canvas.create_window((0, 0), window=self.window, anchor="nw", tags="self.window")
            self.window.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        except Exception as e:
            self.destroy    
class Calculus(ctk.CTkToplevel):
    def __init__(self, app, funct):
        super().__init__(app)
        try:
            self.after(250, self.wm_iconbitmap, app.ico_path)
            self.funct=funct
            disp=app.Display.get()
            app.withdraw()
            self.deiconify()
            self.grab_set() # Receive Events And Prevent app Window Interaction
            hgt=app.screen_height * 0.46
            wid=app.screen_width * 0.4
            x=(app.screen_width/2)-(wid/2)
            y=(app.screen_height/2)-(hgt/2)
            self.geometry('%dx%d+%d+%d' % (wid, hgt, x, y, ))
            self.configure(bg='#f3f6f4')
            self.protocol("WM_DELETE_WINDOW", self.calculus_destroy)
            calculus = Calculus_Scroll(self) 
            calculus.pack(side="top", fill="both", expand=True)
            calculus.canvas.xview_moveto(0)
            calculus.canvas.yview_moveto(0)
            calculus.canvas.bind()
            calculus_font = ctk.CTkFont(family="Arial", size=18)
            app.close_brackets('all')# (Just In Case) Close All Opened Brackets Before Preceding
            if app.Language.get()=="English":txt="Expression"
            else:txt="Expresión"
            self.display_txt=app.Display_Text.get("1.0","2.0").replace("\n","")
            self.display_txt=self.display_txt.replace(f"{txt} = ","")
            self.expr_txt=f"{txt} = {self.display_txt}"
            disp=app.Display.get()
            app.Last_Display.append(f"{txt} = {app.Expression.get()}\n")
            self.expr=app.Expression.get().split("=")[0]# If Equation Has Answer, Trim (= and Answer)
            self.expr2=self.expr
            txt1=self.expr_txt
            r=1    
            self.lbl_1 = ctk.CTkLabel(calculus.window, text=txt1, corner_radius=0, anchor="w",
                            fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
            self.lbl_1.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
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
            for i in range(len(app.Symbol_Names)):# Place Names And Values into Dictionary And Populate Labels
                txt=''
                app.sub_dict[app.Symbol_Names[i]] = app.Symbol_Values[i]
                if app.Symbol_Names[i] not in self.used_symbols:# Prevent Duplicate Symbol Population
                    if str(app.Symbol_Names[i])!= "rad_to_deg" and str(app.Symbol_Names[i])!= "rad_to_grad":
                        txt=str(app.Symbol_Names[i])+' = '+str(app.Symbol_Values[i])
                        self.used_txt.append(txt) # Used To Populate These Labels
                        self.used_symbols.append(str(app.Symbol_Names[i])) # Used To Polulate symbol_bx 
                        r+=1        
                        self.lbl_2.append([c])
                        self.lbl_2[c] = ctk.CTkLabel(calculus.window, text=self.used_txt[c], corner_radius=0, anchor="w",
                                        fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
                        self.lbl_2[c].pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
                        c+=1
            r+=1
            newstr=str(self.expr)
            if newstr[0]=='(' and newstr[-1]==')':newstr=newstr[1:-1] # Remove Extra Brackets
            if app.Language.get()=="English":txt=[f'Expression Symbolized = {newstr}','With Respect To:','Derivative Work Sheet']
            else:txt=[f'Expresión Simbolizada = {newstr}','Con Respecto a:','Hoja de Trabajo de Derivadas']
            self.lbl_3 = ctk.CTkLabel(calculus.window, text=txt[0], corner_radius=0, anchor="w",
                            fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
            self.lbl_3.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
            r+=1
            self.cbo_lbl = ctk.CTkLabel(calculus.window, text=txt[1], corner_radius=0, anchor="w", width=10,
                            fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
            self.cbo_lbl.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
            r+=1
            self.respect=ctk.StringVar()
            if self.funct=='differentiate':cmd=self.do_derivative
            else:cmd=self.do_integral
            self.symbol_bx = ctk.CTkComboBox(calculus.window, values=self.used_symbols, button_color=("#00cccc","#00cccc"), 
                                            button_hover_color=("#ffff99","#ffff99"), text_color=("black", "black"), variable=self.respect, 
                                            fg_color=("#80ffff", "#80ffff"),dropdown_fg_color=("#80ffff", "#80ffff"),  command=cmd, 
                                            dropdown_text_color=("black", "black"), width=10, font=calculus_font, dropdown_font=calculus_font) 
            self.symbol_bx.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10, 0), pady=(0, 0))                     
            self.symbol_bx['state'] = 'readonly'
            if self.funct=='differentiate':
                self.title(f'{app.root_title}  {txt[2]}')
                r+=1
                if app.Language.get()=="English":
                    multiples=['1st Derivative','2nd Derivative','3rd Derivative','4th Derivative','5th Derivative']
                    txt='Number of Derivatives:'
                else:
                    multiples=['1ra Derivada','2da Derivada','3ra Derivada','4ta Derivada','5ta Derivada']    
                    txt='Número de Derivados:'
                self.multi_lbl = ctk.CTkLabel(calculus.window, text=txt, corner_radius=0, anchor="w", width=10,
                                fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
                self.multi_lbl.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
                self.multiple=ctk.StringVar()
                r+=1
                self.multi_bx = ctk.CTkComboBox(calculus.window, values=multiples, button_color=("#00cccc","#00cccc"), 
                                                button_hover_color=("#ffff99","#ffff99"), text_color=("black", "black"), variable=self.multiple, 
                                                fg_color=("#80ffff", "#80ffff"), dropdown_fg_color=("#80ffff", "#80ffff"), command=self.do_derivative, 
                                                dropdown_text_color=("black", "black"), width=10, font=calculus_font, dropdown_font=calculus_font) 
                self.multi_bx.pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
                self.multi_bx['state'] = 'readonly'
            elif self.funct=='integrate':
                if app.Language.get()=="English":txt='Integral Work Sheet'
                else:txt='Hoja de Trabajo de Integrales'
                self.title(f'{app.root_title}  {txt}')
                self.symbol_bx.bind('<<ComboboxSelected>>', self.do_integral)
            self.lbl_4=[]
            for i in range(0,6):
                r+=1
                self.lbl_4.append([i])
                self.lbl_4[i] = ctk.CTkLabel(calculus.window, text="", corner_radius=0, anchor="w", width=10,
                                fg_color=("#f3f6f4", "#f3f6f4"), text_color="black", font=calculus_font)
                self.lbl_4[i].pack(side='top',anchor='nw',fill='x', expand=True, padx=(10,0), pady=(0,0))                     
            self.update()    
            self.mainloop()
        except Exception as e:
            self.destroy    
    def get_next_symbol(self,val):
        if val in app.Symbol_Values:# Value Already Symbolized, return Symbol
            for i, j in enumerate(app.Symbol_Values):
                if j == val:return app.Symbol_Names[i]
        for symbol in list(map(chr,range(ord('a'),ord('z')+1))):
            if not symbol in app._MyClash and not symbol in app.Symbols_Used:
                parsed=parse_expr(symbol, evaluate=False)
                symbol=symbols(symbol)
                app.Symbols_Used.append(str(symbol))
                app.Symbol_Names.append(parsed)
                app.Symbol_Values.append(val)
                return symbol
        else: 
            for symbol in list(map(chr,range(ord('A'),ord('Z')+1))):
                if not symbol in app._MyClash and not symbol in app.Symbols_Used:
                    symbol=symbols(symbol)
                    app.Symbols_Used.append(str(symbol))
                    return symbol
    def do_integral(self, event):
        try:
            resp=parse_expr(self.respect.get(), evaluate=False)
            parsed_integral=parse_expr(self.expr, evaluate=True)
            app.disp_update('clear')
            integral_expr=Integral(parsed_integral,resp)
            exp=integral_expr.doit()
            newstr=str(self.expr2)
            for i in range(5):# Remove Extra Brackets
                if newstr[0]=='(' and newstr[-1]==')':
                    newstr=newstr[1:-1]
                else:break
            answer=app.nround_answer(exp) # Round Answer To User Preference
            app.Answer_Present.set(True)
            app.Answer.set(answer)
            if app.Language.get()=="English":txt=['Equation','"Answer','Invalid Entry!','Get Integral']
            else:txt=['Ecuación','Respuesta','¡Entrada no Válida!','Obtener Integral']
            self.lbl_4[0].configure(text=self.expr_txt)
            self.lbl_4[1].configure(text=self.lbl_3.cget("text"))
            self.lbl_4[2].configure(text=f"{txt[0]} = ∫{resp}({self.display_txt})")
            self.lbl_4[3].configure(text=f"= {exp}")
            self.lbl_4[4].configure(text = f"{txt[1]} = {answer}")
            self.lbl_4[5].configure(text = "--------------------------------------------------------------")
            for d in range(len(self.lbl_4)):
                txt=f"{self.lbl_4[d].cget("text")}\n"
                app.Last_Display.append(txt)
            for d in range(1,len(app.Last_Display)):# Skip Calculator Expression Display (Last_Display[0])
                app.disp_update(app.Last_Display[d])
        except Exception as e:
            app.Answer.set('')
            app.Answer_Present.set(False)
            app.Answer_Err.set(True)
            self.lbl_4[1].configure(text = txt[2])
            app.disp_update(f' = {txt[2]}')
            app.expr_update(f' = {txt[2]}')
            title= txt[3]
            msg1=f"{txt[2]}\n"
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            self.calculus_destroy()
    def do_derivative(self, event):
        multiple_derivatives=self.multiple.get()
        resp=self.respect.get()
        if multiple_derivatives=='':return
        if resp=='':return
        try:
            resp=parse_expr(self.respect.get(), evaluate=False)
            parsed_derative=parse_expr(self.expr, evaluate=True)
            app.disp_update('clear')
            multiple_derivatives=self.multiple.get()
            tmp_str=''
            for i in self.multiple.get(): # Extract Number From String
                if i.isdigit():tmp_str+=i
            multi=parse_expr(tmp_str, evaluate=False)
            if app.Language.get()=="English":    
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
            answer=app.nround_answer(exp)
            app.Answer_Present.set(True)
            app.Answer.set(answer)
            if app.Language.get()=="English":txt=['Equation','"Answer','Invalid Entry!','Get Integral']
            else:txt=['Ecuación','Respuesta','¡Entrada no Válida!','Obtener Integral']
            self.lbl_4[0].configure(text=self.expr_txt)
            self.lbl_4[1].configure(text=self.lbl_3.cget("text"))
            self.lbl_4[2].configure(text=f"{txt[0]} = {mstr}{resp}({self.display_txt})")
            self.lbl_4[3].configure(text=f"= {exp}")
            self.lbl_4[4].configure(text = f"{txt[1]} = {answer}")
            self.lbl_4[5].configure(text = "--------------------------------------------------------------")
            for d in range(len(self.lbl_4)):
                txt=f"{self.lbl_4[d].cget("text")}\n"
                app.Last_Display.append(txt)
            for d in range(1,len(app.Last_Display)):# Skip Calculator Expression Display (Last_Display[0])
                app.disp_update(app.Last_Display[d])
        except Exception as e:
            app.Answer.set('')
            app.Answer_Present.set(False)
            app.Answer_Err.set(True)
            self.lbl_4[1].configure(text = txt[2])
            app.disp_update(f' = {txt[2]}')
            app.expr_update(f' = {txt[2]}')
            title= txt[3]
            msg1=f"{txt[2]}\n"
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            self.calculus_destroy()
    def calculus_destroy(self):# X Icon Was Clicked
        app.Last_Display.clear()
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):
                widget.destroy()
            else:
                widget.destroy()
        self.withdraw()
        app.deiconify()
        app.grab_set()
        app.focus_force()
        app.update()
class MyDialog(ctk.CTkToplevel):
    def __init__(self, parent, 
                 style: Literal["msgbox", "entry"], 
                 title, prompt, 
                 choices=None, 
                 icon: Literal["setup","check", "cancel", "info", "question", "warning"] = None, 
                 init_val=None, min_val=None, max_val=None):
        super().__init__(parent)
        self.style = style
        self.title(title)
        self.prompt = prompt
        self.choices = choices
        self.icon = icon
        self.init_val = init_val
        self.min_val = min_val
        self.max_val = max_val
        self.after(350, self.wm_iconbitmap, parent.ico_path)
        self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        primary_monitor=MonitorFromPoint((0, 0))
        monitor_info=GetMonitorInfo(primary_monitor)
        work_area=monitor_info.get("Work")
        self.screen_width=work_area[2]
        self.screen_height=(work_area[3])
        self.width = int(self.screen_width*0.25)
        self.height = int(self.screen_height*0.25)
        x = int(((self.screen_width // 2) - (self.width // 2)) / self.scale_factor)
        y = int(((self.screen_height // 2) - (self.height // 2)) / self.scale_factor)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.attributes("-topmost", True)
        self.update()
        self.mydialog_font = ctk.CTkFont(family="Arial", size=14, weight="normal", slant="roman")
        self.result = None
        if self.icon != None:# Widget for the icon
            iconfile=f"{self.icon}.png"
            if os.path.exists(iconfile):
                icon_size = self.height * 0.2
                pil_icon = Image.open(iconfile)
                ctk_image = ctk.CTkImage(light_image=pil_icon, dark_image=pil_icon, size=(icon_size, icon_size)) 
                self.icon_label = ctk.CTkLabel(self, image=ctk_image, text="")
                self.icon_label.pack(pady=(5, 0))
        label = ctk.CTkLabel(self, text=prompt, font=self.mydialog_font)# Widgets for the dialog
        label.pack(pady=(10, 10))
        if self.style == "entry": 
            if self.choices is not None:
                wid=len(self.choices)+4
                if type(self.choices)==list:# List
                    for item in self.choices:
                        w=len(item)
                        if w>wid:wid=w
                    self.combobox = ctk.CTkComboBox(self, values=self.choices, font=self.mydialog_font) 
                    self.combobox.pack(pady=(0, 5))
                    self.combobox.focus_set() # Set focus to the entry widget
                    if init_val!= None: 
                        self.combobox.set(init_val)
                else:# String
                    self.entry = ctk.CTkEntry(self, self.choices, font=self.mydialog_font)
                    self.entry.pack(pady=(0, 5))
                    self.entry.focus_set() # Set focus to the entry widget
                    if init_val!= None or init_val!="": 
                        self.entry.insert(ctk.END, init_val)
            else:
                self.entry = ctk.CTkEntry(self, font=self.mydialog_font)
                self.entry.pack(pady=(0, 5))
                self.entry.focus_set() # Set focus to the entry widget
                if init_val!= None or init_val!="": 
                    self.entry.insert(ctk.END, init_val)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)
        self.ok_button = ctk.CTkButton(self.button_frame, text="OK", font=self.mydialog_font, command=self.on_ok)
        self.ok_button.pack(side="left", padx=10)
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", font=self.mydialog_font, command=self.on_cancel)
        self.cancel_button.pack(side="right", padx=10)
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.update()
        self.grab_set()
        parent.wait_window(self)
    def on_ok(self):
        self.grab_release()
        if self.style == "entry":
            if self.choices is not None:
                if type(self.choices)==list:
                    self.result = self.combobox.get()
                else: 
                    self.result = self.entry.get()
            else:self.result = self.entry.get()
        else:self.result = None           
        self.destroy() # Close the dialog
        return self.result    
    def on_cancel(self):
        self.grab_release()
        self.result = None
        self.destroy() # Close the dialog
        return self.result    
class MyTimedPopup(ctk.CTkLabel): # The Popup Is Centered On The Parent Widget. 
    def __init__(self, parent, text, text_color, fg_color, font_size, delay_time): 
        super().__init__(parent)
        self.parent=parent
        self.text=(f" {text} ")
        self.text_color=text_color
        self.fg_color=fg_color
        self.font_size=font_size
        self.delay_time=delay_time
        self.popup_font = ctk.CTkFont(family="Arial", size=self.font_size, weight="normal", slant="roman")
        try:
            self.req_width = self.popup_font.measure(self.text)
            font_metrics = self.popup_font.metrics()
            self.req_height = int(font_metrics['linespace'] * 1.5)
            self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
            parent_wid=self.parent.winfo_width() / self.scale_factor
            parent_hgt=self.parent.winfo_height() / self.scale_factor
            self.x_pos = int(((parent_wid // 2) - (self.req_width // 2)) / self.scale_factor)
            self.y_pos = int(((parent_hgt // 2) - (self.req_height // 2)) / self.scale_factor)
            self.popup_lbl= ctk.CTkLabel(master=parent, text=self.text, width=self.req_width, text_color=self.text_color,
                                    fg_color=self.fg_color, corner_radius=10, font=self.popup_font)
            self.popup_lbl.place(x=self.x_pos, y=self.y_pos)
            self.update()
            self.after(self.delay_time, self.popup_lbl.destroy)
        except Exception as e:
            self.destroy()    
class MyPopupMenu(ctk.CTkToplevel):
    def __init__(self, parent, caption_list, command_list, font_size, x_pos, y_pos):
        super().__init__(parent)
        self.caption_list=caption_list
        self.command_list=command_list
        self.font_size=font_size
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.max_wid=0
        self.menu_font = ctk.CTkFont(family="Arial", size=self.font_size, weight="normal", slant="roman")
        self.transient(parent)  # Set the dialog to be on top of the app
        try:
            for i in range(len(self.caption_list)):# Get Max Text Length For Menu Width
                txt = f"XXXX{self.caption_list[i]}XXX"
                if len(txt)>self.max_wid:
                    self.max_wid = len(txt)
                    self.text = txt
            self.req_width = self.menu_font.measure(self.text)
            font_metrics = self.menu_font.metrics()
            self.req_height = int(font_metrics['linespace'] * 18)
            self.geometry('%dx%d+%d+%d' % (self.req_width, self.req_height, self.x_pos, self.y_pos))
            self.overrideredirect(True)
            self.attributes("-topmost", True) # Keep the popup on top of the main window
            self.frame = ctk.CTkScrollableFrame(self, width=self.max_wid, corner_radius=10)# Container for scrollable items
            self.frame.pack(fill="both", expand=True, padx=(10, 10), pady=(10, 10))
            self.menu_items=[] 
            for i in range(0, len(self.caption_list)):
                self.menu_items.append([i])
                self.menu_items[i] = ctk.CTkButton(self.frame, text=self.caption_list[i], anchor="w", compound="left", fg_color="transparent", hover_color="#ff8080",  
                                            text_color=("#000000", "#ffffff"), font=self.menu_font, corner_radius=10, command=self.command_list[i])
                self.menu_items[i].pack(side='top', anchor='w', pady=0)
                self.menu_items[i].bind("<Button 1>", lambda e: self.withdraw())
            self.bind("<FocusOut>", lambda e: self.withdraw())
            self.update()
            self.focus_set()
        except Exception as e:
            self.withdraw()
class Calculator(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font_sizes = [12, 14, 16, 22, 24] 
        self.base_font=ctk.CTkFont(family='Arial', size=font_sizes[1], weight='bold', slant='roman')# Base Buttons
        self.formula_font=ctk.CTkFont(family='Arial', size=font_sizes[0], weight='normal', slant='roman')# Ratio Formulas
        self.dialog_font=ctk.CTkFont(family='Arial', size=font_sizes[0], weight='normal', slant='italic')# Dialogs
        self.temp_font=ctk.CTkFont(family='Arial', size=font_sizes[1], weight='bold', slant='italic')# F-C, C-F, Ratio Buttons
        self.memory_font=ctk.CTkFont(family='Arial', size=font_sizes[2], weight='normal', slant='italic')# Memory, mod, exp Buttons
        self.integral_font=ctk.CTkFont(family='Arial', size=font_sizes[2], weight='bold', slant='italic')# Integrate Button
        self.symbols_font=ctk.CTkFont(family='Arial', size=font_sizes[3], weight='normal', slant='italic')# Numeric,math symbols, CM Buttons
        self.bracket_font=ctk.CTkFont(family='Arial', size=font_sizes[3], weight='normal', slant='roman')# () Buttons
        self.operator_font=ctk.CTkFont(family='Arial', size=font_sizes[4], weight='normal', slant='roman')# Math operators, sign Buttons
        self.Display_Font=ctk.CTkFont(family='Arial', size=font_sizes[4], weight='normal', slant='italic')# Display Only
        dir=Path(__file__).parent.absolute()
        filename='pycal.ico' # Program icon
        self.ico_path=os.path.join(dir, filename)
        self.iconbitmap(default=self.ico_path)# app and children
        self.iconbitmap(self.ico_path)
        self.withdraw()
        self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        primary_monitor=MonitorFromPoint((0, 0))
        monitor_info=GetMonitorInfo(primary_monitor)
        work_area=monitor_info.get("Work")
        self.screen_width=work_area[2]
        self.screen_height=(work_area[3])
        self.width = int(self.screen_width*0.4)
        self.height = int(self.screen_height*0.35)
        # CTK Variables
        self.Language=ctk.StringVar()
        self.Display=ctk.StringVar()# Text Shown On Display (Advancing Display Update)
        self.Disp_Bkts_Open=ctk.IntVar()# Number Of Display Brackets Open
        self.Temp_Disp_Open=ctk.IntVar()# Used To Highlight Total Display Function.
        self.Expression=ctk.StringVar()# Advancing Expression Update
        self.Expr_Bkts_Open=ctk.IntVar()# Number Of Expression Brackets Open
        self.Temp_Expr_Open=ctk.IntVar()# Used To Highlight Total Expression Function. 
        self.Math_Function=ctk.StringVar()
        self.Last_Function=ctk.StringVar()
        self.Exp_Precision=ctk.IntVar()
        self.Round=ctk.IntVar()
        self.Exp_Digits=ctk.IntVar()
        self.Bit_Size=ctk.IntVar()
        self.Theme=ctk.StringVar()
        self.NewFont=ctk.StringVar()
        self.Selected_Temp=ctk.StringVar()
        self.Selected_Temp.set("°F → °C")
        self.US_Metric=ctk.StringVar()
        self.US_Metric.set("in. → cm")
        self.Answer=ctk.StringVar()# Parsed Answer
        self.Answer_Err=ctk.BooleanVar()
        self.Answer_Present=ctk.BooleanVar()# Answer Received And Present
        self.Engine_Init=ctk.BooleanVar()
        self.Display_bg=ctk.StringVar()
        self.Display_fg=ctk.StringVar()
        self.Base=ctk.StringVar()
        self.Trig_Units=ctk.StringVar()
        self.Arc=ctk.BooleanVar()
        self.Hyp=ctk.BooleanVar()
        self.Disp_List=[]# Final Display Not Shown
        self.Reversed_List=[] # Display Or Expression List Reversed
        self.Expr_List=[]# Final Expression Sent To Parser
        self.Expressions_Used=[]
        self.Symbol_Names=[]
        self.Symbol_Values=[]
        self.Symbols_Used=[]
        self.base_btn=[]# Widget Array List
        self.unit_btn=[]# Widget Array List
        self.num_btn=[]# Widget Array List
        self.log_btn=[]# Widget Array List
        self.trig_btn=[]# Widget Array List
        self.func_btn=[]# Widget Array List
        self.operator_btn=[]# Widget Array List
        self.mem_btn=[]# Widget Array List
        self.Log_var=[]# Widget Array Variables
        self.Trig_var=[]# Widget Array Variables
        self.sub_dict={}
        self.D_Memory1=[]
        self.D_Memory2=[]
        self.D_Memory3=[]
        self.D_Memory4=[]
        self.E_Memory1=[]
        self.E_Memory2=[]
        self.E_Memory3=[]
        self.E_Memory4=[]
        self.Last_Display=[]
        self.operators=[' / ',' * ',' - ',' + '] # Math operators
        self.Hex_List=['a','A','b','B','c','C','d','D','e','E','f','F']
        self.Normal_Script="0123456789"
        self.Super_Script="⁰¹²³⁴⁵⁶⁷⁸⁹"
        self.Sub_Script="₀₁₂₃₄₅₆₇₈₉"
        self._MyClash=['pi','beta','gamma','zeta','radian','C','O','Q','N','I','E','S']
        self._MyConstants = ['𝓔','𝑮','𝜱','𝜯','𝑲','𝑨','𝑴','π','𝒆','𝜁3','Π₂','Π','rad_to_deg','rad_to_grad','arc_rad_to_deg','arc_rad_to_grad']
        self.Distance_List = ['in. → mm','in. → cm', 'in. → m','in. → km','in. → ft','in. → yds','in. → mi','in. → au',
                       'ft → mm','ft → cm','ft → m','ft → km','ft → in.','ft → yds','ft → mi','ft → au',
                       'yds → mm','yds → cm','yds → m','yds → km','yds → in.','yds → ft','yds → mi','yds → au',
                       'mi → mm','mi → cm','mi → m','mi → km','mi → in.','mi → ft','mi → yds','mi → au',
                       'mm → in.','mm → ft','mm → yds','mm → mi','mm → au',
                       'cm → in.','cm → ft','cm → yds','cm → mi','cm → au',
                       'm → in.','m → ft','m → yds','m → mi','m → au',
                       'km → in.','km → ft','km → yds','km → mi','km → au',
                       'au → in.','au → ft','au → yds','au → mi','au → mm','au → cm','au → m','au → km']
        self.Distance_Math = [' / 0.0393700787401575',' / 0.393700787401575', ' / 39.3700787401575',' / 39370.0787401575',' / 12.0',' / 36.0',' / 63360.0',' / 5889679948818.9',
                       ' * 304.8',' * 30.48',' / 3.2808398950131',' / 3280.8398950131',' * 12.0',' / 3.0',' / 5280.0',' / 490806662372.05',
                       ' / 0.00109361329833771',' / 0.0109361329833771',' / 1.09361329833771',' / 1093.61329833771',' * 36.0',' * 3.0',' / 1760.0',' / 163602220790.68',
                       ' / 0.000000621371',' / 0.00000621371 ',' / 0.000621371',' / 0.621371',' * 63360.0',' * 5280.0',' * 1760.0',' / 92955807.267433',
                       ' * 0.0393700787401575','0.0032808399',' * 0.00109361',' * 0.000000621371',' / 149597870700000.0',
                       ' * 0.393700787401575',' * 0.032808398950131',' * 0.0109361329833771',' * 0.00000621371',' / 14959787070000.0',
                       ' * 39.3700787401575',' * 3.2808398950131',' * 1.09361329833771',' * 0.000621371',' / 149597870700.0',
                       ' * 39370.0787401575',' * 3280.8398950131',' * 1093.61329833771',' * 0.621371',' / 149597870.7',
                       ' * 5889679948818.9',' * 490806662372.05',' * 163602220790.68',' *  92955807.267433',' * 149597870700000.0',' * 14959787070000.0',' * 149597870700.0',' * 149597870.7']
        self.Temp_List = ['°F → °C', '°F → °K','°F → °R', '°C → °F', '°C → °K', '°C → °R', '°K → °F','°K → °C','°K → °R', '°R → °F','°R → °C','°R → °K']
        try:
            languages=["English","Spanish"]
            title="Select Language / Seleccionar Idioma"
            msg1="Please Select The Desired Program Language.\n"
            msg2="Por favor, Seleccione el Idioma del Programa Deseado."
            msg=msg1+msg2
            if os.path.exists("Config.json"):
                with open('Config.json', 'r') as json_file:
                    data = json.load(json_file)
                    json_file.close()
                if data["11"]!=str(self.screen_width) or data["12"]!=str(self.screen_height) or data["13"]!=str(self.scale_factor):
                    self.x = int(((self.screen_width // 2) - (self.width // 2)) / self.scale_factor) 
                    self.y = int(((self.screen_height // 2) - (self.height // 2)) / self.scale_factor)
                    data[9]=str(self.x)
                    data[10]=str(self.y)
                    data[11]=str(self.screen_width)
                    data[12]=str(self.screen_height)
                    data[13]=str(self.scale_factor)
                    with open("Config.json", "w") as outfile:json.dump(data, outfile)
                    outfile.close()
                    os.execl(sys.executable, os.path.abspath("ctkCalculator.exe"), *sys.argv)
                else:
                    with open('Config.json', 'r') as json_file:
                        data = json.load(json_file)
                        json_file.close()
                    if data["0"]=="":
                        while self.Language.get()=="":
                            lang = MyDialog(parent=self, style="entry", title=title, prompt=msg, choices=["English", "Spanish"], icon="setup")
                            if lang.result=="" or lang.result==None:self.Language.set("")
                            else:self.Language.set(lang.result)
                        temp_dict={}
                        temp_dict[0]=self.Language.get() 
                        with open("Config.json", "w") as json_file:
                            data["0"] = self.Language.get()
                            json.dump(data, json_file)
                            json_file.close()
                    else:self.Language.set(data["0"])
            else:
                while self.Language.get()=="": 
                    lang = MyDialog(parent=self, style="entry", title=title, prompt=msg, choices=["English", "Spanish"], icon="setup")
                    if lang.result is not None:self.Language.set(lang.result)
                    else:self.Language.set("")
                self.x = int(((self.screen_width // 2) - (self.width // 2)) / self.scale_factor)
                self.y = int(((self.screen_height // 2) - (self.height // 2)) / self.scale_factor)
        except:
            if os.path.exists("Config.json"):
                os.remove("Config.json")
            os.execl(sys.executable, os.path.abspath("ctkCalculator.exe"), *sys.argv)
        self.user=os.getlogin()
        if self.Language.get()=="English":txt=[f"{self.user}'s Calculator: ","Right Click Display For Options"]
        else:txt=[f"{self.user}'s Calculadora: ","Haga Clic Derecho en la Pantalla para Opciones"]
        self.root_title=txt[0]
        options=txt[1]
        self.title(self.root_title + options.rjust(40+len(options)))
        self.configure(fg_color='#14fafa')
        self.resizable(True,True)
        self.protocol("WM_DELETE_WINDOW", self.calculator_destroy)
        # Bind Keyboard Keys
        self.bind("<Return>", self.equal_clicked)
        self.bind("<BackSpace>", self.clear_entry)
        for i in range(10):
            self.bind(str(i), self.numeric_clicked)
        self.bind("<period>", self.numeric_clicked)
        for i, item in enumerate(self.Hex_List):
            self.bind(str(item), self.numeric_clicked)
        Operators2=['/','*','-','+'] # Bind Keyboard Operator Keys
        for i, item in enumerate(Operators2):
            self.bind(str(item), self.operator_clicked)
        self.bind("(", lambda event, a='manual', b='both', c='open':self.bracket_clicked(a,b,c))
        self.bind(")", lambda event, a='manual', b='both', c='close':self.bracket_clicked(a,b,c))
        ####### Widgets #######
        self.Display.set("")
        self.Display_bg.set("#0c012e")
        self.Display_fg.set("#ffffff")
        self.Display_Text=ctk.CTkTextbox(self, fg_color=self.Display_bg.get(), text_color=self.Display_fg.get(), font=self.Display_Font, 
                border_color="navy", border_width=5, corner_radius=10)
        self.Display_Text.place(relx=0.015, rely=0.011, relwidth=0.97, relheight=0.16)
        self.Display_Text.bind("<Control-c>", lambda event:self.copy_to_clipboard(self.Display_Text, "selected")) 
        self.Display_Text.delete("0.0", "end")
        Unbound_Keys='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&{[}]|:;",?~`'
        for i, item in enumerate(Unbound_Keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
            if item in Unbound_Keys:
                self.Display_Text.bind(str(item), lambda e: "break")
        self.Display_Text.bind("<Button-3>", self.show_menu_popup)
        if self.Language.get()=="English":text=['Binary','Decimal','Hexadecimal','Octal']
        else:text=['Binario','Decimal','Hexadecimal','Octal']
        wid=[0.19,0.21,0.32,0.185]
        x=[0.02,0.23,0.455,0.793]
        hgt=0.75
        y=0.15
        self.base_frame=ctk.CTkFrame(self, fg_color='#999999', border_width=2, border_color="black", corner_radius=10) 
        self.base_frame.place(relx=0.015, rely=0.185, relwidth=0.479, relheight=0.1)
        for num in range(0,len(text)):
            self.base_btn.append([num])
            self.base_btn[num] = ctk.CTkButton(self.base_frame, text=text[num], border_width=2, corner_radius=5, font=self.base_font, anchor="center",
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                            command=lambda i=text[num]: self.base_clicked(i))  
            self.base_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        if self.Language.get()=="English":
            text=['Degrees','Radians','Gradians']
        else:
            text=['Grados','Radianes','Gradianos']
        wid=[0.29,0.29,0.305]
        x=[0.03,0.35,0.665]
        self.unit_frame=ctk.CTkFrame(self, fg_color='#999999', border_width=2, border_color="black", corner_radius=10) 
        self.unit_frame.place(relx=0.506, rely=0.185, relwidth=0.365, relheight=0.1)
        for num in range(0,len(text)):
            self.unit_btn.append([num])
            self.unit_btn[num] = ctk.CTkButton(self.unit_frame, text=text[num], border_width=2, corner_radius=5, font=self.base_font, anchor="center",
                            border_color="black", fg_color=("#004d00", "#004d00"), hover_color="#00ced1", text_color="#ffffff",
                            command=lambda i=text[num]: self.trig_unit_clicked(i))  
            self.unit_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        self.clrmem_btn = ctk.CTkButton(self, text='CM', border_width=2, corner_radius=5, font=self.symbols_font, anchor="center",
                            border_color="black", fg_color=("#ffff99", "#ffff99"), hover_color="#00ced1", text_color="maroon",
                            command=lambda i='CM': self.clear_memories(i))  
        self.clrmem_btn.place(relx=0.886, rely=0.185, relwidth=0.085, relheight=0.1)
        self.clrmem_btn.bind('<Button-3>', lambda event, txt="CM",: self.button_popups(event, txt))
        self.pad_fra=ctk.CTkFrame(self, fg_color='#999999', border_width=2, border_color="black", corner_radius=10) 
        self.pad_fra.place(relx=0.015, rely=0.3, relwidth=0.97, relheight=0.68)    
        y,x1,x2=0.015,0.01,0.098
        for num in range(0,10):# Numbers 0 - 9
            self.num_btn.append([num])
            if (num % 2)==0:x=x1# Even 
            else:x=x2 
            self.num_btn[num] = ctk.CTkButton(self.pad_fra, text=num, border_width=2, corner_radius=5, font=self.symbols_font, anchor="center",
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff", 
                            command=lambda i=num: self.numeric_clicked(i))  
            self.num_btn[num].place(relx=x, rely=y, relwidth=0.08, relheight=0.12)
            self.num_btn[num].bind("<Button-1>", self.numeric_clicked) # Bind all the number keys with the callback function
            if (num % 2)!=0:y+=0.14# Odd
        x=[0.01,0.1,0.19,0.28,0.39,0.5]
        wid=[0.08,0.08,0.08,0.1,0.1,0.1]    
        text=['A','B','C','D','E','F'] # Hex Numbers A - F
        for num in range(10,16):
            self.num_btn.append([num])
            self.num_btn[num] = ctk.CTkButton(self.pad_fra, text=text[num-10], border_width=2, corner_radius=5, font=self.symbols_font,
                            border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="#ffffff",
                            command=lambda i=text[num-10]: self.numeric_clicked(i))  
            self.num_btn[num].place(relx=x[num-10], rely=y, relwidth=wid[num-10], relheight=0.12)
            self.num_btn[num].bind("<Button-1>", self.numeric_clicked) # Bind all the number keys with the callback function
        x=0.19
        y=0.015
        wid=0.08
        hgt=0.12
        for num in range(0,len(self.operators)):
            self.operator_btn.append([num])
            self.operator_btn[num] = ctk.CTkButton(self.pad_fra, text=self.operators[num], anchor="c", border_width=2, corner_radius=5, font=self.operator_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="navy",
                            command=lambda i=self.operators[num]: self.operator_clicked(i))  
            self.operator_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.operator_btn[num].bind("<Button-1>", self.operator_clicked)
            y+=0.14
        self.equal_btn = ctk.CTkButton(self.pad_fra, text=' = ', anchor="c", border_width=2, corner_radius=5, font=self.operator_font,
                        border_color="black", fg_color=("#14fafa", "#14fafa"), hover_color="yellow", text_color="navy",
                        command=lambda i='=':self.equal_clicked(i))  
        self.equal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        text=['log𝒆','log10','log(x,b)']
        x=0.28
        y=0.015
        wid=0.1
        hgt=0.12
        for num in range(0,len(text)):
            self.Log_var.append(ctk.StringVar(master=None))
            self.log_btn.append([num])
            self.log_btn[num] = ctk.CTkButton(self.pad_fra, text=text[num], anchor="c", border_width=2, corner_radius=5, font=self.base_font,
                            border_color="black", fg_color=("purple", "purple"), hover_color="#00ced1", text_color="whitesmoke",
                            command=lambda i=text[num]: self.log_clicked(i))  
            self.log_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.log_btn[num].bind('<Button-3>', lambda event, txt=text[num]: self.button_popups(event, txt))
            self.Log_var[num].set(num)
            y+=0.14
        self.sign_btn = ctk.CTkButton(self.pad_fra, text=chr(177), anchor="n", border_width=2, corner_radius=5, font=self.operator_font,
                        border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="whitesmoke",
                        command=lambda i=chr(177): self.sign_clicked(i))  
        self.sign_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        y+=0.14
        self.decimal_btn = ctk.CTkButton(self.pad_fra, text=chr(46), anchor="n", border_width=2, corner_radius=5, font=self.operator_font,
                        border_color="black", fg_color=("navy", "navy"), hover_color="#00ced1", text_color="whitesmoke",
                        command=lambda i=chr(46): self.numeric_clicked(i))  
        self.decimal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        y+=0.14
        odd_list=['sec','csc','cot']
        text=['sin','sec','cos','csc','tan','cot']
        x1=0.39
        x2=0.5
        y=0.015
        wid=0.1
        hgt=0.12
        for num in range(0,len(text)):
            self.Trig_var.append(ctk.StringVar(master=None))
            self.trig_btn.append([num])
            if text[num] in odd_list:x=x2
            else:x=x1
            self.trig_btn[num] = ctk.CTkButton(self.pad_fra, text=text[num], anchor="c", border_width=2, corner_radius=5, font=self.base_font,
                            border_color="black", fg_color=("#004d00", "#004d00"), hover_color="#00ced1", text_color="whitesmoke",
                            command=lambda i=text[num]: self.trig_clicked(i))  
            self.trig_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.trig_btn[num].bind('<Button-3>', lambda event, txt=text[num]: self.button_popups(event, txt))
            self.Trig_var[num].set(num)
            if text[num] in odd_list:y+=0.14
        odd_list.clear()    
        self.arc_btn = ctk.CTkButton(self.pad_fra, text='Arc', anchor="c", border_width=2, corner_radius=5, font=self.base_font,
                        border_color="black", fg_color=("#004d00", "#004d00"), hover_color="#00ced1", text_color="whitesmoke",
                        command=lambda i='Arc': self.config_trig_btns(i))  
        self.arc_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
        self.arc_btn.bind('<Button-3>', lambda event, txt="Arc": self.button_popups(event, txt))
        self.hyp_btn = ctk.CTkButton(self.pad_fra, text='Hyp', anchor="c", border_width=2, corner_radius=5, font=self.base_font,
                        border_color="black", fg_color=("#004d00", "#004d00"), hover_color="#00ced1", text_color="whitesmoke",
                        command=lambda i='Hyp': self.config_trig_btns(i))  
        self.hyp_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
        self.hyp_btn.bind('<Button-3>', lambda event, txt="Hyp": self.button_popups(event, txt))
        x1=0.39
        x2=0.5
        y+=0.14
        self.open_btn = ctk.CTkButton(self.pad_fra, text='('+chr(8304), anchor="n", border_width=2, corner_radius=5, font=self.operator_font,
                        border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black")  
        self.open_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
        self.open_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='open':self.bracket_clicked(a,b,c))
        self.closed_btn = ctk.CTkButton(self.pad_fra, text=')', anchor="n", border_width=2, corner_radius=5, font=self.operator_font,
                        border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black")  
        self.closed_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
        self.closed_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='close':self.bracket_clicked(a,b,c))
        x=0.61
        y=0.015
        wid=0.08
        hgt=0.12
        text=[' 1/𝓧 ',' 𝓧ʸ ',' 𝓧³ ',' 𝓧² ',' n! ',' 𝜯 ',' 𝑮 ']
        for num in range(0,len(text)): # Function Buttons Column 1
            self.func_btn.append([num])
            self.func_btn[num] = ctk.CTkButton(self.pad_fra, text=text[num], anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                            command=lambda i=text[num]: self.funct_clicked(i))  
            self.func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.func_btn[num].bind('<Button-3>', lambda event, txt=text[num]: self.button_popups(event, txt))
            y+=0.14
        self.func_btn[0].configure(font=("Arial", 18, 'italic'))   
        self.clr = ctk.CTkButton(self.pad_fra, text="C", anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                    border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                    command=lambda:self.clear_all())  
        self.clr.place(relx=0.7, rely=0.015, relwidth=0.09, relheight=0.12)
        self.clr.bind('<Button-3>', lambda event, txt="C": self.button_popups(event, txt))
        x=0.7
        y=0.155
        wid=0.09
        hgt=0.12
        text=[' ʸ√ ',' ³√ ',' ²√ ',' 𝓔 ',' π ',' 𝜁3 ']
        i=0
        num+=1
        for num in range(6, 12): # Function Buttons Column 2
            self.func_btn.append([num])
            self.func_btn[num] = ctk.CTkButton(self.pad_fra, text=text[i], anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                            command=lambda i=text[i]: self.funct_clicked(i))  
            self.func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.func_btn[num].bind('<Button-3>', lambda event, txt=text[i]: self.button_popups(event, txt))
            y+=0.14
            i+=1
        self.func_btn[6]['font']=self.symbols_font
        self.ce=ctk.CTkButton(self.pad_fra, text='CE', anchor="c", border_width=2, corner_radius=5, font=self.symbols_font, 
                        border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black") # Clear Entry Button 
        self.ce.place(relx=0.8, rely=0.015, relwidth=0.09, relheight=0.12)
        self.ce.bind("<Button-1>", self.clear_entry)
        self.ce.bind('<Button-3>', lambda event, txt="CE": self.button_popups(event, txt))
        x=0.8
        y=0.155
        wid=0.09
        hgt=0.12
        text=[ '% ',' 𝑴 ',' Π₂ ',' 𝒆 ',' 𝜱 ',' 𝑲 ',' 𝑨 ']
        i=0
        for num in range(12,18): # Function Buttons Column 3
            if num == 14: anchor_pos = "center"
            elif num == 18:anchor_pos = "n"
            else: anchor_pos = "s"
            self.func_btn.append([num])
            self.func_btn[num] = ctk.CTkButton(self.pad_fra, text=text[i], anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                            command=lambda i=text[i]: self.funct_clicked(i))  
            self.func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.func_btn[num].bind('<Button-3>', lambda event, txt=text[i]: self.button_popups(event, txt))
            y+=0.14
            i+=1
        self.func_btn[15]['font'] = self.bracket_font       
        x=0.9
        y-=0.14
        self.func_btn.append([num])# '𝑨'
        self.func_btn[num] = ctk.CTkButton(self.pad_fra, text=text[i], anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                        border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                        command=lambda i='𝑨': self.funct_clicked(i))  
        self.func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        self.func_btn[num].bind('<Button-3>', lambda event, txt=text[i]: self.button_popups(event, txt))
        self.mem_btn=[]
        x=0.9
        y=0.015
        wid=0.09
        hgt=0.12
        text=['ms1','ms2','ms3','ms4']
        for num in range(0,len(text)): 
            self.mem_btn.append([num])
            self.mem_btn[num] = ctk.CTkButton(self.pad_fra, text=text[num], anchor="c", border_width=2, corner_radius=5, font=self.memory_font,
                        border_color="black", fg_color=("#ffff99", "#ffff99"), hover_color="#00ced1", text_color="maroon",
                        command=lambda i=text[num]: self.memory_clicked(i))  
            self.mem_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
            self.mem_btn[num].bind('<Button-3>', lambda event, txt=text[num]: self.button_popups(event, txt))
            y+=0.14
        self.mod_btn = ctk.CTkButton(self.pad_fra, text="mod", anchor="c", border_width=2, corner_radius=5, font=self.memory_font,
                    border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                    command=lambda i="mod": self.funct_clicked(i))  
        self.mod_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        self.mod_btn.bind('<Button-3>', lambda event, txt="mod": self.button_popups(event, txt))
        y+=0.14
        self.exp_btn = ctk.CTkButton(self.pad_fra, text="exp", anchor="c", border_width=2, corner_radius=5, font=self.memory_font,
                    border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                    command=lambda i="exp": self.funct_clicked(i))  
        self.exp_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        self.exp_btn.bind('<Button-3>', lambda event, txt="exp": self.button_popups(event, txt))
        self.us_metric_btn = ctk.CTkButton(self.pad_fra, text=self.US_Metric.get(), anchor="c", border_width=2, corner_radius=5, font=self.temp_font,
                    border_color="black", fg_color=("#80ff80", "#80ff80"), hover_color="#00ced1", text_color="black",
                    textvariable=self.US_Metric, command=lambda: self.distance_clicked())  
        self.us_metric_btn.place(relx=0.137, rely=0.855, relwidth=0.117, relheight=0.12,)
        self.us_metric_btn.bind('<Button-3>', lambda event, txt=self.US_Metric.get(): self.select_distance(txt))
        self.temp_btn = ctk.CTkButton(self.pad_fra, text=self.Selected_Temp.get(), anchor="c", border_width=2, corner_radius=5, font=self.temp_font,
                    border_color="black", fg_color=("#ff9c95", "#ff9c95"), hover_color="#00ced1", text_color="black",
                    textvariable=self.Selected_Temp, command=lambda: self.temp_clicked())  
        self.temp_btn.bind('<Button-3>', lambda event, txt=self.Selected_Temp.get(): self.select_temps(txt))
        self.temp_btn.place(relx=0.01, rely=0.855, relwidth=0.117, relheight=0.12)
        self.ratio_btn = ctk.CTkButton(self.pad_fra, text="A : B", anchor="c", border_width=2, corner_radius=5, font=self.temp_font,
                    border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                    command=lambda:Ratio_Calculator(self))
        self.ratio_btn.place(relx=0.264, rely=0.855, relwidth=0.117, relheight=0.12)
        self.ratio_btn.bind('<Button-3>', lambda event, txt="A : B": self.button_popups(event, txt))
        self.integrate_btn = ctk.CTkButton(self.pad_fra, text="∫", anchor="c", border_width=2, corner_radius=5, font=self.integral_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",
                            command=lambda i="∫": self.do_calculus(i))  
        self.integrate_btn.place(relx=0.39, rely=0.855, relwidth=0.1, relheight=0.12)
        self.integrate_btn.bind('<Button-3>', lambda event, txt="∫": self.button_popups(event, txt))
        self.diff_btn = ctk.CTkButton(self.pad_fra, text="f´(𝓧)", anchor="c", border_width=2, corner_radius=5, font=self.symbols_font,
                            border_color="black", fg_color=("whitesmoke", "whitesmoke"), hover_color="#00ced1", text_color="black",  
                            command=lambda i="f´(𝓧)": self.do_calculus(i))
        self.diff_btn.place(relx=0.5, rely=0.855, relwidth=0.1, relheight=0.12)
        self.diff_btn.bind('<Button-3>', lambda event, txt="f´(𝓧)": self.button_popups(event, txt))
        text=[]
        self.set_defaults()
        self.give_greeting("open")
    def do_calculus(self, txt):
        if not app.Disp_List:return
        if app.Base.get()!='Decimal':return
        app.Display.set(app.Expression.get())
        if txt=="∫":funct="integrate"
        elif txt=="f´(𝓧)":funct="differentiate"
        calc=Calculus(self, funct)
    def convert_script(self, from_script, to_script,txt):# Convert Between Normal Script, Superscript And Subscript
        new_txt=txt.maketrans(''.join(from_script), ''.join(to_script))
        return txt.translate(new_txt)
    def about(self):
        self.popup_menu.withdraw()
        self.update()
        if self.Language.get()=="English":
            title="About Calculator"
            msg1='Creator: Ross Waters\n'
            msg2='Email: RossWatersjr@gmail.com\n'
            msg3=f'Revision: {version}\n'
            msg4='Created For Windows 11'
        else:    
            title="Acerca de la Calculadora"
            msg1='Creador: Ross Waters\n'
            msg2='Correo Electrónico: RossWatersjr@gmail.com\n'
            msg3=f'Revisión: {version}\n'
            msg4='Creado para Windows 11'
        msg=msg1+msg2+msg3+msg4
        info_dialog=MyDialog(parent=self, style="msgbox", title=title, prompt=msg, icon="info")
        self.grab_release()
    def precision(self, which): # Calculator Precision Configuration
        self.popup_menu.withdraw()
        self.update()
        if self.Language.get()=="English":
            titles=["< Calculator Precision >","<Round Displayed Answer>","<Scientific Notation Digits>",
                    "< Exponential Notation Digits >","< Binary Bit Size >"]
            messages=["Enter Number Of Digits For Calculation Precision.\nMinimum = 1\nMaximum = 500",
                        "Round Answer To nth Decimal Places.\n 0 = No Rounding\nMaximum = 500",
                        "Total Decimal Digits To Display For Scientific Notation.\n0 = Minimum\nMaximum = 500",
                        "Exponential Notation Precision.\n0 = Minimum\nMaximum = 4",
                        "Choices Are:\n"
                        "8 bits (Byte), 16 bits (Word),\n32 bits (Dword), 64 bits (Qword),\n"
                        "128 bits (Double Qword), 256 bits\n (Yword), 512 (ZWord)"]
        else:
            titles=["< Precisión de la Calculadora >","< Redondear Respuesta Mostrada >","< Dígitos en Notación Científica >",
                    "< Dígitos en Notación Exponencial >","< Tamaño de Bit Binario >"]
            messages=["Ingrese el Número de Dígitos para la Precisión del Cálculo.\nMínimo = 1\nMáximo = 500",
                        "Redondear la Respuesta a n Decimales.\n0 = Sin Redondeo\nMáximo = 500",
                        "Total de Dígitos Decimales a Mostrar para Notación Científica.\n0 = Mínimo\nMáximo = 500", 
                        "Precisión de Notación Exponencial.\n0 = Mínimo\nMáximo = 4",
                        "Opciones Son:\n"
                        "8 bits (Byte), 16 bits (Palabra),\n32 bits (Dpalabra), 64 bits (Qpalabra),\n "
                        "128 bits (Doble Qpalabra), 256 bits (Ypalabra),\n512 bits (Zpalabra)"]
        if which=='dp':
            dpp=MyDialog(self, title=titles[0], style="entry", prompt=messages[0], choices=None, init_val=mp.dps, min_val=1, max_val=500, icon="setup")
            if dpp.result is not None:
                while int(dpp.result) < 1 or int(dpp.result) > 500: 
                    dpp=MyDialog(self, title=titles[0], style="entry", prompt=messages[0], choices=None, init_val=mp.dps, min_val=1, max_val=500, icon="setup")
                mp.dps=int(dpp.result)
                mp.pretty==False
        elif which=='round':        
            rnd=MyDialog(self, title=titles[1], style="entry", prompt=messages[1], choices=None, init_val=self.Round.get(), min_val=0, max_val=500, icon="setup")
            if rnd.result is not None:
                while int(rnd.result) < 0 or int(rnd.result) > 500: 
                    rnd=MyDialog(self, title=titles[1], style="entry", prompt=messages[1], choices=None, init_val=self.Round.get(), min_val=0, max_val=500, icon="setup")
                self.Round.set(int(rnd.result))
        elif which=='exp':        
            snp=MyDialog(self, title=titles[2], style="entry", prompt=messages[2], choices=None, init_val=self.Exp_Precision.get(), min_val=1, max_val=500, icon="setup")
            if snp.result is not None:
                while int(snp.result) < 1 or int(snp.result) > 500: 
                    snp=MyDialog(self, title=titles[2], style="entry", prompt=messages[2], choices=None, init_val=self.Exp_Precision.get(), min_val=1, max_val=500, icon="setup")
                self.Exp_Precision.set(int(snp.result))
        elif which=='exp_digits':
            enp=MyDialog(self, title=titles[3], style="entry", prompt=messages[3], choices=None, init_val=self.Exp_Digits.get(), min_val=1, max_val=4, icon="setup")
            if enp.result is not None:
                while int(enp.result) < 1 or int(enp.result) > 4: 
                    enp=MyDialog(self, title=titles[3], style="entry", prompt=messages[3], choices=None, init_val=self.Exp_Digits.get(), min_val=1, max_val=4, icon="setup")
                self.Exp_Digits.set(int(enp.result))
        elif which=='bit_size':
            bbs=MyDialog(self, title=titles[4], style="entry", prompt=messages[4], choices=['8','16','32','64','128','256','512'], init_val=self.Bit_Size.get(), min_val=None, max_val=None, icon="setup")
            if bbs.result is not None:
                self.Bit_Size.set(int(bbs.result))
        self.grab_release()
    def choose_font(self): # Calculator Display Font
        try:
            self.popup_menu.withdraw()
            app.update()
            if self.Language.get()=="English":txt=["Sample text for selected font","Choose Display Font"]
            else:txt=["Texto de Ejemplo para la Fuente Seleccionada","Elegir Fuente de Visualización"]
            if self.Display.get()!='':sample=self.Display.get()
            else:sample=txt[0]
            family_now=self.Display_Font.cget("family")
            size_now=self.Display_Font.cget("size")
            weight_now=self.Display_Font.cget("weight")
            slant_now=self.Display_Font.cget("slant")
            font_dict={'family': family_now, 'size': size_now, 'weight': weight_now, 'slant': slant_now}
            chooser = MyFontChooser(self, font_dict, text=sample)
            if chooser.new_font != '': 
                new_font_dict=chooser.new_font
                family_new=new_font_dict["family"]
                size_new=new_font_dict["size"]
                weight_new=new_font_dict["weight"]
                slant_new=new_font_dict["slant"]
                self.Display_Font=ctk.CTkFont(family=family_new, size=size_new, weight=weight_new, slant=slant_new)# Display Only
                self.NewFont.set(self.Display_Font)
                self.Display_Text.focus_force()
                self.Display_Text.configure(font=self.Display_Font)
        except Exception as e:
            return
    def choose_theme(self, theme):
        if self.Language.get()=="English":
            msg = "Select The Desired Color Theme Then Click OK."
        else:
            msg = "Seleccione el Tema de Color Deseado y Luego Haga Clic en OK."
        theme=MyDialog(self, title=" < Set Color Theme >", style="entry", prompt=msg, choices=["System", "Dark", "Light"], init_val=self.Theme.get(), icon="setup")
        if theme.result is not None:
            self.Theme.set(theme.result)
            self.grab_release()
            self.restart_program(False)
        else:self.grab_release()    
    
    def choose_color(self, which): # Display fg and bg Colors
        self.popup_menu.withdraw()
        if self.Language.get()=="English":
            txt_0="Choose Display Background Color"
            txt_1="Choose Display Text Color"
        else:
            txt_0="Elegir Color de Fondo de la Pantalla"
            txt_1="Elegir Color del Texto de Vvisualización"
        _width = int(self.screen_width*0.3)
        _height = int(self.screen_height*0.5)
        _x = int(((self.screen_width // 2) - (_width // 2)) / self.scale_factor)
        _y = int(((self.screen_height // 2) - (_height // 2)) / self.scale_factor)
        if which=='fg_color':
            title=txt_0# Background Color
            init_color = self.Display_bg.get() 
        elif which=='text_color':# Foreground  
            title=txt_1# Text Color
            init_color = self.Display_fg.get() 
        dialog = AskColor(title=title, initial_color=init_color, bg_color="#009999", 
                        button_color="#0000ff", button_hover_color="#800000")
        dialog.geometry('%dx%d+%d+%d' % (_width, _height, _x, _y))
        dialog.after(250, dialog.wm_iconbitmap, self.ico_path)
        dialog.set_initial_color(self.Display_bg.get())
        dialog.default_hex_color=self.Display_bg.get()
        dialog.get_target_color()
        color_code = dialog.get()
        if color_code:
            if which=='fg_color':
                self.Display_bg.set(color_code)
                self.Display_Text.focus_force()
                self.Display_Text.configure(fg_color = self.Display_bg.get())
                self.Display_Text.configure(text_color=self.Display_fg.get())
            elif which=='text_color':# Foreground      
                self.Display_fg.set(color_code)
                self.Display_Text.focus_force()
                self.Display_Text.configure(fg_color = self.Display_bg.get())
                self.Display_Text.configure(text_color=self.Display_fg.get())
    def calculator_destroy(self):
        try:# X Icon Was Clicked
            self.give_greeting("close")
            sleep(2)
            self.write_setup()
            self.clear_memories()
            self.clear_all()
            self.Symbol_Names.clear()
            self.Symbol_Values.clear()
            self._MyClash.clear()
            self._MyConstants.clear()
            self.operators.clear()
            for widget in app.winfo_children():
                if isinstance(widget, ctk.CTkCanvas):widget.destroy()
                else:widget.destroy()
            os._exit(0)
        except:
            os._exit(0)
    def disp_update(self, txt, b=None):
        if txt!='clear':
            if txt==' = ' or self.Answer_Present.get():
                disp=self.Display.get()
                disp+=txt
                self.Display_Text.delete("0.0", "end")
                self.Display_Text.insert('end',disp)
                self.Display.set(disp)
                self.Disp_List.append(str(txt))
            elif txt=='refresh':    
                self.Display.set('')
                self.Display_Text.delete("0.0", "end")
                disp=''.join(self.Disp_List)
                disp2=str(disp).replace('{','').replace('}','')
                self.Display.set(disp2)
                self.Display_Text.insert('end',disp2)
            else:     
                self.Display.set('')
                self.Display_Text.delete("0.0", "end")
                self.Disp_List.append(str(txt))
                disp=''.join(self.Disp_List)
                disp2=str(disp).replace('{','').replace('}','')
                self.Display.set(disp2)
                self.Display_Text.delete("0.0", "end")
                self.Display_Text.insert('end',disp2)
                if b==None:
                    if txt=='(':self.bracket_clicked('auto','disp','open')
                    elif txt==')':self.bracket_clicked('auto','disp','close')
                if txt=='{':
                    td_open=self.Temp_Disp_Open.get()
                    td_open+=1
                    self.Temp_Disp_Open.set(td_open)
                elif txt=='}':
                    td_open=self.Temp_Disp_Open.get()
                    td_open-=1
                    self.Temp_Disp_Open.set(td_open)
        else:
            self.Display.set('')
            self.Display_Text.delete("0.0", "end")
            self.Disp_List.clear()
            self.bracket_clicked('manual','both','clear')
    def expr_update(self, txt, b=None):
        if txt!='clear':
            if txt==' = ' or self.Answer_Present.get():
                expr=self.Expression.get()
                expr+=txt
                self.Expression.set(expr)
                self.Expr_List.append(str(txt))
            elif txt=='refresh':    
                self.Expression.set('')
                expr=''.join(self.Expr_List)
                expr2=str(expr).replace('{','').replace('}','')
                self.Expression.set(expr2)
            else:     
                self.Expression.set('')
                self.Expr_List.append(str(txt))
                expr=''.join(self.Expr_List)
                expr2=str(expr).replace('{','').replace('}','')
                self.Expression.set(expr2)
                if b==None: 
                    if txt=='(':self.bracket_clicked('auto','expr','open')
                    elif txt==')':self.bracket_clicked('auto','expr','close')
                if txt=='{':
                    te_open=self.Temp_Expr_Open.get()
                    te_open+=1
                    self.Temp_Expr_Open.set(te_open)
                elif txt=='}':
                    te_open=self.Temp_Expr_Open.get()
                    te_open-=1
                    self.Temp_Expr_Open.set(te_open)
        else:
            self.Expression.set('')
            self.Expr_List.clear()
            self.bracket_clicked('manual','both','clear')
    def numeric_clicked(self, event):
        try:
            numeric_values=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
            if str(event) not in numeric_values:
                try:
                    if event.type=='2':text=event.char # KeyPress
                except:text = str(event)    
            else: text = str(event)    
            self.Display_Text.focus_force()    
            self.Display_Text.unbind('<period>')
            if text=='??': # Binding event Overrides Disabled State So Check State. If State = 'disabled' return
                if 'disabled' in event.widget.configure('state'):return
            elif text=='.' and not self.Disp_List:
                self.clear_all()
                return
            elif text=='.'and self.Disp_List[-1]=='.':
                disp=self.Display.get()
                self.Display_Text.delete("0.0", "end")
                self.Display_Text.insert('end',disp)
                self.Display.set(disp)
                return    
            if self.Answer_Present.get() and text=='.':return  
            if self.Answer_Present.get() or self.Answer_Err.get():self.clear_all()
            base=self.Base.get()
            self.Display_Text.focus_set()
            if base=='Decimal':
                text=str(text)    
                dec_values=['0','1','2','3','4','5','6','7','8','9']
                if text=='.':# Prevent Multiple Periods From Keyboard Entry
                    self.reverse_value('disp',False)
                    value=self.return_value('disp',False,True) 
                    if '.' in value:
                        text=''
                        self.Display_Text.focus_force()    
                        self.Display_Text.bind(('<period>'), lambda e: "break")
                        return
                    else:    
                        self.Display_Text.focus_force()    
                        self.Display_Text.unbind('<period>')
                    if self.Disp_List:
                        if not self.type_isnumerical(self.Disp_List[-1]):return       
                        if self.Disp_List[-1]=='.':return       
                        self.disp_update(text)
                        self.expr_update(text)
                elif text in dec_values:     
                    if self.Answer_Present.get() or self.Answer_Err.get():self.clear_all()
                    self.disp_update(text)
                    self.expr_update(text)
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
                if self.Answer_Present.get() or self.Answer_Err.get():self.clear_all()
                self.disp_update(text)
                self.Reversed_List.clear()
                opened=0
                closed=0
                if self.Disp_List:# Reverse Disp_List  But Do Not Pop
                    if self.Disp_List[-1]==')':# Value Inside Brackets
                        for i in list(reversed(self.Disp_List)):
                            if i=='(':opened+=1
                            if i==')':closed+=1
                            if i in active_values:self.Reversed_List.append(i)
                            if opened==closed:break
                    else:# No Brackets, Only Get Numbers    
                        for i in list(reversed(self.Disp_List)):
                            if i in active_values:self.Reversed_List.append(i)
                            else:break
                val2='' # Return Hex Sequence And Get Decimal Equalivent
                for i in list(reversed(self.Reversed_List)):
                    val2+=i
                if base=='Hexadecimal':value=str(Convert_Base(16,10,str(val2)))
                elif base=='Octal':value=str(Convert_Base(8,10,str(val2)))
                elif base=='Binary' or base=='Binario':value=str(Convert_Base(2,10,str(val2)))
                # Update Expr_List With New Value
                if self.Expr_List:
                    self.reverse_value('expr',True)
                    self.expr_update(value)
                else:self.expr_update(value)
        except Exception as e:
            return 'break'
    def set_numeric_type(self, value):
        try:
            float(value)
            status=float(value).is_integer()
            if status and '.' in str(value):return str(value) # Convert xx.0 To Integer xx
            elif status and not '.' in value:return str(int(value))# True Integer
            elif not status and 'e' in value:return str(mpf(value))# Scientific Notation
            elif not status and '.' in value:return str(mpf(value))# True Float
            else:return value   
        except Exception:return 'Invalid Type!'
    def type_isnumerical(self, instr):
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
    def clear_memories(self, txt):
        if txt == "CM":
            self.mem_btn[0].configure(text='ms1')
            self.mem_btn[0].configure(fg_color=('#ffff99', '#ffff99'))
            self.D_Memory1.clear()
            self.E_Memory1.clear()
            self.mem_btn[1].configure(text='ms2')
            self.mem_btn[1].configure(fg_color=('#ffff99', '#ffff99'))
            self.D_Memory2.clear()
            self.E_Memory2.clear()
            self.mem_btn[2].configure(text='ms3')
            self.mem_btn[2].configure(fg_color=('#ffff99', '#ffff99'))
            self.D_Memory3.clear()
            self.E_Memory3.clear()
            self.mem_btn[3].configure(text='ms4')
            self.mem_btn[3].configure(fg_color=('#ffff99', '#ffff99'))
            self.D_Memory4.clear()
            self.E_Memory4.clear()
    def memory_clicked(self, txt):
        try:
            orig_list=['ms1','ms2','ms3','ms4']
            if txt in orig_list:# Check For Button Text Change. Only Original Text Was Used For Binding
                for num in range(0,len(orig_list)):
                    if orig_list[num] == txt:
                        txt_now = self.mem_btn[num].cget("text")
                        break
            else:return        
            allowed=['^','**',', ']
            if self.Disp_List and self.Expr_List:
                if self.Answer_Present.get():
                    display_value=self.Disp_List[-1]
                    expression_value=self.Expr_List[-1]
                else:
                    disp_open=self.Disp_Bkts_Open.get()
                    expr_open=self.Expr_Bkts_Open.get()
                    if disp_open==0 and expr_open>0: # If Display Closed, Close Expression
                        for i in range(expr_open):
                            self.expr_update(')')
                    display_value=''.join(self.Disp_List)
                    expression_value=''.join(self.Expr_List)
            else:
                display_value=''
                expression_value=''    
            if txt_now=='ms1':
                self.D_Memory1.clear()
                self.E_Memory1.clear()
                if display_value!='':
                    for i in display_value:self.D_Memory1.append(i)
                    self.mem_btn[0].configure(text='mr1')
                    self.mem_btn[0].configure(fg_color=('#ffffff', '#ffffff'))
                if expression_value!='':
                    for i in expression_value:self.E_Memory1.append(i)
            elif txt_now=='ms2':
                self.D_Memory2.clear()
                self.E_Memory2.clear()
                if display_value!='':
                    for i in display_value:self.D_Memory2.append(i)
                    self.mem_btn[1].configure(text='mr2')
                    self.mem_btn[1].configure(fg_color=('#ffffff', '#ffffff'))
                if expression_value!='':
                    for i in expression_value:self.E_Memory2.append(i)
            elif txt_now=='ms3':
                self.D_Memory3.clear()
                self.E_Memory3.clear()
                if display_value!='':
                    for i in display_value:self.D_Memory3.append(i)
                    self.mem_btn[2].configure(text='mr3')
                    self.mem_btn[2].configure(fg_color=('#ffffff', '#ffffff'))
                if expression_value!='':
                    for i in expression_value:self.E_Memory3.append(i)
            elif txt_now=='ms4':
                self.D_Memory4.clear()
                self.E_Memory4.clear()
                if display_value!='':
                    for i in display_value:self.D_Memory4.append(i)
                    self.mem_btn[3].configure(text='mr4')
                    self.mem_btn[3].configure(fg_color=('#ffffff', '#ffffff'))
                if expression_value!='':
                    for i in expression_value:self.E_Memory4.append(i)
            if txt_now=='mr1':
                if not self.Disp_List and not self.Expr_List:
                    for i in range(len(self.D_Memory1)): 
                        self.disp_update(self.D_Memory1[i])
                    for i in range(len(self.E_Memory1)): 
                        self.expr_update(self.E_Memory1[i])
                else:    
                    if self.Disp_List[-1] == self.D_Memory1[-1] and self.Expr_List[-1] == self.E_Memory1[-1]:return
                    else:
                        if self.Disp_List[-1] not in self.operators and self.Disp_List[-1] not in allowed:return
                        else:    
                            for i in range(len(self.D_Memory1)): 
                                self.disp_update(self.D_Memory1[i])
                            for i in range(len(self.E_Memory1)): 
                                self.expr_update(self.E_Memory1[i])
            elif txt_now=='mr2':
                if not self.Disp_List and not self.Expr_List:
                    for i in range(len(self.D_Memory2)): 
                        self.disp_update(self.D_Memory2[i])
                    for i in range(len(self.E_Memory2)): 
                        self.expr_update(self.E_Memory2[i])
                else:    
                    if self.Disp_List[-1] == self.D_Memory2[-1] and self.Expr_List[-1] == self.E_Memory2[-1]:return
                    else:    
                        if self.Disp_List[-1] not in self.operators and self.Expr_List[-1] not in self.operators:return
                        else:    
                            for i in range(len(self.D_Memory2)): 
                                self.disp_update(self.D_Memory2[i])
                            for i in range(len(self.E_Memory2)): 
                                self.expr_update(self.E_Memory2[i])
            elif txt_now=='mr3':
                if not self.Disp_List and not self.Expr_List:
                    for i in range(len(self.D_Memory3)): 
                        self.disp_update(self.D_Memory3[i])
                    for i in range(len(self.E_Memory3)): 
                        self.expr_update(self.E_Memory3[i])
                else:    
                    if self.Disp_List[-1] == self.D_Memory3[-1] and self.Expr_List[-1] == self.E_Memory3[-1]:return
                    else:    
                        if self.Disp_List[-1] not in self.operators and self.Expr_List[-1] not in self.operators:return
                        else:    
                            for i in range(len(self.D_Memory3)): 
                                self.disp_update(self.D_Memory3[i])
                            for i in range(len(self.E_Memory3)): 
                                self.expr_update(self.E_Memory3[i])
            elif txt_now=='mr4':
                if not self.Disp_List and not self.Expr_List:
                    for i in range(len(self.D_Memory4)): 
                        self.disp_update(self.D_Memory4[i])
                    for i in range(len(self.E_Memory4)): 
                        self.expr_update(self.E_Memory1[4])
                else:    
                    if self.Disp_List[-1] == self.D_Memory4[-1] and self.Expr_List[-1] == self.E_Memory4[-1]:return
                    else:    
                        if self.Disp_List[-1] not in self.operators and self.Expr_List[-1] not in self.operators:return
                        else:    
                            for i in range(len(self.D_Memory4)): 
                                self.disp_update(self.D_Memory4[i])
                            for i in range(len(self.E_Memory4)): 
                                self.expr_update(self.E_Memory4[i])
        except Exception as e:
            if self.Language.get()=="English":
                title= f"{txt_now} Memory Error"
                msg1='Exception occurred while code execution:\n'
            else:
                title=f"{txt_now} Error de Memoria"  
                msg1="Ocurrió una excepción durante la ejecución del código:"  
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def sign_clicked(self, text):
        base=self.Base.get()
        if self.Answer_Present.get() or base!='Decimal':return
        if text != chr(177): return
        dbo,tdo,ebo,teo = self.Disp_Bkts_Open.get(), self.Temp_Disp_Open.get(), self.Expr_Bkts_Open.get(), self.Temp_Expr_Open.get() 
        # If Display Closed, Close Expression
        if dbo==0:
            for i in range(ebo):self.expr_update(')')
        if tdo==0:            
            for i in range(teo):self.expr_update('}')
        try:
            if self.Disp_List and self.Expr_List:
                # Open Brackets With Numeric End ,'-10.3'(10.3' or Is Constant Or % 
                if self.Disp_List[-1].isdecimal() and self.Expr_List[-1].isdecimal() or self.Disp_List[-1] in self._MyConstants and \
                    self.Expr_List[-1] in self._MyConstants or self.Disp_List[-1]=='%': # Change Sign For Value Not Enclosed In Brackets
                    allowed=['-','.','%']
                    for l in range(2): # Do Both List
                        if l==0:active_list=self.Disp_List
                        elif l==1:active_list=self.Expr_List     
                        n=len(active_list)        
                        for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10' 
                            if i.isdecimal() or i in allowed or i in self._MyConstants:n-=1
                            else:break
                        if active_list[n]!='-':active_list.insert(n,'-')
                        elif active_list[n]=='-':active_list.pop(n)
                        if l==0:self.disp_update('refresh')        
                        elif l==1:self.expr_update('refresh')        
                    return        
                elif self.Disp_List[-1]==')' and self.Expr_List[-1]==')': # Change Sign For Values Inside Parentheses
                    bkt_opened,bkt_closed=0,0
                    for l in range(2): # Do Both List
                        if l==0:active_list=self.Disp_List
                        elif l==1:active_list=self.Expr_List     
                        n=len(active_list)        
                        for i in list(reversed(active_list)): # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                            n-=1
                            if i==')':bkt_closed+=1
                            elif i=='(':bkt_opened+=1
                            if bkt_opened==bkt_closed:
                                if i=='(':
                                    if active_list[n-1]!='-':active_list.insert(n,'-')
                                    elif active_list[n-1]=='-':active_list.pop(n-1)
                                    if l==0:self.disp_update('refresh')        
                                    elif l==1:self.expr_update('refresh')        
                                    break
                    return        
                elif self.Disp_List[-1]=='}' and self.Expr_List[-1]=='}': # Change Sign For Completed Functions Inside Temp Brackets
                    for l in range(2): # Do Both List
                        if l==0:active_list=self.Disp_List
                        elif l==1:active_list=self.Expr_List     
                        n=len(active_list)        
                        closed,opened=0,0        
                        for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                            n-=1
                            if i=='}':closed+=1
                            elif i=='{':opened+=1
                            if i=='{' and closed==opened:
                                if active_list[n+1]!='-':active_list.insert(n+1,'-')
                                elif active_list[n+1]=='-':active_list.pop(n+1)
                                if l==0:self.disp_update('refresh')        
                                elif l==1:self.expr_update('refresh')        
                                break
                    return                
        except:pass
    def operator_clicked(self, event):
        try:
            operator_values=[' / ',' * ',' - ',' + ']
            if str(event) not in operator_values:
                if event.type=='2':text=event.char # Key Press
            else: text = str(event)# Button Press    
            if not self.Disp_List:return
            if self.Disp_List[-1] in self.operators:return # Prevent Multiple operators
            disp_open=self.Disp_Bkts_Open.get()
            expr_open=self.Expr_Bkts_Open.get()
            if not disp_open and expr_open:self.bracket_clicked('manual','expr','close')
            if not self.Answer_Err.get():
                self.disp_update(text)
                self.expr_update(text)
                if self.Answer_Present.get():# Answer Becomes 1st Entry, Operator Becomes Second Entry
                    answer=self.Answer.get()
                    self.clear_all()# Start Fresh
                    self.disp_update(answer)
                    self.disp_update(text)
                    base=self.Base.get() # If Base = Hex, Convert Expression Answer To Decimal
                    if base=='Hexadecimal':answer=str(Convert_Base(16,10,str(answer)))
                    elif base=='Octal':answer=str(Convert_Base(8,10,str(answer)))
                    elif base=='Binary' or base=='Binario':answer=str(Convert_Base(2,10,str(answer)))
                    self.expr_update(answer)
                    self.expr_update(text)
        except Exception as e:
            if self.Language.get()=="English":
                title=f"Operator Clicked {text}"
                msg1=f'Exception occurred while code execution {self.Math_Function.get()}:\n'
            else:    
                title=f"Operador hizo clic {text}"
                msg1=f'Ocurrió una excepción durante la ejecución del código {self.Math_Function.get()}:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def is_float(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    def reverse_value(self, which, pop):
        self.Reversed_List.clear()
        if not self.Disp_List:return
        if not self.Expr_List:return
        try:
            active_list=[]
            if which=='disp':active_list=self.Disp_List
            elif which=='expr':active_list=self.Expr_List
            # Populate With Value (Exposed) Not Enclosed In Brackets
            if active_list[-1].isdecimal() or self.is_float(active_list[-1]) or active_list[-1] in self._MyConstants  or active_list[-1]=='%':
                allowed=['-','.','%']
                for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10', ', 10'
                    if i.isdecimal() or self.is_float(i) or i in allowed or i in self._MyConstants or i in self.Hex_List:
                        self.Reversed_List.append(i)
                        if pop:active_list.pop()
                    else:break
                return ''.join(self.Reversed_List)
            elif active_list[-1]==')': # Values Inside Parentheses (Rounded Brackets).
                bkt_opened,bkt_closed=0,0
                for i in list(reversed(active_list)):  # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                    self.Reversed_List.append(i)
                    if pop:active_list.pop()
                    if i==')':bkt_closed+=1
                    elif i=='(':bkt_opened+=1
                    if bkt_opened==bkt_closed:break
                return ''.join(self.Reversed_List)
            elif active_list[-1]=='}': # Value Is Completed Function Inside Temp Brackets
                bkt_opened,bkt_closed=0,0
                for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                    self.Reversed_List.append(i)
                    if pop:active_list.pop()
                    if i=='}':bkt_closed+=1
                    elif i=='{':bkt_opened+=1
                    if bkt_opened==bkt_closed:break
                return ''.join(self.Reversed_List)
        except:pass
    def return_value(self, which, update, bracket):
        try:
            value=''
            for i in list(reversed(self.Reversed_List)):value+=i
            if value[0]!='{' and value[-1]!='}': # Value Not Enclosed In {}
                if value[0]!='(' and value[-1]!=')': # Value Not Enclosed In ()
                    if bracket:value='('+value+')' # Bracket value With ()
                    if update:
                        if which=='disp':
                            for element in value:self.disp_update(element,'Some')
                        elif which=='expr':    
                            for element in value:self.expr_update(element,'Some')
                    return value
                elif value[0]=='(' and value[-1]==')': # Value Enclosed In ()
                    if update:
                        if which=='disp':        
                            for element in value:self.disp_update(element,'Some')
                        elif which=='expr':    
                            for element in value:self.expr_update(element,'Some')
                    return value
                else: # Something Else    
                    if update:
                        if which=='disp':        
                            for element in value:self.disp_update(element,'Some')
                        elif which=='expr':    
                            for element in value:self.expr_update(element,'Some')
                    return value
            else: # Value Enclosed With {}     
                if update:
                    if which=='disp':
                        for element in value:self.disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:self.expr_update(element,'Some')
                return value
        except:pass
    def open_temp_bracket(self, which): # Only Used To Increment Unfinished Function Brackets
        if which=='disp':
            td_open=self.Temp_Disp_Open.get()
            td_open+=1
            self.Temp_Disp_Open.set(td_open)
        elif which=='expr':
            te_open=self.Temp_Expr_Open.get()
            te_open+=1
            self.Temp_Expr_Open.set(te_open)
    def close_brackets(self, which): # Close Unfinished Function Brackets
        if which=='all' or which=='disp':
            disp_open=self.Disp_Bkts_Open.get()
            if disp_open>0:
                for b in range(0,disp_open):
                    self.disp_update(')')
        if which=='all' or which=='expr':            
            expr_open=self.Expr_Bkts_Open.get()
            if expr_open>0:
                for b in range(0,expr_open):
                    self.expr_update(')')
        if which=='all' or which=='temp_disp':    
            td_open=self.Temp_Disp_Open.get()
            if td_open>0:
                for b in range(0,td_open):
                    self.disp_update('}')
        if which=='all' or which=='temp_expr':            
            te_open=self.Temp_Expr_Open.get()
            if te_open>0:
                for b in range(0,te_open):
                    self.expr_update('}')
    def function_check(self, val):# Prevents Decimal Functions From Trying To Be Converted To Another Base.
        val=str(val)
        list1=['sin','cos','tan','sec','csc','cot','sinh','cosh','tanh','sech','csch','coth']
        list2=['asin','acos','atan','asec','acsc','acot','asinh','acosh','atanh','asech','acsch','acoth']
        list3=['log𝒆','log₁₀','log','1 / ','^','**','ʸ√','²√','³√','n!']
        for item in list1:
            for value in self.Disp_List:
                if item in value:return True
        for item in list2:
            for value in self.Disp_List:
                if item in value:return True
        for item in list3:
            for value in self.Disp_List:
                if item in value:return True
        return False        
    def funct_clicked(self, txt):
        txt=txt.replace(" ","")
        base=self.Base.get()
        if base!='Decimal':return
        if txt=='':return
        if self.Answer_Err.get():return
        try:
            answer_was_present=False
            if self.Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
                answer=self.Answer.get()
                self.clear_all()
                answer_was_present=True
                for i, item in enumerate(answer):
                    self.disp_update(item)
                    self.expr_update(item)
            funct=txt
            if self.Math_Function.get()=='':self.Last_Function.set(txt)
            else:self.Last_Function.set(self.Math_Function.get())    
            self.Math_Function.set(txt)
            if self.Disp_List:# Prevent Double Constants
                if txt in self._MyConstants and self.Disp_List[-1] in self._MyConstants:return
            # Functions Requiring Data Entry First 
            if funct=='1/𝓧':
                if not self.Disp_List:return
                if self.Disp_List[-1] in self.operators:return       
                self.reverse_value('disp',True) # Display 
                self.disp_update('{')
                self.disp_update('(')
                self.disp_update('1')    
                self.disp_update(' / ')
                value=self.return_value('disp',True,False) 
                self.disp_update(')')
                self.disp_update('}')
                self.reverse_value('expr',True) # Expression
                self.expr_update('{')
                self.expr_update('(')
                self.expr_update('1')    
                self.expr_update(' / ')
                value=self.return_value('expr',True,True)
                self.expr_update(')')
                self.expr_update('}')
            elif funct=='𝓧ʸ':# Expression = x**y, Display = x^y
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in self._MyConstants:
                    self.reverse_value('disp',True) # Display
                    self.disp_update('{')
                    self.disp_update('(')
                    self.return_value('disp',True,False)
                    self.disp_update('^')
                    self.reverse_value('expr',True) # Expression
                    self.expr_update('{')
                    self.expr_update('(')
                    self.value=self.return_value('expr',True,False)
                    self.expr_update('**')
            elif funct=='𝓧²' or funct=='𝓧³':
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in self._MyConstants:
                    self.reverse_value('disp',True) # Display
                    self.disp_update('{')
                    self.disp_update('(')
                    value=self.return_value('disp',True,False)
                    self.disp_update('^')
                    if funct=='𝓧²':self.disp_update('2')
                    if funct=='𝓧³':self.disp_update('3')
                    self.disp_update(')')
                    self.disp_update('}')
                    self.reverse_value('expr',True)
                    self.expr_update('{')
                    self.expr_update('(')
                    value=self.return_value('expr',True,False)
                    self.expr_update('**')
                    if funct=='𝓧²':self.expr_update('2')
                    if funct=='𝓧³':self.expr_update('3')
                    self.expr_update(')')
                    self.expr_update('}')
            elif funct=='ʸ√':# mpMath = app(x, y), Simplified = x**(1 / y), Display = ʸ√(x, y)
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in self._MyConstants:
                    self.reverse_value('disp',True) # Display
                    if self.Disp_List and self.Disp_List[-1]=='(':bracket=True
                    else:bracket=False
                    self.disp_update('{')
                    self.disp_update('ʸ√')
                    if not bracket:self.disp_update('(')
                    value=self.return_value('disp',True,False) 
                    self.disp_update(', ')
                    self.reverse_value('expr',True) # Expression
                    if self.Expr_List and self.Expr_List[-1]=='(':bracket=True
                    else:bracket=False
                    self.expr_update('{')
                    self.expr_update('(')
                    value=self.return_value('expr',True,True)
                    self.expr_update('**')
                    self.expr_update('(')
                    self.expr_update('1')
                    self.expr_update(' / ')
            elif funct=='²√'or funct=='³√':#sympify = x**(1 / 2), Display = ²√x, sympify = x**(1 / 3), Display = ³√x
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in self._MyConstants:
                    self.reverse_value('disp',True) # Display
                    self.disp_update('{')
                    self.disp_update(txt)
                    value=self.return_value('disp',True,True)
                    self.disp_update('}')
                    self.reverse_value('expr',True) # Expression
                    self.expr_update('{')
                    self.expr_update('(')
                    value=self.return_value('expr',True,True)
                    self.expr_update('**') 
                    self.expr_update('(')
                    self.expr_update('1')
                    self.expr_update(' / ')
                    if funct=='²√':self.expr_update(' 2 ')
                    if funct=='³√':self.expr_update(' 3 ')
                    self.expr_update(')')
                    self.expr_update(')')
                    self.expr_update('}')
            elif funct=='n!': # Factorial Of n where n Is Natural Number And Positive, expr=factorial(n)
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in self._MyConstants:
                    self.reverse_value('disp',True) # Display
                    self.disp_update('{')
                    self.disp_update('fact')
                    value=self.return_value('disp',True,True)
                    self.disp_update('}')
                    self.reverse_value('expr',True) # Expression
                    self.expr_update('{')
                    self.expr_update('(')
                    self.expr_update('factorial')
                    value=self.return_value('expr',True,True)
                    self.expr_update(')')
                    self.expr_update('}')
            elif funct=='%':
                if not self.Disp_List:return
                if self.Disp_List[-1] in self.operators:return
                if not self.Disp_List[-1].isdecimal() or self.Disp_List[-1] in self._MyConstants:return        
                self.disp_update('%') # Display
                self.reverse_value('expr',True) # Expression
                value=self.return_value('disp',False,True)
                expr=str(value+' * 0.01')    
                expr=parse_expr(expr, evaluate=False)# Change Reversed_List To Percent
                f=str(expr.evalf())
                for i in f:self.expr_update(i)# Recreate Expr_List With Calculated Percent
            elif funct=='mod':# a % b, remainder, expr = Mod(100, 21)= 16, Display = Mod(100, 21)
                if not self.Disp_List:return
                self.reverse_value('disp',True) # Display
                self.disp_update('{')
                self.disp_update('mod')
                self.disp_update('(')
                value=self.return_value('disp',True,False)
                if value=='break':
                    self.mod_btn.configure(state="normal")
                    return
                self.disp_update(' / ')
                self.reverse_value('expr',True) # Expression
                self.expr_update('{')
                self.expr_update('Mod')
                self.expr_update('(')
                value=self.return_value('expr',True,False)
                self.expr_update(', ')
            elif funct=='exp':# Scientific Notation
                if not self.Disp_List:return
                if self.type_isnumerical(self.Disp_List[-1]):
                    self.reverse_value('disp',True)
                    val1=self.return_value('disp',False,True)# Do Not Update
                    val2=str(val1).replace('{','').replace('}','').replace('(','').replace(')','') # Remove Temp Brackets For Examination
                    value=np.format_float_scientific(mpf(val2), unique=False, precision=self.Exp_Precision.get(), exp_digits=self.Exp_Digits.get())            
                    self.disp_update(value)
                    self.reverse_value('expr',True)
                    self.expr_update(value)
            elif funct in self._MyConstants: # Constants
                if self.Disp_List: # End Strip All Brackets For Examination
                    allowed=['^','**',', ']
                    val=''.join(self.Disp_List)
                    val2 = str(val).replace('{','').replace('}','').replace('(','').replace(')','')
                    if val2!='':
                        if txt in self._MyConstants:
                            if val2[-1] in allowed or self.Disp_List[-1] in self.operators or self.Disp_List[-1] in allowed:
                                pass
                            else:
                                if not answer_was_present:return
                        else:return
                if funct=='Π₂':
                    self.disp_update(txt)
                    self.expr_update('Π')
                    parsed=parse_expr('Π')
                else:
                    if answer_was_present:self.clear_all()
                    self.disp_update(txt)
                    self.expr_update(txt)
                    parsed=parse_expr(txt, evaluate=False)
                    self.Symbol_Names.append(parsed)
                    if funct=='𝓔':self.Symbol_Values.append(mp.euler)
                    elif funct=='π':self.Symbol_Values.append(mp.pi)
                    elif funct=='𝜯':self.Symbol_Values.append(2*mp.pi)
                    elif funct=='𝜱':self.Symbol_Values.append(mp.phi)
                    elif funct=='𝑮':self.Symbol_Values.append(mp.catalan)
                    elif funct=='𝜁3':self.Symbol_Values.append(mp.apery)
                    elif funct=='𝑲':self.Symbol_Values.append(mp.khinchin)
                    elif funct=='𝑨':self.Symbol_Values.append(mp.glaisher)
                    elif funct=='𝑴':self.Symbol_Values.append(mp.mertens)
                    elif funct=='Π₂':self.Symbol_Values.append(mp.twinprime)
                    elif funct=='𝒆':self.Symbol_Values.append(mp.e)
        except Exception as e:
            if self.Language.get()=="English":
                title=f"Function {funct} Error"
                msg1=f'Exception occurred while code execution {funct}:\n'
            else:
                title=f"Error en la Función {funct}"
                msg1=f'Se produjo una excepción durante la ejecución del código {funct}:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def trig_clicked(self, txt):
        orig_list=['sin','sec','cos','csc','tan','cot']
        if txt in orig_list:# Check For Button Text Change. Only Original Text Was Used For Binding
            for num in range(0,len(orig_list)):
                if orig_list[num] == txt:
                    txt_now = self.trig_btn[num].cget("text")
                    break
        else:return        
        base=self.Base.get()
        if base!='Decimal':return
        if not self.Disp_List:return
        if self.Disp_List[-1]=='^':return
        if self.Disp_List[-1] in self.operators:return
        try:       
            if self.Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
                answer=self.Answer.get()
                self.clear_all()
                self.disp_update(answer)
                self.expr_update(answer)
            unit=self.Trig_Units.get()
            if unit=='Radians' or unit=='Radianes':unit_txt='ʳ'
            elif unit=='Degrees' or unit=='Grados':unit_txt='ᵈ'
            elif unit=='Gradians' or unit=='Gradianos':unit_txt='ᵍ'
            if self.Math_Function.get()=='':self.Last_Function.set(txt_now)
            else:self.Last_Function.set(self.Math_Function.get())    
            self.Math_Function.set(txt_now)
            # Display
            self.reverse_value('disp',True)
            self.disp_update('{')
            self.disp_update(txt_now+unit_txt)
            disp_value=self.return_value('disp',False,False)
            bkt=False
            if disp_value[0]=='{' and disp_value[-1]=='}':
                if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
            elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
            if not bkt:self.disp_update('(')
            self.disp_update(disp_value)
            if not bkt:self.disp_update(')')
            self.disp_update('}')
            # Expression
            self.reverse_value('expr',True)
            self.expr_update('{')
            self.expr_update(txt_now)
            expr_value=self.return_value('expr',False,True)
            if unit=='Radians' or unit=='Radianes':
                self.expr_update(expr_value)
                self.expr_update('}')
                return
            if txt_now[0]!='a': # (No arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
                if unit=='Degrees' or unit=='Grados':# {sin(40 * (pi / 180))}, {sin((20 + 20) * (pi / 180))}
                    parsed=parse_expr('rad_to_deg', evaluate=False)
                    self.Symbol_Names.append(parsed)
                    self.Symbol_Values.append(mp.pi/180)
                    self.expr_update('(')
                    self.expr_update(expr_value)
                    self.expr_update(' * ')
                    self.expr_update('rad_to_deg')
                    self.expr_update(')')
                elif unit=='Gradians' or unit=='Gradianos':# {sin(40 * (pi / 200))}, {sin((20 + 20) * (pi / 200))}          
                        parsed=parse_expr('rad_to_grad', evaluate=False)
                        self.Symbol_Names.append(parsed)
                        self.Symbol_Values.append(mp.pi/200)
                        self.expr_update('(')
                        self.expr_update(expr_value)
                        self.expr_update(' * ')
                        self.expr_update('rad_to_grad')
                        self.expr_update(')')
            elif txt_now[0]=='a': # (arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
                if unit=='Degrees' or unit=='Grados':
                    parsed=parse_expr('arc_rad_to_deg', evaluate=False)
                    self.Symbol_Names.append(parsed)
                    self.Symbol_Values.append(180/mp.pi)
                    self.expr_update(expr_value)
                    self.expr_update(' * ')
                    self.expr_update('arc_rad_to_deg')
                elif unit=='Gradians' or unit=='Gradianos':          
                    parsed=parse_expr('arc_rad_to_grad', evaluate=False)
                    self.Symbol_Names.append(parsed)
                    self.Symbol_Values.append(200/mp.pi)
                    self.expr_update(expr_value)
                    self.expr_update(' * ')
                    self.expr_update('arc_rad_to_grad')
            self.expr_update('}')
        except Exception as e:
            if self.Language.get()=="English":
                title=f"Trigonometry {self.Math_Function.get()} Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title=f"Error de Trigonometría {self.Math_Function.get()}"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def log_clicked(self, text):
        base=self.Base.get()
        if base!='Decimal':return
        if not self.Disp_List:return
        if self.Disp_List[-1]=='^' or self.Disp_List[-1]==', ':return
        if self.Disp_List[-1] in self.operators:return
        try:       
            if self.Answer_Present.get():# For Only Functions That Require Entry Before Function Click.
                answer=self.Answer.get()
                self.clear_all()
                self.disp_update(answer)
                self.expr_update(answer)
            if self.Math_Function.get()=='':self.Last_Function.set(text)
            else:self.Last_Function.set(self.Math_Function.get())    
            self.Math_Function.set(text)
            if text=='log𝒆':text='log𝒆'     
            elif text=='log10':text='log₁₀'     
            elif text=='log(x,b)':text='log'
            # Display
            ret=self.reverse_value('disp',True)
            self.disp_update('{')
            self.disp_update(text)
            disp_value=self.return_value('disp',False,False)# Only Return Value
            bkt=False
            if disp_value[0]=='{' and disp_value[-1]=='}':
                if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
            elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
            # Expression
            self.reverse_value('expr',True)
            self.expr_update('{')
            self.expr_update('log')
            expr_value=self.return_value('expr',False,True)# Only Return Value
            if text=='log𝒆':    
                if not bkt:self.disp_update('(')
                self.disp_update(disp_value)
                if not bkt:self.disp_update(')')
                self.disp_update('}')
                self.expr_update(expr_value)
                self.expr_update('}')
            elif text=='log₁₀':
                if not bkt:self.disp_update('(')
                self.disp_update(disp_value)
                if not bkt:self.disp_update(')')
                self.disp_update('}')
                self.expr_update('(')
                self.expr_update(expr_value)
                self.expr_update(', ')
                self.expr_update('10')
                self.expr_update(')')
                self.expr_update('}')
            elif text=='log': #'log(x,b)'
                self.disp_update('(')
                self.disp_update(disp_value)
                self.disp_update(', ')
                self.expr_update('(')
                self.expr_update(expr_value)
                self.expr_update(', ')
        except Exception as e:
            if self.Language.get()=="English":
                title=f"Logarithmic Function {self.Math_Function.get()} Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title=f"Error de Función Logarítmica {self.Math_Function.get()}"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def select_distance(self, event):
        commands=[]
        for c in range(len(self.Distance_List)):
            commands.append(c)
            commands[c] = lambda arg=self.Distance_List[c]: self.update_distance_btn(arg)
        x = self.winfo_pointerx() - ((70 / self.width) * self.width)
        y = self.winfo_pointery() - self.height
        self.popup_menu = MyPopupMenu(self, caption_list=self.Distance_List ,command_list=commands, font_size=16, x_pos=x, y_pos=y)
        self.wait_window(self.popup_menu)
        self.popup_menu.grab_release()
        self.popup_menu.destroy()
        if not self.Disp_List:return
        else:self.distance_clicked()
    def update_distance_btn(self, txt):
        self.us_metric_btn.configure(text=txt)       
        self.US_Metric.set(txt)
    def distance_clicked(self):
        base=self.Base.get()
        if base!='Decimal':return
        txt=self.us_metric_btn.cget("text")
        if not self.Disp_List:return
        try:
            if self.Answer_Present.get():
                newval=self.Answer.get()
                self.Answer_Present.set(False)
                self.disp_update('clear')
                self.expr_update('clear')
                self.disp_update(str(newval))
                self.expr_update(str(newval))
            self.reverse_value('expr',True)
            if txt in self.Distance_List:
                index = self.Distance_List.index(txt)
                display_txt=txt.split(" → ")[0]
                self.disp_update(f' {display_txt}')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(self.Distance_Math[index])
                self.expr_update(')')
            self.equal_clicked(txt)
        except Exception as e:
            if self.Language.get()=="English":
                title="US/Metric Conversion Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title="Error de Conversión de EE.UU./Métrico"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def select_temps(self, event):
        commands=[]
        for c in range(len(self.Temp_List)):
            commands.append(c)
            commands[c] = lambda arg=self.Temp_List[c]: self.update_temp_btn(arg)
        x = self.winfo_pointerx() - ((70 / self.width) * self.width)
        y = self.winfo_pointery() - self.height
        self.popup_menu = MyPopupMenu(self, caption_list=self.Temp_List ,command_list=commands, font_size=16, x_pos=x, y_pos=y)
        self.wait_window(self.popup_menu)
        self.popup_menu.grab_release()
        self.popup_menu.destroy()
        if not self.Disp_List:return
        else:self.temp_clicked()
    def update_temp_btn(self, txt):
        self.temp_btn.configure(text=txt)       
        self.Selected_Temp.set(txt)
    def temp_clicked(self):
        base=self.Base.get()
        if base!='Decimal':return
        txt=self.temp_btn.cget("text")
        if not self.Disp_List:return
        try:
            if self.Answer_Present.get():
                newval=self.Answer.get()
                self.Answer_Present.set(False)
                self.disp_update('clear')
                self.expr_update('clear')
                self.disp_update(str(newval))
                self.expr_update(str(newval))
            self.reverse_value('expr',True)
            if txt=='°F → °C':
                self.disp_update(' °F')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' - 32) * (5 / 9')
                self.expr_update(')')
            elif txt=='°F → °K':#K = (°F - 32) × 5/9 + 273.15. 
                self.disp_update(' °F')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' - 32) * (5 / 9')
                self.expr_update(')')
                self.expr_update(' + 273.15')
            elif txt=='°F → °R':# F + 459.67
                self.disp_update(' °F')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' + 459.67')
                self.expr_update(')')
            elif txt=='°C → °F':
                self.disp_update(' °C')
                self.expr_update('32 + ')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' / (5 / 9)')
                self.expr_update(')')
            elif txt== '°C → °K':# C + 273.15 
                self.disp_update(' °C')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update('+ 273.15')
                self.expr_update(')')
            elif txt== '°C → °R':# C * 9/5 + 491.67
                self.disp_update(' °C')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' * (9 / 5')
                self.expr_update(')')
                self.expr_update(' + 491.67')
                self.expr_update(')')
            elif txt=='°K → °C':# K − 273.15
                self.disp_update(' °K')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update('- 273.15')
                self.expr_update(')')
            elif txt=='°K → °F':#K − 273.15) × 9/5 + 32
                self.disp_update(' °K')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' - 273.15) * (9 / 5')
                self.expr_update(')')
                self.expr_update(' + 32')
            elif txt=='°K → °R':# K * 9/5
                self.disp_update(' °K')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' * 9 / 5')
                self.expr_update(')')
            elif txt=='°R → °C':# R − 491.67) × 5/9
                self.disp_update(' °R')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' - 491.67')
                self.expr_update(')')
                self.expr_update(' * (5 / 9)')
            elif txt== '°R → °F':# R − 459.67
                self.disp_update(' °R')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update('- 459.67')
                self.expr_update(')')
            elif txt== '°R → °K':# R * 5 / 9
                self.disp_update(' °R')
                self.expr_update('(')
                self.return_value('expr',True,True) 
                self.expr_update(' * (5 / 9)')
                self.expr_update(')')
            self.equal_clicked(txt)
        except Exception as e:
            if self.Language.get()=="English":
                title="Temperature Conversion Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title="Error de Conversión de Temperatura"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def bracket_clicked(self, how, which, status):
        if self.Answer_Present.get():return# Brackets Not Allowed If Answer Present
        if self.Answer_Err.get():return
        if  self.Disp_List and self.Disp_List[-1]=='^' and status=='close':return
        if status=='close' and self.Disp_List[-1]=='(':
            disp=self.Display.get()
            self.Display_Text.delete("0.0", "end")
            self.Display_Text.insert('end',disp)
            self.Display.set(disp)
            return    
        unwanted_list=['-','.',',','!',')']
        disp_open=self.Disp_Bkts_Open.get()
        expr_open=self.Expr_Bkts_Open.get()
        try:
            # Avoid Unwanted Brackets
            if status=='open':
                if which=='disp' or which=='both':
                    if self.Disp_List:
                        if self.type_isnumerical(self.Disp_List[-1]) or self.Disp_List[-1] in unwanted_list:
                            if self.Disp_List[-1]!='^':return
            elif status=='close' and how!='auto':
                if which=='disp' or which=='both':
                    if self.Disp_List:
                        early_list=['(','.',',']
                        if self.Disp_List[-1]in early_list:return
                        if disp_open==0:return
            elif status=='clear': # Reset Brackets To Zero
                if which=='disp' or which=='both':
                    self.Disp_Bkts_Open.set(0)
                    self.Temp_Disp_Open.set(0)
                    self.open_btn.configure(text='('+(self.convert_script(self.Normal_Script, self.Super_Script, '0')))# Convert To Superscript And Update Button
                if which=='expr' or which=='both':
                    self.Expr_Bkts_Open.set(0)
                    self.Temp_Expr_Open.set(0)
                return
            if how=='manual': # Brackets Entered Manually By Click. Add Bracket And Increase Or Decrease Count   
                if which=='disp' or which=='both':
                    disp_open=self.Disp_Bkts_Open.get()
                    if status=='open':# Create New '('
                        disp_open+=1
                        self.disp_update('(','Some')
                        self.Disp_Bkts_Open.set(disp_open)
                    elif status=='close':# Create New ')'
                        if disp_open > 0:
                            self.disp_update(')','Some')
                            disp_open-=1
                            self.Disp_Bkts_Open.set(disp_open)
                            disp_open=self.Disp_Bkts_Open.get()
                            td_open=self.Temp_Disp_Open.get()
                            if td_open>0 and disp_open==0:self.close_brackets('temp_disp')
                    disp_open=self.Disp_Bkts_Open.get()
                    self.open_btn.configure(text='('+(self.convert_script(self.Normal_Script, self.Super_Script, str(disp_open))))# Convert To Superscript And Update Button
                if which=='expr' or which=='both':
                    expr_open=self.Expr_Bkts_Open.get()
                    if status=='open':# Create New '('
                        expr_open+=1
                        self.expr_update('(','Some')
                        self.Expr_Bkts_Open.set(expr_open)
                    elif status=='close':# Create New ')'
                        if expr_open > 0:
                            self.expr_update(')','Some')    
                            expr_open-=1
                            self.Expr_Bkts_Open.set(expr_open)
                            expr_open=self.Expr_Bkts_Open.get()
                            disp_open=self.Disp_Bkts_Open.get()
                            if disp_open==0:
                                for i in range(expr_open):
                                    expr=self.Expression.get()
                                    self.expr_update(')','Some')
                                    expr_open-=1
                                    self.Expr_Bkts_Open.set(expr_open)
                                td_open=self.Temp_Expr_Open.get()
                                if td_open>0 and expr_open==0:self.close_brackets('temp_expr')
            elif how=='auto': # Brackets Entered Automatically By Expression. Only Increase Or Decrease Count.
                if which=='disp' or which=='both':
                    disp_open=self.Disp_Bkts_Open.get()
                    if status=='open':# Increase open count
                        disp_open+=1
                    elif status=='close':# Decrease open count 
                        if disp_open > 0:
                            disp_open-=1
                    self.Disp_Bkts_Open.set(disp_open)
                    self.open_btn.configure(text='('+(self.convert_script(self.Normal_Script, self.Super_Script, str(disp_open))))# Convert To Superscript And Update Button
                if which=='expr' or which=='both':
                    expr_open=self.Expr_Bkts_Open.get()
                    if status=='open':expr_open+=1 # Increase open count
                    elif status=='close':
                        if expr_open > 0:expr_open-=1 # Decrease open count
                    self.Expr_Bkts_Open.set(expr_open)
        except Exception as e:
            if self.Language.get()=="English":
                title="Bracket Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title="Error de Corchete"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def equal_clicked(self, event):
        if not self.Disp_List:return
        if self.Answer_Err.get():return
        if self.Disp_List[-1]==' = ':return
        expr=self.Expression.get()
        self.close_brackets('all')# (Just In Case) Close All Opened Brackets Before continuing
        if event in self.Distance_List or event in self.Temp_List:
            txt=event.split(" →")[1]
        else:txt=""
        sub_dict={}
        for i in range(len(self.Symbol_Names)):
            sub_dict[self.Symbol_Names[i]] = self.Symbol_Values[i]
        if not self.Answer_Present.get():
            try:
                expr=self.Expression.get()
                exp=parse_expr(expr, evaluate=True)
                expr_answer=exp.evalf(mp.dps, subs=sub_dict)
                if not expr in self._MyConstants:answer=self.nround_answer(expr_answer)
                else:
                    answer=str(expr_answer)
                if answer!='' or answer!=None:# Required 2 Entries (= And Answer)
                    answer=self.set_numeric_type(answer) # Test For Valid Answer
                    newval=answer
                    self.disp_update(' = ')
                    self.expr_update(' = ')
                    if newval!='Invalid Type!'and newval!='Type is Imaginary Literal!':
                        base=self.Base.get()
                        if base=='Decimal':
                            self.Answer.set(newval)
                        elif base=='Hexadecimal':
                            hex=str(Convert_Base(10,16,str(newval)))
                            self.Answer.set(hex)
                        elif base=='Octal':
                            oct=str(Convert_Base(10,8,str(newval)))
                            self.Answer.set(oct)
                        elif base=='Binary' or base=='Binario':
                            bin=str(Convert_Base(10,2,str(newval)))
                            self.Answer.set(bin)
                        self.Answer_Present.set(True)
                        self.Answer_Err.set(False)
                        self.disp_update(f'{self.Answer.get()}{txt}')
                        self.expr_update(self.Answer.get())
                    else:    
                        self.Answer.set('')
                        self.Answer_Present.set(False)
                        self.Answer_Err.set(True)
                        self.disp_update(str(newval))
                        self.expr_update(str(newval))
                self.Math_Function.set('')
            except Exception as e:
                self.Answer.set('')
                self.Answer_Present.set(False)
                self.Answer_Err.set(True)
                if self.Language.get()=="English":
                    self.disp_update(' = Invalid Entry!')
                    self.expr_update(' = Invalid Entry!')
                else:    
                    self.disp_update(' = ¡Entrada no válida!')
                    self.expr_update(' = ¡Entrada no válida!')
                return 'break'
    def config_base(self, base):
        self.Base.set(base)
        if base=='Binary' or base=='Binario':
            self.base_btn[0].configure(fg_color='white', text_color='navy')
            self.base_btn[1].configure(fg_color='navy', text_color='white')
            self.base_btn[2].configure(fg_color='navy', text_color='white')
            self.base_btn[3].configure(fg_color='navy', text_color='white')
            for num in range(0,2):
                self.num_btn[num].configure(state="normal")
            for num in range(2,16):
                self.num_btn[num].configure(state="disabled")
            self.Display_Text.focus_force()    
            self.Display_Text.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.Display_Text.bind(str(item), lambda e: "break")
            self.focus_force()
            self.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.bind(str(item), lambda e: "break")
        if base=='Octal':
            self.base_btn[0].configure(fg_color='navy', text_color='white')
            self.base_btn[1].configure(fg_color='navy', text_color='white')
            self.base_btn[2].configure(fg_color='navy', text_color='white')
            self.base_btn[3].configure(fg_color='white', text_color='navy')
            for num in range(0,8):
                self.num_btn[num].configure(state="normal")
            for num in range(8,16):
                self.num_btn[num].configure(state="disabled")
            self.Display_Text.focus_force()    
            self.Display_Text.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.Display_Text.bind(str(item), lambda e: "break")
            self.focus_force()
            self.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.bind(str(item), lambda e: "break")
        if base=='Decimal':
            self.base_btn[0].configure(fg_color='navy', text_color='white')
            self.base_btn[1].configure(fg_color='white', text_color='navy')
            self.base_btn[2].configure(fg_color='navy', text_color='white')
            self.base_btn[3].configure(fg_color='navy', text_color='white')
            for num in range(0,10):
                self.num_btn[num].configure(state="normal")
            for num in range(10,16):
                self.num_btn[num].configure(state="disabled")
            self.Display_Text.focus_force()    
            self.Display_Text.unbind('<period>')
            self.Display_Text.bind('<period>')
            for i, item in enumerate(self.Hex_List):
                self.Display_Text.bind(str(item), lambda e: "break")
            self.focus_force()
            self.bind('<period>')
            for i, item in enumerate(self.Hex_List):
                self.bind(str(item), lambda e: "break")
        if base=='Hexadecimal':
            self.base_btn[0].configure(fg_color='navy', text_color='white')
            self.base_btn[1].configure(fg_color='navy', text_color='white')
            self.base_btn[2].configure(fg_color='white', text_color='navy')
            self.base_btn[3].configure(fg_color='navy', text_color='white')
            for num in range(0,16):
                self.num_btn[num].configure(state="normal")
            self.Display_Text.focus_force()    
            self.Display_Text.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.Display_Text.unbind(str(item))
            for i, item in enumerate(self.Hex_List):
                self.Display_Text.bind(str(item))
            self.focus_force()
            self.bind(('<period>'), lambda e: "break")
            for i, item in enumerate(self.Hex_List):
                self.bind(str(item), self.numeric_clicked)
    def base_clicked(self, base):
        value=self.Disp_List
        exist=False
        if not self.Answer_Present.get():
            exist=self.function_check(value)
        if exist:return
        if value=='':return
        hex_values=['A','B','C','D','E','F']
        try:
            if self.Answer_Present.get():from_val=self.Answer.get()
            else:from_val=self.Display.get()
            if from_val=='':
                self.Base.set(base)
                self.config_base(base)
            elif from_val!='' and self.Base.get()!= base:
                f_base=self.Base.get()# Get Present Base
                if f_base=='Binary' or f_base=='Binario':from_base=2
                elif f_base=='Octal':from_base=8
                elif f_base=='Decimal':from_base=10
                elif f_base=='Hexadecimal':from_base=16
                is_numerical=False
                disp=self.Display.get()
                for i in disp: # Examine Display String For Only Numerical Value
                    if i.isdigit() or i in hex_values:is_numerical=True
                    else:
                        is_numerical=False
                        break
                if self.Answer_Present.get() or is_numerical==True: # If Answer Or Only Numerical Value Exist Then Convert
                    self.Answer_Present.set(False)
                    self.Base.set(base)
                    t_base=self.Base.get()    
                    if t_base=='Binary' or t_base=='Binario':to_base=2
                    elif t_base=='Octal':to_base=8
                    elif t_base=='Decimal':to_base=10
                    elif t_base=='Hexadecimal':to_base=16
                    self.config_base(t_base)
                    base_val=str(Convert_Base(from_base,to_base,from_val))
                else:return    
                # Pop Last Base Value From Both List And Replace With New Base Value
                self.disp_update('clear')
                if self.Answer.get():self.expr_update('clear')
                for i, item in enumerate(str(base_val)):
                    self.disp_update(item)
                if self.Answer_Present.get():
                    if from_base!=10:
                        answer_val=str(Convert_Base(from_base,10,from_val))
                    else:
                        answer_val=from_val   
                    for i, item in enumerate(answer_val):
                        self.expr_update(item)
                    self.Answer_Present.set(False)
                    self.Answer.set('')    
            else: self.Base.set(base)   
            self.config_trig(self.Trig_Units.get())
        except Exception as e:
            if self.Language.get()=="English":
                title=f"Changing Base {self.Base.get()}"
                msg1='Exception occurred while code execution:\n'
            else:    
                title=f"Cambiando Base {self.Base.get()}"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def config_trig(self, unit):
        base=self.Base.get()
        self.Trig_Units.set(unit)
        if base=='Decimal':
            for num in range(0, len(self.unit_btn)):
                self.unit_btn[num].configure(state="normal")
        else:    
            for num in range(0, len(self.unit_btn)):
                self.unit_btn[num].configure(state="disabled")
        if unit=='Degrees' or unit=='Grados':
            self.unit_btn[0].configure(fg_color='white', text_color='#004d00')
            self.unit_btn[1].configure(fg_color='#004d00', text_color='white')
            self.unit_btn[2].configure(fg_color='#004d00', text_color='white')
        elif unit=='Radians' or unit=='Radianes':
            self.unit_btn[1].configure(fg_color='white', text_color='#004d00')
            self.unit_btn[0].configure(fg_color='#004d00', text_color='white')
            self.unit_btn[2].configure(fg_color='#004d00', text_color='white')
        elif unit=='Gradians' or unit=='Gradianos':
            self.unit_btn[2].configure(fg_color='white', text_color='#004d00')
            self.unit_btn[0].configure(fg_color='#004d00', text_color='white')
            self.unit_btn[1].configure(fg_color='#004d00', text_color='white')
    def trig_unit_clicked(self, trig_base):
        base=self.Base.get() # Only Allow Conversions For Decimal Base
        if base!='Decimal':return
        if self.Answer_Present.get():
            str_val=self.Answer.get()
        else:
            str_val=self.Display.get()
        if str_val=='':
            self.Trig_Units.set(trig_base)
            self.config_trig(trig_base)    
        from_angle=self.Trig_Units.get()
        if str_val!='':
            self.Trig_Units.set(trig_base)
            unit=self.Trig_Units.get()
            self.config_trig(unit)
            is_numerical=False
            disp=self.Display.get()
            is_numerical=self.type_isnumerical(disp)
            if self.Answer_Present.get() or is_numerical: # If Answer Or Only Numerical Value Exist Then Convert
                val=str(Convert_Trig_Units(from_angle,unit,str_val))
                self.Answer_Present.set(False)
            else:return
            rund=self.Round.get()
            if rund>0:
                expr=val
                exp=parse_expr(expr, evaluate=True)
                expr_answer=exp.evalf(mp.dps, subs=self.sub_dict)
                answer=self.nround_answer(expr_answer)
            else:answer=val    
            self.Display.set(answer)
            self.Display_Text.delete("0.0", "end")
            self.Display_Text.insert('end',answer)
            self.Answer_Present.set(True)
            self.Answer.set(answer)
    def config_trig_btns(self, txt):
        arc=self.Arc.get()
        hyp=self.Hyp.get()
        if txt=='Hyp':
            if hyp:
                self.Hyp.set(False)
                hyp=False
            else:
                self.Hyp.set(True)
                hyp=True
        elif txt=='Arc':        
            if arc:
                self.Arc.set(False)
                arc=False
            else:
                self.Arc.set(True)
                arc=True
        if not hyp and not arc:
            trig1=['sin','sec','cos','csc','tan','cot']
            for i, item in enumerate(trig1):
                self.trig_btn[i].configure(text=item)
            self.hyp_btn.configure(fg_color='#004d00', text_color='white')
            self.arc_btn.configure(fg_color='#004d00', text_color='white')
        elif hyp and not arc:
            trig2=['sinh','sech','cosh','csch','tanh','coth']
            for i, item in enumerate(trig2):
                self.trig_btn[i].configure(text=item)
            self.hyp_btn.configure(fg_color='white', text_color='#004d00')
            self.arc_btn.configure(fg_color='#004d00', text_color='white')
        elif not hyp and arc:
            trig3=['asin','asec','acos','acsc','atan','acot']
            for i, item in enumerate(trig3):
                self.trig_btn[i].configure(text=item)
            self.arc_btn.configure(fg_color='white', text_color='#004d00')
            self.hyp_btn.configure(fg_color='#004d00', text_color='white')
        elif hyp and arc:        
            trig4=['asinh','asech','acosh','acsch','atanh','acoth']
            for i, item in enumerate(trig4):
                self.trig_btn[i].configure(text=item)
            self.arc_btn.configure(fg_color='white', text_color='#004d00')
            self.hyp_btn.configure(fg_color='white', text_color='#004d00')
    def clear_entry(self, event):
        if self.Answer_Present.get():self.Answer_Present.set(False)
        if self.Disp_List and self.Expr_List:
            if self.Disp_List[-1] == self.Expr_List[-1] or self.Disp_List[-1] == '^' and self.Expr_List[-1]=='**': 
                last_element = self.Disp_List[-1]
                if last_element==')':self.bracket_clicked('auto','both','open')
                if last_element=='(':self.bracket_clicked('auto','both','close')
                if self.Disp_List:self.Disp_List.pop()
                if self.Expr_List:self.Expr_List.pop()
                e1=''.join([str(item) for item in self.Expr_List])
                self.Expression.set(e1)
                d1=''.join([str(item) for item in self.Disp_List])
                d2 = str(d1).replace('{','').replace('}','') # Remove Temp Brackets For Examination
                self.Display.set(d2)
                self.Display_Text.delete("0.0", "end")
                self.Display_Text.insert('end',d2)
        else:self.clear_all()
    def button_popups(self, event, txt):# display the popup menu
        btn=txt.replace(" ","")
        orig_list=['sin','sec','cos','csc','tan','cot']
        if txt in orig_list:# Check For Button Text Change. Only Original Text Was Used For Binding
            for num in range(0,len(orig_list)):
                if orig_list[num] == txt:
                    btn = self.trig_btn[num].cget("text")
                    break
        trig_btns=['sin','cos','tan','sec','csc','cot','asin','acos','atan','asec','acsc','acot','sinh',
                    'cosh','tanh','sech','csch','coth','asinh','acosh','atanh','asech','acsch','acoth']
        if self.Language.get()=="English":
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
            elif btn=='n!':text='Factorial of Positive Natural Number n. Enter n Then Click Me.'
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
            elif btn=='A:B':text="Calculate Ratios And Porportions."
            elif btn=='∫':text="Integrate Expression. An Expression Must Be Present To Integrate."
            elif btn=='f´(𝓧)':text="Differentiate Expression. An Expression Must Be Present To Differentiate."
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
            elif btn=='n!':text='Factorial de un Número Natural Positivo n. Ingrese n Luego Haga Clic en Mí.'
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
            elif btn=='A:B':
                text="Calcular Razones y Proporciones."
            elif btn=='∫':text="Integrar Expresión. Debe Estar Ppresente una Expresión para Integrar."
            elif btn=='f´(𝓧)':text="Diferenciar Expresión. Debe Estar Presente una Eexpresión para Diferenciar."
        btn_popup = MyTimedPopup(self.Display_Text, text=text, text_color="#000000", 
                            fg_color="#14fafa", font_size=14, delay_time=1000)
    def copy_to_clipboard(self, parent, which) -> str:
        # Parent Widget Has To Be A Text Object
        try:
            if which=="selected":
                text=parent.selection_get()
                if self.Language.get()=="English":txt=" Selected Text Copied To Clipboard! "
                else:txt="¡Texto Seleccionado Copiado al Portapapeles!"
            elif which=="all":
                text=parent.get("1.0", 'end')
                if text=="\n":text=""
                if self.Language.get()=="English":txt=" Display Text Copied To Clipboard! "
                else:txt=" ¡Texto Mostrado Copiado al Portapapeles! "
            if text!="":
                parent_font=parent.cget("font")
                txt=f" {txt} "#Add Spaces
                scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
                parent_wid=parent.winfo_width()
                parent_hgt=parent.winfo_height()
                popup_width = int(parent_wid * 0.75)
                font_metrics = parent_font.metrics()
                popup_height = int(font_metrics['linespace'] * 1.5)
                x_pos = int(((parent_wid // 2) - (popup_width // 2)) / scale_factor)
                y_pos = int(((parent_hgt // 2) - (popup_height // 2)) / scale_factor)
                copy(text)
                clipboard_msg = ctk.CTkLabel(parent, text=txt, font=parent_font, anchor="center", corner_radius=15, width=popup_width,
                                            height=popup_height, fg_color=("#33FFFF","#33FFFF"),text_color=("#000000","#000000"))
                clipboard_msg.place(x=x_pos, y=y_pos)
                self.after(3000, clipboard_msg.destroy)
        except Exception as e:
            pass
    def restart_program(self, lang_change=False):# app
        self.popup_menu.withdraw()
        app.update()
        self.give_greeting("restart")
        sleep(1)
        try:
            self.write_setup()
            self.clear_memories()
            self.clear_all()
            self.Symbol_Names.clear()
            self.Symbol_Values.clear()
            self._MyClash.clear()
            self._MyConstants.clear()
            self.operators.clear()
        except:
            pass
        if lang_change:
            if os.path.exists('Config.json'):
                self.Language.set("")
                self.write_setup()
        try:
            for widget in self.winfo_children():# Destroys Menu Bars, Frame, Canvas And Scroll Bars
                if isinstance(widget, ctk.CTkCanvas):widget.destroy()
                else:widget.destroy()
            os.execl(sys.executable, os.path.abspath("ctkCalculator.exe"), *sys.argv) 
        except:
            pass
            os.execl(sys.executable, os.path.abspath("ctkCalculator.exe"), *sys.argv)
    def show_menu_popup(self, event):# app
        if self.Language.get()=="English":
            captions=['Set Calculator Precision',"Set Answer Rounding","Set Scientific Notation Precision","Set Exponential Notation Precision","Set Binary Bit Size (8, 16, 32, 64, 128, 256, 512)",
                    "Set Display Font","Set Color Theme","Set Display Text Color","Set Display Background Color","Copy Display Text To Clipboard","Change Language","About My Calculator"]
        else:
            captions=['Precisión de la Calculadora','Redondear Respuesta','Precisión en Notación Científica','Precisión en Notación Exponencial','Tamaño de Bit Binario (8, 16, 32, 64, 128, 256, 512)',
                'Fuente de Visualización','Cambiar Tema de Color','Color del Texto','Color de Fondo','Copiar Texto de la Pantalla al Portapapeles','Cambiar idioma','Acerca de Mi Calculadora']
        commands=[lambda arg='dp': self.precision(arg), lambda arg='round': self.precision(arg), lambda arg='exp': self.precision(arg), lambda arg='exp_digits': self.precision(arg),
                        lambda arg='bit_size': self.precision(arg), lambda: self.choose_font(), lambda arg='color_theme': self.choose_theme(arg), lambda arg='text_color': self.choose_color(arg), lambda arg='fg_color': self.choose_color(arg),
                        lambda arg1=self.Display_Text,arg2='all': self.copy_to_clipboard(arg1 ,arg2), lambda arg=True: self.restart_program(arg), lambda: self.about()]
        self.popup_menu = MyPopupMenu(self, captions ,commands, 16, self.winfo_pointerx(), self.winfo_pointery())
        self.wait_window(self.popup_menu)
        try:
            self.popup_menu.grab_release()
            self.popup_menu.destroy()
        except:pass    
    def nround_answer(self, expr):# Use nstr In Conj. With Round.get() To Round Answer
        try:
            expr_answer=expr.evalf(mp.dps, subs=self.sub_dict)
            answer_str=str(expr_answer)
            rund=self.Round.get()
            n_str=''
            for i in answer_str:
                n_str=i+n_str
                if i=='.':break
                else:count=len(n_str)
            if '-' in answer_str:count-=1
            n=rund+count
            if rund>0:
                if self.type_isnumerical(answer_str):
                    answer=nstr(mpf(expr_answer), n)
                else:answer=str(expr_answer) # Answer Isn't Numerical   
            else:answer=str(expr_answer) # No Rounding
            return answer # Return Value = n For nstr
        except Exception as e:
            if self.Language.get()=="English":
                title="Round Answer Error"
                msg1='Exception occurred while code execution:\n'
            else:    
                title="Error de Respuesta Redondeada"
                msg1='Ocurrió una excepción durante la ejecución del código:\n'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            return 'break'
    def write_setup(self):
        self.update_idletasks()
        temp_dict={}
        sc=json.load(open("Config.json", "r"))
        json.dump(sc,open("Config.json", "w"),indent=4)
        temp_dict[0]=self.Language.get()
        temp_dict[1]=str(mp.dps)
        temp_dict[2]=str(self.Round.get())
        temp_dict[3]=str(self.Exp_Precision.get())
        temp_dict[4]=str(self.Exp_Digits.get())
        temp_dict[5]=str(self.Bit_Size.get())
        temp_dict[6]=str(self.Display_fg.get())
        temp_dict[7]=str(self.Display_bg.get())
        family_now=self.Display_Font.cget("family")
        size_now=self.Display_Font.cget("size")
        weight_now=self.Display_Font.cget("weight")
        slant_now=self.Display_Font.cget("slant")
        temp_dict[8]=str({'family': family_now, 'size': size_now, 'weight': weight_now, 'slant': slant_now})
        temp_dict[9]=str(self.winfo_x())
        temp_dict[10]=str(self.winfo_y())
        temp_dict[11]=str(self.screen_width)
        temp_dict[12]=str(self.screen_height)
        temp_dict[13]=str(self.scale_factor)
        temp_dict[14]=str(self.Theme.get())
        with open("Config.json", "w") as outfile:json.dump(temp_dict, outfile)
        outfile.close()
        temp_dict.clear()
    def read_setup(self):
        self.update_idletasks()
        try:
            with open('Config.json', 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
            for key, value in data.items():
                if key=="0":self.Language.set(value)
                elif key=="1":mp.dps=int(value)
                elif key=="2":self.Round.set(int(value))
                elif key=="3":self.Exp_Precision.set(int(value))
                elif key=="4":self.Exp_Digits.set(int(value))
                elif key=="5":self.Bit_Size.set(int(value))
                elif key=="6":
                    self.Display_fg.set(value)
                    self.Display_Text.focus_force()
                    self.Display_Text.configure(text_color=self.Display_fg.get())
                elif key=="7":
                    self.Display_bg.set(value)
                    self.Display_Text.focus_force()
                    self.Display_Text.configure(fg_color=self.Display_bg.get())
                elif key=="8":
                    self.NewFont.set(value)
                    new_font=parse_expr(value, evaluate=False)
                    self.Display_Font.configure(family=new_font['family'], size=new_font['size'], 
                                        weight=new_font['weight'], slant=new_font['slant'])
                    self.Display_Text.focus_force()
                    self.Display_Text.configure(font=self.Display_Font)
                elif key=="9":self.x=int(value)
                elif key=="10":self.y=int(value)
                elif key=="11":self.width=int(value)
                elif key=="12":self.screen_height=int(value)
                elif key=="13":self.scale_factor=float(value)
                elif key=="14":self.Theme.set(value)
        except Exception as e:
            if self.Language.get()=="English":
                title='Error Reading Config.json File'
                msg1=f'Error Reading {key}, {value} In Config.json:\n'
            else:
                title='Error al leer el archivo Config.json\n'
                msg1=f'Error al leer {key}, {value} en Config.json:'
            msg2= repr(e)
            msg=msg1+msg2
            cancel_dialog=MyDialog(parent=app, style="msgbox", title=title, prompt=msg, icon="cancel")
            pass
        self.width = int(self.screen_width*0.4)
        self.height = int(self.screen_height*0.35)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y, ))
        self.update()
    def free_sys_symbols(self, *args):
        if not self.D_Memory1 and not  self.D_Memory2 and not  self.D_Memory3 and not  self.D_Memory4:
            if not args:
                for abc in self.Symbols_Used:
                    Symbol(abc).free_symbols
                self.Symbols_Used.clear()
                self.Symbol_Names.clear()
                self.Symbol_Values.clear()
            else:
                for ar in args:
                    Symbol(ar).free_symbols
        else:return
    def clear_all(self):
        self.Display.set('')
        self.Display_Text.delete("0.0", "end")
        self.Math_Function.set('')
        self.Last_Function.set('')
        self.Disp_List.clear() 
        self.Disp_Bkts_Open.set(0)
        self.Temp_Disp_Open.set(0)
        self.Temp_Expr_Open.set(0)
        self.Reversed_List.clear()
        self.Expression.set('')
        self.Expr_List.clear()
        self.Expressions_Used.clear()  
        self.Expr_Bkts_Open.set(0)  
        self.bracket_clicked('auto','both','clear')
        self.Answer.set('')
        self.Answer_Present.set(False)
        self.Answer_Err.set(False)
        self.disp_update('clear') 
        self.expr_update('clear')
        self.free_sys_symbols()
    def set_defaults(self):
        if not os.path.exists("Config.json"):
            mp.dps=50
            self.Round.set(15)
            self.Exp_Precision.set(30)
            self.Exp_Digits.set(4)
            self.Bit_Size.set(128)
            self.Display_fg.set("#ffffff")
            self.Display_bg.set("#0c012e")
            self.Theme.set("Dark")
            data={}
            with open("Config.json", "w") as json_file:# Create Empty json File
                    json.dump(data, json_file, indent=4) # indent=4 for pretty-printing
                    json_file.close()
            self.write_setup()
            self.geometry('%dx%d+%d+%d' % (self.width, self.height, self.x, self.y, ))
        else:
            self.read_setup()    
        mp.pretty=True
        self.Hyp.set(False)  
        self.Arc.set(False)
        self.config_base('Decimal')     
        self.config_trig('Degrees')
        self.clear_all()
        self.deiconify()
        self.update()
    def give_greeting(self, status):
        current_datetime = datetime.now()
        if self.Language.get()=="English":
            if status == "open":
                if current_datetime.hour<12:
                    greeting=f"Good Morning {self.user}."
                elif current_datetime.hour>=12 and current_datetime.hour<17:
                    greeting=f"Good Afternoon {self.user}."
                elif current_datetime.hour>=17 and current_datetime.hour<=24:
                    greeting=f"Good Evening {self.user}."
            elif status == "close":        
                if current_datetime.hour<12:
                    greeting=f"Goodbye {self.user}. Have a Wonderful Morning!"
                elif current_datetime.hour>=12 and current_datetime.hour<17:
                    greeting=f"Goodbye {self.user}. Have a Wonderful Afternoon!"
                elif current_datetime.hour>=17 and current_datetime.hour<=24:
                    greeting=f"Goodbye {self.user}. Have a Wonderful Evening!"
            elif status == "restart":
                greeting = "Restarting Program!"        
        elif self.Language.get()=="Spanish":            
            if status == "open":
                if current_datetime.hour<12:
                    greeting=f"Buenos Días {self.user}."
                elif current_datetime.hour>=12 and current_datetime.hour<17:
                    greeting=f"Buenas Tardes {self.user}."
                elif current_datetime.hour>=17 and current_datetime.hour<=24:
                    greeting=f"Buenas Noches {self.user}."
            elif status == "close":        
                if current_datetime.hour<12:
                    greeting=f"Adiós {self.user}. ¡Que Tengas una Mañana Maravillosa!"
                elif current_datetime.hour>=12 and current_datetime.hour<17:
                    greeting=f"Adiós {self.user}. ¡Que Ttengas una Maravillosa Tarde!"
                elif current_datetime.hour>=17 and current_datetime.hour<=24:
                    greeting=f"Adiós {self.user}. ¡Que Tengas una Noche Maravillosa!"
            elif status == "restart":
                greeting = "¡Reiniciando el Programa!"        
        self.greet_popup = MyTimedPopup(self. Display_Text, text=greeting, text_color="#000000", 
                            fg_color="#14fafa", font_size=14, delay_time=1500)
if __name__ == "__main__":
    version="2026.04.17"
    ctk.DrawEngine.preferred_drawing_method = "circle_shapes"
    ctypes.windll.shcore.SetProcessDpiAwareness(2)# Text Size Change Awareness
    if os.path.exists("Config.json"):# Get Color Theme
        with open('Config.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
    try:        
        if data["14"]:
            theme = data.get("14")
            ctk.set_appearance_mode(theme)  # Options: "System", "Dark", "Light"
    except:        
        ctk.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
    app = Calculator()
    app.mainloop()
