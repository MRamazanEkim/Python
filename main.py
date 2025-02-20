import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import colorchooser


class ScoreboardApp:
    MAX_PLAYERS = 12  

    def __init__(self, root):
        self.root = root
        self.fullscreen = True
        self.root.attributes('-fullscreen', self.fullscreen)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.bg_image = None
        self.bg_label = tk.Label(root)
        self.bg_label.place(relwidth=1, relheight=1)

        # SCOREBOARD Title
        self.scoreboard_label = tk.Label(root, text="SCOREBOARD", font=("Arial", 50, "bold"), bg="black", fg="white")
        self.scoreboard_label.place(relx=0.5, rely=0.05, anchor="center")

        # Team Data
        self.team1_players = []

        # Scoreboard Frame (Wider)
        self.scoreboard_frame = tk.Frame(root, bg="black", bd=10, padx=50, pady=30)  
        self.scoreboard_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Delete & Add Buttons (Side by Side with Team Name)
        self.delete_team1_button = tk.Button(self.scoreboard_frame, text="−", font=("Arial", 24), width=3, command=self.delete_team1_player, bg="red", fg="white", relief="raised", bd=5)
        self.delete_team1_button.grid(row=0, column=0, padx=10, pady=10)

        self.team_name_var = tk.StringVar(value="Team Name")
        self.team_name_entry = tk.Entry(self.scoreboard_frame, textvariable=self.team_name_var, font=("Arial", 40), width=14, justify="center")
        self.team_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_team1_button = tk.Button(self.scoreboard_frame, text="+", font=("Arial", 24), width=3, command=self.add_team1_player, bg="green", fg="white", relief="raised", bd=5)
        self.add_team1_button.grid(row=0, column=2, padx=10, pady=10)

        # Change Background Button (Small, Bottom Right Corner)
        self.change_bg_button = tk.Button(self.root, text="🌄", font=("Arial", 20), command=self.change_background, width=3, height=1, bg="blue", fg="white", relief="raised", bd=5)
        self.change_bg_button.place(relx=0.98, rely=0.98, anchor="se")

        # Adding Color Pickers to Upper Right Corner with Distinct Style (Icons without text)
        self.frame_color_button = tk.Button(root, text="🎨", command=self.change_frame_color, bg="yellow", fg="black", relief="raised", bd=5, font=("Arial", 12))
        self.frame_color_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.team_name_color_button = tk.Button(root, text="🎨", command=self.change_team_name_color, bg="purple", fg="white", relief="raised", bd=5, font=("Arial", 12))
        self.team_name_color_button.place(relx=0.94, rely=0.02, anchor="ne")

        self.player_name_color_button = tk.Button(root, text="🎨", command=self.change_player_names_color, bg="orange", fg="black", relief="raised", bd=5, font=("Arial", 12))
        self.player_name_color_button.place(relx=0.90, rely=0.02, anchor="ne")

    


    def add_team1_player(self):
        if len(self.team1_players) < self.MAX_PLAYERS:
            self.add_player(self.team1_players)

    def delete_team1_player(self):
        if self.team1_players:
            player = self.team1_players.pop()
            for widget in player["widgets"]:
                widget.destroy()
            self.update_ranks(self.team1_players)

    def add_player(self, team):
        row = len(team) + 1

        player = {
            "name": tk.StringVar(value=f"Player {row}"),
            "score": tk.IntVar(value=0),
            "rank": tk.StringVar(value=str(row))
        }

        entry_rank = tk.Label(self.scoreboard_frame, textvariable=player["rank"], font=("Arial", 24), width=3, bg="black", fg="white")
        entry_rank.grid(row=row, column=0, pady=10, padx=10)

        entry_name = tk.Entry(self.scoreboard_frame, textvariable=player["name"], font=("Arial", 24), width=12, justify="center")
        entry_name.grid(row=row, column=1, pady=10, padx=10)

        entry_score = tk.Entry(self.scoreboard_frame, textvariable=player["score"], font=("Arial", 24), width=6, justify="center")
        entry_score.grid(row=row, column=2, pady=10, padx=10)

        player["score"].trace_add("write", lambda *args, p=team: self.update_ranks(p))
        player["widgets"] = [entry_rank, entry_name, entry_score]
        team.append(player)

    def update_ranks(self, players):
        if not players:
            return  # Avoid errors if no players exist

        # Sort players by score (highest first)
        players.sort(key=lambda p: p["score"].get(), reverse=True)

        # Update ranks and reorder widgets
        for rank, player in enumerate(players, start=1):
            player["rank"].set(str(rank))

            # Reposition widgets dynamically
            player["widgets"][0].grid(row=rank, column=0, pady=10, padx=10)  # Rank
            player["widgets"][1].grid(row=rank, column=1, pady=10, padx=10)  # Name
            player["widgets"][2].grid(row=rank, column=2, pady=10, padx=10)  # Score

    def change_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label.config(image=self.bg_image)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.root.geometry("800x600")

    # Function to change Scoreboard Frame color
    def change_frame_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.scoreboard_frame.config(bg=color)

    # Function to change Team Name color
    def change_team_name_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.team_name_entry.config(fg=color)

    # Function to change Player Names color
    def change_player_names_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            for player in self.team1_players:
                player["widgets"][1].config(fg=color)  # Name Label


root = tk.Tk()
root.geometry("800x600")
app = ScoreboardApp(root)
root.mainloop()


