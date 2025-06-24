import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# Try to import both libraries
PYNPUT_AVAILABLE = False
PYAUTOGUI_AVAILABLE = False

try:
    from pynput.keyboard import Key, Controller as KeyboardController
    PYNPUT_AVAILABLE = True
    print("✅ pynput library loaded")
except ImportError:
    print("❌ pynput not available")

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    print("✅ pyautogui library loaded")
except ImportError:
    print("❌ pyautogui not available")

class AutoWASDProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto WASD Program - Roblox Compatible")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        # Variable untuk mengontrol thread
        self.running = False
        self.thread = None
        
        # WASD sequence
        self.keys = ['w', 'a', 's', 'd']
        self.current_key_index = 0
        
        # Keyboard controller for pynput
        if PYNPUT_AVAILABLE:
            self.keyboard = KeyboardController()
        
        # Current method
        self.current_method = "pynput" if PYNPUT_AVAILABLE else "pyautogui"
        
        self.setup_gui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Auto WASD - Roblox Compatible", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Method selection frame
        method_frame = ttk.LabelFrame(main_frame, text="Input Method", padding="10")
        method_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.method_var = tk.StringVar(value=self.current_method)
        
        if PYNPUT_AVAILABLE:
            pynput_radio = ttk.Radiobutton(method_frame, text="pynput (Recommended for games)", 
                                          variable=self.method_var, value="pynput")
            pynput_radio.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        if PYAUTOGUI_AVAILABLE:
            pyautogui_radio = ttk.Radiobutton(method_frame, text="pyautogui (Standard)", 
                                             variable=self.method_var, value="pyautogui")
            pyautogui_radio.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Stopped", 
                                     foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        
        # Current key label
        self.current_key_label = ttk.Label(main_frame, text="Current Key: None", 
                                          font=("Arial", 12, "bold"))
        self.current_key_label.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Play button
        self.play_button = ttk.Button(buttons_frame, text="Play", 
                                     command=self.start_program, width=10)
        self.play_button.grid(row=0, column=0, padx=5)
        
        # Stop button
        self.stop_button = ttk.Button(buttons_frame, text="Stop", 
                                     command=self.stop_program, width=10,
                                     state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Close button
        close_button = ttk.Button(buttons_frame, text="Close", 
                                 command=self.close_program, width=10)
        close_button.grid(row=0, column=2, padx=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Informasi", padding="10")
        info_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        info_text = """• Interval: 0.5 detik per tombol
• Urutan: W → A → S → D (repeat)
• Untuk Roblox: Gunakan pynput method
• Pastikan game dalam keadaan aktif/focus"""
        
        info_label = ttk.Label(info_frame, text=info_text, font=("Arial", 9))
        info_label.grid(row=0, column=0, sticky=tk.W)
        
        # Countdown label
        self.countdown_label = ttk.Label(main_frame, text="", 
                                        font=("Arial", 10), foreground="blue")
        self.countdown_label.grid(row=6, column=0, columnspan=3, pady=5)
    
    def press_key_pynput(self, key):
        """Press key using pynput (better for games)"""
        try:
            self.keyboard.press(key)
            time.sleep(0.05)  # Small delay to ensure proper key press
            self.keyboard.release(key)
            return True
        except Exception as e:
            print(f"Error with pynput: {e}")
            return False
    
    def press_key_pyautogui(self, key):
        """Press key using pyautogui"""
        try:
            pyautogui.keyDown(key)
            time.sleep(0.05)
            pyautogui.keyUp(key)
            return True
        except Exception as e:
            print(f"Error with pyautogui: {e}")
            return False
    
    def start_program(self):
        if not self.running:
            # Check if selected method is available
            selected_method = self.method_var.get()
            if selected_method == "pynput" and not PYNPUT_AVAILABLE:
                messagebox.showerror("Error", "pynput library tidak tersedia!\nInstall dengan: pip install pynput")
                return
            elif selected_method == "pyautogui" and not PYAUTOGUI_AVAILABLE:
                messagebox.showerror("Error", "pyautogui library tidak tersedia!\nInstall dengan: pip install pyautogui")
                return
            
            self.current_method = selected_method
            self.running = True
            self.play_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self.status_label.config(text=f"Status: Running ({self.current_method})", foreground="green")
            
            # Show countdown before starting
            self.countdown_start()
    
    def countdown_start(self):
        """3 second countdown before starting"""
        for i in range(3, 0, -1):
            if not self.running:
                return
            self.countdown_label.config(text=f"Starting in {i}...")
            self.root.update()
            time.sleep(1)
        
        if self.running:
            self.countdown_label.config(text="Program Started!")
            self.stop_button.config(state="normal")
            
            # Start thread untuk auto WASD
            self.thread = threading.Thread(target=self.auto_wasd_loop, daemon=True)
            self.thread.start()
            
            print(f"Program dimulai - Auto WASD dengan {self.current_method}")
    
    def stop_program(self):
        if self.running:
            self.running = False
            self.play_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="Status: Stopped", foreground="red")
            self.current_key_label.config(text="Current Key: None")
            self.countdown_label.config(text="")
            
            print("Program dihentikan")
    
    def close_program(self):
        self.stop_program()
        self.root.quit()
        self.root.destroy()
    
    def auto_wasd_loop(self):
        consecutive_errors = 0
        max_errors = 5
        
        while self.running:
            if not self.running:
                break
            
            # Get current key
            current_key = self.keys[self.current_key_index]
            
            # Update GUI untuk menampilkan key yang akan ditekan
            self.root.after(0, lambda k=current_key.upper(): 
                           self.current_key_label.config(text=f"Pressing: {k}"))
            
            # Press key based on selected method
            success = False
            if self.current_method == "pynput" and PYNPUT_AVAILABLE:
                success = self.press_key_pynput(current_key)
            elif self.current_method == "pyautogui" and PYAUTOGUI_AVAILABLE:
                success = self.press_key_pyautogui(current_key)
            
            if success:
                consecutive_errors = 0
                print(f"Key '{current_key.upper()}' pressed at {time.strftime('%H:%M:%S')} using {self.current_method}")
                
                # Move to next key
                self.current_key_index = (self.current_key_index + 1) % len(self.keys)
                
                # Show next key info
                next_key = self.keys[self.current_key_index]
                self.root.after(0, lambda k=next_key.upper(): 
                               self.countdown_label.config(text=f"Next: {k} in 0.5s"))
            else:
                consecutive_errors += 1
                self.root.after(0, lambda: self.countdown_label.config(
                    text=f"Error pressing key! ({consecutive_errors}/{max_errors})"))
                
                if consecutive_errors >= max_errors:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Error", f"Too many consecutive errors with {self.current_method}!\nProgram will stop."))
                    self.running = False
                    break
            
            # Wait 0.5 seconds
            time.sleep(0.5)
        
        # Update GUI when loop ends
        self.root.after(0, self.stop_program)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Apakah Anda yakin ingin keluar?"):
            self.stop_program()
            self.root.destroy()

def main():
    # Check available libraries
    if not PYNPUT_AVAILABLE and not PYAUTOGUI_AVAILABLE:
        print("❌ Tidak ada library input yang tersedia!")
        print("Install salah satu atau kedua library berikut:")
        print("  pip install pynput")
        print("  pip install pyautogui")
        return
    
    print("\n🎮 Program Auto WASD untuk Roblox")
    print("=" * 40)
    
    if PYNPUT_AVAILABLE:
        print("✅ pynput tersedia (Recommended untuk game)")
    if PYAUTOGUI_AVAILABLE:
        print("✅ pyautogui tersedia")
        pyautogui.FAILSAFE = True
    
    print("\n📋 Tips untuk Roblox:")
    print("1. Gunakan method 'pynput' untuk hasil terbaik")
    print("2. Pastikan Roblox dalam keadaan aktif/focus")
    print("3. Test di game sederhana dulu")
    print("4. Beberapa game Roblox mungkin memiliki anti-cheat")
    
    # Buat dan jalankan aplikasi
    root = tk.Tk()
    app = AutoWASDProgram(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()