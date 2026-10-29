from datetime import datetime
import json
import os


class HistoryManager:

  def __init__(self, json_path: str = "history.json", max_items: int = 50):
    if not os.path.isabs(json_path):
      base_dir = os.path.dirname(
          os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      )
      self.json_path = os.path.join(base_dir, json_path)
    else:
      self.json_path = json_path

    self.max_items = max_items
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    """Garante que o arquivo JSON exista com uma estrutura inicial válida."""
    if not os.path.exists(self.json_path):
      self._write_data([])

  def _read_data(self) -> list[dict]:
    """Lê o conteúdo do arquivo JSON de forma segura."""
    try:
      with open(self.json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError, Exception):
      return []

  def _write_data(self, data: list[dict]):
    """Escreve a lista de histórico no arquivo JSON."""
    try:
      parent = os.path.dirname(self.json_path)
      if parent:
        os.makedirs(parent, exist_ok=True)
      with open(self.json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
      print(f"[HistoryManager] Erro ao salvar histórico: {e}")

  def add_entry(
      self, title: str, format_type: str, file_path: str, duration_str: str = ""
  ) -> dict:
    """Adiciona um novo registro de download/conversão no topo da lista."""
    history = self._read_data()

    entry = {
        "id": f"{int(datetime.now().timestamp())}_{len(history)}",
        "title": title,
        "format": format_type.upper(),  # 'MP3' ou 'MP4'
        "file_path": file_path,
        "duration": duration_str,
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "exists": os.path.exists(file_path),
    }

    # Remove duplicados com o mesmo caminho de arquivo, se houver
    history = [item for item in history if item.get("file_path") != file_path]

    # Insere no início (mais recente primeiro)
    history.insert(0, entry)

    # Mantém apenas a quantidade máxima limite de itens
    if len(history) > self.max_items:
      history = history[: self.max_items]

    self._write_data(history)
    return entry

  def get_history(self, search_query: str = "") -> list[dict]:
    """Retorna a lista de histórico atualizada, verificando a existência dos arquivos e aplicando filtro de busca."""
    history = self._read_data()
    updated_history = []

    for item in history:
      # Atualiza em tempo real se o arquivo ainda existe no disco
      item["exists"] = os.path.exists(item.get("file_path", ""))

      # Filtro de busca simples por título ou formato
      if search_query:
        query = search_query.lower()
        title_match = query in item.get("title", "").lower()
        format_match = query in item.get("format", "").lower()
        if title_match or format_match:
          updated_history.append(item)
      else:
        updated_history.append(item)

    return updated_history

  def clear_history(self):
    """Limpa todo o histórico de downloads."""
    self._write_data([])

  def remove_entry(self, entry_id: str):
    """Remove um item específico do histórico pelo ID."""
    history = self._read_data()
    history = [item for item in history if item.get("id") != entry_id]
    self._write_data(history)