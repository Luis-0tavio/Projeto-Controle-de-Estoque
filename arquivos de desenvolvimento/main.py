import customtkinter as ctk
import os
import shutil
import sys

def resource_path(relative_path):
    """Retorna o caminho correto do recurso para o exe."""
    try:
        # Quando estiver rodando como exe criado pelo PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Quando estiver rodando normalmente no Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_external_file(nome_arquivo):
    """
    Retorna o caminho do arquivo CSV externo.
    Se não existir, copia do recurso interno do exe.
    """
    arquivo_externo = os.path.join(os.path.abspath("."), nome_arquivo)
    
    # Se não existir, copia do arquivo embutido
    if not os.path.exists(arquivo_externo):
        shutil.copy(resource_path(nome_arquivo), arquivo_externo)
    
    return arquivo_externo

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Controle de Estoque")
        self.geometry("1280x720")
        self.state("zoomed")

        # ===== GRID PRINCIPAL =====
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== SIDEBAR =====
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="Controle de Estoque",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 30), padx=20, anchor="w")

        ctk.CTkButton(self.sidebar, text="Adicionar Item", command=self.mostrar_selecionar_tipo_add).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Remover Item", command=self.mostrar_selecionar_tipo_remover).pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Editar Item", command=self.mostrar_selecionar_tipo_editar).pack(fill="x", padx=20, pady=5)

        # ===== TABVIEW =====
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.tab_substratos = self.tabs.add("Substratos")
        self.tab_tintas = self.tabs.add("Tintas")
        self.tab_papel = self.tabs.add("Papéis")
        self.tab_carimbos = self.tabs.add("Carimbos")
        self.tab_chapas = self.tabs.add("Chapas")

        # ===== SUBSTRATOS =====
        substratos = self.ler_arqv("substratos.csv")
        self.criar_tabela(
            parent=self.tab_substratos,
            titulo="Substratos",
            headers=["Material", "Modelo", "Largura(m)", "Comprimento(m)", "Preço(R$)", "Marca", "Data de Compra", "Data de Validade", "Data de Início de Uso"],
            dados=substratos
        )

        # ===== TINTAS =====
        tintas = self.ler_arqv("tintas.csv")
        self.criar_tabela(
            parent=self.tab_tintas,
            titulo="Tintas",
            headers=["Marca", "Cor", "Tipo", "Quantidade", "Preço(R$)", "Data de Compra", "Data de Validade", "Data de Início de Uso"],
            dados=tintas
        )

        # ===== PAPÉIS =====
        papeis = self.ler_arqv("papeis.csv")
        self.criar_tabela(
            parent=self.tab_papel,
            titulo="Papéis",
            headers=["Tipo", "Gramatura", "Largura(m)", "Comprimento(m)", "Preço(R$)", "Marca", "Data de Compra", "Data de Validade", "Data de Início de Uso"],
            dados=papeis
        )

        # ===== CARIMBOS =====
        carimbos = self.ler_arqv("carimbos.csv")
        self.criar_tabela(
            parent=self.tab_carimbos,
            titulo="Carimbos",
            headers=["Modelo", "Tamanho", "Preço(R$)", "Marca", "Data de Compra", "Data de Validade", "Data de Início de Uso"],
            dados=carimbos
        )

        # ===== CHAPAS =====
        chapas = self.ler_arqv("chapas.csv")
        self.criar_tabela(
            parent=self.tab_chapas,
            titulo="Chapas",
            headers=["Material", "Espessura(mm)", "Largura(m)", "Comprimento(m)", "Preço(R$)", "Marca", "Data de Compra", "Data de Validade", "Data de Início de Uso"],
            dados=chapas
        )

    # ==========================================================
    def criar_tabela(self, parent, titulo, headers, dados):

        total_colunas_visiveis = 5  # 4 dados + 1 coluna "Ver mais"

        # Configuração da aba
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(3, weight=1)

        # TÍTULO
        ctk.CTkLabel(
            parent,
            text=titulo,
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        # TOPBAR
        topbar = ctk.CTkFrame(parent)
        topbar.grid(row=1, column=0, sticky="ew", pady=5)
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkEntry(topbar, placeholder_text="Buscar itens...").grid(
            row=0, column=0, sticky="ew", padx=(0, 10)
        )
        ctk.CTkButton(topbar, text="Filtrar", width=100).grid(row=0, column=1)

        # LISTA (SCROLL)
        lista = ctk.CTkScrollableFrame(parent, fg_color="#3d516e")
        lista.grid_columnconfigure(0, weight=1)
        lista.grid(row=3, column=0, sticky="nsew", pady=(0, 10), padx=5)

        # HEADER (usa os primeiros 4 headers)
        self.add_linha(lista, headers, 0, is_header=True)

        # LINHAS
        for index, linha in enumerate(dados[1:], start=1):
            self.add_linha(lista, linha, index)

    # ==========================================================
    def add_linha(self, parent, dados, row_index, is_header=False):

        # Frame da linha
        row_frame = ctk.CTkFrame(
            parent,
            fg_color="#2b3950" if is_header else "#e3e3e3",
            height=40
        )

        row_frame.grid(row=row_index, column=0, sticky="ew", padx=2, pady=1)
        row_frame.grid_propagate(False)

        # Mostrar apenas os 4 primeiros campos
        dados_exibidos = dados[:4]

        # Larguras fixas das colunas
        col_widths = [150, 150, 150, 450, 100]  # ajuste se quiser

        for i, width in enumerate(col_widths):
            row_frame.grid_columnconfigure(i, minsize=width)

        # Criar células
        for col_index, valor in enumerate(dados_exibidos):
            ctk.CTkLabel(
                row_frame,
                text=valor,
                anchor="w",
                font=ctk.CTkFont(weight="bold") if is_header else None,
                text_color="white" if is_header else "black"
            ).grid(
                row=0,
                column=col_index,
                sticky="w",
                padx=10,
                pady=5
            )

        # Última coluna
        if is_header:
            ctk.CTkLabel(
                row_frame,
                text="Ver mais",
                anchor="w",
                font=ctk.CTkFont(weight="bold"),
                text_color="white"
            ).grid(row=0, column=4, sticky="w", padx=10)
        else:
            ctk.CTkButton(
                row_frame,
                text="°°°",
                width=30,
                height=25
            ).grid(row=0, column=4, sticky="w", padx=10)

    # ==========================================================
    def ler_arqv(self, nome_arquivo):
        substratos = []
        with open(get_external_file(f"{nome_arquivo}"), 'r', encoding="utf-8") as f:

            substrato=f.readlines()
        for subs in substrato:
            subs=subs.replace("\n","").split(",")
            substratos.append(subs)
        return substratos

    # ==========================================================
    def editar_item(self, item):
        pass

    # ==========================================================
    def remover_item(self, item):
        pass

    # ==========================================================
    def adicionar_item(self, tela_form, feedback_label, entries, arqv):
        # coleta valores não vazios
        valores_entrada = [entry.get().strip() for entry in entries.values()]
        
        if "" in valores_entrada:
            feedback_label.configure(text="Por favor, preencha todos os campos!", text_color="red")
            return

        string_valores = ",".join(valores_entrada)

        try:
            # abre arquivo correto com extensão
            with open(get_external_file(f"{arqv}.csv"), 'a', encoding="utf-8") as f:
                f.write(f"{string_valores}\n")
        except Exception as e:
            feedback_label.configure(text=f"Erro ao adicionar: {e}", text_color="red")
            return

        print(f"Produto adicionado ao arquivo \"{arqv}.csv\" com sucesso!")
        feedback_label.configure(text=f"Item adicionado ao arquivo \"{arqv}.csv\" com sucesso!", text_color="green")

        # Limpa mensagem após 2 segundos
        feedback_label.after(2000, lambda: feedback_label.configure(text=""))

        # Botão para fechar a janela
        ctk.CTkButton(
            feedback_label.master,
            text="Fechar",
            command=lambda: self.fechar_janela(tela_form)
        ).grid(row=len(entries)+2, column=0, columnspan=2, pady=10)

    def fechar_janela(self, janela):
        self.atualizar_lista()
        janela.destroy()

    def mostrar_selecionar_tipo_add(self):

        tela_selec_tipo = ctk.CTkToplevel(self)
        tela_selec_tipo.title("Adicionar Item")
        tela_selec_tipo.geometry("500x100")
        tela_selec_tipo.resizable(False, False)

        tela_selec_tipo.grab_set()  # trava foco na janela

        # ===== SELEÇÃO DE TIPO =====

        frame_selecao = ctk.CTkFrame(tela_selec_tipo)
        frame_selecao.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            frame_selecao,
            text="Selecione o tipo do item:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        tipo_item = ctk.CTkComboBox(
            frame_selecao,
            values=["substratos", "tintas", "papeis", "carimbos", "chapas"]
        )
        tipo_item.set("-- selecionar --")
        tipo_item.pack(side="left", padx=10)

        ctk.CTkButton(frame_selecao, text="Selecionar", command=lambda: self.mostrar_formulario(tela_selec_tipo, tipo_item.get())).pack(padx=10)

        label_aviso = ctk.CTkLabel(tela_selec_tipo, text="", text_color="red")
        label_aviso.pack(pady=10)

    def mostrar_formulario(self, tela_selec_tipo, tipo):

        if tipo == "-- selecionar --":
            # exibe mensagem de erro
            for widget in tela_selec_tipo.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
                    widget.configure(text="Por favor, selecione um tipo válido!")
            return

        tela_selec_tipo.destroy()  # fecha a tela de seleção de tipo
        
        tela_form = ctk.CTkToplevel(self)
        tela_form.title("Adicionar Item")
        tela_form.geometry("500x550")
        tela_form.resizable(False, False)

        tela_form.grab_set()  # trava foco na janela   

        
        # ===== FORMULÁRIO =====
        form = ctk.CTkFrame(tela_form)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        if tipo == "substratos":
            labels = [
                "Material:", "Modelo:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "tintas":
            labels = [
                "Marca:", "Cor:", "Tipo:", "Quantidade:",
                "Preço:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "papeis":
            labels = [
                "Tipo:", "Gramatura:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "carimbos":
            labels = [
                "Modelo:", "Tamanho:", "Preço:", "Marca:",
                "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "chapas":
            labels = [
                "Material:", "Espessura:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]

        entries = {}

        for i, texto in enumerate(labels):
            ctk.CTkLabel(form, text=texto).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(form, width=250)
            entry.grid(row=i, column=1, pady=5)
            entries[texto] = entry

        #feedback para o usuário
        feedback_label = ctk.CTkLabel(form, text="", text_color="green")
        feedback_label.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        ctk.CTkButton(form, text="Adicionar", command=lambda: self.adicionar_item(tela_form, feedback_label, entries, tipo)).grid(row=len(labels), column=0, columnspan=2, pady=20)

    def mostrar_selecionar_tipo_remover(self):

        tela_selec_tipo = ctk.CTkToplevel(self)
        tela_selec_tipo.title("Remover Item")
        tela_selec_tipo.geometry("500x100")
        tela_selec_tipo.resizable(False, False)

        tela_selec_tipo.grab_set()  # trava foco na janela

        # ===== SELEÇÃO DE TIPO =====

        frame_selecao = ctk.CTkFrame(tela_selec_tipo)
        frame_selecao.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            frame_selecao,
            text="Selecione o tipo do item:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        tipo_item = ctk.CTkComboBox(
            frame_selecao,
            values=["Substratos", "Tintas", "Papeis", "Carimbos", "Chapas"]
        )
        tipo_item.set("-- Selecionar --")
        tipo_item.pack(side="left", padx=10)

        ctk.CTkButton(frame_selecao, text="Selecionar", command=lambda: self.mostrar_tela_remover(tela_selec_tipo, tipo_item.get())).pack(padx=10)

        label_aviso = ctk.CTkLabel(tela_selec_tipo, text="", text_color="red")
        label_aviso.pack(pady=10)

    def mostrar_tela_remover(self, tela_selec_tipo, tipo):

        if tipo == "-- Selecionar --":
            # exibe mensagem de erro
            for widget in tela_selec_tipo.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
                    widget.configure(text="Por favor, selecione um tipo válido!")
            return

        tela_selec_tipo.destroy()  # fecha a tela de seleção de tipo

        tela_remover = ctk.CTkToplevel(self)
        tela_remover.title("Remover Item")
        tela_remover.geometry("500x200")
        tela_remover.resizable(False, False)

        tela_remover.grab_set()  # trava foco na janela

        frame_selecao = ctk.CTkFrame(tela_remover)
        frame_selecao.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            frame_selecao,
            text="Selecione o item:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        itens = self.ler_arqv(f"{tipo.lower()}.csv")[1:]  # lê os itens do arquivo correspondente, ignorando o header
        itens_formatados = [", ".join(item[:4]) for item in itens]

        item = ctk.CTkComboBox(
            frame_selecao,
            values=itens_formatados
        )
        item.set("-- Selecionar --")
        item.pack(side="left", padx=10)

        ctk.CTkButton(frame_selecao, text="Excluir", command=lambda: self.remover_item(tela_remover, item.get(), tipo)).pack(padx=10)

    def remover_item(self, tela_remover, item, tipo):

        tela_remover.destroy()  # fecha a tela de remoção

        tela_confirmar_exclusão = ctk.CTkToplevel(self)
        tela_confirmar_exclusão.title("Remover Item")
        tela_confirmar_exclusão.geometry("500x200")
        tela_confirmar_exclusão.resizable(False, False)

        tela_confirmar_exclusão.grab_set()  # trava foco na janela

        ctk.CTkLabel(tela_confirmar_exclusão, text=f"Tem certeza que deseja remover o item: '{item}'?", text_color="red").pack(pady=10)
        ctk.CTkButton(tela_confirmar_exclusão, text="Sim", command=lambda: self.confirmar_remocao(tela_confirmar_exclusão, item, tipo)).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(tela_confirmar_exclusão, text="Não", command=lambda: tela_confirmar_exclusão.destroy()).pack(side="right", padx=20, pady=10)

    def confirmar_remocao(self, tela_confirmar_exclusao, item, tipo):
        # Lê todos os itens
        itens = self.ler_arqv(f"{tipo.lower()}.csv")
        
        # 'item' contém os primeiros 4 campos que o usuário selecionou
        campos_selecionados = item.split(", ")

        # Filtra apenas as linhas que **não correspondem** aos campos selecionados
        novos_itens = [linha for linha in itens if linha[:len(campos_selecionados)] != campos_selecionados]

        # Reescreve o arquivo
        with open(get_external_file(f"{tipo.lower()}.csv"), 'w', encoding="utf-8") as f:
            for linha in novos_itens:
                f.write(",".join(linha) + "\n")  # junta os campos em string

        self.atualizar_lista()
        tela_confirmar_exclusao.destroy()

    def mostrar_selecionar_tipo_editar(self):

        tela_selec_tipo_editar = ctk.CTkToplevel(self)
        tela_selec_tipo_editar.title("Editar Item")
        tela_selec_tipo_editar.geometry("500x100")
        tela_selec_tipo_editar.resizable(False, False)

        tela_selec_tipo_editar.grab_set()  # trava foco na janela

        # ===== SELEÇÃO DE TIPO =====

        frame_selecao = ctk.CTkFrame(tela_selec_tipo_editar)
        frame_selecao.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            frame_selecao,
            text="Selecione o tipo do item:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        tipo_item = ctk.CTkComboBox(
            frame_selecao,
            values=["Substratos", "Tintas", "Papeis", "Carimbos", "Chapas"]
        )
        tipo_item.set("-- Selecionar --")
        tipo_item.pack(side="left", padx=10)

        ctk.CTkButton(frame_selecao, text="Selecionar", command=lambda: self.mostrar_tela_editar(tela_selec_tipo_editar, tipo_item.get())).pack(padx=10)

        label_aviso = ctk.CTkLabel(tela_selec_tipo_editar, text="", text_color="red")
        label_aviso.pack(pady=10)

    def mostrar_tela_editar(self, tela_selec_tipo_editar, tipo):

        if tipo == "-- Selecionar --":
            # exibe mensagem de erro
            for widget in tela_selec_tipo_editar.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
                    widget.configure(text="Por favor, selecione um tipo válido!")
            return

        tela_selec_tipo_editar.destroy()  # fecha a tela de seleção de tipo
        
        tela_editar = ctk.CTkToplevel(self)
        tela_editar.title("Editar Item")
        tela_editar.geometry("500x200")
        tela_editar.resizable(False, False)

        tela_editar.grab_set()  # trava foco na janela

        frame_selecao = ctk.CTkFrame(tela_editar)
        frame_selecao.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(
            frame_selecao,
            text="Selecione o item:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        itens = self.ler_arqv(f"{tipo.lower()}.csv")[1:]  # lê os itens do arquivo correspondente, ignorando o header
        itens_formatados = [", ".join(item[:4]) for item in itens]

        combo_item = ctk.CTkComboBox(
            frame_selecao,
            values=itens_formatados
        )
        combo_item.set("-- Selecionar --")
        combo_item.pack(side="left", padx=10)

        ctk.CTkButton(frame_selecao, text="Editar", command=lambda: self.mostrar_editar_item(tela_editar, combo_item.get(), tipo)).pack(padx=10)

    def mostrar_editar_item(self, tela_editar, item, tipo):

        if tipo == "-- selecionar --":
            # exibe mensagem de erro
            for widget in tela_editar.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget.cget("text_color") == "red":
                    widget.configure(text="Por favor, selecione um tipo válido!")
            return

        tela_editar.destroy()  # fecha a tela de seleção de tipo
        
        tela_edit = ctk.CTkToplevel(self)
        tela_edit.title("Editar Item")
        tela_edit.geometry("500x550")
        tela_edit.resizable(False, False)

        tela_edit.grab_set()  # trava foco na janela   

        
        # ===== FORMULÁRIO =====
        form = ctk.CTkFrame(tela_edit)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        if tipo == "Substratos":
            labels = [
                "Material:", "Modelo:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "Tintas":
            labels = [
                "Marca:", "Cor:", "Tipo:", "Quantidade:",
                "Preço:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "Papeis":
            labels = [
                "Tipo:", "Gramatura:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "Carimbos":
            labels = [
                "Modelo:", "Tamanho:", "Preço:", "Marca:",
                "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]
        elif tipo == "Chapas":
            labels = [
                "Material:", "Espessura:", "Largura:", "Comprimento:",
                "Preço:", "Marca:", "Data de Compra:", "Data de Validade:", "Data de Início de Uso:", "Fornecedor:"
            ]

        entries = {}
        all_itens = self.ler_arqv(f"{tipo.lower()}.csv")[1:]  # lê os itens do arquivo correspondente, ignorando o header

        item_selecionado = all_itens[[", ".join(i[:4]) for i in all_itens].index(item)]  # encontra o item selecionado com base nos primeiros 4 campos

        for i, texto in enumerate(labels):
            ctk.CTkLabel(form, text=texto).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ctk.CTkEntry(form, width=250)
            entry.grid(row=i, column=1, pady=5)
            entry.insert(0, item_selecionado[i] if i < len(item_selecionado) else "")  # preenche o campo com o valor do item selecionado
            entries[texto] = entry

        #feedback para o usuário
        feedback_label = ctk.CTkLabel(form, text="", text_color="green")
        feedback_label.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

        ctk.CTkButton(form, text="Editar", command=lambda: self.editar_item(tela_edit, feedback_label, entries, tipo, item)).grid(row=len(labels), column=0, columnspan=2, pady=20)

    def editar_item(self, tela_edit, feedback_label, entries, tipo, item):
        # Coleta os dados dos campos de entrada
        dados = {}
        for label, entry in entries.items():
            dados[label] = entry.get()

        # Atualiza o item no banco de dados
        self.atualizar_item_no_banco(tipo, item, dados)

        # Exibe feedback ao usuário
        feedback_label.configure(text="Item editado com sucesso!", text_color="green")
        tela_edit.after(1000, lambda: tela_edit.destroy())  # fecha a tela após 3 segundos

    def atualizar_item_no_banco(self, tipo, item, dados):
        # Lê todos os itens
        itens = self.ler_arqv(f"{tipo.lower()}.csv")
        
        # 'item' contém os primeiros 4 campos que o usuário selecionou
        campos_selecionados = item.split(", ")

        # Atualiza a linha correspondente ao item editado
        novos_itens = []

        # Reescreve o arquivo
        with open(get_external_file(f"{tipo.lower()}.csv"), 'w', encoding="utf-8") as f:
            for linha in itens:
                if linha[:len(campos_selecionados)] == campos_selecionados:
                    # Substitui os dados antigos pelos novos, mantendo os campos que não foram editados
                    nova_linha = []
                    for i, campo in enumerate(linha):
                        if i < len(dados):
                            nova_linha.append(dados.get(list(dados.keys())[i], campo))
                        else:
                            nova_linha.append(campo)
                    novos_itens.append(nova_linha)
                else:
                    novos_itens.append(linha)
                    
            for linha in novos_itens:
                f.write(",".join(linha) + "\n")  # junta os campos em string

        self.atualizar_lista()


    def atualizar_lista(self):
        self.destroy()  # destrói a janela atual
        self.__init__()  # reinicializa a aplicação para atualizar as listas

    def ver_mais(self, item):
        pass
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
