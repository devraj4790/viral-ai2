import streamlit as st
import yt_dlp
import os
from clipsai import ClipFinder, Transcriber, resize

st.set_page_config(page_title="AI Viral Clip Maker", layout="wide")

st.title("🎬 AI Viral Moment Detector (Stealth Mode)")

url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("🚀 Kill the 403 & Process"):
        with st.status("📥 Stealth Downloading...", expanded=True) as status:
            
            # --- STEALTH KILLER SETTINGS ---
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'temp_video.mp4',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # This mimics a real Google Chrome browser on Windows 11
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                    'Referer': 'https://www.google.com/',
                },
                'nocheckcertificate': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    st.write("📡 Bypassing YouTube Security...")
                    ydl.download([url])
                
                st.write("🎤 Step 1: Transcribing Audio...")
                transcriber = Transcriber()
                transcription = transcriber.transcribe(audio_file_path="temp_video.mp4")

                st.write("🧠 Step 2: AI Finding Viral Moments...")
                clipfinder = ClipFinder()
                clips = clipfinder.find_clips(transcription=transcription)
                
                st.success(f"✅ Found {len(clips)} Viral Clips!")

                for i, clip in enumerate(clips[:3]): 
                    with st.expander(f"Clip {i+1}: View & Download"):
                        st.video("temp_video.mp4", start_time=int(clip.start_time))
                
                status.update(label="Complete!", state="complete")
                
            except Exception as e:
                st.error(f"YouTube Blocked the Server: {e}")
                st.info("💡 Pro-Tip: If this fails, DELETE your app on Streamlit and RE-DEPLOY. It resets your IP address.")


