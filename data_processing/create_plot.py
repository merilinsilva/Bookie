######IMPORTS######
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for non-interactive plotting
import matplotlib.pyplot as plt
from matplotlib import cm
import io
import base64
import matplotlib.colors as mcolors
import numpy as np
###################

def lighten_color(color, amount=0.5):
    """
    Lightens a given color by blending it with white.
    Args:
        color (tuple): The RGBA color to lighten.
        amount (float): The amount of lightening (0.0 = no change, 1.0 = white).
    Returns:
        tuple: The lightened RGBA color.
    """
    white = np.array([1, 1, 1, 1])  # White RGBA
    color = np.array(color)
    return tuple(color + (white - color) * amount)

def create_percentage_plot(percentages):
    """
    Create a donut chart for subgenre percentages and return it as a base64-encoded string.
    
    Args:
        percentages (dict): Dictionary with subgenres and percentages.
    
    Returns:
        str: Base64-encoded string of the plot image.
    """
    # Filter out subgenres and percentages with 0% values
    subgenres = [subgenre for subgenre, value in percentages.items() if value > 0]
    values = [value for value in percentages.values() if value > 0]

    # Function to format autopct and hide 0% labels
    def autopct_format(pct):
        return f'{pct:.1f}%' if pct > 0 else ''

    # Generate colors from a colormap and lighten them
    colormap = cm.get_cmap('tab20b')
    original_colors = colormap(range(len(subgenres)))
    lightened_colors = [lighten_color(color, amount=0.2) for color in original_colors]

    # Create the pie chart with a donut (center circle)
    plt.figure(figsize=(6, 6))
    plt.pie(values, colors=lightened_colors, labels=subgenres,
            autopct=autopct_format, pctdistance=0.85, startangle=90, textprops={'fontsize': 14, 'fontweight': 'bold'})

    # Add a white circle at the center to create the donut effect
    centre_circle = plt.Circle((0, 0), 0.70, fc='#e1e1e1')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')  # Ensure the pie chart is a perfect circle

    # Save the image to an in-memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    plt.close()  # Close the plot to free resources
    buffer.seek(0)

    # Encode the image as base64
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Create the data URI for embedding in HTML or as a link
    return f"data:image/png;base64,{base64_image}"
