"""
AI Advisor Module for Material and Design Recommendations
Uses LLM to provide intelligent recommendations for optimized production
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import logging
from cost_calculator import CostCalculator

# Try to load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars

logger = logging.getLogger(__name__)

class AIAdvisor:
    def __init__(self):
        self.cost_calculator = CostCalculator()
        
        # Read .env file first
        env_vars = {}
        try:
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8-sig') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            logger.warning(f"Could not read .env file: {e}")
        
        # Check if using OpenRouter (preferred for free models)
        use_openrouter_str = env_vars.get('USE_OPENROUTER', os.getenv('USE_OPENROUTER', 'false'))
        self.use_openrouter = use_openrouter_str.lower() == 'true'
        
        if self.use_openrouter:
            # OpenRouter configuration
            self.api_key = env_vars.get('OPENROUTER_API_KEY', os.getenv('OPENROUTER_API_KEY', ''))
            self.api_base = 'https://openrouter.ai/api/v1'
            self.model = env_vars.get('OPENROUTER_MODEL', os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.1-8b-instruct:free'))
            self.provider = 'openrouter'
        else:
            # OpenAI configuration (default)
            self.api_key = env_vars.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
            self.api_base = None  # Uses default OpenAI endpoint
            self.model = env_vars.get('OPENAI_MODEL', os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'))
            self.provider = 'openai'
        
        # Filter out placeholder keys
        if self.api_key and ('your-' in self.api_key.lower() or 'placeholder' in self.api_key.lower() or len(self.api_key) < 20):
            self.api_key = ''
            logger.warning("Invalid or placeholder API key detected, using rule-based recommendations")
        
        self.use_ai = bool(self.api_key) and len(self.api_key) > 20
        
        if self.use_ai:
            logger.info(f"AI Advisor initialized with {self.provider.upper()}, model: {self.model}")
        else:
            logger.info("AI Advisor initialized in rule-based mode (no API key)")
        
        # Available materials for recommendations
        self.available_materials = ['steel', 'aluminum', 'plastic', 'wood', 'brass', 'copper']
        
        if not self.use_ai:
            logger.warning("API key not found. AI recommendations will use rule-based fallback.")
    
    def get_recommendations(self, geometry_data: Dict, material: str, 
                          thickness: float, machining_time: float, 
                          total_cost: float) -> Dict:
        """
        Get comprehensive AI recommendations for material and design optimization
        
        Returns:
            Dict with material_recommendations, design_suggestions, and cost_analysis
        """
        try:
            if self.use_ai:
                return self._get_llm_recommendations(
                    geometry_data, material, thickness, machining_time, total_cost
                )
            else:
                return self._get_rule_based_recommendations(
                    geometry_data, material, thickness, machining_time, total_cost
                )
        except Exception as e:
            logger.error(f"Error getting AI recommendations: {str(e)}")
            return self._get_rule_based_recommendations(
                geometry_data, material, thickness, machining_time, total_cost
            )
    
    def get_comprehensive_ai_analysis(self, geometry_data: Dict, material: str,
                                     thickness: float, machining_time: float,
                                     total_cost: float) -> Dict:
        """
        Get comprehensive AI analysis including:
        - Material recommendations
        - Design optimization
        - Path optimization suggestions
        - Nesting optimization
        - Cost analysis
        - Manufacturing insights
        """
        base_recommendations = self.get_recommendations(
            geometry_data, material, thickness, machining_time, total_cost
        )
        
        # Add path optimization analysis
        try:
            path_analysis = self._analyze_path_optimization(geometry_data, material, machining_time)
            logger.info(f"Path optimization analysis completed: {len(path_analysis.get('optimization_strategies', []))} strategies")
        except Exception as e:
            logger.error(f"Error in path optimization: {e}")
            path_analysis = {
                "optimization_strategies": [{
                    "strategy": "Basic Path Optimization",
                    "description": "Optimize cutting sequence to minimize travel distance",
                    "time_savings": "5-10%",
                    "implementation": "Use nearest-neighbor algorithm"
                }],
                "estimated_savings": "5-10% time reduction",
                "priority_actions": ["Optimize cutting sequence"]
            }
        
        # Add nesting optimization analysis
        try:
            nesting_analysis = self._analyze_nesting_optimization(geometry_data, material, thickness)
        except Exception as e:
            logger.error(f"Error in nesting optimization: {e}")
            nesting_analysis = {}
        
        # Add manufacturing insights
        try:
            manufacturing_insights = self._get_manufacturing_insights(
                geometry_data, material, thickness, machining_time
            )
        except Exception as e:
            logger.error(f"Error in manufacturing insights: {e}")
            manufacturing_insights = {}
        
        return {
            **base_recommendations,
            'path_optimization': path_analysis,
            'nesting_optimization': nesting_analysis,
            'manufacturing_insights': manufacturing_insights
        }
    
    def _analyze_path_optimization(self, geometry_data: Dict, material: str,
                                  machining_time: float) -> Dict:
        """Analyze and suggest path optimization strategies"""
        if self.use_ai:
            return self._get_llm_path_analysis(geometry_data, material, machining_time)
        else:
            return self._get_rule_based_path_analysis(geometry_data, material, machining_time)
    
    def _analyze_nesting_optimization(self, geometry_data: Dict, material: str,
                                     thickness: float) -> Dict:
        """Analyze and suggest nesting optimization strategies"""
        if self.use_ai:
            return self._get_llm_nesting_analysis(geometry_data, material, thickness)
        else:
            return self._get_rule_based_nesting_analysis(geometry_data, material, thickness)
    
    def _get_manufacturing_insights(self, geometry_data: Dict, material: str,
                                   thickness: float, machining_time: float) -> Dict:
        """Get manufacturing insights and best practices"""
        if self.use_ai:
            return self._get_llm_manufacturing_insights(geometry_data, material, thickness, machining_time)
        else:
            return self._get_rule_based_manufacturing_insights(geometry_data, material, thickness, machining_time)
    
    def _get_llm_recommendations(self, geometry_data: Dict, material: str,
                                thickness: float, machining_time: float,
                                total_cost: float) -> Dict:
        """Get recommendations using LLM (OpenAI or OpenRouter)"""
        try:
            import openai
            
            # Prepare context data
            complexity_score = geometry_data.get('complexity_metrics', {}).get('complexity_score', 0)
            total_length = geometry_data.get('total_length', 0)
            bounding_box = geometry_data.get('bounding_box', {})
            entity_counts = {
                'lines': geometry_data.get('line_count', 0),
                'arcs': geometry_data.get('arc_count', 0),
                'circles': geometry_data.get('circle_count', 0),
                'polylines': geometry_data.get('polyline_count', 0),
                'splines': geometry_data.get('spline_count', 0),
                'ellipses': geometry_data.get('ellipse_count', 0)
            }
            
            # Calculate alternative material costs
            alternatives = self._calculate_material_alternatives(
                total_length, thickness, machining_time, material
            )
            
            prompt = self._build_recommendation_prompt(
                material, thickness, total_cost, machining_time,
                complexity_score, total_length, bounding_box,
                entity_counts, alternatives
            )
            
            # Initialize client based on provider
            if self.use_openrouter:
                # OpenRouter requires headers to be set on the client
                from openai import OpenAI
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base,
                    default_headers={
                        "HTTP-Referer": "https://github.com/cnc-quotation",  # Optional
                        "X-Title": "CNC Quotation System"  # Optional
                    }
                )
            else:
                client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert CNC machining advisor specializing in material selection and design optimization for cost-effective production."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse LLM response
            return self._parse_llm_response(ai_response, alternatives)
            
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            return self._get_rule_based_recommendations(
                geometry_data, material, thickness, machining_time, total_cost
            )
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            return self._get_rule_based_recommendations(
                geometry_data, material, thickness, machining_time, total_cost
            )
    
    def _build_recommendation_prompt(self, material: str, thickness: float,
                                    total_cost: float, machining_time: float,
                                    complexity_score: float, total_length: float,
                                    bounding_box: Dict, entity_counts: Dict,
                                    alternatives: List[Dict]) -> str:
        """Build the prompt for LLM"""
        
        alternatives_text = "\n".join([
            f"- {alt['material'].capitalize()}: ₹{alt['total_cost']:.2f} "
            f"(Save ₹{alt['savings']:.2f}, {alt['time_change']:+.1f}% time)"
            for alt in alternatives[:3]
        ])
        
        prompt = f"""
Analyze this CNC machining quote and provide optimization recommendations:

CURRENT QUOTE:
- Material: {material.capitalize()}
- Thickness: {thickness} mm
- Total Cost: ₹{total_cost:.2f}
- Machining Time: {machining_time:.1f} minutes
- Cutting Length: {total_length:.2f} mm
- Complexity Score: {complexity_score}/100

GEOMETRY ANALYSIS:
- Bounding Box: {bounding_box.get('width', 0):.2f} x {bounding_box.get('height', 0):.2f} mm
- Entity Counts: {entity_counts['lines']} lines, {entity_counts['arcs']} arcs, {entity_counts['circles']} circles, {entity_counts['polylines']} polylines, {entity_counts['splines']} splines

ALTERNATIVE MATERIAL COSTS:
{alternatives_text}

Please provide:
1. MATERIAL RECOMMENDATIONS (2-3 alternatives with pros/cons):
   - Best cost-effective option
   - Best for strength/durability
   - Best for lightweight applications
   - Include cost savings and trade-offs

2. DESIGN OPTIMIZATION SUGGESTIONS:
   - Thickness optimization (if applicable)
   - Geometry improvements for faster machining
   - Feature modifications to reduce cost
   - Manufacturing considerations

3. COST BREAKDOWN ANALYSIS:
   - Main cost drivers
   - Opportunities for savings
   - Quick wins

Format your response as JSON with this structure:
{{
    "material_recommendations": [
        {{
            "material": "material_name",
            "reason": "why this material",
            "cost": cost_value,
            "savings": savings_amount,
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"],
            "best_for": "use case"
        }}
    ],
    "design_suggestions": [
        {{
            "suggestion": "what to change",
            "impact": "cost/time impact",
            "reason": "why this helps",
            "priority": "high/medium/low"
        }}
    ],
    "cost_analysis": {{
        "main_drivers": ["driver1", "driver2"],
        "quick_wins": ["win1", "win2"],
        "potential_savings": "estimated savings percentage"
    }}
}}
"""
        return prompt
    
    def _parse_llm_response(self, ai_response: str, alternatives: List[Dict]) -> Dict:
        """Parse LLM response and structure it"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                # Enhance with calculated alternatives
                parsed['calculated_alternatives'] = alternatives
                return parsed
            else:
                # Fallback: return text response
                return {
                    'raw_response': ai_response,
                    'calculated_alternatives': alternatives,
                    'material_recommendations': [],
                    'design_suggestions': [],
                    'cost_analysis': {}
                }
        except json.JSONDecodeError:
            logger.warning("Could not parse LLM JSON response, using fallback")
            return {
                'raw_response': ai_response,
                'calculated_alternatives': alternatives,
                'material_recommendations': [],
                'design_suggestions': [],
                'cost_analysis': {}
            }
    
    def _calculate_material_alternatives(self, cutting_length: float,
                                       thickness: float,
                                       current_machining_time: float,
                                       current_material: str = None) -> List[Dict]:
        """Calculate costs for alternative materials"""
        alternatives = []
        
        # Get current material feed rate for time calculation
        if current_material:
            current_feed_rate = self.cost_calculator.feed_rates.get(current_material.lower(), 300)
        else:
            current_feed_rate = 300
        
        for alt_material in self.available_materials:
            # Calculate new machining time
            alt_feed_rate = self.cost_calculator.feed_rates.get(alt_material, 300)
            current_feed_rate = 300  # Default, will be overridden
            
            # Estimate time change based on feed rate difference
            # Time is inversely proportional to feed rate
            if alt_feed_rate > 0:
                time_factor = current_feed_rate / alt_feed_rate
                alt_machining_time = current_machining_time * time_factor
            else:
                alt_machining_time = current_machining_time
            
            # Calculate costs
            alt_material_cost = self.cost_calculator.calculate_material_cost(
                cutting_length, thickness, alt_material
            )
            alt_labor_cost = self.cost_calculator.calculate_labor_cost(
                alt_machining_time, alt_material
            )
            alt_total_cost = alt_material_cost + alt_labor_cost
            
            time_change_pct = 0
            if current_machining_time > 0:
                time_change_pct = ((alt_machining_time - current_machining_time) / current_machining_time) * 100
            
            alternatives.append({
                'material': alt_material,
                'total_cost': alt_total_cost,
                'material_cost': alt_material_cost,
                'labor_cost': alt_labor_cost,
                'machining_time': alt_machining_time,
                'time_change': time_change_pct,
                'feed_rate': alt_feed_rate,
                'savings': 0  # Will be calculated below
            })
        
        # Calculate savings relative to current material
        if current_material and alternatives:
            current_alt = next((a for a in alternatives if a['material'] == current_material.lower()), None)
            if current_alt:
                baseline_cost = current_alt['total_cost']
                for alt in alternatives:
                    alt['savings'] = baseline_cost - alt['total_cost']
            else:
                # If current material not in alternatives, use first as baseline
                if alternatives:
                    baseline_cost = alternatives[0]['total_cost']
                    for alt in alternatives:
                        alt['savings'] = baseline_cost - alt['total_cost']
        
        # Sort by total cost
        alternatives.sort(key=lambda x: x['total_cost'])
        
        return alternatives
    
    def _get_rule_based_recommendations(self, geometry_data: Dict, material: str,
                                      thickness: float, machining_time: float,
                                      total_cost: float) -> Dict:
        """Fallback rule-based recommendations when LLM is not available"""
        
        cutting_length = geometry_data.get('total_length', 0)
        complexity_score = geometry_data.get('complexity_metrics', {}).get('complexity_score', 0)
        bounding_box = geometry_data.get('bounding_box', {})
        
        # Calculate alternatives
        alternatives = self._calculate_material_alternatives(
            cutting_length, thickness, machining_time, material
        )
        
        # Find best alternative
        current_material_lower = material.lower()
        current_alt = next((a for a in alternatives if a['material'] == current_material_lower), None)
        
        if current_alt:
            baseline_cost = current_alt['total_cost']
            for alt in alternatives:
                alt['savings'] = baseline_cost - alt['total_cost']
        
        # Material recommendations
        material_recommendations = []
        for alt in alternatives[:3]:
            if alt['material'] != current_material_lower:
                pros, cons, best_for = self._get_material_pros_cons(alt['material'])
                material_recommendations.append({
                    'material': alt['material'].capitalize(),
                    'reason': f"Could save ₹{alt['savings']:.2f} ({abs(alt['savings']/baseline_cost*100):.1f}%)",
                    'cost': alt['total_cost'],
                    'savings': alt['savings'],
                    'pros': pros,
                    'cons': cons,
                    'best_for': best_for,
                    'time_change': alt['time_change']
                })
        
        # Design suggestions
        design_suggestions = []
        
        # Thickness optimization
        if thickness > 2.0:
            design_suggestions.append({
                'suggestion': f"Consider reducing thickness from {thickness}mm to {thickness-0.5}mm",
                'impact': f"Could reduce material cost by ~15-20%",
                'reason': "Thinner material uses less material and may reduce machining time",
                'priority': 'medium'
            })
        
        # Complexity-based suggestions
        if complexity_score > 70:
            design_suggestions.append({
                'suggestion': "Simplify geometry by reducing splines and complex curves",
                'impact': "Could reduce machining time by 10-15%",
                'reason': "High complexity requires slower feed rates and more tool changes",
                'priority': 'high'
            })
        
        # Entity-based suggestions
        spline_count = geometry_data.get('spline_count', 0)
        if spline_count > 10:
            design_suggestions.append({
                'suggestion': "Convert splines to arcs where possible",
                'impact': "Could improve machining speed by 5-10%",
                'reason': "Arcs are faster to machine than splines",
                'priority': 'medium'
            })
        
        # Cost analysis
        material_cost = self.cost_calculator.calculate_material_cost(
            cutting_length, thickness, material
        )
        labor_cost = self.cost_calculator.calculate_labor_cost(machining_time, material)
        
        main_drivers = []
        if labor_cost > material_cost * 1.5:
            main_drivers.append("High machining time (labor cost is main driver)")
        if material_cost > labor_cost * 1.5:
            main_drivers.append("Expensive material (material cost is main driver)")
        if complexity_score > 70:
            main_drivers.append("High part complexity requiring slower machining")
        
        quick_wins = []
        if alternatives and alternatives[0]['savings'] > 0:
            best_alt = alternatives[0]
            quick_wins.append(f"Switch to {best_alt['material'].capitalize()} to save ₹{best_alt['savings']:.2f}")
        
        return {
            'material_recommendations': material_recommendations,
            'design_suggestions': design_suggestions,
            'cost_analysis': {
                'main_drivers': main_drivers,
                'quick_wins': quick_wins,
                'potential_savings': f"{abs(alternatives[0]['savings']/baseline_cost*100):.1f}%" if alternatives and alternatives[0]['savings'] > 0 else "0%"
            },
            'calculated_alternatives': alternatives
        }
    
    def _get_material_pros_cons(self, material: str) -> Tuple[List[str], List[str], str]:
        """Get pros and cons for a material"""
        material_lower = material.lower()
        
        material_info = {
            'steel': {
                'pros': ['High strength', 'Durable', 'Good for structural parts'],
                'cons': ['Heavier', 'Higher cost', 'Slower machining'],
                'best_for': 'Structural and high-strength applications'
            },
            'aluminum': {
                'pros': ['Lightweight', 'Good corrosion resistance', 'Faster machining', 'Lower cost'],
                'cons': ['Lower strength than steel', 'Softer material'],
                'best_for': 'Lightweight and corrosion-resistant applications'
            },
            'plastic': {
                'pros': ['Very low cost', 'Lightweight', 'Fast machining', 'Good for prototypes'],
                'cons': ['Lower strength', 'Not suitable for high loads', 'Temperature sensitive'],
                'best_for': 'Prototypes and low-stress applications'
            },
            'wood': {
                'pros': ['Lowest cost', 'Very fast machining', 'Natural material'],
                'cons': ['Low strength', 'Moisture sensitive', 'Not for precision parts'],
                'best_for': 'Decorative and low-precision applications'
            },
            'brass': {
                'pros': ['Good machinability', 'Corrosion resistant', 'Aesthetic appeal'],
                'cons': ['Higher cost', 'Heavier than aluminum'],
                'best_for': 'Decorative and electrical applications'
            },
            'copper': {
                'pros': ['Excellent conductivity', 'Corrosion resistant'],
                'cons': ['Very high cost', 'Softer material'],
                'best_for': 'Electrical and thermal applications'
            }
        }
        
        info = material_info.get(material_lower, {
            'pros': ['Good general purpose material'],
            'cons': ['Consider alternatives'],
            'best_for': 'General applications'
        })
        
        return info['pros'], info['cons'], info['best_for']
    
    # ========== Path Optimization Methods ==========
    
    def _get_llm_path_analysis(self, geometry_data: Dict, material: str,
                               machining_time: float) -> Dict:
        """Get path optimization analysis using LLM"""
        try:
            import openai
            
            total_length = geometry_data.get('total_length', 0)
            entity_counts = {
                'lines': geometry_data.get('line_count', 0),
                'arcs': geometry_data.get('arc_count', 0),
                'circles': geometry_data.get('circle_count', 0),
                'polylines': geometry_data.get('polyline_count', 0),
                'splines': geometry_data.get('spline_count', 0)
            }
            
            prompt = f"""
Analyze this CNC cutting path for optimization opportunities:

CUTTING PARAMETERS:
- Material: {material}
- Total cutting length: {total_length:.2f} mm
- Estimated machining time: {machining_time:.1f} minutes
- Entity breakdown: {entity_counts}

Provide path optimization recommendations:
1. Cutting sequence optimization (TSP-like routing)
2. Tool path efficiency improvements
3. Rapid move minimization
4. Tool change optimization
5. Estimated time savings

Format as JSON:
{{
    "optimization_strategies": [
        {{
            "strategy": "strategy name",
            "description": "what to do",
            "time_savings": "estimated %",
            "implementation": "how to implement"
        }}
    ],
    "estimated_savings": "X% time reduction",
    "priority_actions": ["action1", "action2"]
}}
"""
            # Initialize client based on provider
            if self.use_openrouter:
                from openai import OpenAI
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base,
                    default_headers={
                        "HTTP-Referer": "https://github.com/cnc-quotation",
                        "X-Title": "CNC Quotation System"
                    }
                )
            else:
                client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CNC path optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_path_analysis(ai_response, geometry_data, machining_time)
            
        except Exception as e:
            logger.error(f"LLM path analysis error: {e}")
            return self._get_rule_based_path_analysis(geometry_data, material, machining_time)
    
    def _get_rule_based_path_analysis(self, geometry_data: Dict, material: str,
                                     machining_time: float) -> Dict:
        """Rule-based path optimization analysis"""
        total_length = geometry_data.get('total_length', 0)
        entity_count = sum([
            geometry_data.get('line_count', 0),
            geometry_data.get('arc_count', 0),
            geometry_data.get('circle_count', 0),
            geometry_data.get('polyline_count', 0)
        ])
        
        strategies = []
        
        # Always suggest basic optimization
        strategies.append({
            "strategy": "Optimize Cutting Sequence",
            "description": "Use nearest-neighbor algorithm to minimize travel distance between cuts",
            "time_savings": "5-15%",
            "implementation": "Reorder entities to minimize rapid moves between cutting operations"
        })
        
        # Suggest grouping similar entities
        if entity_count > 20:
            strategies.append({
                "strategy": "Group Similar Entities",
                "description": "Group lines, arcs, and circles by type to minimize tool changes and setup time",
                "time_savings": "5-10%",
                "implementation": "Reorder cutting sequence to process all lines first, then arcs, then circles"
            })
        
        # Suggest minimizing rapid moves
        if geometry_data.get('polyline_count', 0) > 5:
            strategies.append({
                "strategy": "Minimize Rapid Moves",
                "description": "Connect polylines end-to-end to reduce rapid positioning moves",
                "time_savings": "8-15%",
                "implementation": "Use nearest-neighbor algorithm to sequence polyline cutting"
            })
        
        # Suggest optimizing arc direction
        if geometry_data.get('arc_count', 0) > 10:
            strategies.append({
                "strategy": "Optimize Arc Direction",
                "description": "Cut arcs in consistent direction to maintain tool engagement and reduce tool wear",
                "time_savings": "3-7%",
                "implementation": "Standardize all arcs to clockwise or counter-clockwise direction"
            })
        
        # Suggest reducing tool lifts
        if entity_count > 10:
            strategies.append({
                "strategy": "Reduce Tool Lifts",
                "description": "Minimize Z-axis movements by grouping cuts that can be done in sequence",
                "time_savings": "4-8%",
                "implementation": "Plan cutting sequence to minimize tool retractions and re-entries"
            })
        
        # Material-specific suggestions
        material_lower = material.lower()
        if material_lower in ['steel', 'brass', 'copper']:
            strategies.append({
                "strategy": "Optimize Feed Rate for Hard Materials",
                "description": f"For {material}, use conservative feed rates on complex curves to maintain quality",
                "time_savings": "Quality improvement",
                "implementation": "Reduce feed rate by 20% on arcs and splines, maintain speed on straight lines"
            })
        
        return {
            "optimization_strategies": strategies,
            "estimated_savings": "10-25% time reduction",
            "priority_actions": [s["strategy"] for s in strategies[:3]]
        }
    
    def _parse_path_analysis(self, ai_response: str, geometry_data: Dict,
                            machining_time: float) -> Dict:
        """Parse LLM path analysis response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._get_rule_based_path_analysis(geometry_data, '', machining_time)
    
    # ========== Nesting Optimization Methods ==========
    
    def _get_llm_nesting_analysis(self, geometry_data: Dict, material: str,
                                 thickness: float) -> Dict:
        """Get nesting optimization analysis using LLM"""
        try:
            import openai
            
            bounding_box = geometry_data.get('bounding_box', {})
            width = bounding_box.get('width', 0)
            height = bounding_box.get('height', 0)
            area = bounding_box.get('area', 0)
            
            # Standard sheet sizes
            standard_sheets = [
                {"name": "1000x2000mm", "area": 2000000},
                {"name": "1250x2500mm", "area": 3125000},
                {"name": "1500x3000mm", "area": 4500000}
            ]
            
            prompt = f"""
Analyze nesting optimization for this part:

PART DIMENSIONS:
- Width: {width:.2f} mm
- Height: {height:.2f} mm
- Area: {area:.2f} mm²
- Material: {material}
- Thickness: {thickness} mm

STANDARD SHEET SIZES:
{chr(10).join([f"- {s['name']}: {s['area']} mm²" for s in standard_sheets])}

Provide nesting optimization recommendations:
1. Optimal sheet size selection
2. Parts per sheet calculation
3. Material utilization percentage
4. Waste minimization strategies
5. Cost savings estimation

Format as JSON:
{{
    "recommended_sheet": "sheet size",
    "parts_per_sheet": number,
    "material_utilization": "X%",
    "waste_reduction": "X%",
    "cost_savings": "₹X per sheet",
    "nesting_strategies": ["strategy1", "strategy2"]
}}
"""
            # Initialize client based on provider
            if self.use_openrouter:
                from openai import OpenAI
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base,
                    default_headers={
                        "HTTP-Referer": "https://github.com/cnc-quotation",
                        "X-Title": "CNC Quotation System"
                    }
                )
            else:
                client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a nesting optimization expert for CNC manufacturing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_nesting_analysis(ai_response, geometry_data, material, thickness)
            
        except Exception as e:
            logger.error(f"LLM nesting analysis error: {e}")
            return self._get_rule_based_nesting_analysis(geometry_data, material, thickness)
    
    def _get_rule_based_nesting_analysis(self, geometry_data: Dict, material: str,
                                       thickness: float) -> Dict:
        """Rule-based nesting optimization analysis"""
        bounding_box = geometry_data.get('bounding_box', {})
        width = bounding_box.get('width', 0)
        height = bounding_box.get('height', 0)
        area = bounding_box.get('area', 0)
        
        if area == 0:
            return {
                "recommended_sheet": "N/A",
                "parts_per_sheet": 0,
                "material_utilization": "0%",
                "waste_reduction": "0%",
                "cost_savings": "₹0",
                "nesting_strategies": []
            }
        
        # Find best sheet size
        standard_sheets = [
            {"name": "1000x2000mm", "width": 1000, "height": 2000, "area": 2000000},
            {"name": "1250x2500mm", "width": 1250, "height": 2500, "area": 3125000},
            {"name": "1500x3000mm", "width": 1500, "height": 3000, "area": 4500000}
        ]
        
        best_sheet = None
        max_parts = 0
        
        for sheet in standard_sheets:
            # Calculate how many parts fit (simple calculation)
            parts_x = int(sheet['width'] / (width + 10))  # 10mm spacing
            parts_y = int(sheet['height'] / (height + 10))
            total_parts = parts_x * parts_y
            
            if total_parts > max_parts:
                max_parts = total_parts
                best_sheet = sheet
        
        if best_sheet:
            utilization = (area * max_parts / best_sheet['area']) * 100
            waste_reduction = max(0, 30 - (100 - utilization))  # Estimate
            
            return {
                "recommended_sheet": best_sheet['name'],
                "parts_per_sheet": max_parts,
                "material_utilization": f"{utilization:.1f}%",
                "waste_reduction": f"{waste_reduction:.1f}%",
                "cost_savings": f"₹{area * max_parts * 0.001:.2f} per sheet",
                "nesting_strategies": [
                    "Rotate parts 90° for better fit",
                    "Use edge-to-edge placement",
                    "Minimize spacing between parts"
                ]
            }
        
        return {
            "recommended_sheet": "Custom size needed",
            "parts_per_sheet": 1,
            "material_utilization": "N/A",
            "waste_reduction": "0%",
            "cost_savings": "₹0",
            "nesting_strategies": []
        }
    
    def _parse_nesting_analysis(self, ai_response: str, geometry_data: Dict,
                               material: str, thickness: float) -> Dict:
        """Parse LLM nesting analysis response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._get_rule_based_nesting_analysis(geometry_data, material, thickness)
    
    # ========== Manufacturing Insights Methods ==========
    
    def _get_llm_manufacturing_insights(self, geometry_data: Dict, material: str,
                                      thickness: float, machining_time: float) -> Dict:
        """Get manufacturing insights using LLM"""
        try:
            import openai
            
            complexity_score = geometry_data.get('complexity_metrics', {}).get('complexity_score', 0)
            total_length = geometry_data.get('total_length', 0)
            entity_counts = {
                'lines': geometry_data.get('line_count', 0),
                'arcs': geometry_data.get('arc_count', 0),
                'circles': geometry_data.get('circle_count', 0),
                'splines': geometry_data.get('spline_count', 0)
            }
            
            prompt = f"""
Provide manufacturing insights for this CNC part:

PART DETAILS:
- Material: {material}
- Thickness: {thickness} mm
- Complexity: {complexity_score}/100
- Cutting length: {total_length:.2f} mm
- Machining time: {machining_time:.1f} minutes
- Entity counts: {entity_counts}

Provide insights on:
1. Manufacturing challenges
2. Quality considerations
3. Tool selection recommendations
4. Feed rate optimization
5. Best practices for this material/thickness
6. Potential issues to watch for

Format as JSON:
{{
    "challenges": ["challenge1", "challenge2"],
    "quality_tips": ["tip1", "tip2"],
    "tool_recommendations": ["tool1", "tool2"],
    "feed_rate_notes": "notes",
    "best_practices": ["practice1", "practice2"],
    "watch_outs": ["issue1", "issue2"]
}}
"""
            # Initialize client based on provider
            if self.use_openrouter:
                from openai import OpenAI
                client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base,
                    default_headers={
                        "HTTP-Referer": "https://github.com/cnc-quotation",
                        "X-Title": "CNC Quotation System"
                    }
                )
            else:
                client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CNC manufacturing expert with deep knowledge of materials, tools, and best practices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_manufacturing_insights(ai_response, geometry_data, material, thickness)
            
        except Exception as e:
            logger.error(f"LLM manufacturing insights error: {e}")
            return self._get_rule_based_manufacturing_insights(geometry_data, material, thickness, machining_time)
    
    def _get_rule_based_manufacturing_insights(self, geometry_data: Dict, material: str,
                                              thickness: float, machining_time: float) -> Dict:
        """Rule-based manufacturing insights"""
        material_lower = material.lower()
        complexity_score = geometry_data.get('complexity_metrics', {}).get('complexity_score', 0)
        spline_count = geometry_data.get('spline_count', 0)
        
        challenges = []
        quality_tips = []
        tool_recommendations = []
        watch_outs = []
        
        # Material-specific insights
        if material_lower == 'steel':
            tool_recommendations.append("Use carbide tools for steel")
            watch_outs.append("Watch for work hardening")
            quality_tips.append("Use proper coolant to prevent overheating")
        elif material_lower == 'aluminum':
            tool_recommendations.append("High-speed steel or carbide tools work well")
            watch_outs.append("Aluminum can stick to tools - use proper chip evacuation")
            quality_tips.append("Use higher feed rates for better surface finish")
        elif material_lower == 'plastic':
            tool_recommendations.append("Sharp HSS tools recommended")
            watch_outs.append("Plastic can melt - control heat buildup")
            quality_tips.append("Use air blast for chip removal")
        
        # Complexity-based insights
        if complexity_score > 70:
            challenges.append("High complexity may require slower feed rates")
            quality_tips.append("Consider multiple passes for complex geometry")
        
        if spline_count > 10:
            challenges.append("Many splines may require specialized tooling")
            watch_outs.append("Spline machining can be time-consuming")
        
        # Thickness-based insights
        if thickness > 5:
            challenges.append("Thick material requires deeper cuts and more time")
            tool_recommendations.append("Use tools with sufficient length")
        elif thickness < 1:
            watch_outs.append("Thin material may warp - use proper fixturing")
            quality_tips.append("Use slower feed rates for thin materials")
        
        return {
            "challenges": challenges if challenges else ["Standard manufacturing process"],
            "quality_tips": quality_tips if quality_tips else ["Follow standard CNC best practices"],
            "tool_recommendations": tool_recommendations if tool_recommendations else ["Standard CNC tools"],
            "feed_rate_notes": f"Recommended feed rate: {self.cost_calculator.feed_rates.get(material_lower, 300)} mm/min for {material}",
            "best_practices": [
                "Maintain consistent feed rate",
                "Use appropriate tool diameter",
                "Ensure proper material clamping"
            ],
            "watch_outs": watch_outs if watch_outs else ["Monitor tool wear"]
        }
    
    def _parse_manufacturing_insights(self, ai_response: str, geometry_data: Dict,
                                     material: str, thickness: float) -> Dict:
        """Parse LLM manufacturing insights response"""
        try:
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._get_rule_based_manufacturing_insights(geometry_data, material, thickness, 0)

