import streamlit as st
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from PIL import Image, ImageEnhance
import numpy as np
import tempfile

# Configuração da Página
st.set_page_config(page_title="Synthwave Hub", page_icon="🌃", layout="wide")

# Estilização CSS para a vibe Synthwave
st.markdown("""
    <style>
    .main { background-color: #0d0221; color: #00f2ff; }
    .stButton>button { background-color: #ff007f; color: white; border-radius: 20px; border: none; }
    .stDownloadButton>button { background-color: #7000ff; color: white; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌃 Synthwave Creative Hub")
st.write("Siga os passos abaixo para construir seu post imersivo.")

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

# PASSO 1: BACKGROUND
with col1:
    st.subheader("1. Fundo (Background)")
    st.link_button("Ir para Recraft.ai", "https://www.recraft.ai")
    bg_file = st.file_uploader("Upload do Fundo", type=['png', 'jpg'], key="bg")

# PASSO 2: LOGO 3D
with col2:
    st.subheader("2. Logo 3D")
    st.link_button("Ir para 3DLogoLab.io", "https://3dlogolab.io")
    logo_file = st.file_uploader("Upload do Logo (PNG)", type=['png'], key="logo")

# PASSO 3: ÁUDIO IMERSIVO
with col3:
    st.subheader("3. Áudio 8D/Reverb")
    st.link_button("Ir para AudioAlter.com", "https://audioalter.com")
    audio_file = st.file_uploader("Upload da Trilha", type=['mp3', 'wav'], key="audio")

st.divider()

# CONFIGURAÇÕES FINAIS
st.sidebar.header("🎛️ Ajustes de Vibe")
duration = st.sidebar.slider("Duração do Post (seg)", 5, 15, 10)
zoom_speed = st.sidebar.slider("Intensidade do Zoom", 0.01, 0.10, 0.03)

if st.button("🚀 RENDERIZAR VIBE FINAL", use_container_width=True):
    if bg_file and logo_file and audio_file:
        with st.spinner("Sintonizando frequências neon..."):
            try:
                # Processamento de arquivos temporários
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
                    img = Image.open(bg_file).convert("RGB")
                    img = apply_synthwave_filter(img)
                    img.save(tmp_bg.name)
                    bg_path = tmp_bg.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
                    tmp_logo.write(logo_file.getvalue())
                    logo_path = tmp_logo.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                    tmp_audio.write(audio_file.getvalue())
                    audio_path = tmp_audio.name

                # Montagem do Vídeo
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

                video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920))
                video = video.fl(glitch_effect)
                video = video.set_audio(audio)

                output_filename = "synthwave_vibe.mp4"
                video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac", remove_temp=True)

                st.success("✨ Masterização Concluída!")
                st.video(output_filename)
                
                with open(output_filename, "rb") as f:
                    st.download_button("💾 Baixar para Instagram/TikTok", f, file_name=output_filename)

                # Cleanup
                os.remove(bg_path)
                os.remove(logo_path)
                os.remove(audio_path)

            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.error("Ops! Você precisa carregar os 3 arquivos para prosseguir.")

st.info("💡 Dica: No Recraft, use o estilo 'Glow' ou 'Synthwave' para melhores resultados.")
