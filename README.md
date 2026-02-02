# Video_and_Audio_Downloader
you can download the youtube vedio and the audio that waht i tested till now



# Media Downloader

A robust Python-based GUI application to download high-quality videos and audio from various platforms (like YouTube).

## Features

- **Video & Audio**: Download in MP4 (Video) or MP3 (Audio) format.
- **Quality Selection**: Choose from 1080p, 720p, 480p, or Best Available.
- **Media Preview**: Automatically displays the video thumbnail when you paste a URL.
- **Progress Tracking**: Real-time progress bar showing download percentage, speed, and ETA.
- **Smart Audio**: Automatically converts downloaded audio to universally compatible AAC (for video) or MP3.
- **Custom Save Location**: easy-to-use "Browse" button to select where files are saved.
- **User Friendly**: Paste button, Clear button, and Right-click menu support.
- **Built-in Tools**: Automatically handles dependencies like `ffmpeg` so you don't have to install them manually.

## Requirements

- Python 3.x
- Internet connection

## Installation

1. Open a terminal/command prompt in the project folder.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python media_downloader.py
   ```
2. **Paste the URL** of the video you want to download.
3. Select **Video** or **Audio**.
4. If downloading video, select your desired **Quality**.
5. (Optional) Click **Browse** to change the save folder.
6. Click **Download**.

## Dependencies

- `yt-dlp`: The core downloading engine.
- `ffmpeg-python` & `imageio-ffmpeg`: logic for media conversion.
- `Pillow`: For displaying thumbnails.
- `requests`: For fetching thumbnails.
- `tkinter`: Standard Python GUI library (built-in).

## Troubleshooting

- **"ffmpeg not found"**: The app includes a built-in version, but if you see this, try running `pip install imageio-ffmpeg` again.
- **Download fails**: Ensure the URL is valid and accessible. Some live streams or age-restricted content might require additional authentication (not currently supported).

## License

This project is for educational purposes. Please respect copyright laws and terms of service of the websites you download from.

