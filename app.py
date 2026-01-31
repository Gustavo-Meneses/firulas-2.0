import streamlit as st
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
import moviepy.video.fx.all as vfx_all
from PIL import Image, ImageEnhance
import numpy as np
import tempfile

# Correção de compatibilidade para versões novas do Pillow que o MoviePy 1.0.3 exige
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

# Configuração da Página
st.set_page_config(page_title="Synthwave Hub", page_icon="🌃", layout="wide")

# Estilização CSS
st.markdown("""
    <style>
    .main { background-color: #0d0221; color: #00f2ff; }
    .stButton>button { background-color: #ff007f; color: white; border-radius: 20px; border: none; width: 100%; }
    .stDownloadButton>button { background-color: #7000ff; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌃 Synthwave Creative Hub")
st.write("Hub de automação para posts imersivos.")

def apply_synthwave_filter(pil_img):
    """Aplica o color grading neon."""
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.4)
    return pil_img

def glitch_effect(get_frame, t):
    """Efeito de distorção de cor (RGB Shift)."""
    frame = get_frame(t)
    frame_glitch = frame.copy()
    shift = int(6 * np.sin(t * 12))
    frame_glitch[:, :, 0] = np.roll(frame[:, :, 0], shift, axis=1)
    return frame_glitch

# --- PASSO A PASSO ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Fundo (Background)")
    st.link_button("Ir para Recraft.ai", "https://www.recraft.ai")
    bg_file = st.file_uploader("Upload do Fundo", type=['png', 'jpg'], key="bg")

with col2:
    st.subheader("2. Logo 3D")
    st.link_button("Ir para 3DLogoLab.io", "https://3dlogolab.io")
    logo_file = st.file_uploader("Upload do Logo (PNG)", type=['png'], key="logo")

with col3:
    st.subheader("3. Áudio 8D/Reverb")
    st.link_button("Ir para AudioAlter.com", "https://audioalter.com")
    audio_file = st.file_uploader("Upload (.mp3, .wav, .ogg)", type=['mp3', 'wav', 'ogg'], key="audio")

st.divider()

# CONFIGURAÇÕES SIDEBAR
st.sidebar.header("🎛️ Ajustes de Vibe")
duration = st.sidebar.slider("Duração (seg)", 5, 15, 10)
zoom_speed = st.sidebar.slider("Intensidade do Zoom", 0.01, 0.10, 0.03)

if st.button("🚀 RENDERIZAR VIBE FINAL"):
    if bg_file and logo_file and audio_file:
        with st.spinner("Limpando ruídos e masterizando neon..."):
            try:
                # 1. Processar Imagem de Fundo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
                    img = Image.open(bg_file).convert("RGB")
                    img = apply_synthwave_filter(img)
                    img.save(tmp_bg.name)
                    bg_path = tmp_bg.name

                # 2. Processar Logo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
                    tmp_logo.write(logo_file.getvalue())
                    logo_path = tmp_logo.name

                # 3. Processar Áudio com Extensão Dinâmica
                suffix = "." + audio_file.name.split(".")[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
                    tmp_audio.write(audio_file.getvalue())
                    audio_path = tmp_audio.name

                # MONTAGEM MOVIEPY
                bg_clip = (ImageClip(bg_path)
                           .set_duration(duration)
                           .resize(height=1920)
                           .set_position('center')
                           .fx(vfx.resize, lambda t: 1 + zoom_speed * t))

                logo_clip = (ImageClip(logo_path)
                             .set_duration(duration)
                             .resize(width=500)
                             .set_position(('center', 'center')))

                audio = AudioFileClip(audio_path).subclip(0, duration)

                # Composição
                video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920))
                video = video.fl(glitch_effect)
                video = video.set_audio(audio)

                output_path = "synthwave_vibe.mp4"
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.success("✨ Post Masterizado!")
                st.video(output_path)
                
                with open(output_path, "rb") as f:
                    st.download_button("💾 Baixar Vídeo", f, file_name="post_synthwave.mp4")

                # Cleanup
                os.remove(bg_path)
                os.remove(logo_path)
                os.remove(audio_path)

            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.error("Carregue todos os arquivos antes de renderizar.")
