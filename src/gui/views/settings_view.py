import os
import re
import customtkinter as ctk
from tkinter import filedialog


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Título da Tela
        self.lbl_title = ctk.CTkLabel(
            self, text="Configurações Gerais",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold")
        )
        self.lbl_title.pack(anchor="w", padx=30, pady=(30, 20))
        
        # --- Card 1: Diretório Padrão ---
        self.card_dir = ctk.CTkFrame(self, fg_color=("gray90", "#18181A"), corner_radius=12)
        self.card_dir.pack(fill="x", padx=30, pady=10)
        
        lbl_dir_title = ctk.CTkLabel(
            self.card_dir, text="Pasta de Download Padrão",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold")
        )
        lbl_dir_title.pack(anchor="w", padx=20, pady=(15, 5))
        
        dir_controls = ctk.CTkFrame(self.card_dir, fg_color="transparent")
        dir_controls.pack(fill="x", padx=20, pady=(0, 15))
        
        self.default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.entry_dir = ctk.CTkEntry(
            dir_controls, width=350, height=32,
            font=ctk.CTkFont(family="Inter", size=12),
            border_width=1, border_color=("#C7C7CC", "#3A3A3C")
        )
        self.entry_dir.insert(0, self.default_path)
        self.entry_dir.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.entry_dir.bind("<FocusOut>", lambda e: self._on_entry_changed())
        self.entry_dir.bind("<Return>", lambda e: self._on_entry_changed())
        
        self.btn_browse = ctk.CTkButton(
            dir_controls, text="Procurar...", width=90, height=32,
            fg_color=("#E5E5EA", "#2C2C2E"), hover_color=("#D1D1D6", "#3A3A3C"), text_color=("black", "white"),
            font=ctk.CTkFont(family="Inter", size=12), command=self.choose_folder
        )
        self.btn_browse.pack(side="right")

        # --- Card 2: Preferências de Qualidade ---
        self.card_qual = ctk.CTkFrame(self, fg_color=("gray90", "#18181A"), corner_radius=12)
        self.card_qual.pack(fill="x", padx=30, pady=10)
        
        lbl_qual_title = ctk.CTkLabel(
            self.card_qual, text="Qualidade de Conversão",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold")
        )
        lbl_qual_title.pack(anchor="w", padx=20, pady=(15, 5))

        # Container para lado a lado
        qual_container = ctk.CTkFrame(self.card_qual, fg_color="transparent")
        qual_container.pack(fill="x", padx=20, pady=(0, 15))

        # Coluna MP3
        col_mp3 = ctk.CTkFrame(qual_container, fg_color="transparent")
        col_mp3.pack(side="left", expand=True, fill="x", padx=(0,10))

        lbl_audio = ctk.CTkLabel(
            col_mp3, text="Bitrate do MP3:", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=12)
        )
        lbl_audio.pack(anchor="w", padx=0, pady=(5, 0))
        
        # Ajustado para 320 kbps como padrão
        self.audio_menu = ctk.CTkOptionMenu(
            col_mp3, values=["320 kbps (Máxima)", "192 kbps", "128 kbps"],
            font=ctk.CTkFont(family="Inter", size=12),
            fg_color=("#E5E5EA", "#2C2C2E"), text_color=("black", "white"), button_color=("#D1D1D6", "#3A3A3C")
        )
        self.audio_menu.pack(anchor="w", fill="x")
        self.audio_menu.set("320 kbps (Máxima)")

        # Coluna MP4
        col_mp4 = ctk.CTkFrame(qual_container, fg_color="transparent")
        col_mp4.pack(side="right", expand=True, fill="x", padx=(10,0))

        lbl_video = ctk.CTkLabel(
            col_mp4, text="Resolução do MP4", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=12)
        )
        lbl_video.pack(anchor="w", pady=(0, 5))

        # Ajustando para Melhor Disponivel como padrão
        self.video_menu = ctk.CTkOptionMenu(
            col_mp4, values=["Melhor disponível (Máxima)", "1080p", "720p", "480p"],
            font=ctk.CTkFont(family="Inter", size=12),
            fg_color=("#E5E5EA", "#2C2C2E"), text_color=("black", "white"), button_color=("#D1D1D6", "#3A3A3C")
        )
        self.video_menu.pack(anchor="w", fill="x")
        self.video_menu.set("Melhor disponível (Máxima)")

        # Card de Autenticação
        self.card_auth = ctk.CTkFrame(self, fg_color=("gray90", "#18181A"), corner_radius=12)
        self.card_auth.pack(fill="x", padx=30, pady=10)
        
        lbl_auth_title = ctk.CTkLabel(
            self.card_auth, text="Autentificação (Evitar Bloqueios/Age Restriction)",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold")
        )
        lbl_auth_title.pack(anchor="w", padx=20, pady=(15, 5))

        lbl_auth_desc = ctk.CTkLabel(
            self.card_auth, text="Usar cookies do navegador para baixar vídeos privados ou com restrição de idade.",
            text_color="gray", font=ctk.CTkFont(family="Inter", size=12)
        )
        lbl_auth_desc.pack(anchor="w", padx=20, pady=(0, 10))

        self.cookie_menu = ctk.CTkOptionMenu(
            self.card_auth,
            values=["Nenhum (Padrão)", "Chrome", "Edge", "Firefox", "Brave", "Opera", "Vivaldi", "Safari"],
            font=ctk.CTkFont(family="Inter", size=12),
            fg_color= ("#E5E5EA", "#2C2C2E"), text_color= ("black", "white"), button_color= ("#D1D1D6", "#3A3A3C")
        )
        self.cookie_menu.pack(anchor="w", padx=20, pady=(0, 15))
        self.cookie_menu.set("Nenhum (Padrão)")

    def choose_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.default_path)
        if chosen:
            self.default_path = chosen
            self.entry_dir.delete(0, "end")
            self.entry_dir.insert(0, self.default_path)
            self._sync_settings()

    def _on_entry_changed(self):
        new_path = self.entry_dir.get().strip()
        if new_path and os.path.exists(new_path):
            self.default_path = new_path
            self._sync_settings()

    def _sync_settings(self):
        """Propaga o novo caminho padrão para a tela Home se estiver disponível."""
        home_frame = getattr(self.master, "frames", {}).get("home")
        if home_frame and hasattr(home_frame, "drop_zone"):
            home_frame.drop_zone.download_path = self.default_path

    def get_audio_quality(self) -> str:
        val = self.audio_menu.get()
        return val.split(" ")[0]

    def get_video_resolution(self):
        val = self.video_menu.get()
        if "Melhor" in val:
            return "best"
        return val.replace("p", "") 


    def get_browser_cookies(self):
        val = self.cookie_menu.get()
        if "Nenhum" in val:
            return None
        return val.lower()

    # Alias para compatibilidade caso seja chamado no singular
    get_browser_cookie = get_browser_cookies

