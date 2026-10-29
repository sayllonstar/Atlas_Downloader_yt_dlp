import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, nav_callback, **kwargs):
        # Fundo mais denso para estruturar o app
        super().__init__(master, fg_color=("gray95", "#0D0D0E"), corner_radius=0, **kwargs)
        self.nav_callback = nav_callback
        
        # Logo/Nome
        self.lbl_logo = ctk.CTkLabel(
            self, text="Filee Studio", anchor="w",
            font=ctk.CTkFont(family="Inter", size=20, weight="bold")
        )
        self.lbl_logo.pack(padx=20, pady=(30, 5), fill="x")
        
        self.lbl_sub = ctk.CTkLabel(
            self, text="Arraste, solte, convertido.", anchor="w", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=11)
        )
        self.lbl_sub.pack(padx=20, pady=(0, 30), fill="x")
        
        # Criação dos Menus
        self.btn_home = self._create_nav_button("Início", lambda: self._on_nav_click("home"))
        self.btn_home.pack(padx=10, pady=2, fill="x")
        
        self.btn_settings = self._create_nav_button("Geral", lambda: self._on_nav_click("settings"))
        self.btn_settings.pack(padx=10, pady=2, fill="x")
        
        self.btn_about = self._create_nav_button("Sobre", lambda: self._on_nav_click("about"))
        self.btn_about.pack(padx=10, pady=2, fill="x")
        
        # Spacer para empurrar o switch para o fundo
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # Controles de Rodapé
        self.theme_switch = ctk.CTkSwitch(
            self, text="Modo Escuro", command=self.toggle_theme,
            font=ctk.CTkFont(family="Inter", size=12),
            progress_color="#FF3B30"
        )
        self.theme_switch.pack(padx=20, pady=20, anchor="w")
        self.theme_switch.select()  # Inicia no modo dark
        
        # Dicionário de botões para facilitar a atualização visual
        self.buttons = {
            "home": self.btn_home,
            "settings": self.btn_settings,
            "about": self.btn_about
        }
        
        # Define o estado visual inicial
        self.update_active_button("home")

    def _create_nav_button(self, text, command):
        return ctk.CTkButton(
            self, text=text, anchor="w", height=36, corner_radius=8,
            fg_color="transparent", hover_color=("#D1D1D6", "#2C2C2E"), text_color=("black", "white"),
            font=ctk.CTkFont(family="Inter", size=13),
            command=command
        )

    def _on_nav_click(self, name):
        """Atualiza a UI e dispara o callback para trocar a view."""
        self.update_active_button(name)
        self.nav_callback(name)

    def update_active_button(self, active_name):
        """Varre os botões e aplica estilo de selecionado apenas ao botão ativo."""
        for name, btn in self.buttons.items():
            if name == active_name:
                btn.configure(
                    fg_color=("#E5E5EA", "#1C1C1E"), 
                    font=ctk.CTkFont(family="Inter", size=13, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent", 
                    font=ctk.CTkFont(family="Inter", size=13, weight="normal")
                )

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")