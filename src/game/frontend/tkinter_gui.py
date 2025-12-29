import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from backend.gamelogic import GameLogic

class GameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Raiders of the Lost Ark - Game Configuration")
        self.root.geometry("400x300")
        
        self.game = None
        self.game_window = None
        self.selected_cell = None
        self.selected_sensor = "GPR"
        
        self.create_config_window()
    
    def create_config_window(self):
        """Creates config window"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Game Configuration", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Fields
        ttk.Label(main_frame, text="Rows:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.rows_var = tk.IntVar(value=4)
        rows_spinbox = ttk.Spinbox(main_frame, from_=2, to=20, textvariable=self.rows_var, width=10)
        rows_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Columns:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cols_var = tk.IntVar(value=4)
        cols_spinbox = ttk.Spinbox(main_frame, from_=2, to=20, textvariable=self.cols_var, width=10)
        cols_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Initial Budget:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.budget_var = tk.IntVar(value=100)
        budget_spinbox = ttk.Spinbox(main_frame, from_=50, to=500, textvariable=self.budget_var, width=10)
        budget_spinbox.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Random Seed:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.seed_var = tk.IntVar(value=42)
        seed_spinbox = ttk.Spinbox(main_frame, from_=1, to=1000, textvariable=self.seed_var, width=10)
        seed_spinbox.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(main_frame, text="Create Game", command=self.create_game).grid(
            row=5, column=0, columnspan=2, pady=20)
    
    def create_game(self):
        """Creates the game"""
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            seed = int(self.seed_var.get())
            budget = int(self.budget_var.get())
            
            if rows < 2 or cols < 2:
                messagebox.showerror("Error", "Grid must be at least 2x2")
                return
            
            self.game = GameLogic(rows, cols, seed, budget)
            
            # Fecha janela de configuração
            self.root.withdraw()
            
            # Cria janela do jogo
            self.create_game_window()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create game: {str(e)}")
    
    def create_game_window(self):
        """Creates game window"""
        self.game_window = tk.Toplevel()
        self.game_window.title("Raiders of the Lost Ark")
        self.game_window.geometry("1000x700")
        self.game_window.protocol("WM_DELETE_WINDOW", self.on_game_window_close)
        
        # Main container
        main_container = ttk.Frame(self.game_window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel for info and controls
        top_panel = ttk.Frame(main_container)
        top_panel.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        # Left side: Game info
        info_frame = ttk.LabelFrame(top_panel, text="Game Status", padding="10")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.budget_label = ttk.Label(
            info_frame, 
            text=f"Budget: {self.game.budget} points", 
            font=("Arial", 12, "bold")
        )
        self.budget_label.pack(anchor=tk.W, pady=2)
        
        self.score_label = ttk.Label(
            info_frame, 
            text=f"Score: {self.game.score} points", 
            font=("Arial", 12, "bold")
        )
        self.score_label.pack(anchor=tk.W, pady=2)
        
        self.survey_label = ttk.Label(
            info_frame, 
            text=f"Surveys: {self.game.survey_count}", 
            font=("Arial", 11)
        )
        self.survey_label.pack(anchor=tk.W, pady=2)
        
        # Right side: Controls
        control_frame = ttk.LabelFrame(top_panel, text="Actions", padding="10")
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Sensor selection
        ttk.Label(control_frame, text="Select Sensor:").pack(anchor=tk.W, pady=2)
        self.sensor_var = tk.StringVar(value="GPR")
        sensor_frame = ttk.Frame(control_frame)
        sensor_frame.pack(fill=tk.X, pady=5)
        
        sensors = [("GPR (5 points)", "GPR"), ("MAG (3 points)", "MAG"), ("VIS (1 point)", "VIS")]
        for text, value in sensors:
            rb = ttk.Radiobutton(sensor_frame, text=text, variable=self.sensor_var, value=value)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Selected cell info
        self.selected_cell_label = ttk.Label(
            control_frame, 
            text="No cell selected", 
            font=("Arial", 10, "italic")
        )
        self.selected_cell_label.pack(anchor=tk.W, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        survey_btn = ttk.Button(
            action_frame,
            text="Perform Survey",
            command=self.perform_survey,
            width=15
        )
        survey_btn.pack(side=tk.LEFT, padx=5)
        
        excavate_btn = ttk.Button(
            action_frame,
            text="Excavate",
            command=self.perform_excavation,
            width=15,
            style="Danger.TButton"
        )
        excavate_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure style for danger button
        style = ttk.Style()
        style.configure("Danger.TButton", foreground="white", background="#dc3545")
        
        # Grid display area
        grid_container = ttk.Frame(main_container)
        grid_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas for grid
        canvas_frame = ttk.Frame(grid_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame for grid cells
        self.grid_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor=tk.NW
        )
        
        # Configure scroll
        self.grid_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Create grid
        self.create_grid()
        
        # History panel
        history_frame = ttk.LabelFrame(main_container, text="Survey History", padding="10")
        history_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame, height=4, width=80, state=tk.DISABLED
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.add_history_message("Game started. Select a cell and choose a sensor.")
    
    def on_frame_configure(self, event):
        """Updates scrollregion when frame changes size"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Adjusts inner frame size when canvas changes size"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def create_grid(self):
        """Creates grid cells with detailed information"""
        rows = self.game.grid.rows
        cols = self.game.grid.columns
        
        # Calculate cell size based on content
        cell_width = 120
        cell_height = 120
        
        # Clear existing widgets
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # Create grid of cells
        self.cell_frames = []
        self.cell_buttons = []
        
        for i in range(rows):
            row_frames = []
            row_buttons = []
            for j in range(cols):
                # Create cell frame - use tk.Frame instead of ttk.Frame
                cell_frame = tk.Frame(
                    self.grid_frame,
                    borderwidth=2,
                    relief="ridge",
                    width=cell_width,
                    height=cell_height,
                    bg='#f0f0f0'  # Background color
                )
                cell_frame.grid(row=i, column=j, padx=2, pady=2, sticky=(tk.W, tk.E, tk.N, tk.S))
                cell_frame.grid_propagate(False)
                
                # Get cell data
                pos = self.game.grid.positions[i, j]
                
                # Create labels with cell information - use tk.Label instead of ttk.Label
                # Cell coordinates
                coord_label = tk.Label(
                    cell_frame, 
                    text=f"({i},{j})", 
                    font=("Arial", 9, "bold"),
                    anchor=tk.W,
                    bg='#f0f0f0'  # Same background as frame
                )
                coord_label.place(x=5, y=5)
                
                # Probability
                prob = pos.get_probability()
                prob_label = tk.Label(
                    cell_frame,
                    text=f"P: {prob:.4f}",
                    font=("Arial", 9),
                    anchor=tk.W,
                    bg='#f0f0f0'
                )
                prob_label.place(x=5, y=25)
                
                # Sensor readings
                sensors = ['GPR', 'MAG', 'VIS']
                sensor_labels = []
                
                for idx, sensor in enumerate(sensors):
                    reading = pos.status.get(sensor, 'None')
                    label = tk.Label(
                        cell_frame,
                        text=f"{sensor}: {reading}",
                        font=("Arial", 8),
                        anchor=tk.W,
                        bg='#f0f0f0'
                    )
                    label.place(x=5, y=45 + idx * 18)
                    sensor_labels.append(label)
                
                # Store references for updates
                cell_data = {
                    'coord': coord_label,
                    'prob': prob_label,
                    'sensors': sensor_labels,
                    'frame': cell_frame
                }
                row_frames.append(cell_data)
                
                # Canvas transparente para capturar cliques
                cell_button = tk.Canvas(
                    cell_frame,
                    highlightthickness=0,
                    borderwidth=0
                )
                cell_button.place(x=0, y=0, relwidth=1, relheight=1)
                cell_button.bind('<Button-1>', lambda e, r=i, c=j: self.select_cell(r, c))
                row_buttons.append(cell_button)
                
                coord_label.lift()
                prob_label.lift()
                for label in sensor_labels:
                    label.lift()
            
            self.cell_frames.append(row_frames)
            self.cell_buttons.append(row_buttons)


    def select_cell(self, row, col):
        """Selects a cell and updates display"""
        # Deselect previous cell
        if self.selected_cell:
            old_row, old_col = self.selected_cell
            if 0 <= old_row < len(self.cell_frames) and 0 <= old_col < len(self.cell_frames[0]):
                # Restaurar aparência original do frame
                old_frame = self.cell_frames[old_row][old_col]['frame']
                old_frame.config(
                    relief="ridge",
                    bg='#f0f0f0'  # Cor original - use bg, não background
                )
                
                # Restaurar cor dos labels
                old_cell_data = self.cell_frames[old_row][old_col]
                old_cell_data['coord'].config(bg='#f0f0f0')
                old_cell_data['prob'].config(bg='#f0f0f0')
                for sensor_label in old_cell_data['sensors']:
                    sensor_label.config(bg='#f0f0f0')
        
        # Select new cell
        self.selected_cell = (row, col)
        
        # Alterar aparência do novo frame
        selected_frame = self.cell_frames[row][col]['frame']
        selected_frame.config(
            relief="solid",
            bg="#a0c8ff"  # Azul claro para seleção
        )
        
        # Atualizar cor dos labels na célula selecionada
        selected_cell_data = self.cell_frames[row][col]
        selected_cell_data['coord'].config(bg="#a0c8ff")
        selected_cell_data['prob'].config(bg="#a0c8ff")
        for sensor_label in selected_cell_data['sensors']:
            sensor_label.config(bg="#a0c8ff")
        
        # Update selected cell label
        self.selected_cell_label.config(text=f"Selected: ({row}, {col})")
        
        # Update probability display
        pos = self.game.grid.positions[row, col]
        self.cell_frames[row][col]['prob'].config(
            text=f"P: {pos.get_probability():.4f}"
        )
        
            
    def perform_excavation(self):
        """Performs excavation on selected cell"""
        if not self.selected_cell:
            messagebox.showwarning("No Cell Selected", "Please select a cell first.")
            return
        
        if self.game.game_over:
            messagebox.showinfo("Game Over", "The game is over.")
            return
        
        row, col = self.selected_cell
        
        # Confirmation
        if not messagebox.askyesno(
            "Confirm Excavation",
            f"Are you sure you want to excavate at ({row},{col})?\n"
            f"This will end the game!"
        ):
            return
        
        # Perform excavation
        success, score = self.game.excavate(row, col)
        
        # Update interface
        self.update_interface()
        
        # Show result
        if success:
            messagebox.showinfo(
                "Congratulations!",
                f"You found the artifact at ({row},{col})!\n"
                f"Final Score: {score} points"
            )
            self.add_history_message(f"EXCAVATED at ({row},{col}): SUCCESS! Score: {score}")
            
            # Highlight artifact location
            if 0 <= row < len(self.cell_frames) and 0 <= col < len(self.cell_frames[0]):
                self.cell_buttons[row][col].config(bg="#90ee90")  # Light green
                self.cell_frames[row][col]['frame'].config(relief="solid", borderwidth=3)
        else:
            messagebox.showinfo(
                "Game Over",
                f"No artifact found at ({row},{col}).\n"
                f"Final Score: 0 points"
            )
            self.add_history_message(f"EXCAVATED at ({row},{col}): FAILED! Score: 0")
            
            # Highlight incorrect guess
            if 0 <= row < len(self.cell_frames) and 0 <= col < len(self.cell_frames[0]):
                self.cell_buttons[row][col].config(bg="#ffcccb")  # Light red
    
    def update_interface(self):
        """Updates entire game interface"""
        # Update labels
        self.budget_label.config(text=f"Budget: {self.game.budget} points")
        self.score_label.config(text=f"Score: {self.game.score} points")
        self.survey_label.config(text=f"Surveys: {self.game.survey_count}")
        
        # Update all cell displays
        rows = self.game.grid.rows
        cols = self.game.grid.columns
        
        for i in range(rows):
            for j in range(cols):
                pos = self.game.grid.positions[i, j]
                cell_data = self.cell_frames[i][j]
                
                # Update probability
                prob = pos.get_probability()
                cell_data['prob'].config(text=f"P: {prob:.4f}")
                
                # Update sensor readings
                sensors = ['GPR', 'MAG', 'VIS']
                for idx, sensor in enumerate(sensors):
                    reading = pos.status.get(sensor, 'None')
                    cell_data['sensors'][idx].config(text=f"{sensor}: {reading}")
        
        # Reselect current cell to update highlight
        if self.selected_cell:
            row, col = self.selected_cell
            self.select_cell(row, col)
        
        # Update scrollregion
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def add_history_message(self, message):
        """Adds message to history"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"• {message}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def on_game_window_close(self):
        """Handles game window closing"""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.game_window.destroy()
            self.root.quit()
    
    def run(self):
        """Starts the application"""
        self.root.mainloop()

    def perform_survey(self):
        """Performs survey on selected cell"""
        if not self.selected_cell:
            messagebox.showwarning("No Cell Selected", "Please select a cell first.")
            return
        
        if self.game.game_over:
            messagebox.showinfo("Game Over", "The game is over.")
            return
        
        row, col = self.selected_cell
        sensor_type = self.sensor_var.get()
        
        # Perform survey
        reading, success, cost = self.game.survey(row, col, sensor_type)
        
        if not success:
            messagebox.showwarning("Cannot Survey", reading)
            return
        
        # Update interface
        self.update_interface()
        
        # Add to history
        message = f"Survey at ({row},{col}) with {sensor_type}: {reading} (Cost: {cost})"
        self.add_history_message(message)
        
        # Show result in status
        self.selected_cell_label.config(
            text=f"Selected: ({row}, {col}) - {sensor_type}: {reading}"
        )
        
        # Check budget
        if self.game.budget <= 0:
            messagebox.showwarning("Budget Depleted", "You have no more budget! You must excavate now.")
    