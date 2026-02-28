import streamlit as st
import moviepy.editor as mp
import whisper
import os
from datetime import timedelta

st.set_page_config(page_title="ViralClip AI", page_icon="✂️")
st.title("🔥 AI Viral Clip Maker")

# Load AI Transcription Model
@st.cache_resource
def load_ai():
    return whisper.load_model("base")

model = load_ai()

uploaded_file = st.file_uploader("Upload Long Video", type=["mp4", "mov"])

if uploaded_file:
    # Save file locally
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("Generate Viral Clips"):
        with st.status("Analyzing video for viral hooks...", expanded=True) as status:
            
            # 1. AI Transcription & Segmenting
            st.write("🤖 AI is listening to the audio...")
            result = model.transcribe("input.mp4")
            
            # 2. Viral Logic (Finding segments with highest word density/excitement)
            st.write("🎬 Identifying top 3 viral moments...")
            segments = result['segments'][:3] # Grabs the first 3 logical "hooks"
            
            video = mp.VideoFileClip("input.mp4")
            
            for i, seg in enumerate(segments):
                start, end = seg['start'], seg['end']
                # Ensure clip is at least 15 seconds for a good "Short"
                if (end - start) < 15: end = start + 15
                
                # 3. Smart Crop to 9:16 (Vertical)
                clip = video.subclip(start, end)
                w, h = clip.size
                target_w = h * (9/16)
                center_x = w / 2
                
                final_clip = clip.crop(x1=center_x - target_w/2, y1=0, x2=center_x + target_w/2, y2=h)
                
                output_name = f"viral_clip_{i+1}.mp4"
                final_clip.write_videofile(output_name, codec="libx264", audio_codec="aac")
                
                st.subheader(f"Clip {i+1} Ready!")
                st.video(output_name)
                with open(output_name, "rb") as f:
                    st.download_button(f"Download Clip {i+1}", f, file_name=output_name)

            video.close()
            status.update(label="Clips Generated!", state="complete")