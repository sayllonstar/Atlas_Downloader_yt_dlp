import os
import customtkinter as ctk
from tkinter import filedialog

class DropZone(ctk.CTkFrame):
    def __init__(self, master, on_download_request, default_path, **kwargs):
        # Cor de fundo simulando um card em destaque
        super().__init__(master, fg_color=("gray90", "#18181A"), corner_radius=12, **kwargs)
        self.on_download_request = on_download_request
        self.download_path = default_path

        # icone/titulo central
        self.lbl_title = ctk.CTkLabel(
            self, text="Cole o link ou solte aqui",
            font=ctk.CTkFont(family="Inter", size=16, weight="bold")
        )
        self.lbl_title.pack(pady=(20, 10))

        # Input de URL
        self.entry_url = ctk.CTkEntry(
            self, placeholder_text="https://...", width=400, height=36,
            font=ctk.CTkFont(family="Inter", size=13),
            border_width=1, border_color=("#C7C7CC", "#3A3A3C")
        )
        self.entry_url.pack(pady=5)
        self.entry_url.bind("<Return>", lambda event: self._handle_download())

        # Controles: Formato e Pasta
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.pack(pady=10)

        self.format_var = ctk.StringVar(value="mp4")
        self.radio_mp4 = ctk.CTkRadioButton(
            controls_frame, text="MP4 (Video)", variable=self.format_var, value="mp4",
            font=ctk.CTkFont(family="Inter", size=12), fg_color="#FF3B30", hover_color="#E53935"
        )
        self.radio_mp4.pack(side="left", padx=10)

        self.radio_mp3 = ctk.CTkRadioButton(
            controls_frame, text="MP3 (Audio)", variable=self.format_var, value="mp3",
            font=ctk.CTkFont(family="Inter", size=12), fg_color="#FF3B30", hover_color="#E53935"
        )
        self.radio_mp3.pack(side="left", padx=10)

        self.btn_folder = ctk.CTkButton(
            controls_frame, text="Destino...", width=90, height=26,
            fg_color="transparent", border_width=1, border_color=("#C7C7CC", "#3A3A3C"),
            text_color=("black", "white"), hover_color=("#E5E5EA", "#2C2C2E"),
            font=ctk.CTkFont(family="Inter", size=11), command=self.choose_folder
        )
        self.btn_folder.pack(side="left", padx=10)

        # Botão Principal de Download
        self.btn_download = ctk.CTkButton(
            self, text="Baixar Mídia", width=200, height=40, corner_radius=20,
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            fg_color="#FF3B30", hover_color="#E53935",
            command=self._handle_download
        )
        self.btn_download.pack(pady=(15, 20))

    def choose_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.download_path)
        if chosen:
            self.download_path = chosen
            folder_name = os.path.basename(chosen) or chosen
            if len(folder_name) > 12:
                folder_name = folder_name[:10] + "..."
            self.btn_folder.configure(text=f"📁 {folder_name}")

    def _handle_download(self):
        url = self.entry_url.get().strip()
        if not url:
            self.entry_url.focus()
            self.entry_url.configure(placeholder_text="Cole o link antes de baixar!")
            return

        self.btn_download.configure(state="disabled", text="Iniciando...")
        self.on_download_request(url, self.format_var.get(), self.download_path)

    def reset_state(self, clear_url: bool = True):
        if clear_url:
            self.entry_url.delete(0, 'end')
            self.entry_url.configure(placeholder_text="https://...")
        self.btn_download.configure(state="normal", text="Baixar Mídia")