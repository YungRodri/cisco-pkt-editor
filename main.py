import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os
import sys

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
        
        self.btn_open = tk.Button(self.top_frame, text="Open & Decode .pkt", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)
        
        self.btn_save = tk.Button(self.top_frame, text="Encode & Save .pkt", command=self.save_file, state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        
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
            filetypes=(("Packet Tracer Files", "*.pkt"), ("All Files", "*.*"))
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
            self.text_area.insert(tk.END, xml_data.decode('utf-8'))
            
            self.current_file = filepath
            self.btn_save.config(state=tk.NORMAL)
            self.status_var.set(f"Successfully decoded {os.path.basename(filepath)}")
            
        except PkaError as e:
            messagebox.showerror("Decryption Error", str(e))
            self.status_var.set("Error during decryption.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
            self.status_var.set("Error opening file.")
            
    def save_file(self):
        if not self.current_file:
            return
            
        filepath = filedialog.asksaveasfilename(
            title="Save Packet Tracer file as",
            defaultextension=".pkt",
            initialfile="modified_" + os.path.basename(self.current_file),
            filetypes=(("Packet Tracer Files", "*.pkt"), ("All Files", "*.*"))
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
