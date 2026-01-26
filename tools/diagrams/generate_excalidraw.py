#!/usr/bin/env python3
"""
Generate BMM Workflow Diagram in Excalidraw format.
Reads tools/diagrams/workflow-manifest.yaml and outputs bmm-workflow.excalidraw.
"""

import yaml
import json
import datetime
import os
from pathlib import Path

# =============================================================================
# CONSTANTS & THEME
# =============================================================================

GRID_SIZE = 20
PHASE_COLORS = {
    "discovery": {"bg": "#e8f4f8", "stroke": "#2d7d9a"},
    "planning": {"bg": "#f0e8f8", "stroke": "#7d2d9a"},
    "solutioning": {"bg": "#f8f0e8", "stroke": "#9a7d2d"},
    "implementation": {"bg": "#e8f8f0", "stroke": "#2d9a7d"}
}

NODE_WIDTH = 300
NODE_HEIGHT_BASE = 60
GAP_Y = 60
PHASE_PADDING = 40
PHASE_WIDTH = 400

# =============================================================================
# EXCALIDRAW HELPERS
# =============================================================================

def generate_id():
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

def get_current_ts():
    return int(datetime.datetime.now().timestamp() * 1000)

def create_base_element(type_name, x, y, width, height, **kwargs):
    return {
        "id": generate_id(),
        "type": type_name,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": kwargs.get("strokeColor", "#000000"),
        "backgroundColor": kwargs.get("backgroundColor", "transparent"),
        "fillStyle": kwargs.get("fillStyle", "solid"),
        "strokeWidth": kwargs.get("strokeWidth", 1),
        "strokeStyle": kwargs.get("strokeStyle", "solid"),
        "roughness": 1,
        "opacity": 100,
        "groupIds": kwargs.get("groupIds", []),
        "frameId": None,
        "roundness": kwargs.get("roundness", None),
        "seed": random_seed(),
        "version": 1,
        "versionNonce": 0,
        "isDeleted": False,
        "boundElements": [],
        "updated": get_current_ts(),
        "link": None,
        "locked": False,
    }

def random_seed():
    import random
    return random.randint(1, 1000000)

def create_rectangle(x, y, w, h, **kwargs):
    return create_base_element("rectangle", x, y, w, h, **kwargs)

def create_diamond(x, y, w, h, **kwargs):
    return create_base_element("diamond", x, y, w, h, **kwargs)

def create_text(x, y, text, **kwargs):
    # Rough estimation of width/height based on length and font size
    font_size = kwargs.get("fontSize", 20)
    width = len(text) * font_size * 0.6 + 10
    height = font_size * 1.5 * (text.count('\n') + 1)
    
    element = create_base_element("text", x, y, width, height, **kwargs)
    element.update({
        "text": text,
        "fontSize": font_size,
        "fontFamily": 1, # 1: Virgil, 2: Helvetica, 3: Cascadia
        "textAlign": kwargs.get("textAlign", "center"),
        "verticalAlign": kwargs.get("verticalAlign", "middle"),
        "baseline": height * 0.8,
    })
    return element

def create_arrow(start_elem, end_elem, **kwargs):
    # Simply connecting centers for now
    sx = start_elem['x'] + start_elem['width'] / 2
    sy = start_elem['y'] + start_elem['height']
    ex = end_elem['x'] + end_elem['width'] / 2
    ey = end_elem['y']
    
    # Adjust for side connections if specified (e.g. decision -> architecture)
    if kwargs.get('side') == 'right-right':
         sx = start_elem['x'] + start_elem['width']
         sy = start_elem['y'] + start_elem['height']/2
         ex = end_elem['x'] + end_elem['width']
         ey = end_elem['y'] + end_elem['height']/2
         
         # Elbow output
         points = [
             [0, 0],
             [40, 0],
             [40, ey - sy],
             [ex - sx, ey - sy]
         ]
    else:
        # Standard vertical
         points = [
             [0, 0],
             [ex - sx, ey - sy]
         ]

    element = create_base_element("arrow", sx, sy, 0, 0, **kwargs)
    element.update({
        "points": points,
        "startBinding": {"elementId": start_elem['id'], "focus": 0, "gap": 10},
        "endBinding": {"elementId": end_elem['id'], "focus": 0, "gap": 10},
    })
    return element

# =============================================================================
# GENERATOR
# =============================================================================

def generate_diagram():
    # Load manifest
    manifest_path = Path("workflow-manifest.yaml")
    if not manifest_path.exists():
        print("Manifest not found!")
        return
        
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)

    elements = []
    
    # Title
    title = create_text(0, 0, f"BMAD METHOD V{manifest['bmad_version']}", fontSize=40, textAlign="left")
    elements.append(title)
    
    current_y = 100
    
    # Track node elements for connections {node_id: element}
    node_map = {}
    
    # --- PHASE 1: DISCOVERY ---
    p1_nodes = []
    
    # Activities Box
    act_group_id = generate_id()
    act_rect = create_rectangle(0, 0, NODE_WIDTH, 80, strokeStyle="dashed", groupIds=[act_group_id], backgroundColor="#ffffff")
    act_label = create_text(0, 0, "Activities\n/research\n/brainstorming", fontSize=16, groupIds=[act_group_id])
    
    # Workflow: create-product-brief
    cpb_group_id = generate_id()
    cpb_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[cpb_group_id], backgroundColor="#ffffff")
    cpb_label = create_text(0, 0, "/create-product-brief\n@product-brief.md", fontSize=16, groupIds=[cpb_group_id])
    node_map['create-product-brief'] = cpb_rect
    
    p1_nodes = [(act_rect, act_label), (cpb_rect, cpb_label)]
    
    current_y = layout_phase(elements, "PHASE 1: DISCOVERY", PHASE_COLORS['discovery'], current_y, p1_nodes)
    
    # Connect Activities to product brief
    elements.append(create_arrow(act_rect, cpb_rect))
    
    
    # --- PHASE 2: PLANNING ---
    p2_nodes = []
    
    # PRD
    prd_group_id = generate_id()
    prd_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[prd_group_id], backgroundColor="#ffffff")
    prd_label = create_text(0, 0, "/prd\n@PRD.md", fontSize=16, groupIds=[prd_group_id])
    node_map['prd'] = prd_rect
    
    # Decision
    dec_group_id = generate_id()
    dec_shape = create_diamond(0, 0, 160, 100, groupIds=[dec_group_id], backgroundColor="#fff8e8", strokeColor="#7d2d9a")
    dec_label = create_text(0, 0, "Has UI?", fontSize=20, groupIds=[dec_group_id])
    node_map['has-ui'] = dec_shape

    # UX
    ux_group_id = generate_id()
    ux_rect = create_rectangle(0, 0, NODE_WIDTH, 120, groupIds=[ux_group_id], backgroundColor="#ffffff")
    ux_label = create_text(0, 0, "/create-ux-design\n@ux-design-specification.md\n@ux-color-themes.html", fontSize=16, groupIds=[ux_group_id])
    node_map['create-ux-design'] = ux_rect

    p2_nodes = [(prd_rect, prd_label), (dec_shape, dec_label), (ux_rect, ux_label)]
    
    current_y = layout_phase(elements, "PHASE 2: PLANNING", PHASE_COLORS['planning'], current_y, p2_nodes)

    # Connections Phase 2
    elements.append(create_arrow(node_map['create-product-brief'], node_map['prd']))
    elements.append(create_arrow(node_map['prd'], node_map['has-ui']))
    elements.append(create_arrow(node_map['has-ui'], node_map['create-ux-design']))
    
    # Yes Label
    yes_label = create_text(node_map['has-ui']['x'] + 80, node_map['has-ui']['y'] + 100, "Yes", fontSize=16)
    elements.append(yes_label)

    # --- PHASE 3: SOLUTIONING ---
    p3_nodes = []
    
    # Architecture
    arch_group_id = generate_id()
    arch_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[arch_group_id], backgroundColor="#ffffff")
    arch_label = create_text(0, 0, "/create-architecture\n@architecture.md", fontSize=16, groupIds=[arch_group_id])
    node_map['create-architecture'] = arch_rect
    
    # Epics
    epic_group_id = generate_id()
    epic_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[epic_group_id], backgroundColor="#ffffff")
    epic_label = create_text(0, 0, "/create-epics-and-stories\n@epics.md", fontSize=16, groupIds=[epic_group_id])
    node_map['create-epics-and-stories'] = epic_rect
    
    # Readiness
    read_group_id = generate_id()
    read_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[read_group_id], backgroundColor="#ffffff")
    read_label = create_text(0, 0, "/check-implementation-readiness\n@readiness-report.md", fontSize=16, groupIds=[read_group_id])
    node_map['check-implementation-readiness'] = read_rect
    
    p3_nodes = [(arch_rect, arch_label), (epic_rect, epic_label), (read_rect, read_label)]
    
    current_y = layout_phase(elements, "PHASE 3: SOLUTIONING", PHASE_COLORS['solutioning'], current_y, p3_nodes)

    # Connections Phase 3
    elements.append(create_arrow(node_map['create-ux-design'], node_map['create-architecture']))
    
    # NO CONNECTION ("No" branch) - Custom Arrow
    no_arrow = create_arrow(node_map['has-ui'], node_map['create-architecture'], side="right-right")
    elements.append(no_arrow)
    no_label = create_text(node_map['has-ui']['x'] + 160, node_map['has-ui']['y'], "No", fontSize=16)
    elements.append(no_label)

    elements.append(create_arrow(node_map['create-architecture'], node_map['create-epics-and-stories']))
    elements.append(create_arrow(node_map['create-epics-and-stories'], node_map['check-implementation-readiness']))

    # --- PHASE 4: IMPLEMENTATION ---
    p4_nodes = []
    
    # Sprint Planning
    sp_group_id = generate_id()
    sp_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[sp_group_id], backgroundColor="#ffffff")
    sp_label = create_text(0, 0, "/sprint-planning\n@sprint-status.yaml", fontSize=16, groupIds=[sp_group_id])
    node_map['sprint-planning'] = sp_rect
    
    # Create Story
    cs_group_id = generate_id()
    cs_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[cs_group_id], backgroundColor="#ffffff")
    cs_label = create_text(0, 0, "/create-story\n@{epic}-{story}.md", fontSize=16, groupIds=[cs_group_id])
    node_map['create-story'] = cs_rect
    
    # Dev Story
    dev_group_id = generate_id()
    dev_rect = create_rectangle(0, 0, NODE_WIDTH, 60, groupIds=[dev_group_id], backgroundColor="#ffffff")
    dev_label = create_text(0, 0, "/dev-story", fontSize=16, groupIds=[dev_group_id])
    node_map['dev-story'] = dev_rect
    
    # Code Review
    cr_group_id = generate_id()
    cr_rect = create_rectangle(0, 0, NODE_WIDTH, 60, groupIds=[cr_group_id], backgroundColor="#ffffff")
    cr_label = create_text(0, 0, "/code-review", fontSize=16, groupIds=[cr_group_id])
    node_map['code-review'] = cr_rect
    
    # Retro
    retro_group_id = generate_id()
    retro_rect = create_rectangle(0, 0, NODE_WIDTH, 60, groupIds=[retro_group_id], backgroundColor="#ffffff")
    retro_label = create_text(0, 0, "/retrospective", fontSize=16, groupIds=[retro_group_id])
    node_map['retrospective'] = retro_rect

    # Correct Course (Separate Group at bottom)
    cc_group_id = generate_id()
    cc_rect = create_rectangle(0, 0, NODE_WIDTH, 80, groupIds=[cc_group_id], backgroundColor="#ffffff")
    cc_label = create_text(0, 0, "/correct-course\n@sprint-change-proposal.md", fontSize=16, groupIds=[cc_group_id])
    node_map['correct-course'] = cc_rect
    
    # Remark for Correct Course
    msg_label = create_text(0, 0, "(run when issues arise)", fontSize=14, strokeColor="#1a684a")

    p4_nodes = [
        (sp_rect, sp_label),
        (cs_rect, cs_label),
        (dev_rect, dev_label),
        (cr_rect, cr_label),
        (retro_rect, retro_label),
        # Gap
        (cc_rect, cc_label),
        (msg_label, None) # None as dummy for shape, handle manually
    ]
    
    current_y = layout_phase(elements, "PHASE 4: IMPLEMENTATION", PHASE_COLORS['implementation'], current_y, p4_nodes)
    
    # Connections Phase 4
    elements.append(create_arrow(node_map['check-implementation-readiness'], node_map['sprint-planning']))
    elements.append(create_arrow(node_map['sprint-planning'], node_map['create-story']))
    elements.append(create_arrow(node_map['create-story'], node_map['dev-story']))
    elements.append(create_arrow(node_map['dev-story'], node_map['code-review']))
    elements.append(create_arrow(node_map['code-review'], node_map['retrospective']))
    
    # Loop back (Retro -> Planning)
    # Simple straight arrow for now as Excalidraw auto-routing is complex to script
    # User can adjust manually
    
    # Save Output
    output = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": GRID_SIZE
        }
    }
    
    with open("bmm-workflow.excalidraw", "w") as f:
        json.dump(output, f, indent=2)

    print("Generated bmm-workflow.excalidraw")

def layout_phase(elements, title, colors, start_y, node_pairs):
    """
    Layout a phase container and stack nodes vertically inside it.
    Returns the next available Y coordinate.
    """
    
    PHASE_PADDING_TOP = 60
    NODE_GAP = 40
    
    # Calculate content height
    content_height = 0
    valid_nodes = []
    
    for shape, label in node_pairs:
        # Special case for text-only (remark)
        if label is None: # shape is actually the text
            h = 30 
            valid_nodes.append((shape, None, h))
        else:
            h = shape['height']
            valid_nodes.append((shape, label, h))
        content_height += h + NODE_GAP

    box_height = content_height + PHASE_PADDING_TOP
    
    # Create Phase Container
    cx = 0
    cy = start_y
    
    container = create_rectangle(cx, cy, PHASE_WIDTH, box_height, 
                                 backgroundColor=colors['bg'], 
                                 strokeColor=colors['stroke'],
                                 strokeWidth=2,
                                 roundness={"type": 3})
    elements.append(container)
    
    # Title
    t_label = create_text(cx + 20, cy + 15, title, 
                          fontSize=20, 
                          strokeColor=colors['stroke'], # Use stroke color for text
                          textAlign="left")
    elements.append(t_label)
    
    # Place Nodes
    curr_ay = cy + PHASE_PADDING_TOP
    center_x = cx + (PHASE_WIDTH / 2)
    
    for shape, label, h in valid_nodes:
        # Position Shape
        
        if label is None:
            # It's just a text element (remark)
            shape['x'] = center_x - (shape['width'] / 2)
            shape['y'] = curr_ay
            elements.append(shape)
        else:
            shape['x'] = center_x - (shape['width'] / 2)
            shape['y'] = curr_ay
            elements.append(shape)
            
            # Position Label (Center in shape)
            label['x'] = shape['x'] + (shape['width'] - label['width']) / 2
            label['y'] = shape['y'] + (shape['height'] - label['height']) / 2
            elements.append(label)
        
            # Ensure label is bound to shape
            shape['boundElements'].append({"type": "text", "id": label['id']})
            label['containerId'] = shape['id']
            
        curr_ay += h + NODE_GAP
        
    return cy + box_height + GAP_Y

if __name__ == "__main__":
    generate_diagram()
