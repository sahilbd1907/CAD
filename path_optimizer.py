"""
Path Optimizer - TSP-based cutting path optimization
"""

import math
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class PathOptimizer:
    def __init__(self):
        self.logger = logger
    
    def calculate_tsp_path(self, geometry_data: Dict) -> Dict:
        """
        Calculate optimized cutting path using TSP (Traveling Salesman Problem) algorithm
        
        Returns detailed path optimization information
        """
        entities = geometry_data.get('entities', [])
        
        # Extract cutting points (start/end points of entities)
        points = []
        entity_map = {}
        
        for i, entity in enumerate(entities):
            try:
                if entity.get('type') == 'LINE' and 'start' in entity and 'end' in entity:
                    start = entity['start']
                    end = entity['end']
                    # Handle different start/end formats
                    start_x = start[0] if isinstance(start, (list, tuple)) else (start.x if hasattr(start, 'x') else 0)
                    start_y = start[1] if isinstance(start, (list, tuple)) else (start.y if hasattr(start, 'y') else 0)
                    end_x = end[0] if isinstance(end, (list, tuple)) else (end.x if hasattr(end, 'x') else 0)
                    end_y = end[1] if isinstance(end, (list, tuple)) else (end.y if hasattr(end, 'y') else 0)
                    
                    points.append({
                        'id': i,
                        'x': float(start_x),
                        'y': float(start_y),
                        'type': 'start',
                        'entity_id': i
                    })
                    points.append({
                        'id': i + len(entities),
                        'x': float(end_x),
                        'y': float(end_y),
                        'type': 'end',
                        'entity_id': i
                    })
                    entity_map[i] = entity
                elif entity.get('type') == 'CIRCLE' and 'center' in entity:
                    center = entity['center']
                    center_x = center[0] if isinstance(center, (list, tuple)) else (center.x if hasattr(center, 'x') else 0)
                    center_y = center[1] if isinstance(center, (list, tuple)) else (center.y if hasattr(center, 'y') else 0)
                    points.append({
                        'id': i,
                        'x': float(center_x),
                        'y': float(center_y),
                        'type': 'circle',
                        'entity_id': i,
                        'radius': float(entity.get('radius', 0))
                    })
                    entity_map[i] = entity
            except (KeyError, TypeError, AttributeError) as e:
                # Skip entities that can't be processed
                continue
        
        if len(points) < 2:
            return {
                'success': False,
                'error': 'Not enough points for path optimization'
            }
        
        # Calculate original path distance
        original_distance = self._calculate_original_distance(entities)
        
        # Apply Nearest Neighbor TSP algorithm
        optimized_path = self._nearest_neighbor_tsp(points)
        
        # Calculate optimized distance
        optimized_distance = self._calculate_path_distance(optimized_path)
        
        # Calculate savings
        savings_percent = ((original_distance - optimized_distance) / original_distance * 100) if original_distance > 0 else 0
        savings_distance = original_distance - optimized_distance
        
        # Build detailed path information
        path_details = []
        for i, point in enumerate(optimized_path):
            entity = entity_map.get(point['entity_id'], {})
            path_details.append({
                'step': i + 1,
                'x': round(point['x'], 2),
                'y': round(point['y'], 2),
                'entity_type': entity.get('type', 'UNKNOWN'),
                'entity_id': point['entity_id'],
                'point_type': point.get('type', 'point')
            })
        
        return {
            'success': True,
            'original_distance': round(original_distance, 2),
            'optimized_distance': round(optimized_distance, 2),
            'savings_distance': round(savings_distance, 2),
            'savings_percent': round(savings_percent, 2),
            'total_points': len(points),
            'path_steps': len(optimized_path),
            'path_details': path_details,
            'optimized_path': optimized_path,
            'algorithm': 'Nearest Neighbor TSP',
            'time_savings_estimate': f"{savings_percent:.1f}% reduction in travel time"
        }
    
    def _calculate_original_distance(self, entities: List[Dict]) -> float:
        """Calculate total distance of original entity order"""
        total = 0.0
        last_point = None
        
        for entity in entities:
            if entity['type'] == 'LINE' and 'start' in entity and 'end' in entity:
                start = entity['start']
                end = entity['end']
                start_pt = (start[0] if isinstance(start, (list, tuple)) else start.x,
                           start[1] if isinstance(start, (list, tuple)) else start.y)
                end_pt = (end[0] if isinstance(end, (list, tuple)) else end.x,
                         end[1] if isinstance(end, (list, tuple)) else end.y)
                
                if last_point:
                    total += self._distance(last_point, start_pt)
                total += self._distance(start_pt, end_pt)
                last_point = end_pt
            elif entity['type'] == 'CIRCLE' and 'center' in entity:
                center = entity['center']
                center_pt = (center[0] if isinstance(center, (list, tuple)) else center.x,
                           center[1] if isinstance(center, (list, tuple)) else center.y)
                if last_point:
                    total += self._distance(last_point, center_pt)
                last_point = center_pt
        
        return total
    
    def _nearest_neighbor_tsp(self, points: List[Dict]) -> List[Dict]:
        """Nearest Neighbor TSP algorithm"""
        if len(points) < 2:
            return points
        
        # Start with first point
        unvisited = points[1:]
        path = [points[0]]
        current = points[0]
        
        while unvisited:
            nearest_idx = 0
            min_dist = float('inf')
            
            for i, point in enumerate(unvisited):
                dist = self._distance(
                    (current['x'], current['y']),
                    (point['x'], point['y'])
                )
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = i
            
            current = unvisited.pop(nearest_idx)
            path.append(current)
        
        return path
    
    def _calculate_path_distance(self, path: List[Dict]) -> float:
        """Calculate total distance of a path"""
        total = 0.0
        for i in range(len(path) - 1):
            total += self._distance(
                (path[i]['x'], path[i]['y']),
                (path[i+1]['x'], path[i+1]['y'])
            )
        return total
    
    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx*dx + dy*dy)
    
    def _improve_path_2opt(self, path: List[Dict]) -> List[Dict]:
        """2-opt improvement for TSP path"""
        improved = True
        best_path = path[:]
        best_distance = self._calculate_path_distance(path)
        
        while improved:
            improved = False
            for i in range(1, len(best_path) - 2):
                for j in range(i + 1, len(best_path)):
                    if j - i == 1:
                        continue
                    
                    # Try reversing segment
                    new_path = best_path[:i] + best_path[i:j+1][::-1] + best_path[j+1:]
                    new_distance = self._calculate_path_distance(new_path)
                    
                    if new_distance < best_distance:
                        best_path = new_path
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
        
        return best_path

