# 🌃 Synthwave Creative Hub

Bem-vindo ao **Synthwave Creative Hub**, uma ferramenta de "Vibe Coding" projetada para transformar ativos isolados em posts imersivos para redes sociais (Reels, TikTok, Shorts). 

Este projeto orquestra inteligência artificial, design 3D e processamento de áudio através de um pipeline Python automatizado.

---

## 🛠️ O Ecossistema
O projeto utiliza o melhor das ferramentas externas para alimentar o motor de renderização:

1.  **[Recraft.ai](https://www.recraft.ai)**: Geração de cenários e backgrounds com estética Neon/Glow.
2.  **[3DLogoLab.io](https://3dlogolab.io)**: Criação de logotipos e ícones com profundidade 3D.
3.  **[AudioAlter.com](https://audioalter.com)**: Processamento de áudio para efeitos imersivos (8D, Reverb e Slowed).
4.  **Python (MoviePy & Streamlit)**: O cérebro que une tudo, aplica filtros de cores, efeitos de glitch e exporta o vídeo final.

---

## 🚀 Funcionalidades
* **Interface Hub**: Links diretos para as ferramentas de criação de assets.
* **Synthwave Filter**: Ajuste automático de contraste e saturação via código para estética neon.
* **Efeito Glitch**: Aberração cromática dinâmica (RGB Shift) aplicada frame a frame.
* **Movimento Imersivo**: Efeito de zoom suave (Ken Burns) no background.
* **Exportação Otimizada**: Vídeo em formato 9:16 pronto para redes sociais.

---

## 📦 Instalação e Uso Local

Se preferir rodar em sua máquina, siga os passos:

1. **Clone o repositório**:
  
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd seu-repositorio



2. **Instale as dependências**:

pip install -r requirements.txt



3. **Execute o App**:

streamlit run app.py

```



---

## ☁️ Deploy no Streamlit Cloud

Para manter o app online:

1. Suba o código para um repositório no GitHub.
2. Certifique-se de que o arquivo `requirements.txt` contém:
* `moviepy==1.0.3`
* `Pillow`
* `numpy`
* `streamlit`


3. Conecte o repositório ao [share.streamlit.io](https://share.streamlit.io).

---

## 🎨 Vibe Guide (Dicas de Prompt)

* **Para o Recraft**: `Synthwave landscape, retro sun, neon grid, purple and cyan color palette, high detail --style glow`
* **Para o AudioAlter**: Use o efeito **8D Audio** para criar uma sensação de movimento espacial no som.

---

Codado com ⚡ e muita vibe.
