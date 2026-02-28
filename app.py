import streamlit as st
import yt_dlp
import os
from clipsai import ClipFinder, Transcriber, resize

st.set_page_config(page_title="AI Viral Clip Maker", layout="wide")

st.title("🎬 AI Viral Moment Detector")
st.subheader("Paste a link to turn long videos into viral-ready clips.")

url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    if st.button("Process Video"):
        with st.status("📥 Running AI Pipeline...", expanded=True) as status:
            
            # --- NEW DOWNLOAD STRATEGY ---
            st.write("Attempting Stealth Stream...")
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'temp_video.mp4',
                'quiet': True,
                'no_warnings': True,
                # This mimics a real browser session even more strictly
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'add_header': [
                    'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language: en-US,en;q=0.5',
                ],
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.write("Step 1: Transcribing...")
                transcriber = Transcriber()
                transcription = transcriber.transcribe(audio_file_path="temp_video.mp4")

                st.write("Step 2: Finding viral moments...")
                clipfinder = ClipFinder()
                clips = clipfinder.find_clips(transcription=transcription)
                
                st.success(f"✅ Found {len(clips)} clips!")

                for i, clip in enumerate(clips[:3]): 
                    with st.expander(f"Clip {i+1}"):
                        if st.button(f"Generate Vertical Clip {i+1}", key=f"btn_{i}"):
                            # Note: Replace with your actual HF token
                            crops = resize(
                                video_file_path="temp_video.mp4",
                                pyannote_auth_token="YOUR_HUGGINGFACE_TOKEN", 
                                aspect_ratio=(9, 16)
                            )
                            st.video("temp_video.mp4", start_time=int(clip.start_time))
                
                status.update(label="Complete!", state="complete")
                
            except Exception as e:
                st.error(f"Error encountered: {e}")
                st.info("Tip: If you see '403 Forbidden', try a shorter video or a different channel.")
else:
    st.info("Paste a URL above to start.")

