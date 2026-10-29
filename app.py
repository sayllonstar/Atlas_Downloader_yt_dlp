import os
import threading
import customtkinter as ctk
from tkinter import filedialog
import yt_dlp

# Configuração de tema da interface
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Dark/Light)
ctk.set_default_color_theme("blue")


class DownloaderApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("Baixador de Mídia (yt-dlp)")
        self.geometry("560x360")
        self.resizable(False, False)

        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # Título Principal
        self.label_title = ctk.CTkLabel(
            self, text="yt-dlp Downloader", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(padx=20, pady=(20, 10))

        # Campo de Texto (URL)
        self.entry_url = ctk.CTkEntry(
            self, placeholder_text="Cole o link do vídeo ou playlist aqui...", width=480
        )
        self.entry_url.pack(padx=20, pady=10)

        # Container de Seleção de Pasta
        self.frame_folder = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_folder.pack(padx=20, pady=5)

        self.entry_folder = ctk.CTkEntry(self.frame_folder, width=370)
        self.entry_folder.insert(0, self.download_path)
        self.entry_folder.pack(side="left", padx=(0, 5))

        self.btn_browser = ctk.CTkButton(
            self.frame_folder,
            text="Procurar...",
            width=100,
            command=self.select_folder,
        )
        self.btn_browser.pack(side="left", padx=5)

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

    def select_folder(self):
        chosen_folder = filedialog.askdirectory(initialdir=self.download_path)
        if chosen_folder:
            self.download_path = chosen_folder
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, self.download_path)

    def progress_hook(self, d):
        """Atualiza o texto de status com o progresso do download."""
        if d.get("status") == "downloading":
            percent = d.get("_percent_str", "").strip()
            self.label_status.configure(
                text=f"Baixando: {percent}", text_color="white"
            )
        elif d.get("status") == "finished":
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

        output_dir = self.download_path or os.path.join(os.path.expanduser("~"), "Downloads")

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
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best",
                "merge_output_format": "mp4",
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.label_status.configure(
                text="Download concluído com sucesso!", text_color="green"
            )
        except Exception as e:
            self.label_status.configure(
                text=f"Erro ao baixar: {str(e)[:90]}", text_color="red"
            )
        finally:
            self.btn_download.configure(state="normal")


if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()