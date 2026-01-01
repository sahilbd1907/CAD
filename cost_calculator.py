from typing import Dict
import math

class CostCalculator:
    def __init__(self):
        # Material costs per cubic mm in INR (approx for Pune market)
        self.material_costs = {
            'steel': 0.0065,      # ₹6.5 per cm³
            'aluminum': 0.0200,   # ₹20 per cm³
            'plastic': 0.0030,    # ₹3 per cm³
            'wood': 0.0015,       # ₹1.5 per cm³
            'brass': 0.0600,      # ₹60 per cm³
            'copper': 0.0750      # ₹75 per cm³
        }
        
        # Machine hourly rates in INR (laser/waterjet equivalents, Pune)
        self.machine_rates = {
            'steel': 1800.0,
            'aluminum': 1600.0,
            'plastic': 1200.0,
            'wood': 900.0,
            'brass': 1700.0,
            'copper': 1800.0
        }
        
        # Material-specific feed rates (mm/min)
        self.feed_rates = {
            'steel': 300,
            'aluminum': 600,
            'plastic': 800,
            'wood': 1200,
            'brass': 400,
            'copper': 350
        }
        
        # Setup time in minutes
        self.setup_time = 10.0
        
        # Tool change time in minutes
        self.tool_change_time = 3.0
        
        # Safety factor for time estimation
        self.time_safety_factor = 1.15
    
    def calculate_machining_time(self, cutting_length: float, material: str, thickness: float) -> float:
        """
        Calculate machining time in minutes
        
        Args:
            cutting_length: Total cutting length in mm
            material: Material type
            thickness: Material thickness in mm
        """
        material = material.lower()
        
        # Get feed rate for material
        feed_rate = self.feed_rates.get(material, 300)
        
        # Calculate cutting time
        cutting_time = cutting_length / feed_rate
        
        # Add setup and tool change time
        total_time = cutting_time + self.setup_time + self.tool_change_time
        
        # Apply safety factor
        total_time *= self.time_safety_factor
        
        return total_time
    
    def calculate_material_cost(self, cutting_length: float, thickness: float, material: str) -> float:
        """
        Calculate material cost
        
        Args:
            cutting_length: Total cutting length in mm
            thickness: Material thickness in mm
            material: Material type
        """
        material = material.lower()
        
        # Estimate material area (assuming 1mm kerf width)
        kerf_width = 1.0  # mm
        material_area = cutting_length * (thickness + kerf_width)
        
        # Convert to cm³
        material_volume_cm3 = material_area / 1000
        
        # Get material cost per cm³ in INR
        cost_per_cm3 = self.material_costs.get(material, 0.0065)
        
        return material_volume_cm3 * cost_per_cm3
    
    def calculate_labor_cost(self, machining_time: float, material: str) -> float:
        """
        Calculate labor cost based on machining time
        
        Args:
            machining_time: Machining time in minutes
            material: Material type
        """
        material = material.lower()
        
        # Convert minutes to hours
        hours = machining_time / 60.0
        
        # Get hourly rate for material in INR
        hourly_rate = self.machine_rates.get(material, 1500.0)
        
        return hours * hourly_rate
    
    def calculate_total_cost(self, machining_time: float, material: str, thickness: float, cutting_length: float) -> float:
        """
        Calculate total cost including material and labor
        
        Args:
            machining_time: Machining time in minutes
            material: Material type
            thickness: Material thickness in mm
            cutting_length: Total cutting length in mm
        """
        material_cost = self.calculate_material_cost(cutting_length, thickness, material)
        labor_cost = self.calculate_labor_cost(machining_time, material)
        
        total_cost = material_cost + labor_cost
        
        return total_cost
    
    def get_material_properties(self, material: str) -> Dict:
        """
        Get material properties for display
        """
        material = material.lower()
        
        return {
            'name': material.capitalize(),
            'feed_rate': self.feed_rates.get(material, 300),
            'material_cost_per_cm3': self.material_costs.get(material, 0.00008),
            'hourly_rate': self.machine_rates.get(material, 40.0)
        }
