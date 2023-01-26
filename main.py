import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

from pathlib import Path
from tkinter import filedialog

from commandfilegenerator import generate_script_file

class FileSelectionUI():

    def __init__(self):
       self._setup()

    def _setup(self):
        
        self.window = tk.Tk()
        self.window.title('Parse labels')
        self.window.resizable(width=True, height=False)

        self.var_labels_file = tk.StringVar()
        self.var_media_file = tk.StringVar()
        self.var_script_file = tk.StringVar()

        top_frame = ttk.Frame(master=self.window, padding=(5, 5, 5, 0))
        top_frame.columnconfigure(index=0, weight=0)
        top_frame.columnconfigure(index=1, weight=1, minsize=120)
        top_frame.columnconfigure(index=2, weight=0)
        top_frame.rowconfigure(index=0, weight=0)
        top_frame.rowconfigure(index=1, weight=0)
        top_frame.rowconfigure(index=2, weight=0)

        lbl_labels_file = ttk.Label(master=top_frame, text='Labels file:')
        lbl_labels_file.grid(row=0, column=0, sticky='nw')

        self.ent_labels_file = ttk.Entry(master=top_frame, 
            textvariable=self.var_labels_file)
        self.ent_labels_file.grid(row=0, column=1, columnspan=2, sticky='new')

        btn_browse_labels_file = ttk.Button(master=top_frame, text='Browse ...', 
            command=self.browse_for_labels_file)
        btn_browse_labels_file.grid(row=0, column=3, sticky='ne')

        lbl_media_file = ttk.Label(master=top_frame, text='Media file:')
        lbl_media_file.grid(row=1, column=0, sticky='nw')

        self.ent_media_file = ttk.Entry(master=top_frame,
            textvariable=self.var_media_file)
        self.ent_media_file.grid(row=1, column=1, columnspan=2, sticky='new')

        btn_browse_media_file = ttk.Button(master=top_frame, text='Browse ...',
            command=self.browse_for_media_file)
        btn_browse_media_file.grid(row=1, column=3, sticky='ne')

        lbl_script_file = ttk.Label(master=top_frame, text='Script file:')
        lbl_script_file.grid(row=2, column=0, sticky='nw')

        self.ent_script_file = ttk.Entry(master=top_frame,
            textvariable=self.var_script_file)
        self.ent_script_file.grid(row=2, column=1, columnspan=2, sticky='new')

        btn_browse_script_file = ttk.Button(master=top_frame, text='Browse ...',
            command=self.browse_for_script_file)
        btn_browse_script_file.grid(row=2, column=3, sticky='ne')

        top_frame.pack(fill=tk.X)
        
        bottom_frame = ttk.Frame(master=self.window, padding=(5,0,5,5))

        btn_ok = ttk.Button(master=bottom_frame, text="OK",
            command=self.create_ffmpeg_script)
        btn_ok.pack(side=tk.RIGHT)
        
        btn_cancel = ttk.Button(master=bottom_frame, text="Cancel",
            command=self.window.destroy)
        btn_cancel.pack(side=tk.RIGHT)

        bottom_frame.pack(fill=tk.X)
        
    def browse_for_labels_file(self):
        filename = filedialog.askopenfilename(
                        title='Select labels file',
                        filetypes=[('text files', '*.txt'),
                                   ('All files', '*.*')],
                        defaultextension='.txt')
        if filename:
            self.var_labels_file.set(filename)
        
    def browse_for_media_file(self):
        filename = filedialog.askopenfilename(
            title='Select media file',
            filetypes=[('MP4 files', '*.mp4'),
                       ('M4A files', '*.m4a'),
                       ('MP3 files', '*.mp3'),
                       ('All files', '*.*')],
                       defaultextension='.mp4')
        if filename:
            self.var_media_file.set(filename)
        
    def browse_for_script_file(self):
        filename = filedialog.asksaveasfilename(
                    title='Save script as',
                    defaultextension='.sh',
                    filetypes=[('bash scripts', '*.sh'),
                               ('All files', '*.*')])
        if filename:
            self.var_script_file.set(filename)
            
    def create_ffmpeg_script(self):
        labels_file = Path(self.var_labels_file.get())
        media_file = Path(self.var_media_file.get())
        script_file = Path(self.var_script_file.get())
        generate_script_file(labels_file, media_file, script_file)        
        tkinter.messagebox.showinfo(title='Create ffmpeg script', 
                                    message='Done!')
        
def main():
    ui = FileSelectionUI()

    width = 400
    height = 135

    screen_width = ui.window.winfo_screenwidth()
    screen_height = ui.window.winfo_screenheight()

    left = (screen_width - width) // 2 
    top = (screen_height - height) // 2

    ui.window.geometry(f'{width}x{height}+{left}+{top}')

    ui.window.mainloop()
    
if __name__ == '__main__':
    main()
