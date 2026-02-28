import streamlit as st
import yt_dlp
import os
from clipsai import ClipFinder, Transcriber, resize

st.set_page_config(page_title="AI Viral Clip Maker", layout="wide")

st.title("🎬 AI Viral Moment Detector (URL Edition)")
st.subheader("Paste a link to turn long videos into viral-ready clips.")

url = st.text_input("Paste YouTube or Video URL here:", placeholder="...")

if url:
if st.button("Process Video from URL"):
with st.status("📥 Downloading and Analyzing...", expanded=True) as status:
st.write("Downloading video...")
ydl_opts = {
'format': 'best[ext=mp4]',
'outtmpl': 'temp_video.mp4',
'noplaylist': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
ydl.download([url])

else:
st.info("Please paste a URL to begin.")
