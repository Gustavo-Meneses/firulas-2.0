import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, vfx
from PIL import Image, ImageEnhance

def setup_project():
    """Cria a estrutura de pastas para o projeto Vibe Coding."""
    folders = ['assets/images', 'assets/audio', 'assets/logos', 'output']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ Estrutura de pastas pronta.")

def apply_synthwave_filter(image_path):
    """Aplica um boost de saturação e contraste na imagem de fundo."""
    img = Image.open(image_path)
    
    # Aumentando o contraste (Vibe Neon)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    
    # Aumentando a saturação
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    
    temp_path = "assets/images/temp_filtered.png"
    img.save(temp_path)
    return temp_path

def generate_social_post(bg_name, logo_name, audio_name, output_name="synthwave_final.mp4", duration=15):
    """
    Renderiza o vídeo final com fundo animado, logo centralizado e áudio.
    """
    bg_path = os.path.join('assets/images', bg_name)
    logo_path = os.path.join('assets/logos', logo_name)
    audio_path = os.path.join('assets/audio', audio_name)
    output_path = os.path.join('output', output_name)

    print(f"🚀 Masterizando seu post Synthwave...")

    try:
        # 1. Preparar o Background com Filtro e Efeito de Zoom
        filtered_bg = apply_synthwave_filter(bg_path)
        bg_clip = (ImageClip(filtered_bg)
                   .set_duration(duration)
                   .resize(height=1080) # Padroniza para Full HD vertical
                   .set_position('center')
                   .fx(vfx.resize, lambda t: 1 + 0.02*t)) # Efeito de zoom lento

        # 2. Preparar o Logo (3DLogoLab)
        logo_clip = (ImageClip(logo_path)
                     .set_duration(duration)
                     .resize(width=400) # Ajuste o tamanho do logo aqui
                     .set_position(('center', 'center')))

        # 3. Preparar o Áudio (AudioAlter)
        audio = AudioFileClip(audio_path).subclip(0, duration)
        
        # 4. Compor Vídeo Final
        final_video = CompositeVideoClip([bg_clip, logo_clip], size=(1080, 1920)) # Formato Stories/Reels
        final_video = final_video.set_audio(audio)
        
        # 5. Exportar
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        
        # Limpeza
        if os.path.exists(filtered_bg):
            os.remove(filtered_bg)
            
        print(f"✨ Pronto! Confira em: {output_path}")
    
    except Exception as e:
        print(f"❌ Erro na renderização: {e}")

if __name__ == "__main__":
    setup_project()
    
    # Ajuste os nomes dos seus arquivos aqui:
    IMG_BG = "background.png"    # Do Recraft.ai
    LOGO_3D = "logo.png"         # Do 3DLogoLab.io
    AUDIO_FILE = "track.mp3"     # Do AudioAlter.com
    
    # Verifica se todos os assets existem antes de rodar
    paths = [f"assets/images/{IMG_BG}", f"assets/logos/{LOGO_3D}", f"assets/audio/{AUDIO_FILE}"]
    if all(os.path.exists(p) for p in paths):
        generate_social_post(IMG_BG, LOGO_3D, AUDIO_FILE)
    else:
        missing = [p for p in paths if not os.path.exists(p)]
        print(f"\n⚠️  Arquivos faltando: {missing}")
        print("Certifique-se de colocar o logo na pasta 'assets/logos'!")
