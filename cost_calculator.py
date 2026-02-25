from typing import Dict
import math

class CostCalculator:
    def __init__(self):
        # Material costs per cubic mm in INR (updated for 2024-2025 Indian market)
        # Based on average material costs in Pune/Mumbai market
        self.material_costs = {
            'steel': 0.41,      # Rs. 410 per cm³ (mild steel sheets)
            'aluminum': 0.35,   # Rs. 350 per cm³ (aluminum sheets)
            'plastic': 0.004,    # Rs. 4 per cm³ (acrylic/plastic sheets)
            'wood': 0.020,       # Rs. 20 per cm³ (plywood/MDF)
            'brass': 0.6,      # Rs. 600 per cm³ (brass sheets)
            'copper': 0.6      # Rs. 600 per cm³ (copper sheets)
        }
        
        # Machine hourly rates in INR (time-based costing as per Indian standards)
        # Based on research: Laser cutting service rates in India range Rs. 300-500/hour
        # Operational cost base: Rs. 230/hour + 50% markup = Rs. 345/hour average
        # Material-specific adjustments applied
        self.machine_rates = {
            'steel': 4000.0,       # Rs. 4000/hour (most common, optimized for steel)
            'aluminum': 4000.0,    # Rs. 4000/hour (faster cutting, slightly lower)
            'plastic': 4000.0,     # Rs. 4000/hour (faster, lower operational cost)
            'wood': 4000.0,        # Rs. 4000/hour (fastest, lowest operational cost)
            'brass': 4000.0,       # Rs. 4000/hour (harder material, higher cost)
            'copper': 4000.0       # Rs. 4000/hour (highly reflective, requires more power)
        }
        
        # Water jet cutting rates (when applicable)
        # Operational cost base: Rs. 333/hour + 50% markup = Rs. 500/hour average
        self.waterjet_rates = {
            'steel': 4000.0,
            'aluminum': 400.0,
            'plastic': 4000.0,
            'wood': 4000.0,
            'brass': 4000.0,
            'copper': 4000.0
        }
        
        # Material-specific feed rates (mm/min) - Laser cutting speeds
        # Updated based on typical fiber laser cutting speeds in India
        self.feed_rates = {
            'steel': 400,         # 1-3mm steel: 250-400 mm/min
            'aluminum': 600,      # 1-3mm aluminum: 500-800 mm/min
            'plastic': 900,       # Acrylic/PVC: 700-1000 mm/min
            'wood': 1200,         # Plywood/MDF: 1000-1500 mm/min
            'brass': 350,         # 1-3mm brass: 300-500 mm/min
            'copper': 300         # 1-3mm copper: 250-400 mm/min (slower due to reflectivity)
        }
        
        # Setup time in minutes (laser cutting setup: file loading, material positioning, calibration)
        self.setup_time = 8.0     # Reduced from 10 as laser setup is faster than CNC
        
        # Tool change time in minutes (not applicable for laser, but kept for compatibility)
        # For laser: this represents material changeover time
        self.tool_change_time = 5.0
        
        # Safety factor for time estimation
        self.time_safety_factor = 5.0
    
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
        cost_per_cm3 = self.material_costs.get(material, 0.0080)
        
        return material_volume_cm3 * cost_per_cm3
    
    def calculate_labor_cost(self, machining_time: float, material: str, use_waterjet: bool = False) -> float:
        """
        Calculate labor cost based on machining time (time-based costing as per Indian standards)
        
        Args:
            machining_time: Machining time in minutes
            material: Material type
            use_waterjet: If True, use waterjet rates instead of laser rates
        """
        material = material.lower()
        
        # Convert minutes to hours
        hours = machining_time / 60.0
        
        # Get hourly rate for material in INR
        if use_waterjet:
            hourly_rate = self.waterjet_rates.get(material, 500.0)
        else:
            hourly_rate = self.machine_rates.get(material, 400.0)
        
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
            'material_cost_per_cm3': self.material_costs.get(material, 0.0080),
            'hourly_rate': self.machine_rates.get(material, 400.0)
        }
