import os
import threading
import customtkinter as ctk
import yt_dlp

# Configuração de tema da interface
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("blue")


class DownloaderApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    # Configurações da Janela
    self.title("Baixador de Mídia (yt-dlp)")
    self.geometry("550x320")
    self.resizable(False, False)

    # Título Principal
    self.label_title = ctk.CTkLabel(
        self, text="yt-dlp Downloader", font=ctk.CTkFont(size=20, weight="bold")
    )
    self.label_title.pack(padx=20, pady=(20, 10))

    # Campo de Texto (URL)
    self.entry_url = ctk.CTkEntry(
        self, placeholder_text="Cole o link do vídeo ou playlist aqui...", width=450
    )
    self.entry_url.pack(padx=20, pady=10)

    # Opções de Formato (MP3 / MP4)
    self.format_var = ctk.StringVar(value="mp4")

    self.frame_options = ctk.CTkFrame(self, fg_color="transparent")
    self.frame_options.pack(padx=20, pady=5)

    self.radio_mp4 = ctk.CTkRadioButton(
        self.frame_options,
        text="MP4 (Vídeo)",
        variable=self.format_var,
        value="mp4",
    )
    self.radio_mp4.pack(side="left", padx=15)

    self.radio_mp3 = ctk.CTkRadioButton(
        self.frame_options,
        text="MP3 (Áudio)",
        variable=self.format_var,
        value="mp3",
    )
    self.radio_mp3.pack(side="left", padx=15)

    # Botão de Download
    self.btn_download = ctk.CTkButton(
        self, text="Baixar Agora", command=self.start_download_thread
    )
    self.btn_download.pack(padx=20, pady=15)

    # Label de Status
    self.label_status = ctk.CTkLabel(
        self, text="Aguardando link...", text_color="gray"
    )
    self.label_status.pack(padx=20, pady=5)

  def progress_hook(self, d):
    """Atualiza o texto de status com o progresso do download."""
    if d['status'] == 'downloading':
      # Remove caracteres de formatação de cor do terminal
      percent = d.get('_percent_str', '').strip()
      self.label_status.configure(
          text=f"Baixando: {percent}", text_color="white"
      )
    elif d['status'] == 'finished':
      self.label_status.configure(
          text="Processando arquivo / Concluído!", text_color="green"
      )

  def start_download_thread(self):
    """Roda o download em uma thread separada para não travar a interface."""
    threading.Thread(target=self.download_media, daemon=True).start()

  def download_media(self):
    url = self.entry_url.get().strip()

    if not url:
      self.label_status.configure(
          text="Por favor, insira uma URL válida!", text_color="red"
      )
      return

    fmt = self.format_var.get()
    self.btn_download.configure(state="disabled")
    self.label_status.configure(
        text="Iniciando download...", text_color="yellow"
    )

    # Pasta onde os downloads serão salvos (pasta 'Downloads' do usuário)
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads")

    # Configurações do yt-dlp
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [self.progress_hook],
    }

    if fmt == "mp3":
      ydl_opts.update({
          "format": "bestaudio/best",
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": "192",
          }],
      })
    else:  # MP4
      ydl_opts.update({
          "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
      })

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
      self.label_status.configure(
          text="Download concluído com sucesso!", text_color="green"
      )
    except Exception as e:
      self.label_status.configure(
          text=f"Erro ao baixar: {str(e)}", text_color="red"
      )
    finally:
      self.btn_download.configure(state="normal")


if __name__ == "__main__":
  app = DownloaderApp()
  app.mainloop()