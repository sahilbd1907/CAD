#!/usr/bin/env python3
"""
Utility script to create a simple test DXF file for testing the CNC quotation generator.
This creates a basic geometric shape with lines, arcs, and circles.
"""

import ezdxf

def create_test_dxf():
    """Create a simple test DXF file with basic geometry"""
    
    # Create a new DXF document
    doc = ezdxf.new('R2010')  # AutoCAD 2010 format
    msp = doc.modelspace()
    
    # Add a rectangle (4 lines)
    points = [
        (0, 0),      # Bottom-left
        (100, 0),    # Bottom-right
        (100, 50),   # Top-right
        (0, 50),     # Top-left
        (0, 0)       # Back to start
    ]
    
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        msp.add_line(start, end)
    
    # Add a circle in the center
    center = (50, 25)
    radius = 15
    msp.add_circle(center, radius)
    
    # Add an arc
    arc_center = (25, 25)
    arc_radius = 10
    msp.add_arc(arc_center, arc_radius, start_angle=0, end_angle=180)
    
    # Add a polyline (triangle)
    triangle_points = [
        (75, 10),
        (90, 40),
        (60, 40),
        (75, 10)
    ]
    msp.add_lwpolyline(triangle_points)
    
    # Save the DXF file
    filename = 'test_geometry.dxf'
    doc.saveas(filename)
    print(f"Test DXF file created: {filename}")
    print("This file contains:")
    print("- 4 lines (rectangle)")
    print("- 1 circle")
    print("- 1 arc")
    print("- 1 polyline (triangle)")
    print(f"Total entities: {len(msp)}")
    
    return filename

if __name__ == '__main__':
    create_test_dxf()
