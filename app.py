import streamlit as st
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
import moviepy.video.fx.all as vfx_all
from PIL import Image, ImageEnhance
import numpy as np
import tempfile

# Monkey Patch para compatibilidade com Pillow moderno
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

st.set_page_config(page_title="Synthwave Hub", page_icon="🌃", layout="wide")

# Estilo Customizado
st.markdown("""
    <style>
    .main { background-color: #0d0221; color: #00f2ff; }
    .stButton>button { background-color: #ff007f; color: white; border-radius: 20px; border: none; width: 100%; height: 3em; font-weight: bold; }
    .stDownloadButton>button { background-color: #7000ff; color: white; border-radius: 20px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌃 Synthwave Creative Hub")
st.write("Criação automatizada de conteúdo imersivo.")

def apply_synthwave_filter(pil_img):
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.4)
    return pil_img

def glitch_effect(get_frame, t):
    frame = get_frame(t)
    frame_glitch = frame.copy()
    shift = int(6 * np.sin(t * 12))
    frame_glitch[:, :, 0] = np.roll(frame[:, :, 0], shift, axis=1)
    return frame_glitch

# --- UI DE UPLOAD ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Fundo (Background)")
    st.link_button("Ir para Recraft.ai", "https://www.recraft.ai")
    bg_file = st.file_uploader("Upload Imagem", type=['png', 'jpg'], key="bg")

with col2:
    st.subheader("2. Logo 3D")
    st.link_button("Ir para 3DLogoLab.io", "https://3dlogolab.io")
    logo_file = st.file_uploader("Upload Logo (PNG)", type=['png'], key="logo")

with col3:
    st.subheader("3. Áudio 8D/Reverb")
    st.link_button("Ir para AudioAlter.com", "https://audioalter.com")
    audio_file = st.file_uploader("Upload Áudio", type=['mp3', 'wav', 'ogg'], key="audio")

st.divider()

# CONFIGURAÇÕES
st.sidebar.header("🎛️ Ajustes de Vibe")
user_duration = st.sidebar.slider("Duração Desejada (seg)", 3, 15, 10)
zoom_speed = st.sidebar.slider("Intensidade do Zoom", 0.01, 0.10, 0.03)

if st.button("🚀 RENDERIZAR VIBE FINAL"):
    if bg_file and logo_file and audio_file:
        with st.spinner("Sintonizando frequências..."):
            try:
                # 1. Processar Imagens
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
                    img = Image.open(bg_file).convert("RGB")
                    img = apply_synthwave_filter(img)
                    img.save(tmp_bg.name)
                    bg_path = tmp_bg.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
                    tmp_logo.write(logo_file.getvalue())
                    logo_path = tmp_logo.name

                # 2. Processar Áudio
                suffix = "." + audio_file.name.split(".")[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_audio:
                    tmp_audio.write(audio_file.getvalue())
                    audio_path = tmp_audio.name

                # CARREGAR ÁUDIO E VALIDAR DURAÇÃO
                audio = AudioFileClip(audio_path)
                # Se o áudio for menor que a duração pedida, usamos a duração do áudio
                final_duration = min(user_duration, audio.duration)
                audio = audio.subclip(0, final_duration)

                # 3. Montagem Clips
                bg_clip = (ImageClip(bg_path)
                           .set_duration(final_duration)
                           .resize(height=1920)
                           .set_position('center')
                           .fx(vfx.resize, lambda t: 1 + zoom_speed * t))

                logo_clip = (ImageClip(logo_path)
                             .set_duration(final_duration)
                             .resize(width=500)
                             .set_position(('center', 'center')))

                # 4. Composição e Exportação
                video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920))
                video = video.fl(glitch_effect)
                video = video.set_audio(audio)

                output_path = "vibe_final.mp4"
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                st.success(f"✨ Pronto! Vídeo gerado com {final_duration:.1f} segundos.")
                st.video(output_path)
                
                with open(output_path, "rb") as f:
                    st.download_button("💾 Baixar Vídeo", f, file_name="post_synthwave.mp4")

                # Cleanup
                os.remove(bg_path)
                os.remove(logo_path)
                os.remove(audio_path)

            except Exception as e:
                st.error(f"Erro no processamento: {e}")
                st.info("Dica: Verifique se o áudio não é curto demais para a duração selecionada.")
    else:
        st.error("Carregue todos os arquivos (Fundo, Logo e Áudio).")
