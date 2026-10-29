import os
import re
import threading
from typing import Callable, Optional
import yt_dlp

from src.core.history_manager import HistoryManager


class Downloader:

  def __init__(self, history_manager: HistoryManager):
    self.history_manager = history_manager
    self._is_downloading = False

  @staticmethod
  def clean_ansi(text: str) -> str:
    """Remove códigos de formatação ANSI e terminal gerados pelo yt-dlp."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)

  def download_async(
      self,
      url: str,
      output_dir: str,
      format_type: str = "mp4",
      audio_quality: str = "192",
      progress_callback: Optional[Callable[[float, str], None]] = None,
      completion_callback: Optional[Callable[[bool, str, dict], None]] = None,
  ):
    """Inicia o download em uma thread secundária sem bloquear a interface."""
    if self._is_downloading:
      if completion_callback:
        completion_callback(
            False, "Já existe um download em andamento.", {}
        )
      return

    self._is_downloading = True

    thread = threading.Thread(
        target=self._run_download,
        args=(
            url,
            output_dir,
            format_type,
            audio_quality,
            progress_callback,
            completion_callback,
        ),
        daemon=True,
    )
    thread.start()

  def _run_download(
      self,
      url: str,
      output_dir: str,
      format_type: str,
      audio_quality: str,
      progress_callback: Optional[Callable[[float, str], None]],
      completion_callback: Optional[Callable[[bool, str, dict], None]],
  ):
    format_type = format_type.lower()
    os.makedirs(output_dir, exist_ok=True)

    def progress_hook(d):
      if not progress_callback:
        return

      if d.get("status") == "downloading":
        total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        downloaded_bytes = d.get("downloaded_bytes", 0)

        if total_bytes > 0:
          percentage = downloaded_bytes / total_bytes
          progress_callback(percentage, f"Baixando: {int(percentage * 100)}%")
        else:
          percent_str = self.clean_ansi(d.get("_percent_str", "0%")).strip()
          progress_callback(0.0, f"Baixando: {percent_str}")

      elif d.get("status") == "finished":
        progress_callback(1.0, "Processando arquivo...")

    # Template do caminho final
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    if format_type == "mp3":
      ydl_opts.update({
          "format": "bestaudio/best",
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": audio_quality,
          }],
      })
    else:  # MP4
      ydl_opts.update({
          "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best",
          "merge_output_format": "mp4",
      })

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if not info_dict:
          raise Exception("Não foi possível obter dados da URL fornecida.")

        # Se for playlist, seleciona o primeiro item para obter dados do arquivo
        if "entries" in info_dict and info_dict["entries"]:
          first_entry = next((e for e in info_dict["entries"] if e), None)
          if first_entry:
            info_dict = first_entry

        filename = ydl.prepare_filename(info_dict)

        # Ajusta extensão esperada
        if format_type == "mp3":
          base_name, _ = os.path.splitext(filename)
          filename = f"{base_name}.mp3"
        elif format_type == "mp4":
          base_name, _ = os.path.splitext(filename)
          if os.path.exists(f"{base_name}.mp4"):
            filename = f"{base_name}.mp4"

        # Verifica arquivo salvo em requested_downloads se filename não existir
        if not os.path.exists(filename):
          req_dl = info_dict.get("requested_downloads")
          if req_dl and isinstance(req_dl, list) and len(req_dl) > 0:
            actual_file = req_dl[0].get("filepath") or req_dl[0].get("_filename")
            if actual_file and os.path.exists(actual_file):
              filename = actual_file

        title = info_dict.get("title", "Mídia sem título")
        duration = info_dict.get("duration_string", "")
        if not duration and info_dict.get("duration"):
          sec = int(info_dict["duration"])
          m, s = divmod(sec, 60)
          h, m = divmod(m, 60)
          duration = f"{h:d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

        # Registra o download concluído no histórico em JSON
        history_entry = self.history_manager.add_entry(
            title=title,
            format_type=format_type,
            file_path=filename,
            duration_str=duration,
        )

      if completion_callback:
        completion_callback(
            True, "Download concluído com sucesso!", history_entry
        )

    except Exception as e:
      err_msg = self.clean_ansi(str(e))
      if "FFmpeg" in err_msg or "ffmpeg" in err_msg:
        err_msg = (
            "FFmpeg não foi encontrado no sistema. Necessário para conversão."
        )
      if len(err_msg) > 100:
        err_msg = err_msg[:97] + "..."

      if completion_callback:
        completion_callback(False, f"Erro: {err_msg}", {})

    finally:
      self._is_downloading = False