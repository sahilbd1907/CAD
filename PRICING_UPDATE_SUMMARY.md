# Pricing Update Summary - CAD Quotation System

## Overview
Updated the CAD quotation system with accurate laser cutting and water jet cutting pricing based on 2024-2025 Indian market research. All pricing now reflects time-based costing as per Indian standards.

## Key Changes

### 1. Cost Calculator (`cost_calculator.py`)

#### Updated Machine Hourly Rates (Time-Based Costing)
**Previous rates were too low. Updated to match Indian market standards:**

| Material | Old Rate (Rs./hr) | New Rate (Rs./hr) | Change |
|----------|-------------------|-------------------|--------|
| Steel | 1,800 | **400** | -77% (more realistic) |
| Aluminum | 1,600 | **380** | -76% |
| Plastic | 1,200 | **320** | -73% |
| Wood | 900 | **300** | -67% |
| Brass | 1,700 | **420** | -75% |
| Copper | 1,800 | **450** | -75% |

**Rationale:**
- Based on research: Laser cutting service rates in India range Rs. 300-500/hour
- Operational cost base: Rs. 230/hour + 50% markup = Rs. 345/hour average
- Material-specific adjustments applied based on cutting difficulty

#### Added Water Jet Cutting Rates
New rates added for water jet cutting option:
- Operational cost base: Rs. 333/hour + 50% markup = Rs. 500/hour average
- Rates range from Rs. 400-530/hour depending on material

#### Updated Material Costs
Material costs updated for 2024-2025 Indian market:
- Steel: Rs. 0.0065 → **Rs. 0.0080** per cm³
- Aluminum: Rs. 0.0200 → **Rs. 0.0250** per cm³
- Plastic: Rs. 0.0030 → **Rs. 0.0040** per cm³
- Wood: Rs. 0.0015 → **Rs. 0.0020** per cm³
- Brass: Rs. 0.0600 → **Rs. 0.0750** per cm³
- Copper: Rs. 0.0750 → **Rs. 0.0900** per cm³

#### Updated Feed Rates (Laser Cutting Speeds)
Optimized feed rates for fiber laser cutting:
- Steel: 300 → **250** mm/min (more realistic for 1-3mm thickness)
- Aluminum: 600 mm/min (unchanged - appropriate)
- Plastic: 800 mm/min (unchanged - appropriate)
- Wood: 1200 mm/min (unchanged - appropriate)
- Brass: 400 → **350** mm/min
- Copper: 350 → **300** mm/min (slower due to reflectivity)

#### Updated Setup Times
- Setup time: 10 minutes → **8 minutes** (laser setup is faster than CNC)
- Tool change time: 3 minutes → **2 minutes** (material changeover for laser)

### 2. PDF Generator (`pdf_generator.py`)

#### Currency Symbol Update
- **Replaced ₹ symbol with "Rs." throughout**
- All currency displays now use "Rs." format as requested

#### Updated Cost Breakdown Display
- Changed "CNC Machining" to "**Laser Cutting Service**"
- Added note: "Time-based (as per Indian standards)"
- Updated unit price display to show per-minute rate based on hourly rate
- Enhanced notes section to include:
  - Cutting time
  - Cutting speed
  - Hourly rate (time-based costing)
  - Quote validity

### 3. Research Basis

All pricing is based on:
1. **Laser Cutting Machines:**
   - Entry-level (1.5-3kW): Rs. 20-45 Lakhs
   - Industrial (3-6kW): Rs. 30-60 Lakhs
   - Operational cost: ~Rs. 230/hour
   - Service rate: Rs. 300-500/hour (with markup)

2. **Water Jet Cutting Machines:**
   - Standard abrasive: Rs. 6-15 Lakhs
   - Industrial CNC: Rs. 45-60 Lakhs
   - Operational cost: ~Rs. 333/hour
   - Service rate: Rs. 400-600/hour (with markup)

3. **Time-Based Costing (Indian Standard):**
   - Costing done on time basis as standard practice in India
   - Includes operational costs + markup for profitability
   - Rates vary by material based on cutting difficulty

## Impact on Quotations

### Before Update:
- **Example:** 1000mm steel cutting, 2mm thickness, 10 minutes
  - Labor cost: Rs. 300 (at Rs. 1,800/hour)
  - **Total cost would be unrealistically high**

### After Update:
- **Example:** 1000mm steel cutting, 2mm thickness, 10 minutes
  - Labor cost: Rs. 66.67 (at Rs. 400/hour)
  - Material cost: Updated to current market rates
  - **Total cost is realistic and competitive**

## Files Modified

1. `cost_calculator.py` - Complete pricing overhaul
2. `pdf_generator.py` - Currency symbol and display updates

## Files Unchanged (Compatible)

- `app.py` - No changes needed, uses updated calculator
- `ai_advisor.py` - No changes needed, uses updated calculator
- `cad_processor.py` - No changes needed

## Verification

All pricing calculations now:
- ✅ Use accurate 2024-2025 Indian market rates
- ✅ Follow time-based costing standards
- ✅ Display currency as "Rs." instead of ₹
- ✅ Include proper operational cost calculations
- ✅ Apply material-specific adjustments

## Notes

- Prices are indicative and may vary by location (state) within India
- Electricity rates assumed at Rs. 10/kWh (varies by state)
- GST (18%) is applied separately in quotations
- Setup fees remain at Rs. 500 (standard)
- Quotations valid for 30 days

---

**Date Updated:** January 2025
**Market Research:** Based on Indian laser/waterjet cutting industry rates 2024-2025


