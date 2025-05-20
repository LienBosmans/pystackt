# Contains stylesheets used for app elements

graph_stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'text-halign': 'center',
            'min-zoomed-font-size': '4'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'content': 'data(label)',
            'text-rotation': 'autorotate',
            'min-zoomed-font-size': '4',
            'text-background-color': 'white',
            'text-background-opacity': '0.5',
            'font-size': '8'
        }
    },

    # Class selectors
    {
        'selector': '.event',
        'style': {
            'shape': 'round-rectangle',
            'width': '32',
            'height': '32',
            'background-color': 'data(color)',
            'text-background-color': 'data(color)',
            'text-background-opacity': '0.3',
            'text-valign': 'top'
        }
    },
    {
        'selector': '.object',
        'style': {
            'shape': 'circle',
            'width': '16',
            'height': '16',
            'background-color': 'data(color)',
            'text-background-color': 'data(color)',
            'text-background-opacity': '0.3',
            'text-valign': 'bottom',
            'font-size': '6',
            'text-max-width': '80px',
            'text-wrap': 'ellipsis'
        }
    },
    {
        'selector': '.timestamp',
        'style': {
            'border-color': '#62B6CB',
            'background-color': '#62B6CB',
            'background-opacity': '0.2'
        }
    },
    {
        'selector': '.follows',
        'style': {
            'line-style': 'solid',
            'mid-target-arrow-shape': 'triangle',
            'mid-target-arrow-color': 'data(color)',
            'line-color': 'data(color)'
        }
    },
    {
        'selector': '.linked',
        'style': {
            'line-style': 'dashed',
            'line-color': 'data(color)',
        }
    }
]
