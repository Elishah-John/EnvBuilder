import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import ast
import nbformat
import importlib.metadata
import subprocess
import sys
import threading
import time

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x = y = 0
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="lightyellow", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=5)

    def hide_tooltip(self, event=None):
        tw = self.tooltip_window
        if tw:
            tw.destroy()
            self.tooltip_window = None

class EnvBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("EnvBuilder")
        
        self.root.state('zoomed')
        
        self.file_path = tk.StringVar()
        self.output_type = tk.StringVar(value="pip")
        self.venv_name = tk.StringVar(value="venv")
        self.include_comments = tk.BooleanVar(value=True)   
        
        self.import_to_package = {
            "PIL": "Pillow",
            "cv2": "opencv-python",
            "skimage": "scikit-image",
            "sklearn": "scikit-learn",
            "plt": "matplotlib",
            "np": "numpy",
            "pd": "pandas",
        }

        self.standard_libs = {
            "tkinter", "os", "ast", "importlib", "nbformat", 
            "pickle", "random", "datetime", "time", "json", 
            "csv", "math", "re", "sys", "collections", 
            "itertools", "functools", "io", "pathlib", "shutil",
            "threading", "multiprocessing", "subprocess", "argparse",
            "logging", "unittest", "xml", "html", "urllib", "http",
            "socket", "email", "calendar", "zlib", "gzip", "zipfile",
            "tarfile", "hashlib", "copy", "string", "textwrap", "struct"
        }

        self.setup_style()
        self.setup_menu()
        self.setup_gui()

    def setup_menu(self):
        self.root.config(menu="")
        
        menu_frame = tk.Frame(self.root, bg='#2e2e2e', height=30)
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        
        settings_btn = tk.Button(menu_frame, text="Settings", bg='#2e2e2e', fg='#ffffff',
                               activebackground='#4e4e4e', activeforeground='#ffffff',
                               relief=tk.FLAT, bd=0, padx=10, pady=5,
                               command=self.open_config_dialog)
        settings_btn.pack(side=tk.LEFT)
        
        help_btn = tk.Button(menu_frame, text="About", bg='#2e2e2e', fg='#ffffff',
                           activebackground='#4e4e4e', activeforeground='#ffffff',
                           relief=tk.FLAT, bd=0, padx=10, pady=5,
                           command=self.show_about_dialog)
        help_btn.pack(side=tk.LEFT)
        
        dark_line = tk.Frame(self.root, height=1, bg='#1a1a1a')
        dark_line.pack(side=tk.TOP, fill=tk.X)
        
        medium_line = tk.Frame(self.root, height=1, bg='#252525')
        medium_line.pack(side=tk.TOP, fill=tk.X)
        
        light_line = tk.Frame(self.root, height=1, bg='#3e3e3e')
        light_line.pack(side=tk.TOP, fill=tk.X)
        
        padding_frame = tk.Frame(self.root, height=2, bg='#2e2e2e')
        padding_frame.pack(side=tk.TOP, fill=tk.X)

    def show_about_dialog(self):
        about_dialog = tk.Toplevel(self.root)
        about_dialog.title("About EnvBuilder")
        about_dialog.geometry("400x300")
        about_dialog.configure(bg="#2e2e2e")
        about_dialog.resizable(False, False)
        
        header_frame = tk.Frame(about_dialog, bg="#1e1e1e", height=40)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_label = tk.Label(header_frame, text="EnvBuilder",
                               font=("Segoe UI", 16, "bold"), bg="#1e1e1e", fg="#ffffff")
        header_label.pack(pady=10)
        
        content_frame = tk.Frame(about_dialog, bg="#2e2e2e", padx=20, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        version_label = tk.Label(content_frame, text="Version 1.0.0 (I guess...)", 
                               font=("Segoe UI", 10), bg="#2e2e2e", fg="#ffffff")
        version_label.pack(pady=(0, 10))
        
        description = (
            "EnvBuilder is a tool for analyzing Python and Jupyter files\n"
            "to extract dependencies and create virtual environments.\n\n"
            "It helps Python programmers manage their\n"
            "project dependencies efficiently."
        )
        desc_label = tk.Label(content_frame, text=description, 
                            font=("Segoe UI", 9), bg="#2e2e2e", fg="#ffffff",
                            justify=tk.CENTER)
        desc_label.pack(pady=10)
        
        copyright_label = tk.Label(content_frame, text="© 2025 EnvBuilder",
                                 font=("Segoe UI", 8), bg="#2e2e2e", fg="#aaaaaa")
        copyright_label.pack(side=tk.BOTTOM, pady=10)
        
        button_frame = tk.Frame(content_frame, bg="#2e2e2e")
        button_frame.pack(side=tk.BOTTOM, pady=10)
        
        close_btn = tk.Button(button_frame, text="Close", width=10,
                            bg="#3e3e3e", fg="#ffffff", 
                            activebackground="#4e4e4e", activeforeground="#ffffff",
                            relief=tk.RAISED, bd=1,
                            font=("Segoe UI", 9),
                            command=about_dialog.destroy)
        close_btn.pack()
        
        about_dialog.transient(self.root)
        about_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - about_dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - about_dialog.winfo_height()) // 2
        about_dialog.geometry(f"+{x}+{y}")
        
        about_dialog.grab_set()
        about_dialog.focus_set()

    def open_config_dialog(self):
        config_dialog = tk.Toplevel(self.root)
        config_dialog.title("Configuration Options")
        config_dialog.geometry("450x400")
        config_dialog.configure(bg="#2e2e2e")
        config_dialog.resizable(False, False)
        
        header_frame = tk.Frame(config_dialog, bg="#1e1e1e", height=40)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_label = tk.Label(header_frame, text="EnvBuilder Settings",
                               font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ffffff")
        header_label.pack(pady=10)
        
        content_frame = tk.Frame(config_dialog, bg="#2e2e2e", padx=20, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        section_frame1 = tk.Frame(content_frame, bg="#2e2e2e")
        section_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Label(section_frame1, text="Python Interpreter Path:").pack(anchor="w")
        interpreter_frame = tk.Frame(section_frame1, bg="#2e2e2e")
        interpreter_frame.pack(fill=tk.X, pady=5)
        
        interpreter_path = ttk.Entry(interpreter_frame, width=40)
        interpreter_path.pack(side=tk.LEFT, padx=(0, 5))
        browse_btn = ttk.Button(interpreter_frame, text="Browse", 
                               command=lambda: self.browse_interpreter(interpreter_path))
        browse_btn.pack(side=tk.LEFT)
        
        ToolTip(interpreter_path, "Specify the path to the Python interpreter you wish to use")
        ToolTip(browse_btn, "Browse for Python interpreter executable")
        
        section_frame2 = tk.Frame(content_frame, bg="#2e2e2e")
        section_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(section_frame2, text="Default Save Path:").pack(anchor="w")
        save_frame = tk.Frame(section_frame2, bg="#2e2e2e")
        save_frame.pack(fill=tk.X, pady=5)
        
        save_path = ttk.Entry(save_frame, width=40)
        save_path.pack(side=tk.LEFT, padx=(0, 5))
        save_browse_btn = ttk.Button(save_frame, text="Browse", 
                                    command=lambda: self.browse_folder(save_path))
        save_browse_btn.pack(side=tk.LEFT)
        
        ToolTip(save_path, "Specify the default path where environment files will be saved")
        ToolTip(save_browse_btn, "Browse for a folder to save environment files")
        
        options_frame = tk.Frame(content_frame, bg="#2e2e2e")
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(options_frame, text="Options:").pack(anchor="w")
        
        include_comments_var = tk.BooleanVar(value=True)
        include_comments_check = ttk.Checkbutton(options_frame, text="Include comments in requirements file", 
                                               variable=include_comments_var)
        include_comments_check.pack(anchor="w", padx=10, pady=5)
        
        ToolTip(include_comments_check, "Check this box to include comments in the requirements file")
        
        separator = ttk.Separator(config_dialog, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        button_frame = tk.Frame(config_dialog, bg="#2e2e2e")
        button_frame.pack(fill=tk.X, pady=10, padx=20)
        
        save_btn = ttk.Button(button_frame, text="Save", width=10,
                            command=lambda: self.save_config(interpreter_path.get(), save_path.get(), 
                                                           include_comments_var.get(), config_dialog))
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=10,
                              command=config_dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        config_dialog.transient(self.root)
        config_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - config_dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - config_dialog.winfo_height()) // 2
        config_dialog.geometry(f"+{x}+{y}")
        
        config_dialog.grab_set()
        config_dialog.focus_set()

    def browse_interpreter(self, entry_widget):
        if os.name == 'nt':
            filetypes = [("Executable files", "*.exe"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Select Python Interpreter", filetypes=filetypes)
        else:
            filename = filedialog.askopenfilename(title="Select Python Interpreter")
            
        if filename:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filename)
    
    def browse_folder(self, entry_widget):
        folder = filedialog.askdirectory(title="Select Default Save Folder")
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    def save_config(self, interpreter_path, save_path, include_comments, dialog):
        self.python_interpreter = interpreter_path
        self.default_save_path = save_path
        self.include_comments = include_comments
        
        dialog.destroy()
        
        messagebox.showinfo("Configuration Saved", "Your settings have been saved successfully.")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#3e3e3e', foreground='#ffffff')
        style.map('TButton', background=[('active', '#4e4e4e'), ('pressed', '#5e5e5e')])
        style.configure('TLabel', background='#2e2e2e', foreground='#ffffff')
        style.configure('TRadiobutton', background='#2e2e2e', foreground='#ffffff')
        style.map('TRadiobutton', background=[('active', '#4e4e4e')])
        style.configure('TEntry', fieldbackground='#3e3e3e', foreground='#ffffff')

    def setup_gui(self):
        frame = tk.Frame(self.root, padx=10, pady=10, bg="#2e2e2e")
        frame.pack(fill=tk.BOTH, expand=True)

        self.create_file_selection(frame)
        self.create_output_type_selection(frame)
        self.create_venv_options(frame)
        self.create_output_area(frame)

        button_frame = tk.Frame(frame, bg="#2e2e2e")
        button_frame.pack(fill=tk.X, pady=10)

        self.create_generate_button(button_frame)
        self.create_save_button(button_frame)
        self.create_venv_button(button_frame)

        self.progress = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)
        ToolTip(self.progress, "Shows the progress of the current operation")

    def create_file_selection(self, parent):
        ttk.Label(parent, text="Select Python or Jupyter file:").pack(anchor="w")
        file_frame = tk.Frame(parent, bg="#2e2e2e")
        file_frame.pack(fill=tk.X, pady=5)
        entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        entry.pack(side=tk.LEFT, padx=(0, 5))
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT)
        
        ToolTip(entry, "Enter the path to your Python or Jupyter file")
        ToolTip(browse_btn, "Browse for a Python or Jupyter file")

    def create_output_type_selection(self, parent):
        ttk.Label(parent, text="Output Type:").pack(anchor="w", pady=(10, 0))
        output_frame = tk.Frame(parent, bg="#2e2e2e")
        output_frame.pack(anchor="w")
        pip_radio = ttk.Radiobutton(output_frame, text="pip (requirements.txt)", variable=self.output_type, value="pip")
        conda_radio = ttk.Radiobutton(output_frame, text="conda (environment.yml)", variable=self.output_type, value="conda")
        pip_radio.pack(side=tk.LEFT)
        conda_radio.pack(side=tk.LEFT)

        ToolTip(pip_radio, "Generate a pip requirements.txt file")
        ToolTip(conda_radio, "Generate a conda environment.yml file")

    def create_venv_options(self, parent):
        ttk.Label(parent, text="Virtual Environment:").pack(anchor="w", pady=(10, 0))
        venv_frame = tk.Frame(parent, bg="#2e2e2e")
        venv_frame.pack(fill=tk.X, pady=5)
        venv_label = ttk.Label(venv_frame, text="Name:")  
        venv_label.pack(side=tk.LEFT, padx=(0, 5))
        venv_entry = ttk.Entry(venv_frame, textvariable=self.venv_name, width=20)
        venv_entry.pack(side=tk.LEFT, padx=(0, 5))

        ToolTip(venv_label, "Enter the name for the virtual environment")
        ToolTip(venv_entry, "Specify the name for the virtual environment")

    def create_output_area(self, parent):
        ttk.Label(parent, text="Extracted Dependencies:").pack(anchor="w")
        self.output_text = tk.Text(parent, height=10, bg="#3e3e3e", fg="#ffffff")
        self.output_text.pack(fill=tk.BOTH, expand=True)
        ToolTip(self.output_text, "Displays the extracted dependencies from the selected file")

    def create_generate_button(self, parent):
        gen_btn = ttk.Button(parent, text="Generate Environment File", command=self.generate_env_file)
        gen_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(gen_btn, "Extract dependencies from the selected file")

    def create_save_button(self, parent):
        save_btn = ttk.Button(parent, text="Save Environment File", command=self.save_env_file)
        save_btn.pack(side=tk.LEFT, padx=5)
        ToolTip(save_btn, "Save the generated environment file")

    def create_venv_button(self, parent):
        ttk.Button(parent, text="Create Virtual Environment", command=self.create_virtual_environment).pack(side=tk.LEFT, padx=5)

    def create_virtual_environment(self):
        if not hasattr(self, 'content') or not self.content:
            messagebox.showwarning("No Content", "Please generate the environment file first.")
            return

        venv_name = self.venv_name.get()
        if not venv_name:
            messagebox.showwarning("No Name", "Please enter a name for the virtual environment.")
            return

        temp_req_file = os.path.join(os.path.dirname(sys.executable), "temp_requirements.txt")
        with open(temp_req_file, "w", encoding="utf-8") as f:
            f.write(self.content)

        self.progress['value'] = 0
        self.root.update_idletasks()
        
        self.disable_buttons()
        
        thread = threading.Thread(target=self._create_venv_thread, args=(venv_name, temp_req_file))
        thread.daemon = True
        thread.start()
        
        self._monitor_progress(thread)
    
    def _create_venv_thread(self, venv_name, temp_req_file):
        try:
            self.update_output(f"\nCreating virtual environment '{venv_name}'... (This may take a bit)\n")
            
            self.thread_progress = 10
            
            subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
            
            self.thread_progress = 40
            
            if os.name == 'nt':
                pip_path = os.path.join(os.getcwd(), venv_name, "Scripts", "pip.exe")
            else:
                pip_path = os.path.join(os.getcwd(), venv_name, "bin", "pip")
            
            self.update_output("Installing dependencies...\n")
            self.thread_progress = 60
            
            result = subprocess.run([pip_path, "install", "-r", temp_req_file], 
                                   capture_output=True, text=True)
            
            self.thread_progress = 100
            
            if result.returncode == 0:
                self.update_output("Virtual environment created successfully!\n")
                self.update_output(f"Activate with: {venv_name}\\Scripts\\activate (Windows) or source {venv_name}/bin/activate (Unix/Linux/Mac)\n")
            else:
                self.update_output(f"Error installing dependencies:\n{result.stderr}\n")
                
        except Exception as e:
            self.update_output(f"Error creating virtual environment: {str(e)}\n")
        finally:
            if os.path.exists(temp_req_file):
                os.remove(temp_req_file)
            
            self.thread_done = True
    
    def _monitor_progress(self, thread):
        if not hasattr(self, 'thread_progress'):
            self.thread_progress = 0
        if not hasattr(self, 'thread_done'):
            self.thread_done = False
        
        self.progress['value'] = self.thread_progress
        self.root.update_idletasks()
        
        if thread.is_alive() and not self.thread_done:
            self.root.after(100, lambda: self._monitor_progress(thread))
        else:
            if self.thread_done:
                self.progress['value'] = 100
                self.root.update_idletasks()
                self.root.after(500, lambda: self._reset_after_completion())
    
    def _reset_after_completion(self):
        self.progress['value'] = 0
        self.enable_buttons()
        self.thread_done = False
            
        if hasattr(self, 'thread_done') and self.thread_done:
            self.progress['value'] = 0
            self.enable_buttons()
    
    def update_output(self, text):
        self.root.after(0, lambda: self.output_text.insert(tk.END, text))
    
    def disable_buttons(self):
        self._set_button_state(self.root, 'disabled')
    
    def enable_buttons(self):
        self._set_button_state(self.root, 'normal')
    
    def _set_button_state(self, parent, state):
        for child in parent.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(state=state)
            if child.winfo_children():
                self._set_button_state(child, state)

    def browse_file(self):
        filetypes = [("Python & Jupyter Files", "*.py *.ipynb")]
        filename = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)

    def extract_imports(self, filepath):
        imports = set()
        try:
            if filepath.endswith(".py"):
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.add(alias.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                module_name = node.module.split('.')[0]
                                if os.path.isfile(os.path.join(os.path.dirname(filepath), module_name + ".py")):
                                    imports.add(f"{module_name} (local file)")
                                else:
                                    imports.add(module_name)

            elif filepath.endswith(".ipynb"):
                nb = nbformat.read(filepath, as_version=4)
                for cell in nb.cells:
                    if cell.cell_type == 'code':
                        try:
                            tree = ast.parse(cell.source)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Import):
                                    for alias in node.names:
                                        imports.add(alias.name.split('.')[0])
                                elif isinstance(node, ast.ImportFrom):
                                    if node.module:
                                        module_name = node.module.split('.')[0]
                                        if os.path.isfile(os.path.join(os.path.dirname(filepath), module_name + ".py")):
                                            imports.add(f"{module_name} (local file)")
                                        else:
                                            imports.add(module_name)
                        except Exception:
                            continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse file: {e}")

        return sorted(imports)

    def get_versions(self, modules):
        result = []
        
        for mod in modules:
            try:
                package_name = self.import_to_package.get(mod, mod)
                if mod in self.standard_libs or package_name in self.standard_libs:
                    result.append((mod, "standard library"))
                else:
                    version = importlib.metadata.version(package_name)
                    result.append((mod, version))
            except importlib.metadata.PackageNotFoundError:
                result.append((mod, None))
        return result

    def generate_env_file(self):
        filepath = self.file_path.get()
        if not filepath:
            messagebox.showwarning("No File", "Please select a file first.")
            return
        if not os.path.exists(filepath):
            messagebox.showwarning("File Not Found", f"The file {filepath} does not exist.")
            return

        modules = self.extract_imports(filepath)
        versions = self.get_versions(modules)

        self.output_text.delete(1.0, tk.END)
        self.content = ""  

        if self.output_type.get() == "pip":
            for mod, ver in versions:
                if ver == "standard library":
                    line = f"{mod}  # standard library" if self.include_comments else mod
                elif "(local file)" in mod:
                    line = f"{mod}  # local file" if self.include_comments else mod
                else:
                    line = f"{mod}=={ver}" if ver else f"{mod}  # not installed" if self.include_comments else mod
                self.output_text.insert(tk.END, line + "\n")
                
                if ver != "standard library" and "(local file)" not in mod:
                    package_name = self.import_to_package.get(mod, mod)
                    self.content += f"{package_name}=={ver}\n" if ver else f"{package_name}  # not installed\n"
        else:
            self.output_text.insert(tk.END, "name: env\nchannels:\n  - conda-forge\ndependencies:\n")  
            
            self.content = "name: env\nchannels:\n  - conda-forge\ndependencies:\n"  
            
            for mod, ver in versions:
                if ver == "standard library":
                    line = f"  - {mod}  # standard library" if self.include_comments else f"  - {mod}"
                elif "(local file)" in mod:
                    line = f"  - {mod}  # local file" if self.include_comments else f"  - {mod}"
                else:
                    line = f"  - {mod}={ver}" if ver else f"  - {mod}  # not installed" if self.include_comments else f"  - {mod}"
                self.output_text.insert(tk.END, line + "\n")
                
                
                if ver != "standard library" and "(local file)" not in mod:
                    package_name = self.import_to_package.get(mod, mod)
                    self.content += f"  - {package_name}={ver}\n" if ver else f"  - {package_name}  # not installed\n"

    def save_env_file(self):
        if not hasattr(self, 'content') or not self.content:
            messagebox.showwarning("No Content", "Please generate the environment file first.")
            return

        default_extension = ".txt" if self.output_type.get() == "pip" else ".yml"
        filetypes = [("Text files", "*.txt"), ("YAML files", "*.yml"), ("All files", "*.*")]
        save_path = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=filetypes)

        if save_path:
            if (self.output_type.get() == "pip" and not save_path.endswith(".txt")) or \
               (self.output_type.get() == "conda" and not save_path.endswith(".yml")):
                messagebox.showwarning("Incorrect File Type", f"Please save the file with the correct extension ({default_extension}).")
                return

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.content)
            messagebox.showinfo("File Saved", f"Environment file saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvBuilder(root) 
    root.mainloop()
