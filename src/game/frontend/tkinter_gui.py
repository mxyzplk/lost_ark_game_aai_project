import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from backend.gamelogic import GameLogic

class ClickableCard(tk.Frame):
    """Widget personalizado para cada célula do grid"""
    def __init__(self, master, row, col, game_logic, select_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.row = row
        self.col = col
        self.game_logic = game_logic
        self.select_callback = select_callback
        self.is_selected = False
        
        # Configuração visual
        self.config(
            borderwidth=2,
            relief="ridge",
            bg='#f8f9fa',
            width=120,
            height=130
        )
        self.grid_propagate(False)
        
        # Cria a estrutura interna
        self.create_widgets()
        self.update_content()
        
        # Bind de clique em TODO o widget
        self.bind_click_events()
    
    def create_widgets(self):
        """Cria os widgets internos do card"""
        # Frame de conteúdo (texto)
        self.content_frame = tk.Frame(self, bg='#f8f9fa')
        self.content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Cabeçalho com coordenadas
        self.header_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        self.header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.coord_label = tk.Label(
            self.header_frame,
            text=f"({self.row},{self.col})",
            font=("Arial", 10, "bold"),
            bg='#f8f9fa',
            fg='#333333'
        )
        self.coord_label.pack(side=tk.LEFT)
        
        # Probabilidade
        self.prob_label = tk.Label(
            self.content_frame,
            text="P: 0.0000",
            font=("Arial", 9),
            bg='#f8f9fa',
            fg='#666666',
            anchor=tk.W
        )
        self.prob_label.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Leituras dos sensores
        self.sensor_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        self.sensor_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.sensor_labels = {}
        sensors = ['GPR', 'MAG', 'VIS']
        
        for sensor in sensors:
            sensor_label = tk.Label(
                self.sensor_frame,
                text=f"{sensor}: None",
                font=("Arial", 8),
                bg='#f8f9fa',
                fg='#666666',
                anchor=tk.W
            )
            sensor_label.pack(fill=tk.X, pady=1)
            self.sensor_labels[sensor] = sensor_label
    
    def bind_click_events(self):
        """Adiciona bind de clique a todos os elementos"""
        # Bind no frame principal
        self.bind('<Button-1>', self.on_click)
        self.content_frame.bind('<Button-1>', self.on_click)
        self.header_frame.bind('<Button-1>', self.on_click)
        self.sensor_frame.bind('<Button-1>', self.on_click)
        
        # Bind nos labels
        self.coord_label.bind('<Button-1>', self.on_click)
        self.prob_label.bind('<Button-1>', self.on_click)
        for label in self.sensor_labels.values():
            label.bind('<Button-1>', self.on_click)
        
        # Efeito hover
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_click(self, event):
        """Manipula cliques"""
        self.select_callback(self.row, self.col)
    
    def on_enter(self, event):
        """Efeito hover - destaque sutil"""
        if not self.is_selected:
            self.config(bg='#e9ecef')
            self.content_frame.config(bg='#e9ecef')
            self.header_frame.config(bg='#e9ecef')
            self.sensor_frame.config(bg='#e9ecef')
            self.coord_label.config(bg='#e9ecef')
            self.prob_label.config(bg='#e9ecef')
            for label in self.sensor_labels.values():
                label.config(bg='#e9ecef')
    
    def on_leave(self, event):
        """Remove efeito hover"""
        if not self.is_selected:
            self.config(bg='#f8f9fa')
            self.content_frame.config(bg='#f8f9fa')
            self.header_frame.config(bg='#f8f9fa')
            self.sensor_frame.config(bg='#f8f9fa')
            self.coord_label.config(bg='#f8f9fa')
            self.prob_label.config(bg='#f8f9fa')
            for label in self.sensor_labels.values():
                label.config(bg='#f8f9fa')
    
    def select(self):
        """Marca como selecionado"""
        self.is_selected = True
        self.config(
            bg='#d0e7ff',
            relief="solid"
        )
        self.content_frame.config(bg='#d0e7ff')
        self.header_frame.config(bg='#d0e7ff')
        self.sensor_frame.config(bg='#d0e7ff')
        self.coord_label.config(bg='#d0e7ff')
        self.prob_label.config(bg='#d0e7ff')
        for label in self.sensor_labels.values():
            label.config(bg='#d0e7ff')
    
    def deselect(self):
        """Remove seleção"""
        self.is_selected = False
        self.config(
            bg='#f8f9fa',
            relief="ridge"
        )
        self.content_frame.config(bg='#f8f9fa')
        self.header_frame.config(bg='#f8f9fa')
        self.sensor_frame.config(bg='#f8f9fa')
        self.coord_label.config(bg='#f8f9fa')
        self.prob_label.config(bg='#f8f9fa')
        for label in self.sensor_labels.values():
            label.config(bg='#f8f9fa')
    
    def update_content(self):
        """Atualiza conteúdo baseado nos dados do jogo"""
        pos = self.game_logic.grid.positions[self.row, self.col]
        
        # Atualiza probabilidade
        prob = pos.get_probability()
        self.prob_label.config(text=f"P: {prob*100:.4f}%")
        
        # Atualiza leituras dos sensores
        sensors = ['GPR', 'MAG', 'VIS']
        for sensor in sensors:
            reading = pos.status.get(sensor, 'None')
            self.sensor_labels[sensor].config(text=f"{sensor}: {reading}")


class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Raiders of the Lost Ark - Game Configuration")
        self.root.geometry("250x250")
        
        self.game = None
        self.game_window = None
        self.selected_cell = None
        self.selected_sensor = "GPR"
        self.cell_cards = {}  # Dicionário para armazenar os cards
        
        self.create_config_window()
    
    def create_config_window(self):
        """Janela de configuração do jogo"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Game Configuration", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de configuração
        configs = [
            ("Rows:", "rows_var", 4),
            ("Columns:", "cols_var", 4),
            ("Initial Budget:", "budget_var", 100),
            ("Random Seed:", "seed_var", 42)
        ]
        
        for idx, (label_text, var_name, default) in enumerate(configs, 1):
            ttk.Label(main_frame, text=label_text).grid(row=idx, column=0, sticky=tk.W, pady=5)
            var = tk.IntVar(value=default)
            setattr(self, var_name, var)
            spinbox = ttk.Spinbox(main_frame, from_=2, to=20, textvariable=var, width=10)
            spinbox.grid(row=idx, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(main_frame, text="Create Game", command=self.create_game).grid(
            row=5, column=0, columnspan=2, pady=20)
    
    def create_game(self):
        """Cria o jogo com os parâmetros configurados"""
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            seed = int(self.seed_var.get())
            budget = int(self.budget_var.get())
            
            if rows < 2 or cols < 2:
                messagebox.showerror("Error", "Grid must be at least 2x2")
                return
            
            self.game = GameLogic(rows, cols, seed, budget)
            self.root.withdraw()
            self.create_game_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create game: {str(e)}")
    
    def create_game_window(self):
        """Cria a janela principal do jogo"""
        self.game_window = tk.Toplevel()
        self.game_window.title("Raiders of the Lost Ark")
        self.game_window.geometry("1200x800")
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_game_window_close)
        
        # Container principal
        main_container = ttk.Frame(self.game_window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Painel superior: Informações e controles
        self.create_top_panel(main_container)
        
        # Área da grade com scroll
        self.create_grid_area(main_container)
        
        # Painel de histórico
        self.create_history_panel(main_container)
        
        # Cria a grade inicial
        self.create_grid()
    
    def create_top_panel(self, parent):
        """Cria o painel superior com informações e controles"""
        top_panel = ttk.Frame(parent)
        top_panel.pack(side=tk.TOP, fill=tk.X, pady=(0, 20))
        
        # Painel de status do jogo
        status_frame = ttk.LabelFrame(top_panel, text="Game Status", padding="15")
        status_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        self.budget_label = ttk.Label(
            status_frame, 
            text=f"💰 Budget: {self.game.budget} points", 
            font=("Arial", 12)
        )
        self.budget_label.pack(anchor=tk.W, pady=3)
        
        self.score_label = ttk.Label(
            status_frame, 
            text=f"🏆 Score: {self.game.score} points", 
            font=("Arial", 12)
        )
        self.score_label.pack(anchor=tk.W, pady=3)
        
        self.survey_label = ttk.Label(
            status_frame, 
            text=f"📊 Surveys: {self.game.survey_count}", 
            font=("Arial", 12)
        )
        self.survey_label.pack(anchor=tk.W, pady=3)
        
        # Painel de ações
        action_frame = ttk.LabelFrame(top_panel, text="Actions", padding="15")
        action_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Seleção de sensor
        ttk.Label(action_frame, text="Select Sensor:", font=("Arial", 11)).pack(anchor=tk.W)
        self.sensor_var = tk.StringVar(value="GPR")
        
        sensor_frame = ttk.Frame(action_frame)
        sensor_frame.pack(fill=tk.X, pady=(5, 10))
        
        sensors = [
            ("GPR (5 points)", "GPR"),
            ("MAG (3 points)", "MAG"), 
            ("VIS (1 point)", "VIS")
        ]
        
        for text, value in sensors:
            rb = ttk.Radiobutton(
                sensor_frame, 
                text=text, 
                variable=self.sensor_var, 
                value=value
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Célula selecionada
        self.selected_cell_label = ttk.Label(
            action_frame, 
            text="📍 No cell selected",
            font=("Arial", 10, "italic"),
            foreground="#666666"
        )
        self.selected_cell_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Botões de ação
        btn_frame = ttk.Frame(action_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        survey_btn = ttk.Button(
            btn_frame,
            text="Perform Survey",
            command=self.perform_survey,
            width=20
        )
        survey_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        excavate_btn = ttk.Button(
            btn_frame,
            text="Excavate",
            command=self.perform_excavation,
            width=20,
            style="Danger.TButton"
        )
        excavate_btn.pack(side=tk.LEFT)
        
        # Configura estilo do botão perigoso
        style = ttk.Style()
        style.configure("Danger.TButton", foreground="white", background="#dc3545")
    
    def create_grid_area(self, parent):
        """Cria a área da grade com scroll"""
        grid_container = ttk.LabelFrame(parent, text="Archaeological Grid", padding="10")
        grid_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Canvas com scroll
        self.canvas = tk.Canvas(grid_container, bg="white", highlightthickness=0)
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(grid_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(grid_container, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        
        # Frame interno para os cards
        self.grid_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor=tk.NW
        )
        
        # Layout
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind para ajuste de scroll
        self.grid_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
    
    def create_history_panel(self, parent):
        """Cria painel de histórico"""
        history_frame = ttk.LabelFrame(parent, text="Survey History", padding="10")
        history_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame, 
            height=6,
            font=("Arial", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        self.add_history_message("Game started. Select a cell and choose a sensor.")
    
    def on_frame_configure(self, event):
        """Atualiza scrollregion quando o frame muda de tamanho"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Ajusta o tamanho do frame interno quando o canvas muda"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def create_grid(self):
        """Cria a grade de células"""
        # Limpa grade anterior
        self.cell_cards.clear()
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        rows = self.game.grid.rows
        cols = self.game.grid.columns
        
        # Cria os cards
        for i in range(rows):
            for j in range(cols):
                card = ClickableCard(
                    self.grid_frame,
                    row=i,
                    col=j,
                    game_logic=self.game,
                    select_callback=self.select_cell
                )
                card.grid(row=i, column=j, padx=5, pady=5)
                self.cell_cards[(i, j)] = card
    
    def select_cell(self, row, col):
        """Seleciona uma célula"""
        # Deseleciona célula anterior
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            if (old_row, old_col) in self.cell_cards:
                self.cell_cards[(old_row, old_col)].deselect()
        
        # Seleciona nova célula
        self.selected_cell = (row, col)
        if (row, col) in self.cell_cards:
            self.cell_cards[(row, col)].select()
        
        # Atualiza label
        self.selected_cell_label.config(
            text=f"📍 Selected: ({row}, {col})",
            foreground="#007bff"
        )
        
        # Atualiza probabilidade
        pos = self.game.grid.positions[row, col]
        prob = pos.get_probability()
        
        # Atualiza o card (já deve estar atualizado, mas por garantia)
        self.update_cell_content(row, col)
    
    def update_cell_content(self, row, col):
        """Atualiza conteúdo de uma célula específica"""
        if (row, col) in self.cell_cards:
            self.cell_cards[(row, col)].update_content()
    
    def update_all_cells(self):
        """Atualiza todas as células"""
        for (row, col), card in self.cell_cards.items():
            card.update_content()
    
    def perform_survey(self):
        """Executa pesquisa na célula selecionada"""
        if not self.selected_cell:
            messagebox.showwarning("No Cell Selected", "Please select a cell first.")
            return
        
        if self.game.game_over:
            messagebox.showinfo("Game Over", "The game is over.")
            return
        
        row, col = self.selected_cell
        sensor_type = self.sensor_var.get()
        
        # Executa pesquisa
        reading, success, cost = self.game.survey(row, col, sensor_type)
        
        if not success:
            messagebox.showwarning("Cannot Survey", reading)
            return
        
        # Atualiza interface
        self.update_interface()
        
        # Adiciona ao histórico
        message = f"Survey at ({row},{col}) with {sensor_type}: {reading} (Cost: {cost} points)"
        self.add_history_message(message)
        
        # Atualiza status
        self.selected_cell_label.config(
            text=f"📍 Selected: ({row}, {col}) - {sensor_type}: {reading}"
        )
        
        # Verifica orçamento
        if self.game.budget <= 0:
            messagebox.showwarning("Budget Depleted", "You have no more budget! You must excavate now.")
    
    def perform_excavation(self):
        """Executa escavação na célula selecionada"""
        if not self.selected_cell:
            messagebox.showwarning("No Cell Selected", "Please select a cell first.")
            return
        
        if self.game.game_over:
            messagebox.showinfo("Game Over", "The game is over.")
            return
        
        row, col = self.selected_cell
        
        # Confirmação
        if not messagebox.askyesno(
            "Confirm Excavation",
            f"Are you sure you want to excavate at ({row},{col})?\n"
            f"This will end the game!"
        ):
            return
        
        # Executa escavação
        success, score = self.game.excavate(row, col)
        
        # Atualiza interface
        self.update_interface()
        
        # Mostra resultado
        if success:
            messagebox.showinfo(
                "Congratulations!",
                f"🎉 You found the artifact at ({row},{col})!\n"
                f"🏆 Final Score: {score} points"
            )
            self.add_history_message(f"🚨 EXCAVATED at ({row},{col}): SUCCESS! Final Score: {score}")
            
            # Destaca localização do artefato
            if (row, col) in self.cell_cards:
                card = self.cell_cards[(row, col)]
                card.config(bg='#d4edda', relief="solid")
        else:
            messagebox.showinfo(
                "Game Over",
                f"😞 No artifact found at ({row},{col}).\n"
                f"🏆 Final Score: 0 points"
            )
            self.add_history_message(f"🚨 EXCAVATED at ({row},{col}): FAILED! Score: 0")
            
            # Destaca palpite incorreto
            if (row, col) in self.cell_cards:
                card = self.cell_cards[(row, col)]
                card.config(bg='#f8d7da', relief="solid")
    
    def update_interface(self):
        """Atualiza toda a interface"""
        # Atualiza labels de status
        self.budget_label.config(text=f"💰 Budget: {self.game.budget} points")
        self.score_label.config(text=f"🏆 Score: {self.game.score} points")
        self.survey_label.config(text=f"📊 Surveys: {self.game.survey_count}")
        
        # Atualiza todas as células
        self.update_all_cells()
        
        # Re-seleciona célula atual
        if self.selected_cell:
            row, col = self.selected_cell
            self.select_cell(row, col)
        
        # Atualiza scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def add_history_message(self, message):
        """Adiciona mensagem ao histórico"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"• {message}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def on_game_window_close(self):
        """Fecha a janela do jogo"""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.game_window.destroy()
            self.root.quit()
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()

