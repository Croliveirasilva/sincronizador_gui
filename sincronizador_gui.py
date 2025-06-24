import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext

# === CONFIGURAÇÃO: MAPEAR SUAS PASTAS ORIGEM E DESTINO AQUI ===
# Use caminhos absolutos. Cada par representa uma sincronização de uma pasta específica.

PASTAS_MAPEADAS = {
    "Projeto 1": (
        Path(r"C:\Caminho\Origem\Projeto1"),  # Caminho de origem genérico
        Path(r"D:\Backup\Projeto1")            # Caminho de destino genérico
    ),
    "Projeto 2": (
        Path(r"C:\Caminho\Origem\Projeto2"),
        Path(r"D:\Backup\Projeto2")
    ),
    # Adicione mais pares conforme necessário
}


class AppSync:
    def __init__(self, root):
        self.root = root
        self.root.title("Sincronizador de Pastas")
        self.root.geometry("650x450")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Título e exibição dos pares de sincronização
        tk.Label(self.root, text="🔄 Pastas que serão sincronizadas:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        for nome, (origem, destino) in PASTAS_MAPEADAS.items():
            tk.Label(self.root, text=f"{nome}:").pack()
            tk.Label(self.root, text=f"Origem: {origem}", fg="gray").pack()
            tk.Label(self.root, text=f"Destino: {destino}", fg="gray").pack(pady=(0, 10))

        # Botão para iniciar a sincronização
        tk.Button(self.root, text="Iniciar Sincronização", bg="#007BFF", fg="white", command=self.iniciar_sincronizacao).pack(pady=10)

        # Área de log com rolagem
        tk.Label(self.root, text="Log de Sincronização:").pack()
        self.log_area = scrolledtext.ScrolledText(self.root, width=80, height=12, state="disabled")
        self.log_area.pack(pady=(5, 10))

    def log(self, mensagem):
        # Exibe mensagens no log
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, mensagem + "\n")
        self.log_area.yview(tk.END)
        self.log_area.configure(state="disabled")

    def iniciar_sincronizacao(self):
        # Inicia o processo de sincronização para todos os pares definidos
        self.log("🔁 Iniciando sincronização...")
        for nome, (origem, destino) in PASTAS_MAPEADAS.items():
            self.log(f"📁 {nome} → Sincronizando...")
            self.sincronizar_pasta(origem, destino)
        self.log("✅ Sincronização concluída.")

    def sincronizar_pasta(self, origem: Path, destino: Path):
        # Verifica se a pasta de origem existe
        if not origem.exists():
            self.log(f"[⚠️ Aviso] Origem não encontrada: {origem}")
            return

        # Percorre todos os arquivos e subpastas
        for root, dirs, files in os.walk(origem):
            # Ignora diretórios ocultos (que começam com '.')
            dirs[:] = [d for d in dirs if not d.startswith(".")]

            for file in files:
                # Ignora arquivos dentro de pastas ocultas
                if any(part.startswith(".") for part in Path(root).parts):
                    continue

                caminho_origem = Path(root) / file
                caminho_relativo = caminho_origem.relative_to(origem)
                caminho_destino = destino / caminho_relativo

                try:
                    # Garante que o diretório de destino exista
                    caminho_destino.parent.mkdir(parents=True, exist_ok=True)

                    # Copia apenas se o arquivo for novo ou modificado
                    if not caminho_destino.exists() or os.path.getmtime(caminho_origem) > os.path.getmtime(caminho_destino):
                        shutil.copy2(caminho_origem, caminho_destino)
                        self.log(f"✔ Copiado: {caminho_destino}")
                    else:
                        self.log(f"↪ Ignorado (sem alteração): {caminho_destino}")
                except PermissionError:
                    self.log(f"[❌ Permissão negada] {caminho_destino}")
                except Exception as e:
                    self.log(f"[❌ Erro] {caminho_destino} - {str(e)}")


# Ponto de entrada do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = AppSync(root)
    root.mainloop()
