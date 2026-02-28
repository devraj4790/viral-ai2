import streamlit as st
import yt_dlp
import os
from clipsai import ClipFinder, Transcriber, resize

st.set_page_config(page_title="AI Viral Clip Maker", layout="wide")

st.title("🎬 AI Viral Moment Detector (URL Edition)")
st.subheader("Paste a link to turn long videos into viral-ready clips.")

# --- STEP 1: THE URL INPUT ---
url = st.text_input("Paste YouTube or Video URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("Process Video from URL"):
        with st.status("📥 Downloading and Analyzing...", expanded=True) as status:
            
            # STEALH DOWNLOAD SETTINGS
            st.write("Downloading video (Stealth Mode)...")
           # ULTIMATE STEALTH SETTINGS
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'temp_video.mp4',
                'noplaylist': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Sec-Fetch-Mode': 'navigate',
                },
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0'
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # --- STEP 2: CLIPSAI TRANSCRIBING ---
                st.write("Step 1: Transcribing audio...")
                transcriber = Transcriber()
                transcription = transcriber.transcribe(audio_file_path="temp_video.mp4")

                # --- STEP 3: CLIPSAI VIRAL DETECTION ---
                st.write("Step 2: Detecting viral moments...")
                clipfinder = ClipFinder()
                clips = clipfinder.find_clips(transcription=transcription)
                
                st.success(f"✅ Found {len(clips)} potential viral moments!")

                # --- STEP 4: RESIZE AND DISPLAY ---
                for i, clip in enumerate(clips[:3]): 
                    with st.expander(f"Clip {i+1}: {clip.start_time}s - {clip.end_time}s"):
                        if st.button(f"Generate Vertical Clip {i+1}", key=f"btn_{i}"):
                            with st.spinner("Resizing to 9:16 vertical..."):
                                crops = resize(
                                    video_file_path="temp_video.mp4",
                                    pyannote_auth_token="YOUR_HUGGINGFACE_TOKEN", 
                                    aspect_ratio=(9, 16)
                                )
                                st.video("temp_video.mp4", start_time=int(clip.start_time))
                
                status.update(label="All steps complete!", state="complete")
            except Exception as e:
                st.error(f"Download Error: {e}")
else:
    st.info("Please paste a URL to begin.")

