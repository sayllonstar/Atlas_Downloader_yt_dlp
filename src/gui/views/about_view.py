import shutil
import webbrowser
import customtkinter as ctk
import yt_dlp


class AboutView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Container Centralizado
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.45, anchor="center")
        
        # Título / Logo
        lbl_logo = ctk.CTkLabel(
            center_frame, text="Filee Studio",
            font=ctk.CTkFont(family="Inter", size=32, weight="bold")
        )
        lbl_logo.pack(pady=(0, 5))
        
        lbl_version = ctk.CTkLabel(
            center_frame, text="Versão 2.1.0 • Downloader & Converter", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=13)
        )
        lbl_version.pack(pady=(0, 25))
        
        # Card de Motores
        card_engines = ctk.CTkFrame(center_frame, fg_color=("gray90", "#18181A"), corner_radius=12, width=380)
        card_engines.pack(fill="x", pady=10)
        
        lbl_engines_title = ctk.CTkLabel(
            card_engines, text="Motores de Conversão",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold")
        )
        lbl_engines_title.pack(anchor="center", pady=(15, 10))
        
        # Status yt-dlp
        yt_version = getattr(yt_dlp, "__version__", "Ativo")
        self.create_status_row(card_engines, "yt-dlp Engine", f"Ativo ({yt_version})", "#34C759")
        
        # Status FFmpeg (verificação dinâmica no sistema)
        ffmpeg_exists = shutil.which("ffmpeg") is not None
        ffmpeg_status = "Ativo (Instalado)" if ffmpeg_exists else "Não detectado"
        ffmpeg_color = "#34C759" if ffmpeg_exists else "#FF9500"
        self.create_status_row(card_engines, "FFmpeg Post-Processor", ffmpeg_status, ffmpeg_color)
        
        # Botões de Link (GitHub / Patrocinar)
        links_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        links_frame.pack(pady=25)
        
        btn_github = ctk.CTkButton(
            links_frame, text="GitHub", width=110, height=34,
            fg_color=("#E5E5EA", "#2C2C2E"), hover_color=("#D1D1D6", "#3A3A3C"), text_color=("black", "white"),
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://github.com/yt-dlp/yt-dlp")
        )
        btn_github.pack(side="left", padx=10)
        
        btn_sponsor = ctk.CTkButton(
            links_frame, text="❤ Apoiar", width=110, height=34,
            fg_color="#FF3B30", hover_color="#E53935", text_color="white",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            command=lambda: webbrowser.open("https://github.com/sponsors")
        )
        btn_sponsor.pack(side="left", padx=10)

    def create_status_row(self, parent, name, status, color):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(0, 10))
        
        lbl_name = ctk.CTkLabel(row, text=name, font=ctk.CTkFont(family="Inter", size=12))
        lbl_name.pack(side="left")
        
        lbl_status = ctk.CTkLabel(
            row, text=status, text_color=color,
            font=ctk.CTkFont(family="Inter", size=12, weight="bold")
        )
        lbl_status.pack(side="right")