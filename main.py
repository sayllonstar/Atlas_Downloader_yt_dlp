import customtkinter as ctk
from src.gui.components.sidebar import Sidebar
from src.gui.views.home_view import HomeView
from src.gui.views.settings_view import SettingsView
from src.gui.views.about_view import AboutView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Filee Studio - Downloader & Converter")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=("#F5F5F7", "#121214"))
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar com callback de navegação
        self.sidebar = Sidebar(self, width=220, nav_callback=self.select_frame)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Dicionário guardando as views renderizadas
        self.frames = {}
        
        for ViewClass, name in zip(
            [HomeView, SettingsView, AboutView],
            ["home", "settings", "about"]
        ):
            frame = ViewClass(self)
            self.frames[name] = frame
            frame.grid(row=0, column=1, sticky="nsew")
            
        # Inicia mostrando a tela Início
        self.select_frame("home")

    def select_frame(self, name):
        # Esconde todas
        for frame in self.frames.values():
            frame.grid_remove()
            
        # Mostra a selecionada
        if name in self.frames:
            self.frames[name].grid()
            
        # Atualiza o estado visual do botão ativo na Sidebar
        if hasattr(self, "sidebar"):
            self.sidebar.update_active_button(name)


if __name__ == "__main__":
    app = App()
    app.mainloop()