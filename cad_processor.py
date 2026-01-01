import ezdxf
import math
from typing import Dict, List, Tuple
import logging

class CADProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Material-specific cutting parameters (mm/min)
        self.material_feed_rates = {
            'steel': 300,
            'aluminum': 600,
            'plastic': 800,
            'wood': 1200,
            'brass': 400,
            'copper': 350
        }
    
    def process_dxf(self, filepath: str) -> Dict:
        """
        Process DXF file and extract comprehensive geometry information
        """
        try:
            doc = ezdxf.readfile(filepath)
            msp = doc.modelspace()
            
            geometry_data = {
                'total_length': 0.0,
                'line_count': 0,
                'arc_count': 0,
                'circle_count': 0,
                'polyline_count': 0,
                'spline_count': 0,
                'ellipse_count': 0,
                'text_count': 0,
                'block_ref_count': 0,
                'layer_stats': {},
                'entities': [],
                'bounding_box': {'min_x': float('inf'), 'min_y': float('inf'), 
                                'max_x': float('-inf'), 'max_y': float('-inf')},
                'entity_lengths': {'lines': [], 'arcs': [], 'circles': [], 'polylines': [], 
                                 'splines': [], 'ellipses': []},
                'complexity_metrics': {},
                'file_info': {}
            }
            
            all_points = []
            
            # Process different entity types
            for entity in msp:
                layer_name = getattr(entity.dxf, 'layer', '0')
                geometry_data['layer_stats'].setdefault(layer_name, {'count': 0, 'length': 0.0})
                geometry_data['layer_stats'][layer_name]['count'] += 1
                
                if entity.dxftype() == 'LINE':
                    length = self._calculate_line_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['line_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['lines'].append(length)
                    all_points.extend([(entity.dxf.start.x, entity.dxf.start.y), 
                                      (entity.dxf.end.x, entity.dxf.end.y)])
                    geometry_data['entities'].append({
                        'type': 'LINE',
                        'length': length,
                        'start': (round(entity.dxf.start.x, 2), round(entity.dxf.start.y, 2)),
                        'end': (round(entity.dxf.end.x, 2), round(entity.dxf.end.y, 2)),
                        'layer': layer_name
                    })
                
                elif entity.dxftype() == 'ARC':
                    length = self._calculate_arc_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['arc_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['arcs'].append(length)
                    center = (entity.dxf.center.x, entity.dxf.center.y)
                    all_points.append(center)
                    geometry_data['entities'].append({
                        'type': 'ARC',
                        'length': round(length, 2),
                        'center': (round(center[0], 2), round(center[1], 2)),
                        'radius': round(entity.dxf.radius, 2),
                        'start_angle': round(entity.dxf.start_angle, 2),
                        'end_angle': round(entity.dxf.end_angle, 2),
                        'layer': layer_name
                    })
                
                elif entity.dxftype() == 'CIRCLE':
                    length = self._calculate_circle_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['circle_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['circles'].append(length)
                    center = (entity.dxf.center.x, entity.dxf.center.y)
                    all_points.append(center)
                    geometry_data['entities'].append({
                        'type': 'CIRCLE',
                        'length': round(length, 2),
                        'center': (round(center[0], 2), round(center[1], 2)),
                        'radius': round(entity.dxf.radius, 2),
                        'area': round(math.pi * entity.dxf.radius ** 2, 2),
                        'layer': layer_name
                    })
                
                elif entity.dxftype() == 'LWPOLYLINE':
                    length = self._calculate_polyline_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['polyline_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['polylines'].append(length)
                    points = list(entity.get_points())
                    all_points.extend([(p[0], p[1]) for p in points if len(p) >= 2])
                    geometry_data['entities'].append({
                        'type': 'LWPOLYLINE',
                        'length': round(length, 2),
                        'point_count': len(points),
                        'is_closed': entity.closed if hasattr(entity, 'closed') else False,
                        'layer': layer_name
                    })
                
                elif entity.dxftype() == 'POLYLINE':
                    length = self._calculate_polyline_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['polyline_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['polylines'].append(length)
                    points = list(entity.points)
                    all_points.extend([(p[0], p[1]) for p in points if len(p) >= 2])
                    geometry_data['entities'].append({
                        'type': 'POLYLINE',
                        'length': round(length, 2),
                        'point_count': len(points),
                        'is_closed': entity.is_closed if hasattr(entity, 'is_closed') else False,
                        'layer': layer_name
                    })

                elif entity.dxftype() == 'SPLINE':
                    length = self._approximate_spline_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['spline_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['splines'].append(length)
                    geometry_data['entities'].append({
                        'type': 'SPLINE',
                        'length': round(length, 2),
                        'degree': getattr(entity.dxf, 'degree', None),
                        'layer': layer_name
                    })

                elif entity.dxftype() == 'ELLIPSE':
                    length = self._approximate_ellipse_length(entity)
                    geometry_data['total_length'] += length
                    geometry_data['ellipse_count'] += 1
                    geometry_data['layer_stats'][layer_name]['length'] += length
                    geometry_data['entity_lengths']['ellipses'].append(length)
                    center = (entity.dxf.center.x, entity.dxf.center.y)
                    all_points.append(center)
                    geometry_data['entities'].append({
                        'type': 'ELLIPSE',
                        'length': round(length, 2),
                        'center': (round(center[0], 2), round(center[1], 2)),
                        'major_axis': round(entity.dxf.major_axis.magnitude, 2),
                        'ratio': round(entity.dxf.ratio, 4),
                        'layer': layer_name
                    })

                elif entity.dxftype() in ('TEXT', 'MTEXT'):
                    geometry_data['text_count'] += 1
                    text_value = getattr(entity.dxf, 'text', None) or getattr(entity, 'text', '')
                    insert = getattr(entity.dxf, 'insert', None)
                    if insert:
                        all_points.append((insert.x, insert.y))
                    geometry_data['entities'].append({
                        'type': entity.dxftype(),
                        'text': text_value[:50],  # Limit text length
                        'insert': (round(insert.x, 2), round(insert.y, 2)) if insert else None,
                        'layer': layer_name
                    })

                elif entity.dxftype() == 'INSERT':
                    geometry_data['block_ref_count'] += 1
                    insert = (entity.dxf.insert.x, entity.dxf.insert.y)
                    all_points.append(insert)
                    geometry_data['entities'].append({
                        'type': 'BLOCK_REFERENCE',
                        'name': entity.dxf.name,
                        'insert': (round(insert[0], 2), round(insert[1], 2)),
                        'layer': layer_name
                    })
            
            # Calculate bounding box
            if all_points:
                x_coords = [p[0] for p in all_points]
                y_coords = [p[1] for p in all_points]
                geometry_data['bounding_box'] = {
                    'min_x': round(min(x_coords), 2),
                    'min_y': round(min(y_coords), 2),
                    'max_x': round(max(x_coords), 2),
                    'max_y': round(max(y_coords), 2),
                    'width': round(max(x_coords) - min(x_coords), 2),
                    'height': round(max(y_coords) - min(y_coords), 2),
                    'area': round((max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords)), 2)
                }
            
            # Calculate complexity metrics
            total_entities = sum([
                geometry_data['line_count'], geometry_data['arc_count'], 
                geometry_data['circle_count'], geometry_data['polyline_count'],
                geometry_data['spline_count'], geometry_data['ellipse_count']
            ])
            
            geometry_data['complexity_metrics'] = {
                'total_entities': total_entities,
                'entity_density': round(total_entities / max(geometry_data['bounding_box']['area'], 1), 4) if geometry_data['bounding_box']['area'] > 0 else 0,
                'avg_line_length': round(sum(geometry_data['entity_lengths']['lines']) / len(geometry_data['entity_lengths']['lines']), 2) if geometry_data['entity_lengths']['lines'] else 0,
                'avg_arc_length': round(sum(geometry_data['entity_lengths']['arcs']) / len(geometry_data['entity_lengths']['arcs']), 2) if geometry_data['entity_lengths']['arcs'] else 0,
                'avg_circle_radius': round(sum([2*math.pi*r for r in [e.get('radius', 0) for e in geometry_data['entities'] if e['type'] == 'CIRCLE']]) / max(geometry_data['circle_count'], 1), 2) if geometry_data['circle_count'] > 0 else 0,
                'max_line_length': round(max(geometry_data['entity_lengths']['lines']), 2) if geometry_data['entity_lengths']['lines'] else 0,
                'min_line_length': round(min(geometry_data['entity_lengths']['lines']), 2) if geometry_data['entity_lengths']['lines'] else 0,
                'layer_count': len(geometry_data['layer_stats']),
                'complexity_score': self._calculate_complexity_score(geometry_data)
            }
            
            # File information
            geometry_data['file_info'] = {
                'dxf_version': doc.dxfversion if hasattr(doc, 'dxfversion') else 'Unknown',
                'units': doc.units if hasattr(doc, 'units') else 'mm',
                'total_layers': len(geometry_data['layer_stats'])
            }
            
            # Round total length
            geometry_data['total_length'] = round(geometry_data['total_length'], 2)
            
            return geometry_data
            
        except Exception as e:
            self.logger.error(f"Error processing DXF file: {str(e)}")
            raise Exception(f"Failed to process DXF file: {str(e)}")
    
    def _calculate_line_length(self, line) -> float:
        """Calculate length of a line entity"""
        dx = line.dxf.end.x - line.dxf.start.x
        dy = line.dxf.end.y - line.dxf.start.y
        return math.sqrt(dx*dx + dy*dy)
    
    def _calculate_arc_length(self, arc) -> float:
        """Calculate arc length"""
        radius = arc.dxf.radius
        start_angle = math.radians(arc.dxf.start_angle)
        end_angle = math.radians(arc.dxf.end_angle)
        
        # Normalize angles
        if end_angle < start_angle:
            end_angle += 2 * math.pi
        
        angle_diff = end_angle - start_angle
        return radius * angle_diff
    
    def _calculate_circle_length(self, circle) -> float:
        """Calculate circle circumference"""
        return 2 * math.pi * circle.dxf.radius
    
    def _calculate_polyline_length(self, polyline) -> float:
        """Calculate polyline length"""
        total_length = 0.0
        points = list(polyline.get_points()) if hasattr(polyline, 'get_points') else list(polyline.points)
        
        for i in range(len(points) - 1):
            if len(points[i]) >= 2 and len(points[i+1]) >= 2:
                dx = points[i+1][0] - points[i][0]
                dy = points[i+1][1] - points[i][1]
                total_length += math.sqrt(dx*dx + dy*dy)
        
        return total_length

    def _approximate_spline_length(self, spline) -> float:
        """Approximate spline length by sampling points."""
        try:
            points = [spline.point(i/50.0) for i in range(51)]
        except Exception:
            return 0.0
        total_length = 0.0
        for i in range(len(points) - 1):
            dx = points[i+1][0] - points[i][0]
            dy = points[i+1][1] - points[i][1]
            total_length += math.sqrt(dx*dx + dy*dy)
        return total_length

    def _approximate_ellipse_length(self, ellipse) -> float:
        """Approximate ellipse circumference using Ramanujan's formula."""
        try:
            a = ellipse.dxf.major_axis.magnitude / 2.0
            b = a * ellipse.dxf.ratio
            h = ((a - b) ** 2) / ((a + b) ** 2)
            return math.pi * (a + b) * (1 + (3*h)/(10 + math.sqrt(4 - 3*h)))
        except Exception:
            return 0.0
    
    def get_material_feed_rate(self, material: str) -> float:
        """Get feed rate for a specific material"""
        return self.material_feed_rates.get(material.lower(), 300)  # Default to steel rate
    
    def _calculate_complexity_score(self, geometry_data: Dict) -> float:
        """Calculate a complexity score (0-100) based on various factors"""
        score = 0.0
        
        # Calculate total entities directly
        total_entities = sum([
            geometry_data.get('line_count', 0),
            geometry_data.get('arc_count', 0),
            geometry_data.get('circle_count', 0),
            geometry_data.get('polyline_count', 0),
            geometry_data.get('spline_count', 0),
            geometry_data.get('ellipse_count', 0)
        ])
        
        # Entity count factor (max 30 points)
        score += min(30, total_entities / 10)
        
        # Entity diversity factor (max 20 points)
        entity_types = sum([
            1 if geometry_data.get('line_count', 0) > 0 else 0,
            1 if geometry_data.get('arc_count', 0) > 0 else 0,
            1 if geometry_data.get('circle_count', 0) > 0 else 0,
            1 if geometry_data.get('polyline_count', 0) > 0 else 0,
            1 if geometry_data.get('spline_count', 0) > 0 else 0,
            1 if geometry_data.get('ellipse_count', 0) > 0 else 0
        ])
        score += entity_types * 3.33
        
        # Layer complexity (max 15 points)
        layer_count = len(geometry_data.get('layer_stats', {}))
        score += min(15, layer_count * 2)
        
        # Spline and curve complexity (max 15 points)
        if geometry_data.get('spline_count', 0) > 0:
            score += min(15, geometry_data['spline_count'] / 2)
        
        # Size factor (max 10 points)
        bounding_box = geometry_data.get('bounding_box', {})
        if bounding_box.get('area', 0) > 0:
            area = bounding_box['area']
            if area > 1000000:  # Large drawings
                score += 10
            elif area > 100000:
                score += 7
            elif area > 10000:
                score += 5
            else:
                score += 2
        
        # Density factor (max 10 points)
        # Calculate density directly
        area = bounding_box.get('area', 0)
        if area > 0:
            density = total_entities / area
            if density > 1:
                score += min(10, density * 2)
        
        return round(min(100, score), 1)
