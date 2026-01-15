# Laser Cutting & Water Jet Cutting Machines - Professional Quotation PDF Generator

## Overview
This tool generates a professional PDF quotation document with comprehensive pricing and cost analysis for both Laser Cutting and Water Jet Cutting machines, specifically tailored for the Indian market.

## Features

✅ **Professional PDF Layout**
- Clean, modern design with professional color scheme
- Well-organized sections with clear headings
- Professional tables with alternating row colors
- Proper formatting with HTML tags rendered correctly

✅ **Comprehensive Pricing Information**
- Machine prices (initial investment)
- Time-based operational costs (as per Indian standards)
- Detailed cost breakdowns
- Comparative analysis between machine types

✅ **Detailed Calculations**
- Hourly operational costs
- Daily operational costs (8, 16, 24 hours)
- Monthly operational costs
- Service charging rates with markup

✅ **Indian Market Specific**
- All prices in Indian Rupees (Rs.)
- Time-based costing model (standard in India)
- GST considerations mentioned
- Indian currency formatting

## What's Included in the PDF

1. **Laser Cutting Machines**
   - Fiber Laser (Entry, Industrial, Premium)
   - CO2 Laser (Small, Large)
   - Operational costs breakdown
   - Total cost of ownership

2. **Water Jet Cutting Machines**
   - Pure Water Jet
   - Abrasive Water Jet
   - 3D Water Jet
   - CNC Water Jet
   - Portable Water Jet
   - Operational costs breakdown
   - Total cost of ownership

3. **Comparative Analysis**
   - Side-by-side comparison of both technologies
   - Cost comparison
   - Application suitability

4. **Time-Based Costing Calculations**
   - Daily costs (8/16/24 hours)
   - Monthly costs (different shift patterns)
   - Service rates for customers

## Usage

### Install Dependencies
```bash
pip install reportlab
```

### Generate PDF
```bash
python generate_quotation.py
```

The PDF will be generated as `Cutting_Machines_Quotation.pdf` in the current directory.

## Pricing Information Source

The pricing and operational cost data is based on:
- Current 2024-2025 Indian market rates
- Research from multiple suppliers and manufacturers
- Industry-standard operational cost calculations
- Time-based costing models used in India

## Notes

- All prices are indicative and may vary based on location, manufacturer, and specifications
- Electricity rates assumed at Rs. 10 per kWh (varies by state)
- Operational costs calculated for 2,000 hours/year (8 hours/day × 250 working days)
- Quotation valid for 30 days

## Customization

You can customize the quotation by:
- Editing prices in the `generate_quotation.py` file
- Modifying operational cost assumptions
- Adjusting markup percentages for service rates
- Changing color schemes and styling

## File Structure

```
generate_quotation.py     - Main PDF generator script
requirements.txt          - Python dependencies
Cutting_Machines_Quotation.pdf - Generated PDF output
```


