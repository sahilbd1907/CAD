"""
Nesting Optimizer - Calculate optimal part arrangement on material sheets
"""

import math
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class NestingOptimizer:
    def __init__(self):
        self.standard_sheets = [
            {"name": "1000x2000mm", "width": 1000, "height": 2000, "area": 2000000, "cost_per_mm2": 0.0001},
            {"name": "1250x2500mm", "width": 1250, "height": 2500, "area": 3125000, "cost_per_mm2": 0.0001},
            {"name": "1500x3000mm", "width": 1500, "height": 3000, "area": 4500000, "cost_per_mm2": 0.0001},
            {"name": "2000x4000mm", "width": 2000, "height": 4000, "area": 8000000, "cost_per_mm2": 0.0001}
        ]
    
    def calculate_optimal_nesting(self, geometry_data: Dict, material: str, thickness: float) -> Dict:
        """
        Calculate optimal nesting arrangement
        
        Returns detailed nesting information with visual layout
        """
        bounding_box = geometry_data.get('bounding_box', {})
        part_width = bounding_box.get('width', 0)
        part_height = bounding_box.get('height', 0)
        part_area = bounding_box.get('area', 0)
        
        if part_width == 0 or part_height == 0:
            return {
                'success': False,
                'error': 'Invalid part dimensions'
            }
        
        # Calculate nesting for each standard sheet
        best_sheet = None
        best_utilization = 0
        best_arrangement = None
        
        results = []
        
        for sheet in self.standard_sheets:
            # Calculate how many parts fit (with spacing)
            spacing = 5  # 5mm spacing between parts
            parts_x = int((sheet['width'] - spacing) / (part_width + spacing))
            parts_y = int((sheet['height'] - spacing) / (part_height + spacing))
            total_parts = parts_x * parts_y
            
            if total_parts == 0:
                continue
            
            # Calculate utilization
            used_area = total_parts * part_area
            utilization = (used_area / sheet['area']) * 100
            
            # Calculate waste
            waste_area = sheet['area'] - used_area
            waste_percent = (waste_area / sheet['area']) * 100
            
            # Calculate cost savings
            material_cost_per_sheet = sheet['area'] * sheet['cost_per_mm2']
            cost_per_part = material_cost_per_sheet / total_parts if total_parts > 0 else 0
            savings_per_part = (material_cost_per_sheet / 1) - cost_per_part if total_parts > 1 else 0
            
            arrangement = {
                'sheet_name': sheet['name'],
                'sheet_width': sheet['width'],
                'sheet_height': sheet['height'],
                'parts_x': parts_x,
                'parts_y': parts_y,
                'total_parts': total_parts,
                'utilization': round(utilization, 2),
                'waste_percent': round(waste_percent, 2),
                'waste_area': round(waste_area, 2),
                'cost_per_part': round(cost_per_part, 4),
                'savings_per_part': round(savings_per_part, 4),
                'layout': self._generate_layout(parts_x, parts_y, part_width, part_height, spacing, sheet)
            }
            
            results.append(arrangement)
            
            if utilization > best_utilization:
                best_utilization = utilization
                best_sheet = sheet
                best_arrangement = arrangement
        
        if not best_arrangement:
            return {
                'success': False,
                'error': 'Part too large for standard sheets'
            }
        
        return {
            'success': True,
            'part_dimensions': {
                'width': round(part_width, 2),
                'height': round(part_height, 2),
                'area': round(part_area, 2)
            },
            'best_arrangement': best_arrangement,
            'all_arrangements': results,
            'recommendations': self._generate_nesting_recommendations(best_arrangement, part_width, part_height)
        }
    
    def _generate_layout(self, parts_x: int, parts_y: int, part_width: float, 
                        part_height: float, spacing: float, sheet: Dict) -> List[Dict]:
        """Generate visual layout coordinates"""
        layout = []
        start_x = spacing
        start_y = spacing
        
        for y in range(parts_y):
            for x in range(parts_x):
                layout.append({
                    'x': round(start_x + x * (part_width + spacing), 2),
                    'y': round(start_y + y * (part_height + spacing), 2),
                    'width': part_width,
                    'height': part_height,
                    'part_number': len(layout) + 1
                })
        
        return layout
    
    def _generate_nesting_recommendations(self, arrangement: Dict, 
                                         part_width: float, part_height: float) -> List[str]:
        """Generate nesting recommendations"""
        recommendations = []
        
        if arrangement['utilization'] < 50:
            recommendations.append("Consider rotating parts 90° for better fit")
        
        if arrangement['waste_percent'] > 30:
            recommendations.append("High waste percentage - consider custom sheet size")
        
        if arrangement['total_parts'] > 10:
            recommendations.append("Good for batch production - significant cost savings per part")
        
        # Check if rotation would help
        rotated_parts_x = int((arrangement['sheet_width'] - 5) / (part_height + 5))
        rotated_parts_y = int((arrangement['sheet_height'] - 5) / (part_width + 5))
        rotated_total = rotated_parts_x * rotated_parts_y
        
        if rotated_total > arrangement['total_parts']:
            recommendations.append(f"Rotating parts 90° would fit {rotated_total} parts (vs {arrangement['total_parts']} current)")
        
        return recommendations

