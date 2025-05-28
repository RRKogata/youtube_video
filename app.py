from flask import Flask, request, render_template_string
import yt_dlp
import os
from pathlib import Path
import time

app = Flask(__name__)

# Get user's Downloads folder
downloads_folder = str(Path.home() / "Downloads")

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>YouTube Downloader</title>
  <style>
    body { font-family: Arial; text-align: center; padding: 40px; background-color: #f4f4f4; }
    input[type=text] { padding: 10px; width: 60%; }
    input[type=submit] { padding: 10px 20px; }
  </style>
</head>
<body>
  <h1>YouTube Video / Playlist Downloader</h1>
  <form method="post" action="/download">
    <input type="text" name="url" placeholder="Enter YouTube video or playlist URL" required>
    <br><br>
    <input type="submit" value="Download">
  </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'force_overwrites': True,
            'noplaylist': False,
            'no_cache_dir': True,
            'no_mtime': True,
            'cookies': 'cookies.txt'  # ✅ Use browser cookies for login-required videos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # Handle playlist vs single video
            if 'entries' in info:
                titles = [entry.get('title', 'video') for entry in info['entries']]
                msg = f"<h3>✅ Playlist downloaded:</h3><ul>" + ''.join([f"<li>{t}</li>" for t in titles]) + "</ul>"
            else:
                title = info.get('title', 'video')
                extension = info.get('ext', 'mp4')
                file_path = os.path.join(downloads_folder, f"{title}.{extension}")
                now = time.time()
                os.utime(file_path, (now, now))
                msg = f"<h3>✅ Download complete: <i>{title}</i></h3><p>Saved to: <code>{file_path}</code></p>"

        return msg + "<br><a href='/'>Back</a>"

    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
