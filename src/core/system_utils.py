import os
import platform
import subprocess


class SystemUtils:

  @staticmethod
  def open_file(file_path: str) -> tuple[bool, str]:
    """Abre o arquivo no aplicativo padrão do sistema operacional."""
    if not os.path.exists(file_path):
      return False, "O arquivo não foi encontrado no disco."

    try:
      current_os = platform.system()
      if current_os == "Windows":
        os.startfile(os.path.normpath(file_path))
      elif current_os == "Darwin":  # macOS
        subprocess.run(["open", file_path], check=True)
      else:  # Linux
        subprocess.run(["xdg-open", file_path], check=True)
      return True, "Arquivo aberto com sucesso."
    except Exception as e:
      return False, f"Falha ao abrir o arquivo: {str(e)}"

  @staticmethod
  def open_folder(file_path: str) -> tuple[bool, str]:
    """Abre a pasta de destino e seleciona/destaca o arquivo se possível."""
    folder_path = (
        os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
    )

    if not os.path.exists(folder_path):
      return False, "A pasta de destino não foi encontrada."

    try:
      current_os = platform.system()
      if current_os == "Windows":
        # Destaca o arquivo no Explorer se ele existir, senão apenas abre a pasta
        if os.path.isfile(file_path):
          norm_file = os.path.normpath(os.path.abspath(file_path))
          subprocess.run(["explorer", f"/select,{norm_file}"])
        else:
          os.startfile(os.path.normpath(folder_path))
      elif current_os == "Darwin":
        if os.path.isfile(file_path):
          subprocess.run(["open", "-R", file_path], check=True)
        else:
          subprocess.run(["open", folder_path], check=True)
      else:
        subprocess.run(["xdg-open", folder_path], check=True)
      return True, "Pasta aberta com sucesso."
    except Exception as e:
      return False, f"Falha ao abrir a pasta: {str(e)}"