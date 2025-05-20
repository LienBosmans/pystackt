# Contains functionality to dynamically assign colors to event types and object types.

from matplotlib import colormaps
from matplotlib.colors import to_hex

def _assign_colors(types:list,palette:str='viridis') -> dict:
    """Returns a dictionary that assigns a color to each value in `types`, using the color pallette.
    Note that Matplotlib colormaps are case sensitive.
    
    Perceptually uniform sequential colormaps: 'viridis', 'plasma', 'inferno', 'magma', 'cividis'.
    Sequential colormaps: 'Grays', 'Blues', 'Greens', 'Purples', 'Reds', 'Oranges'.
    """
    n = len(types)
    cmap = colormaps.get_cmap(palette)

    color_map = {}

    for i, type in enumerate(sorted(types, reverse=True)):
        if n > 1:
            color_map[type] = to_hex(cmap( i / (n - 1) ))
        else:
            color_map[type] = to_hex(cmap(1))

    return color_map
