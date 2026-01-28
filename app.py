import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from PIL import Image, ImageEnhance
import numpy as np

def setup_project():
    """Cria a estrutura de pastas para o projeto Vibe Coding."""
    folders = ['assets/images', 'assets/audio', 'assets/logos', 'output']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ Estrutura de pastas pronta.")

def apply_synthwave_filter(image_path):
    """Aplica um boost de saturação e contraste na imagem de fundo."""
    img = Image.open(image_path).convert("RGB")
    
    # Aumentando o contraste (Vibe Neon)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Aumentando a saturação
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    
    temp_path = "assets/images/temp_filtered.png"
    img.save(temp_path)
    return temp_path

def glitch_effect(get_frame, t):
    """Adiciona uma leve distorção de cor estilo VHS/Glitch."""
    frame = get_frame(t)
    # Desloca levemente o canal vermelho para criar aberração cromática
    frame_glitch = frame.copy()
    frame_glitch[:, :, 0] = np.roll(frame[:, :, 0], int(5 * np.sin(t*10)), axis=1)
    return frame_glitch

def generate_social_post(bg_name, logo_name, audio_name, output_name="synthwave_glitch.mp4", duration=15):
    """
    Renderiza o vídeo final com efeitos visuais e áudio.
    """
    bg_path = os.path.join('assets/images', bg_name)
    logo_path = os.path.join('assets/logos', logo_name)
    audio_path = os.path.join('assets/audio', audio_name)
    output_path = os.path.join('output', output_name)

    print(f"🚀 Masterizando seu post com efeito Glitch...")

    try:
        # 1. Preparar o Background com Filtro e Zoom
        filtered_bg = apply_synthwave_filter(bg_path)
        bg_clip = (ImageClip(filtered_bg)
                   .set_duration(duration)
                   .resize(height=1920) # Ajustado para Stories
                   .set_position('center')
                   .fx(vfx.resize, lambda t: 1 + 0.03*t))

        # 2. Preparar o Logo (3DLogoLab)
        logo_clip = (ImageClip(logo_path)
                     .set_duration(duration)
                     .resize(width=500)
                     .set_position(('center', 'center')))

        # 3. Preparar o Áudio (AudioAlter)
        audio = AudioFileClip(audio_path).subclip(0, duration)
        
        # 4. Compor Vídeo Final e Aplicar Glitch
        video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920))
        video = video.fl(glitch_effect) # Aplica o efeito de glitch frame a frame
        video = video.set_audio(audio)
        
        # 5. Exportar
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        
        if os.path.exists(filtered_bg):
            os.remove(filtered_bg)
            
        print(f"✨ Pronto! Confira o resultado em: {output_path}")
    
    except Exception as e:
        print(f"❌ Erro na renderização: {e}")

if __name__ == "__main__":
    setup_project()
    
    # Nomes dos arquivos (Certifique-se que eles existem nas pastas assets/)
    IMG_BG = "background.png"    
    LOGO_3D = "logo.png"         
    AUDIO_FILE = "track.mp3"     
    
    paths = [f"assets/images/{IMG_BG}", f"assets/logos/{LOGO_3D}", f"assets/audio/{AUDIO_FILE}"]
    
    if all(os.path.exists(p) for p in paths):
        generate_social_post(IMG_BG, LOGO_3D, AUDIO_FILE)
    else:
        print("\n⚠️  Instale as bibliotecas: pip install moviepy pillow numpy")
        print(f"⚠️  Arquivos faltando: {[p for p in paths if not os.path.exists(p)]}")
