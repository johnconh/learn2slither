import tkinter as tk
from tkinter import ttk, filedialog, messagebox, TclError
import os
from types import SimpleNamespace


def launch_config_panel(run_game_callback, args=None):
    root = tk.Tk()
    root.title("Game Configuration")
    root.resizable(False, False)

    default_args = args or SimpleNamespace(
        sessions=10,
        visual="on",
        save=None,
        load=None,
        dontlearn=False,
        step_by_step=False,
        board_size=20,
        speed=100
    )

    sessions_var = tk.IntVar(value=default_args.sessions)
    visual_var = tk.StringVar(value=default_args.visual)
    save_var = tk.StringVar(value=default_args.save or "")
    load_var = tk.StringVar(value=default_args.load or "")
    dontlearn_var = tk.BooleanVar(value=default_args.dontlearn)
    step_var = tk.BooleanVar(value=default_args.step_by_step)
    boardsize_var = tk.IntVar(value=default_args.board_size)
    speed_var = tk.IntVar(value=default_args.speed)

    def choose_file(entry_var, mode="save"):
        path = (filedialog.asksaveasfilename()
                if mode == "save" else filedialog.askopenfilename())
        if path:
            entry_var.set(path)

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill="both", expand=True)

    def add_row(label, widget, row):
        ttk.Label(main_frame, text=label).grid(
            row=row, column=0, sticky="e", pady=5, padx=10)
        widget.grid(row=row, column=1, sticky="w", pady=5, padx=10)

    def validate_positive_int(value, field_name):
        if value <= 0:
            messagebox.showerror(
                "Input Error",
                f"{field_name} must be a positive integer"
            )
            return False
        if value > 1000:
            messagebox.showerror(
                "Input Error",
                f"{field_name} must be less than 1000"
            )
            return False
        return True

    def validate_board_size(value):
        if value < 10 or value > 42:
            messagebox.showerror(
                "Input Error",
                "Board size must be between 10 and 42"
            )
            return False
        return True

    def validate_pth_file(value, required=False):
        if not value and not required:
            return True
        if not value and required:
            messagebox.showerror("Input Error", "File path is required")
            return False
        if not value.endswith('.pth'):
            messagebox.showerror(
                "Input Error", "File must have .pth extension"
            )
            return False
        return True

    def validate_load_file(value):
        if not value:
            return True
        if not value.endswith('.pth'):
            messagebox.showerror(
                "Input Error", "File must have .pth extension"
            )
            return False
        if not os.path.exists(value):
            messagebox.showerror(
                "Input Error", f"File {value} does not exist"
            )
            return False
        return True

    row = 0
    add_row("Training sessions:", ttk.Entry(main_frame,
                                            textvariable=sessions_var,
                                            width=10), row)
    row += 1

    visual_combo = ttk.Combobox(main_frame,
                                textvariable=visual_var,
                                values=["on", "off"],
                                width=7)
    add_row("Visual mode:", visual_combo, row)
    row += 1

    save_frame = ttk.Frame(main_frame)
    ttk.Entry(save_frame, textvariable=save_var, width=30).pack(side="left")
    ttk.Button(save_frame,
               text="Browse",
               command=lambda: choose_file(save_var, "save")
               ).pack(side="left", padx=5)
    add_row("Save model to:", save_frame, row)
    row += 1

    load_frame = ttk.Frame(main_frame)
    ttk.Entry(load_frame, textvariable=load_var, width=30).pack(side="left")
    ttk.Button(load_frame,
               text="Browse",
               command=lambda: choose_file(load_var, "load")
               ).pack(side="left", padx=5)
    add_row("Load model from:", load_frame, row)
    row += 1

    add_row("Board size (10–42):",
            ttk.Entry(main_frame, textvariable=boardsize_var, width=10), row)
    row += 1
    add_row("Game speed:",
            ttk.Entry(main_frame, textvariable=speed_var, width=10), row)
    row += 1

    ttk.Checkbutton(main_frame,
                    text="Enable step-by-step mode", variable=step_var
                    ).grid(row=row, column=1, sticky="w", pady=5)
    row += 1
    ttk.Checkbutton(main_frame,
                    text="Disable learning (test mode)",
                    variable=dontlearn_var
                    ).grid(row=row, column=1, sticky="w", pady=5)
    row += 1

    def start_game():
        try:
            sessions = sessions_var.get()
            board_size = boardsize_var.get()
            speed = speed_var.get()
        except TclError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid numeric values."
            )
            return

        if not validate_positive_int(sessions, "Training sessions"):
            return
        if not validate_board_size(board_size):
            return
        if not validate_positive_int(speed, "Game speed"):
            return

        save_path = save_var.get() or None
        if save_path and not validate_pth_file(save_path):
            return

        load_path = load_var.get() or None
        if load_path and not validate_load_file(load_path):
            return

        args = SimpleNamespace(
            sessions=sessions_var.get(),
            visual=visual_var.get(),
            save=save_path,
            load=load_path,
            dontlearn=dontlearn_var.get(),
            step_by_step=step_var.get(),
            board_size=boardsize_var.get(),
            speed=speed_var.get(),
            game=False
        )
        root.destroy()
        run_game_callback(args)

    ttk.Button(main_frame,
               text="Start AI Game",
               command=start_game
               ).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1

    def start_human_game():
        root.destroy()
        import snake_game
        snake_game.main()

    ttk.Button(main_frame,
               text="Start Human Game",
               command=start_human_game
               ).grid(row=row, column=0, columnspan=2, pady=10)

    root.update_idletasks()
    root.geometry(
        f"{main_frame.winfo_reqwidth()+80}x{main_frame.winfo_reqheight()+40}"
    )
    root.mainloop()
