import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os


# ================= AUDIO ================= #

def speak_explanation():
    text = (
        "This simulator demonstrates FIFO, LRU and Optimal page replacement algorithms. "
        "FIFO removes the oldest page. "
        "LRU removes the least recently used page. "
        "Optimal removes the page used farthest in future."
    )

    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"'
    )


# ================= ALGORITHMS ================= #

def fifo(pages, capacity):
    frames = []
    index = 0
    steps = []
    faults = 0

    for page in pages:
        status = "HIT"
        if page not in frames:
            status = "MISS"
            faults += 1
            if len(frames) < capacity:
                frames.append(page)
            else:
                frames[index] = page
                index = (index + 1) % capacity

        steps.append((page, frames.copy(), status))

    return faults, steps


def lru(pages, capacity):
    frames = []
    steps = []
    faults = 0

    for page in pages:
        status = "HIT"
        if page not in frames:
            status = "MISS"
            faults += 1
            if len(frames) < capacity:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
        else:
            frames.remove(page)
            frames.append(page)

        steps.append((page, frames.copy(), status))

    return faults, steps


def optimal(pages, capacity):
    frames = []
    steps = []
    faults = 0

    for i in range(len(pages)):
        status = "HIT"
        if pages[i] not in frames:
            status = "MISS"
            faults += 1
            if len(frames) < capacity:
                frames.append(pages[i])
            else:
                future = pages[i + 1:]
                index = -1
                farthest = -1

                for j in range(len(frames)):
                    if frames[j] not in future:
                        index = j
                        break
                    else:
                        pos = future.index(frames[j])
                        if pos > farthest:
                            farthest = pos
                            index = j

                frames[index] = pages[i]

        steps.append((pages[i], frames.copy(), status))

    return faults, steps


# ================= VISUAL STACK STYLE ================= #

def visualize_algorithm(container, steps, capacity, title):
    for widget in container.winfo_children():
        widget.destroy()

    tk.Label(container, text=title,
             font=("Segoe UI", 12, "bold")).pack(pady=5)

    main_frame = tk.Frame(container)
    main_frame.pack()

    for col, step in enumerate(steps):
        page, frame_state, status = step

        column_frame = tk.Frame(main_frame)
        column_frame.grid(row=0, column=col, padx=4)

        tk.Label(column_frame,
                 text=str(page),
                 font=("Segoe UI", 10, "bold"),
                 fg="#2e7d32").pack()

        stack_frame = tk.Frame(column_frame)
        stack_frame.pack()

        for i in reversed(range(capacity)):
            if i < len(frame_state):
                value = frame_state[i]
            else:
                value = ""

            tk.Label(stack_frame,
                     text=value,
                     width=2,     # smaller boxes
                     height=1,
                     borderwidth=1,
                     relief="solid",
                     bg="#e3f2fd").pack()

        color = "#2e7d32" if status == "HIT" else "#c62828"

        tk.Label(column_frame,
                 text=status,
                 fg=color,
                 font=("Segoe UI", 8, "bold")).pack(pady=2)


# ================= SMALL GRAPH ================= #

def draw_graph(faults):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 2))  # smaller graph
    ax.bar(['FIFO', 'LRU', 'Optimal'], faults)
    ax.set_title("Page Faults", fontsize=9)
    ax.set_ylabel("Faults", fontsize=8)
    ax.tick_params(axis='both', labelsize=8)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# ================= RUN ================= #

def run_simulation():
    try:
        ref = entry_ref.get()
        capacity = int(entry_frames.get())
        pages = list(map(int, ref.split()))

        fifo_faults, fifo_steps = fifo(pages, capacity)
        lru_faults, lru_steps = lru(pages, capacity)
        optimal_faults, optimal_steps = optimal(pages, capacity)

        result_text.set(
            f"FIFO: {fifo_faults}   LRU: {lru_faults}   Optimal: {optimal_faults}"
        )

        draw_graph([fifo_faults, lru_faults, optimal_faults])

        visualize_algorithm(fifo_tab, fifo_steps, capacity, "FIFO")
        visualize_algorithm(lru_tab, lru_steps, capacity, "LRU")
        visualize_algorithm(opt_tab, optimal_steps, capacity, "Optimal")

    except:
        messagebox.showerror("Error", "Please enter valid input!")


# ================= GUI ================= #

root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("1200x650")
root.configure(bg="#23272e")  # Dark background

tk.Label(
    root,
    text="Page Replacement Simulator",
    font=("Segoe UI", 16, "bold"),
    bg="#23272e",
    fg="#f8f8f2"
).pack(pady=5)

input_frame = tk.Frame(root, bg="#2d333b")
input_frame.pack(pady=3)

tk.Label(input_frame, text="Reference String:", bg="#2d333b", fg="#8be9fd", font=("Segoe UI", 10, "bold")).grid(row=0, column=0)
entry_ref = tk.Entry(input_frame, width=40, bg="#282a36", fg="#f1fa8c", insertbackground="#f1fa8c")
entry_ref.grid(row=0, column=1)

tk.Label(input_frame, text="Frames:", bg="#2d333b", fg="#8be9fd", font=("Segoe UI", 10, "bold")).grid(row=1, column=0)
entry_frames = tk.Entry(input_frame, width=8, bg="#282a36", fg="#f1fa8c", insertbackground="#f1fa8c")
entry_frames.grid(row=1, column=1)

tk.Button(root, text="Run", command=run_simulation, bg="#44475a", fg="#50fa7b", activebackground="#6272a4", font=("Segoe UI", 10, "bold")).pack(pady=3)
tk.Button(root, text="Audio", command=speak_explanation, bg="#44475a", fg="#ffb86c", activebackground="#6272a4", font=("Segoe UI", 10, "bold")).pack(pady=3)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, bg="#23272e", fg="#f8f8f2", font=("Segoe UI", 11, "bold")).pack(pady=3)

graph_frame = tk.Frame(root, bg="#23272e")
graph_frame.pack(pady=5)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

fifo_tab = ttk.Frame(notebook)
lru_tab = ttk.Frame(notebook)
opt_tab = ttk.Frame(notebook)

notebook.add(fifo_tab, text="FIFO")
notebook.add(lru_tab, text="LRU")
notebook.add(opt_tab, text="Optimal")

root.mainloop()