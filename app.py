import streamlit as st
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from PIL import Image, ImageEnhance
import numpy as np
import tempfile

# Configuração da Página
st.set_page_config(page_title="Synthwave Post Generator", page_icon="⚡")
st.title("⚡ AI Synthwave Generator")
st.markdown("### Vibe Coding: Recraft + 3DLogoLab + AudioAlter")

def apply_synthwave_filter(pil_img):
    """Aplica boost de neon na imagem PIL."""
    # Contraste
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(1.4)
    # Saturação
    enhancer = ImageEnhance.Color(pil_img)
    pil_img = enhancer.enhance(1.3)
    return pil_img

def glitch_effect(get_frame, t):
    """Efeito de aberração cromática leve."""
    frame = get_frame(t)
    frame_glitch = frame.copy()
    # Deslocamento do canal vermelho baseado no tempo
    shift = int(5 * np.sin(t * 10))
    frame_glitch[:, :, 0] = np.roll(frame[:, :, 0], shift, axis=1)
    return frame_glitch

# --- Interface de Upload ---
col1, col2 = st.columns(2)
with col1:
    bg_file = st.file_uploader("Fundo (Recraft.ai)", type=['png', 'jpg'])
    logo_file = st.file_uploader("Logo 3D (3DLogoLab)", type=['png'])
with col2:
    audio_file = st.file_uploader("Áudio (AudioAlter)", type=['mp3', 'wav'])
    duration = st.slider("Duração (segundos)", 5, 15, 10)

if st.button("🚀 Gerar Post Imersivo"):
    if bg_file and logo_file and audio_file:
        with st.spinner("Masterizando sua vibe..."):
            try:
                # Salvar arquivos temporários para o MoviePy ler
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
                    # Aplicar filtro antes de salvar
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

                # 1. Configurar Background com Zoom
                bg_clip = (ImageClip(bg_path)
                           .set_duration(duration)
                           .resize(height=1920)
                           .set_position('center')
                           .fx(vfx.resize, lambda t: 1 + 0.03 * t))

                # 2. Configurar Logo
                logo_clip = (ImageClip(logo_path)
                             .set_duration(duration)
                             .resize(width=500)
                             .set_position(('center', 'center')))

                # 3. Áudio
                audio = AudioFileClip(audio_path).subclip(0, duration)

                # 4. Compositor e Glitch
                video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920))
                video = video.fl(glitch_effect)
                video = video.set_audio(audio)

                # 5. Exportar para arquivo temporário
                output_path = "synthwave_output.mp4"
                video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)

                # Exibir Vídeo
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button("💾 Baixar Vídeo", file, file_name="synthwave_post.mp4")

                # Limpar temporários
                os.remove(bg_path)
                os.remove(logo_path)
                os.remove(audio_path)

            except Exception as e:
                st.error(f"Erro na renderização: {e}")
    else:
        st.warning("Por favor, faça o upload de todos os arquivos.")
