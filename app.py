import streamlit as st
import yt_dlp
import whisper
import os
from moviepy.editor import VideoFileClip

st.set_page_config(page_title="AI Viral Clip Maker")
st.title("🚀 URL to Viral Clips AI")

url = st.text_input("Paste YouTube URL here:")

if url:
if st.button("Generate Clips"):
with st.status("📥 Processing...", expanded=True) as status:
ydl_opts = {'format': 'best[ext=mp4]', 'outtmpl': 'video.mp4'}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
ydl.download([url])
st.write("🤖 AI is finding viral moments...")
model = whisper.load_model("base")
result = model.transcribe("video.mp4")
video = VideoFileClip("video.mp4")
for i, seg in enumerate(result['segments'][:3]):
clip = video.subclip(seg['start'], seg['end'])
w, h = clip.size
final = clip.crop(x_center=w/2, width=h*(9/16), height=h)
name = f"clip_{i}.mp4"
final.write_videofile(name, codec="libx264")
st.video(name)
st.download_button(f"Download {name}", open(name, "rb"), file_name=name)
status.update(label="Done!", state="complete")
