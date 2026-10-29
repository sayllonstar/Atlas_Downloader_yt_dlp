import customtkinter as ctk


class ProgressCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.lbl_status = ctk.CTkLabel(
            self, text="", text_color="gray",
            font=ctk.CTkFont(family="Inter", size=12)
        )
        self.lbl_status.pack(side="top", anchor="w", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self, height=6, progress_color="#FF3B30")
        self.progress_bar.pack(side="bottom", fill="x")
        self.progress_bar.set(0)
        
        # Oculta inicialmente
        self.pack_forget()

    def show(self, after_widget=None):
        target = after_widget or getattr(self.master, "drop_zone", None)
        if target:
            self.pack(fill="x", padx=30, pady=10, after=target)
        else:
            self.pack(fill="x", padx=30, pady=10)
        
    def hide(self):
        self.pack_forget()

    def update_progress(self, percentage: float, text: str):
        clamped = max(0.0, min(1.0, float(percentage)))
        self.progress_bar.set(clamped)
        self.lbl_status.configure(text=text)