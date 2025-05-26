from flask import Flask, request, render_template_string
import yt_dlp
import os
import time
from pathlib import Path

app = Flask(__name__)

# Get user's Downloads folder
downloads_folder = str(Path.home() / "Downloads")


# HTML template
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
  <h1>YouTube Video Downloader</h1>
  <form method="post" action="/download">
    <input type="text" name="url" placeholder="Enter YouTube video URL" required>
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
            'noplaylist': False,    # ✅ Allows downloading full playlists
            'no_cache_dir': True,
            'no_mtime': True  # <<<< This ensures the file shows today's date
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            extension = info.get('ext', 'mp4')
            file_path = os.path.join(downloads_folder, f"{title}.{extension}")


        # ✅ Manually update file's modified time to now (optional but extra-safe)
        now = time.time()
        os.utime(file_path, (now, now))
      
      
        return f"<h3>✅ Download complete: <i>{title}</i></h3><p>Saved to: <code>{file_path}</code></p>"
    except Exception as e:
        return f"<h3>❌ Error: {str(e)}</h3>"

if __name__ == '__main__':
    app.run(debug=True)
