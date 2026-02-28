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
    # Everything below this line MUST be indented by 4 spaces
    if st.button("Process Video from URL"):
        with st.status("📥 Downloading and Analyzing...", expanded=True) as status:
            
            # Download the video using yt_dlp
            st.write("Downloading video...")
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': 'temp_video.mp4',
                'noplaylist': True,
            }
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
                            # Replace YOUR_HUGGINGFACE_TOKEN with your actual token
                            crops = resize(
                                video_file_path="temp_video.mp4",
                                pyannote_auth_token="YOUR_HUGGINGFACE_TOKEN", 
                                aspect_ratio=(9, 16)
                            )
                            st.video("temp_video.mp4", start_time=int(clip.start_time))
            
            status.update(label="All steps complete!", state="complete")
else:
    st.info("Please paste a URL to begin.")
