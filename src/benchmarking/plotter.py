import matplotlib as plt
import matplotlib.pyplot as plt

def create_complexity_chart(results_dict, algorithm_name):
    """
    Takes the dictionary from run_benchmark_data.
    Returns a Matplotlib Figure object ready to be embedded in PyQt.
    """
    sizes = results_dict["sizes"]
    times = results_dict["times"]
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Plot the line
    ax.plot(sizes, times, marker='o', linestyle='-', color='#2b8cbe', linewidth=2, label="Optimized")
    
    # Styling
    ax.set_title(f"Time Complexity: {algorithm_name}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Dataset Size (Number of Nodes)", fontsize=10)
    ax.set_ylabel("Execution Time (Seconds)", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add a text annotation for the final time
    if times:
        max_time = times[-1]
        ax.annotate(f"{max_time:.2f}s", xy=(sizes[-1], times[-1]), 
                    xytext=(sizes[-1], times[-1]+0.5),
                    arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.tight_layout()
    return fig
