import tkinter as tk
from tkinter import ttk, filedialog
from types import SimpleNamespace


def launch_config_panel(run_game_callback, args=None):
    root = tk.Tk()
    root.title("Learn2Slither - Game Configuration")
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

    row = 0
    add_row("Training sessions:",
            ttk.Entry(main_frame, textvariable=sessions_var, width=10),
            row)
    row += 1

    visual_combo = ttk.Combobox(main_frame,
                                textvariable=visual_var,
                                values=["on", "off"], width=7)
    add_row("Visual mode:", visual_combo, row)
    row += 1

    save_frame = ttk.Frame(main_frame)
    ttk.Entry(save_frame, textvariable=save_var, width=30).pack(side="left")
    ttk.Button(save_frame, text="Browse",
               command=lambda: choose_file(save_var, "save")
               ).pack(side="left", padx=5)
    add_row("Save model to:", save_frame, row)
    row += 1

    load_frame = ttk.Frame(main_frame)
    ttk.Entry(load_frame, textvariable=load_var, width=30).pack(side="left")
    ttk.Button(load_frame, text="Browse",
               command=lambda: choose_file(load_var, "load")
               ).pack(side="left", padx=5)
    add_row("Load model from:", load_frame, row)
    row += 1

    add_row("Board size (10–42):", ttk.Entry(main_frame,
            textvariable=boardsize_var, width=10), row)
    row += 1
    add_row("Game speed:", ttk.Entry(main_frame,
            textvariable=speed_var, width=10), row)
    row += 1

    ttk.Checkbutton(main_frame,
                    text="Enable step-by-step mode",
                    variable=step_var
                    ).grid(row=row, column=1, sticky="w", pady=5)
    row += 1
    ttk.Checkbutton(main_frame,
                    text="Disable learning (test mode)",
                    variable=dontlearn_var
                    ).grid(row=row, column=1, sticky="w", pady=5)
    row += 1

    def start_game():
        args = SimpleNamespace(
            sessions=sessions_var.get(),
            visual=visual_var.get(),
            save=save_var.get() or None,
            load=load_var.get() or None,
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
               text="Start Human Snake Game",
               command=start_human_game
               ).grid(row=row, column=0, columnspan=2, pady=10)

    root.update_idletasks()
    root.geometry(
        f"{main_frame.winfo_reqwidth()+40}x{main_frame.winfo_reqheight()+40}")
    root.mainloop()
