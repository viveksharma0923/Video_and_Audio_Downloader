import yt_dlp
import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import imageio_ffmpeg
from PIL import Image, ImageTk
import requests
from io import BytesIO

class MediaDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Downloader")
        self.root.geometry("700x750")
        
        # --- Top Frame: URL & Inputs ---
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)

        # URL Input
        tk.Label(top_frame, text="Enter URL:").pack(anchor=tk.W)
        
        self.input_frame = tk.Frame(top_frame)
        self.input_frame.pack(pady=5, fill=tk.X)

        self.url_entry = tk.Entry(self.input_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        self.url_entry.bind("<FocusOut>", self.on_url_change)

        tk.Button(self.input_frame, text="Paste", command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=2)
        tk.Button(self.input_frame, text="Clear", command=self.clear_input).pack(side=tk.LEFT, padx=2)

        # Save Path
        tk.Label(top_frame, text="Save to:").pack(anchor=tk.W, pady=(10, 0))
        path_frame = tk.Frame(top_frame)
        path_frame.pack(pady=5, fill=tk.X)
        
        self.path_var = tk.StringVar(value=os.getcwd())
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
        
        tk.Button(path_frame, text="Browse", command=self.browse_path).pack(side=tk.LEFT)

        # --- Middle Frame: Options & Thumbnail ---
        mid_frame = tk.Frame(root)
        mid_frame.pack(pady=5, fill=tk.BOTH, expand=True, padx=20)
        
        # Left side: Options
        options_frame = tk.Frame(mid_frame)
        options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        # Download Type
        self.type_var = tk.StringVar(value="video")
        tk.Label(options_frame, text="Type:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        tk.Radiobutton(options_frame, text="Video (MP4)", variable=self.type_var, value="video", command=self.toggle_quality).pack(anchor=tk.W)
        tk.Radiobutton(options_frame, text="Audio (MP3)", variable=self.type_var, value="audio", command=self.toggle_quality).pack(anchor=tk.W)
        
        # Quality
        self.quality_frame = tk.Frame(options_frame)
        self.quality_frame.pack(pady=10, anchor=tk.W)
        tk.Label(self.quality_frame, text="Quality:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.quality_var = tk.StringVar(value="Best (Auto)")
        self.quality_options = ["Best (Auto)", "1080p", "720p", "480p"]
        self.quality_menu = ttk.OptionMenu(self.quality_frame, self.quality_var, self.quality_options[0], *self.quality_options)
        self.quality_menu.pack(pady=5)

        # Right side: Thumbnail
        self.thumb_label = tk.Label(mid_frame, text="No Thumbnail", bg="#e0e0e0", width=40, height=15)
        self.thumb_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Bottom Frame: Actions & Logs ---
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10, fill=tk.X, padx=20)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(bottom_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.progress_label = tk.Label(bottom_frame, text="Ready")
        self.progress_label.pack()

        # Download Button
        self.download_button = tk.Button(bottom_frame, text="Download", command=self.start_download, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.download_button.pack(pady=10)
        
        # Logs
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=10, state='disabled')
        self.log_area.pack(pady=10, padx=20)

        # Context menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Paste", command=self.paste_from_clipboard)
        self.context_menu.add_command(label="Clear", command=self.clear_input)
        self.url_entry.bind("<Button-3>", self.show_context_menu)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def paste_from_clipboard(self):
        try:
            content = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, content)
            self.on_url_change(None) # Trigger thumbnail fetch
        except tk.TclError:
            pass

    def clear_input(self):
         self.url_entry.delete(0, tk.END)
         self.reset_thumbnail()

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
        
    def toggle_quality(self):
        if self.type_var.get() == "audio":
            self.quality_frame.pack_forget()
        else:
            self.quality_frame.pack(pady=10, anchor=tk.W)

    def on_url_change(self, event):
        url = self.url_entry.get().strip()
        if url:
             threading.Thread(target=self.fetch_thumbnail, args=(url,), daemon=True).start()

    def fetch_thumbnail(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                thumb_url = info.get('thumbnail')
                
                if thumb_url:
                    response = requests.get(thumb_url)
                    img_data = response.content
                    img = Image.open(BytesIO(img_data))
                    img.thumbnail((320, 240)) # Resize for display
                    self.tk_thumb = ImageTk.PhotoImage(img)
                    self.thumb_label.config(image=self.tk_thumb, text="")
        except Exception:
            self.reset_thumbnail()

    def reset_thumbnail(self):
         self.thumb_label.config(image='', text="No Thumbnail")

    def log_message(self, message):
        self.root.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_download(self):
        url = self.url_entry.get().strip()
        path = self.path_var.get().strip()
        
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid URL.")
            return
        
        self.download_button.config(state='disabled')
        self.progress_var.set(0)
        self.progress_label.config(text="Starting...")
        self.log_message(f"Starting download for: {url}")
        
        threading.Thread(target=self.download_task, args=(url, path)).start()

    def download_task(self, url, save_path):
        download_type = self.type_var.get()
        quality_choice = self.quality_var.get()
        
        try:
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            self.log_message(f"Using built-in ffmpeg: {ffmpeg_path}")
        except Exception:
            ffmpeg_path = None
            self.log_message("Warning: Could not find built-in ffmpeg.")

        # Ensure directory exists
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
        out_tmpl = os.path.join(save_path, '%(title)s.%(ext)s')

        ydl_opts = {
            'progress_hooks': [self.progress_hook],
            'noplaylist': True,
            'outtmpl': out_tmpl,
            'ffmpeg_location': ffmpeg_path,
        }
        
        if download_type == "audio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
            self.log_message("Mode: Audio (MP3)")
        else:
            format_str = 'bestvideo+bestaudio/best'
            if "1080p" in quality_choice:
                format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif "720p" in quality_choice:
                format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif "480p" in quality_choice:
                format_str = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            
            ydl_opts.update({
                'format': format_str,
                'merge_output_format': 'mp4',
                'postprocessor_args': {'merger': ['-c:a', 'aac']},
            })
            self.log_message(f"Mode: Video (MP4), Quality: {quality_choice} (Forcing AAC audio)")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_message("Download completed successfully!")
            messagebox.showinfo("Success", "Download completed successfully!")
            self.progress_label.config(text="Completed!")
            self.progress_var.set(100)
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.progress_label.config(text="Error occurred")
        finally:
             self.root.after(0, lambda: self.download_button.config(state='normal'))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                self.progress_var.set(float(p))
                
                eta = d.get('_eta_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                self.progress_label.config(text=f"Downloading: {p}% | Speed: {speed} | ETA: {eta}")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.progress_label.config(text="Processing...")


if __name__ == "__main__":
    root = tk.Tk()
    app = MediaDownloaderApp(root)
    root.mainloop()
