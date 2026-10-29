import os
import customtkinter as ctk

from src.core.downloader import Downloader
from src.core.history_manager import HistoryManager
from src.core.system_utils import SystemUtils
from src.gui.components.drop_zone import DropZone
from src.gui.components.progress_card import ProgressCard
from src.gui.components.recent_card import RecentCard


class HomeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Inicializa o Core
        self.history_manager = HistoryManager()
        self.downloader = Downloader(self.history_manager)
        default_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # 1. Drop Zone (Topo)
        self.drop_zone = DropZone(self, self.start_download, default_path)
        self.drop_zone.pack(fill="x", padx=30, pady=(30, 10))
        
        # 2. Barra de Progresso (posicionada logo abaixo do DropZone)
        self.progress_card = ProgressCard(self)
        
        # 3. Cabeçalho dos Recentes
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(15, 5))
        
        lbl_recent = ctk.CTkLabel(
            header_frame, text="Conversões recentes", 
            font=ctk.CTkFont(family="Inter", size=14, weight="bold")
        )
        lbl_recent.pack(side="left")
        
        btn_clear = ctk.CTkButton(
            header_frame, text="Limpar", width=60, height=24,
            fg_color="transparent", hover_color=("#E5E5EA", "#2C2C2E"), text_color="gray",
            font=ctk.CTkFont(family="Inter", size=12), command=self.clear_history
        )
        btn_clear.pack(side="right")
        
        # 4. Lista Rolável (Scrollable Frame)
        self.scroll_list = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_list.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.refresh_history_list()

    def start_download(self, url, fmt, path):
        self.progress_card.show(after_widget=self.drop_zone)
        self.progress_card.update_progress(0.0, "Iniciando download...")
        
        # Obtém qualidade de áudio configurada na tela de Ajustes, se houver
        audio_quality = "192"
        settings_view = getattr(self.master, "frames", {}).get("settings")
        if settings_view and hasattr(settings_view, "get_audio_quality"):
            audio_quality = settings_view.get_audio_quality()

        # Inicia de forma assíncrona
        self.downloader.download_async(
            url=url,
            output_dir=path,
            format_type=fmt,
            audio_quality=audio_quality,
            progress_callback=self.on_progress,
            completion_callback=self.on_complete
        )

    # --- Callbacks do Downloader (Thread-Safe) ---
    def on_progress(self, percentage, text):
        self.after(0, lambda: self.progress_card.update_progress(percentage, text))

    def on_complete(self, success, message, entry_data):
        def update_ui():
            if success:
                self.drop_zone.reset_state(clear_url=True)
                self.progress_card.hide()
                self.refresh_history_list()
            else:
                self.drop_zone.reset_state(clear_url=False)
                self.progress_card.update_progress(0, message)
                
        self.after(0, update_ui)

    # --- Gestão da Interface de Histórico ---
    def refresh_history_list(self):
        # Limpa itens atuais
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
            
        history = self.history_manager.get_history()
        
        if not history:
            lbl_empty = ctk.CTkLabel(
                self.scroll_list, text="Nenhuma conversão recente.", text_color="gray",
                font=ctk.CTkFont(family="Inter", size=13)
            )
            lbl_empty.pack(pady=30)
            return

        for entry in history:
            card = RecentCard(
                self.scroll_list, entry,
                on_open_file=SystemUtils.open_file,
                on_open_folder=SystemUtils.open_folder
            )
            card.pack(fill="x", padx=10, pady=5)

    def clear_history(self):
        self.history_manager.clear_history()
        self.refresh_history_list()