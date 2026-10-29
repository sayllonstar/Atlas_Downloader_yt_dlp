import customtkinter as ctk


class RecentCard(ctk.CTkFrame):
    def __init__(self, master, entry, on_open_file, on_open_folder, **kwargs):
        super().__init__(master, fg_color=("gray85", "#1C1C1E"), corner_radius=8, **kwargs)
        
        self.entry = entry
        file_path = entry.get("file_path", "")
        format_type = entry.get("format", "MP4").upper()
        
        # Badge de Formato (MP3/MP4) com cor Accent
        format_color = "#FF3B30" if format_type == "MP3" else "#E53935"
        self.lbl_badge = ctk.CTkLabel(
            self, text=format_type, 
            fg_color=format_color, text_color="white",
            corner_radius=6, width=40, height=24,
            font=ctk.CTkFont(family="Inter", size=11, weight="bold")
        )
        self.lbl_badge.pack(side="left", padx=(10, 10), pady=10)
        
        # Informações (Título e Data)
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        title_text = entry.get("title", "Mídia sem título")
        if len(title_text) > 50:
            title_text = title_text[:47] + "..."
            
        self.lbl_title = ctk.CTkLabel(
            info_frame, text=title_text, anchor="w",
            font=ctk.CTkFont(family="Inter", size=13, weight="bold")
        )
        self.lbl_title.pack(side="top", fill="x", expand=True)
        
        timestamp = entry.get("timestamp", "")
        duration = entry.get("duration", "--:--")
        info_sub = f"{timestamp} • {duration}" if timestamp else duration
        self.lbl_date = ctk.CTkLabel(
            info_frame, text=info_sub, 
            anchor="w", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=11)
        )
        self.lbl_date.pack(side="bottom", fill="x", expand=True)
        
        # Botões de Ação
        if entry.get("exists", False):
            self.btn_open_file = ctk.CTkButton(
                self, text="Abrir arquivo", width=90, height=28,
                fg_color=("#E5E5EA", "#2C2C2E"), hover_color=("#D1D1D6", "#3A3A3C"), text_color=("black", "white"),
                font=ctk.CTkFont(family="Inter", size=12),
                command=lambda p=file_path: on_open_file(p)
            )
            self.btn_open_file.pack(side="right", padx=(5, 10), pady=10)
            
            self.btn_open_folder = ctk.CTkButton(
                self, text="Abrir pasta", width=90, height=28,
                fg_color="transparent", border_width=1, border_color=("#C7C7CC", "#3A3A3C"),
                hover_color=("#E5E5EA", "#2C2C2E"), text_color=("black", "white"),
                font=ctk.CTkFont(family="Inter", size=12),
                command=lambda p=file_path: on_open_folder(p)
            )
            self.btn_open_folder.pack(side="right", padx=5, pady=10)
        else:
            self.lbl_deleted = ctk.CTkLabel(
                self, text="Arquivo não encontrado", text_color="red",
                font=ctk.CTkFont(family="Inter", size=12, slant="italic")
            )
            self.lbl_deleted.pack(side="right", padx=15)