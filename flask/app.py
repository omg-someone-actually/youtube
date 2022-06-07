from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
from os.path import exists
from typing import Union
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from youtubesearchpython import VideosSearch

app = Flask(__name__)
formatter = WebVTTFormatter()

@app.route('/', methods=('GET', 'POST'))
def index() -> Union[redirect, render_template]:
    if request.method == 'POST':
      url = request.form['url']
      return redirect(f'/watch/{url[len(url)-11:]}')
      
    return render_template('home.html')

@app.route('/watch/<video_id>')
def play_video(video_id: str) -> Union[redirect, render_template]:
  if not exists(f'{video_id}.mp4') and not exists(video_id):
      youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')
      video = youtube.streams.get_highest_resolution()
      video.download(filename=f'{video_id}.mp4', output_path='static')

      try:
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        captions_formatted = formatter.format_transcript(captions)
        with open(f'static/{video_id}-captions.vtt', 'w') as captions_file:
          captions_file.write(captions_formatted)
      except Exception:
        pass
        
  return render_template('video.html', video=f'{video_id}.mp4', captions=f'{video_id}-captions.vtt')

@app.route('/search', methods=('GET', 'POST'))
def search():
  if request.method == 'POST':
    search_query = request.form['search']
    return redirect(f'/search/{search_query}')
    
  return render_template('initial-search.html')

@app.route('/search/<query>', methods=('GET', 'POST'))
def search_videos(query: str):
  videos = VideosSearch(query)
  return render_template('search.html', videos=videos)