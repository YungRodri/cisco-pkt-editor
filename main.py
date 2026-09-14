import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys

import re

# Append current dir to sys.path to ensure module loading works in both source and PyInstaller
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from packet_crypto import decrypt_pka, encrypt_pka, PkaError

class PacketWinnerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PacketWinner - Cisco Packet Tracer .pkt Editor")
        self.geometry("800x600")
        
        # UI Elements
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.btn_open = tk.Button(self.top_frame, text="Open & Decode", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)
        
        self.btn_save = tk.Button(self.top_frame, text="Encode & Save", command=self.save_file, state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        
        self.btn_patch = tk.Button(self.top_frame, text="Marcar 100%", command=self.mark_100_percent, state=tk.DISABLED, bg="#d4edda", fg="#155724", font=("Arial", 10, "bold"))
        self.btn_patch.pack(side=tk.LEFT, padx=15)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready.")
        self.lbl_status = tk.Label(self.top_frame, textvariable=self.status_var, fg="blue")
        self.lbl_status.pack(side=tk.LEFT, padx=20)
        
        self.text_area = ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=(0, 10))
        
        self.current_file = None
        
    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a Packet Tracer file",
            filetypes=(("Packet Tracer Files", "*.pkt;*.pka"), ("All Files", "*.*"))
        )
        if not filepath:
            return
            
        try:
            self.status_var.set("Decoding...")
            self.update_idletasks()
            
            with open(filepath, "rb") as f:
                data = f.read()
                
            xml_data = decrypt_pka(data)
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, xml_data.decode('utf-8', errors='replace'))
            
            self.current_file = filepath
            self.btn_save.config(state=tk.NORMAL)
            self.btn_patch.config(state=tk.NORMAL)
            self.status_var.set(f"Successfully decoded {os.path.basename(filepath)}")
            
        except PkaError as e:
            messagebox.showerror("Decryption Error", str(e))
            self.status_var.set("Error during decryption.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            self.status_var.set("Error opening file.")
            
    def mark_100_percent(self):
        xml_str = self.text_area.get(1.0, tk.END)
        if not xml_str.strip():
            messagebox.showwarning("Warning", "No XML data to modify.")
            return
            
        # Unlock the Activity Wizard
        xml_str = re.sub(r'<USER_PROFILE_LOCKED>.*?</USER_PROFILE_LOCKED>', r'<USER_PROFILE_LOCKED>false</USER_PROFILE_LOCKED>', xml_str, flags=re.IGNORECASE)
        xml_str = re.sub(r'<ACTIVITY_LOCKED>.*?</ACTIVITY_LOCKED>', r'<ACTIVITY_LOCKED>false</ACTIVITY_LOCKED>', xml_str, flags=re.IGNORECASE)
        xml_str = re.sub(r'<OPEN_IF_DENIED>.*?</OPEN_IF_DENIED>', r'<OPEN_IF_DENIED>true</OPEN_IF_DENIED>', xml_str, flags=re.IGNORECASE)
        xml_str = re.sub(r'<SAVING>.*?</SAVING>', r'<SAVING>ALWAYS</SAVING>', xml_str, flags=re.IGNORECASE)
        
        # Clear all passwords to blank
        xml_str = re.sub(r'<PASSWORD>.*?</PASSWORD>', r'<PASSWORD></PASSWORD>', xml_str, flags=re.IGNORECASE)
        xml_str = re.sub(r'<PASSWD>.*?</PASSWD>', r'<PASSWD></PASSWD>', xml_str, flags=re.IGNORECASE)
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, xml_str)
        self.status_var.set("Activity Wizard Unlocked! Ready to save.")
        messagebox.showinfo("¡Hack Exitoso!", "Se ha DESBLOQUEADO el 'Activity Wizard' (Asistente de Actividades) del archivo.\n\nInstrucciones para el 100%:\n1. Haz clic en 'Encode & Save' y guarda el archivo.\n2. Abre el archivo en Packet Tracer.\n3. Presiona Ctrl + W (o ve a Opciones -> Activity Wizard).\n4. Si te pide contraseña, déjalo en blanco y presiona Enter.\n5. Ve a la pestaña 'Answer Network' y haz clic en 'Copy to User Network'.\n¡Listo! Packet Tracer te pondrá el 100% nativamente sin detectar trucos.")
            
    def save_file(self):
        if not self.current_file:
            return
            
        ext = os.path.splitext(self.current_file)[1].lower()
        if not ext:
            ext = ".pkt"
            
        filepath = filedialog.asksaveasfilename(
            title="Save Packet Tracer file as",
            defaultextension=ext,
            initialfile="modified_" + os.path.basename(self.current_file),
            filetypes=(("Packet Tracer Files", f"*{ext}"), ("All Files", "*.*"))
        )
        
        if not filepath:
            return
            
        try:
            self.status_var.set("Encoding...")
            self.update_idletasks()
            
            xml_str = self.text_area.get(1.0, tk.END).strip()
            if not xml_str:
                messagebox.showwarning("Warning", "The XML data is empty.")
                return
                
            xml_data = xml_str.encode('utf-8')
            pkt_data = encrypt_pka(xml_data)
            
            with open(filepath, "wb") as f:
                f.write(pkt_data)
                
            self.status_var.set(f"Successfully saved to {os.path.basename(filepath)}")
            messagebox.showinfo("Success", f"File successfully saved to:\n{filepath}")
            
        except PkaError as e:
            messagebox.showerror("Encryption Error", str(e))
            self.status_var.set("Error during encryption.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            self.status_var.set("Error saving file.")

if __name__ == "__main__":
    app = PacketWinnerApp()
    app.mainloop()
