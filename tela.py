import tkinter as tk
from tkinter import messagebox
import time
import pprint

# Importa as funções diretamente do seu arquivo main_2.py
from main import getPedido, atualizarPedido

def buscar_pedido_ui():
    # Limpa a caixa de texto
    text_resultado.delete(1.0, tk.END)
    label_latencia.config(text="Buscando...")
    root.update() # Força a tela a atualizar antes de travar na busca
    
    try:
        id_str = entry_id.get().strip()
        if not id_str.isdigit():
            messagebox.showwarning("Atenção", "Por favor, digite um número de pedido válido.")
            label_latencia.config(text="Latência: --")
            return
            
        idpedido = int(id_str)
        
        # 1. Inicia o cronômetro
        inicio = time.perf_counter()
        
        # 2. Chama a função importada do main_2.py
        resultado = getPedido(idpedido)
        
        # 3. Finaliza o cronômetro e calcula a latência
        fim = time.perf_counter()
        latencia = fim - inicio
        
        if resultado:
            # Formata o dicionário para ficar bonito e legível na tela
            resultado_formatado = pprint.pformat(resultado, indent=2, width=80)
            text_resultado.insert(tk.END, resultado_formatado)
            label_latencia.config(text=f"Latência da busca: {latencia:.5f} segundos")
        else:
            text_resultado.insert(tk.END, f"O pedido com ID {idpedido} não existe no banco de dados.")
            label_latencia.config(text=f"Não encontrado | Latência: {latencia:.5f} segundos")
            
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao buscar:\n{str(e)}")
        label_latencia.config(text="Status: Erro | Latência: --")

# --- CONSTRUÇÃO DA TELA TKINTER ---
root = tk.Tk()
root.title("Sistema de Pedidos - Teste de Cache-Aside")
root.geometry("750x550")
root.config(padx=20, pady=20)

# Frame do topo (Input e Botão)
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, pady=(0, 10))

lbl_instrucao = tk.Label(frame_top, text="ID do Pedido:", font=("Segoe UI", 12))
lbl_instrucao.pack(side=tk.LEFT, padx=(0, 10))

entry_id = tk.Entry(frame_top, font=("Segoe UI", 12), width=15)
entry_id.pack(side=tk.LEFT, padx=10)
entry_id.bind('<Return>', lambda event: buscar_pedido_ui()) # Permite apertar Enter para buscar

btn_buscar = tk.Button(frame_top, text="Buscar", font=("Segoe UI", 10, "bold"), bg="#4CAF50", fg="white", command=buscar_pedido_ui, width=15)
btn_buscar.pack(side=tk.LEFT, padx=10)

# Label para exibir a latência
label_latencia = tk.Label(root, text="Latência: --", font=("Segoe UI", 11, "bold"), fg="#0056b3")
label_latencia.pack(fill=tk.X, pady=10)

# Frame para o texto e scrollbar
frame_texto = tk.Frame(root)
frame_texto.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Caixa de texto para o JSON/Dicionário
text_resultado = tk.Text(frame_texto, font=("Consolas", 10), bg="#f4f4f4", yscrollcommand=scrollbar.set)
text_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_resultado.yview)

# Inicia o loop da aplicação
if __name__ == "__main__":
    root.mainloop()