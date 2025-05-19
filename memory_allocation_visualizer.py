import customtkinter as ctk

def best_fit_allocate(blocks, processes):
    n = len(blocks)
    allocated_processes = [-1] * n  # -1 indicates a free block
    for p in range(len(processes)):
        process_size = processes[p]
        # Find all free blocks that can fit the process
        eligible = [(i, blocks[i]) for i in range(n) if allocated_processes[i] == -1 and blocks[i] >= process_size]
        if eligible:
            # Select the smallest block that fits
            best_block = min(eligible, key=lambda x: x[1])
            allocated_processes[best_block[0]] = p
    return allocated_processes

def worst_fit_allocate(blocks, processes):
    n = len(blocks)
    allocated_processes = [-1] * n  # -1 indicates a free block
    for p in range(len(processes)):
        process_size = processes[p]
        # Find all free blocks that can fit the process
        eligible = [(i, blocks[i]) for i in range(n) if allocated_processes[i] == -1 and blocks[i] >= process_size]
        if eligible:
            # Select the largest block that fits
            worst_block = max(eligible, key=lambda x: x[1])
            allocated_processes[worst_block[0]] = p
    return allocated_processes

def visualize_allocation(canvas, blocks, processes, allocation):
    canvas.delete("all")  # Clear previous drawings
    total_size = sum(blocks)
    canvas_width = 800
    scale = canvas_width / total_size if total_size > 0 else 1  # Avoid division by zero
    x = 0
    for i in range(len(blocks)):
        block_size = blocks[i]
        width = block_size * scale
        if allocation[i] != -1:
            process_index = allocation[i]
            process_size = processes[process_index]
            color = get_color(process_index)
            canvas.create_rectangle(x, 0, x + width, 50, fill=color, outline="black")
            text = f"P{process_index} ({process_size})"
        else:
            canvas.create_rectangle(x, 0, x + width, 50, fill="white", outline="black")
            text = f"Free ({block_size})"
        # Center the text in the rectangle
        canvas.create_text(x + width / 2, 25, text=text, font=("Arial", 10))
        x += width

def get_color(index):
    colors = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta"]
    return colors[index % len(colors)]

def allocate_and_visualize():
    blocks_str = blocks_entry.get()
    processes_str = processes_entry.get()
    try:
        blocks = [int(x.strip()) for x in blocks_str.split(',')]
        processes = [int(x.strip()) for x in processes_str.split(',')]
    except ValueError:
        print("Invalid input: Please enter comma-separated integers.")
        return
    algorithm = algorithm_var.get()
    if algorithm == "Best Fit":
        allocation = best_fit_allocate(blocks, processes)
    elif algorithm == "Worst Fit":
        allocation = worst_fit_allocate(blocks, processes)
    else:
        print("Unknown algorithm selected.")
        return
    visualize_allocation(canvas, blocks, processes, allocation)

# Initialize the application
app = ctk.CTk()
app.title("Memory Allocation Visualizer")

# Left frame for inputs and controls
left_frame = ctk.CTkFrame(app)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

# Canvas for visualization
canvas = ctk.CTkCanvas(app, width=800, height=200)
canvas.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Input fields
ctk.CTkLabel(left_frame, text="Memory Blocks (comma-separated):").pack(pady=5)
blocks_entry = ctk.CTkEntry(left_frame, width=200)
blocks_entry.pack(pady=5)

ctk.CTkLabel(left_frame, text="Processes (comma-separated):").pack(pady=5)
processes_entry = ctk.CTkEntry(left_frame, width=200)
processes_entry.pack(pady=5)

# Algorithm selection
ctk.CTkLabel(left_frame, text="Select Algorithm:").pack(pady=5)
algorithm_var = ctk.StringVar(value="Best Fit")
ctk.CTkRadioButton(left_frame, text="Best Fit", variable=algorithm_var, value="Best Fit").pack(pady=5)
ctk.CTkRadioButton(left_frame, text="Worst Fit", variable=algorithm_var, value="Worst Fit").pack(pady=5)

# Button to trigger allocation and visualization
ctk.CTkButton(left_frame, text="Allocate and Visualize", command=allocate_and_visualize).pack(pady=20)

# Start the application
app.mainloop()