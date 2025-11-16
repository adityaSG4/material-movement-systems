import cv2
import numpy as np
import heapq
import os
import sys

# Increase recursion limit for path reconstruction (safety)
sys.setrecursionlimit(3000) 

def heuristic(a, b):
    """Euclidean distance heuristic for A*."""
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def snap_to_white(img, x, y, search_radius=5):
    """Finds the nearest white pixel to (x,y) within a radius, focusing on white (path=255)."""
    h, w = img.shape
    if img[y, x] == 255:
        return (x, y)
    
    # Spiral out to find nearest 255 (white)
    for r in range(1, search_radius + 1):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and img[ny, nx] == 255:
                    return (nx, ny)
    return None

def solve_maze_a_star_final(image_path, output_path):
    """Solves a maze image using A* Search with robust Start/End detection 
       and safe 4-connectivity pathfinding."""
    try:
        # --- 1. Load and Preprocess Image ---
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, "Error: Could not load image."
        
        h, w = img.shape
        
        # Standard Binarization (Black Walls=0, White Path=255)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) 
        
        # --- CRITICAL: NO DILATION HERE ---

        def find_robust_start_end(image):
            """Finds path clusters on the border and returns the one closest to the top and the one closest to the bottom."""
            path_val = 255
            
            # Find all path pixels on the absolute border
            border_path_pixels = []
            for x in range(w):
                if image[0, x] == path_val: border_path_pixels.append((x, 0))
                if image[h - 1, x] == path_val: border_path_pixels.append((x, h - 1))
            for y in range(1, h - 1):
                if image[y, 0] == path_val: border_path_pixels.append((0, y))
                if image[y, w - 1] == path_val: border_path_pixels.append((w - 1, y))

            if not border_path_pixels: return None, None
            
            # Cluster the border path pixels
            visited = set()
            clusters = []
            
            for px, py in border_path_pixels:
                if (px, py) not in visited:
                    cluster = []
                    stack = [(px, py)]
                    visited.add((px, py))
                    
                    while stack:
                        cx, cy = stack.pop()
                        cluster.append((cx, cy))
                        
                        # Use 4-connectivity to find connected border pixels
                        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nx, ny = cx + dx, cy + dy
                            neighbor = (nx, ny)
                            
                            is_on_border = (nx == 0 or nx == w - 1 or ny == 0 or ny == h - 1)
                            if is_on_border and neighbor in border_path_pixels and neighbor not in visited:
                                visited.add(neighbor)
                                stack.append(neighbor)
                    
                    if cluster: clusters.append(cluster)
            
            if len(clusters) < 2: return None, None
            
            # Find the center of each cluster
            def get_cluster_center(cluster):
                return (sum(p[0] for p in cluster) / len(cluster), 
                        sum(p[1] for p in cluster) / len(cluster))

            # Sort clusters by their average Y-coordinate
            centers_with_y = [(get_cluster_center(c), c) for c in clusters]
            centers_with_y.sort(key=lambda item: item[0][1])
            
            center_top = centers_with_y[0][0]
            center_bottom = centers_with_y[-1][0]
            
            # Move center 1 pixel inwards from the border
            def move_inward(x, y, w, h):
                x, y = int(x), int(y)
                if x == 0: return x + 1, y
                if x == w - 1: return x - 1, y
                if y == 0: return x, y + 1
                if y == h - 1: return x, y - 1
                return x, y

            # Assign START (Green) to the top-most opening, END (Blue) to the bottom-most opening
            initial_start = move_inward(center_top[0], center_top[1], w, h)
            initial_end = move_inward(center_bottom[0], center_bottom[1], w, h)
            
            # Use snap_to_white to guarantee the final point is on the path
            start = snap_to_white(image, initial_start[0], initial_start[1])
            end = snap_to_white(image, initial_end[0], initial_end[1])
            
            return start, end

        start, end = find_robust_start_end(thresh)

        if start is None or end is None:
            return None, "Error: Could not find two distinct entry/exit points on the border."

        print(f"Starts at (Green, Top-most Opening): {start}")
        print(f"Ends at (Blue, Bottom-most Opening): {end}")

        # --- 2. A* Pathfinding (4-Connectivity) ---
        
        open_set = [(heuristic(start, end), start)]
        came_from = {}
        g_score = {start: 0}
        
        found = False
        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == end:
                found = True
                break

            cx, cy = current
            
            # 4 neighbors: (dx, dy) and cost is always 1
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                neighbor = (nx, ny)

                # Check bounds and path (MUST be 255)
                if 0 <= nx < w and 0 <= ny < h and thresh[ny, nx] == 255:
                    tentative_g = g_score[current] + 1
                    
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f = tentative_g + heuristic(neighbor, end)
                        heapq.heappush(open_set, (f, neighbor))

        if not found: return None, "Path not found by A*."

        # --- 3. Reconstruct & Draw ---
        path = []
        curr = end
        while curr in came_from:
            path.append(curr)
            curr = came_from[curr]
        path.append(start)
        
        color_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
        # Draw path cleanly
        if len(path) > 1:
            pts = np.array(path, np.int32)
            pts = pts.reshape((-1, 1, 2))
            # Use LINE_AA for anti-aliased, smooth line
            cv2.polylines(color_img, [pts], False, (0, 0, 255), 2, cv2.LINE_AA)

        # Draw markers
        cv2.circle(color_img, start, 5, (0, 255, 0), -1) # Green Start
        cv2.circle(color_img, end, 5, (255, 0, 0), -1)   # Blue End
        
        return color_img, "Solved."

    except Exception as e:
        return None, str(e)

# --- Run ---
INPUT = 'maze_image.png' 
OUTPUT = 'maze_solved_final.png'

if os.path.exists(INPUT):
    res, msg = solve_maze_a_star_final(INPUT, OUTPUT)
    if res is not None:
        cv2.imwrite(OUTPUT, res)
        print(f"Success: {msg}. Saved to {OUTPUT}")
    else:
        print(f"Failed: {msg}")
else:
    print(f"Error: {INPUT} not found.")
