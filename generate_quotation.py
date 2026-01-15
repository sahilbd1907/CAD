"""
Professional PDF Quotation Generator for Laser Cutting and Water Jet Cutting Machines
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class QuotationGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
        self.story = []
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        """Setup custom paragraph styles"""
        # Title Style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a4d80'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle Style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2d5a87'),
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Section Header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#3d6ba3'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            backColor=colors.HexColor('#e8f0f8'),
            borderPadding=8
        ))
        
        # Normal text with justified alignment
        self.styles.add(ParagraphStyle(
            name='NormalJustified',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Price Style
        self.styles.add(ParagraphStyle(
            name='Price',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#c41e3a'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        ))
        
    def format_currency(self, amount):
        """Format amount in Indian currency format"""
        if amount >= 10000000:
            return f"Rs. {amount/10000000:.2f} Crores"
        elif amount >= 100000:
            return f"Rs. {amount/100000:.2f} Lakhs"
        elif amount >= 1000:
            return f"Rs. {amount/1000:.2f} Thousands"
        else:
            return f"Rs. {amount:,.0f}"
    
    def format_rupee(self, amount):
        """Format amount with Rs. prefix"""
        return f"Rs. {amount:,.0f}"
    
    def create_header(self):
        """Create quotation header"""
        header_data = [
            [Paragraph('<b>QUOTATION FOR CUTTING MACHINES</b>', self.styles['CustomTitle'])],
            [Paragraph('Laser Cutting & Water Jet Cutting Machines', self.styles['Normal'])],
            [Spacer(1, 0.3*cm)],
            [Paragraph(f'Date: {datetime.now().strftime("%d %B %Y")}', self.styles['Normal'])],
            [Paragraph('Quotation Valid For: 30 Days', self.styles['Normal'])],
        ]
        header_table = Table(header_data, colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        self.story.append(header_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_overview(self):
        """Create overview section"""
        overview_text = """
        This quotation provides comprehensive pricing and operational cost analysis for both 
        Laser Cutting Machines and Water Jet Cutting Machines, including initial investment, 
        operational expenses, and time-based costing calculations as per Indian market standards.
        """
        self.story.append(Paragraph('<b>OVERVIEW</b>', self.styles['SectionHeader']))
        self.story.append(Paragraph(overview_text, self.styles['NormalJustified']))
        self.story.append(Spacer(1, 0.3*cm))
    
    def create_laser_cutting_section(self):
        """Create Laser Cutting Machine section"""
        self.story.append(Paragraph('<b>1. LASER CUTTING MACHINES</b>', self.styles['CustomSubtitle']))
        
        # Machine Prices
        laser_price_data = [
            [Paragraph('<b>Machine Type</b>', self.styles['Normal']), 
             Paragraph('<b>Power Rating</b>', self.styles['Normal']), 
             Paragraph('<b>Price Range</b>', self.styles['Normal']), 
             Paragraph('<b>Best Value</b>', self.styles['Normal'])],
            ['Fiber Laser - Entry Level', '1.5 - 3 kW', self.format_rupee(2000000) + ' - ' + self.format_rupee(4500000), self.format_rupee(3000000)],
            ['Fiber Laser - Industrial', '3 - 6 kW', self.format_rupee(3000000) + ' - ' + self.format_rupee(6000000), self.format_rupee(4000000)],
            ['Fiber Laser - Premium', '10 kW+', self.format_rupee(7000000) + ' - ' + self.format_rupee(10000000), self.format_rupee(8500000)],
            ['CO2 Laser - Small', 'Up to 150W', self.format_rupee(300000) + ' - ' + self.format_rupee(1000000), self.format_rupee(650000)],
            ['CO2 Laser - Large', '150W+', self.format_rupee(600000) + ' - ' + self.format_rupee(1000000), self.format_rupee(800000)],
        ]
        
        laser_price_table = Table(laser_price_data, colWidths=[5*cm, 3*cm, 5*cm, 4*cm])
        laser_price_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d80')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(laser_price_table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Operational Costs
        self.story.append(Paragraph('<b>1.1 Operational Costs (Time-Based)</b>', self.styles['SectionHeader']))
        
        # Example calculation for 3kW Fiber Laser
        laser_op_data = [
            [Paragraph('<b>Cost Component</b>', self.styles['Normal']), 
             Paragraph('<b>Monthly Cost</b>', self.styles['Normal']), 
             Paragraph('<b>Annual Cost</b>', self.styles['Normal']), 
             Paragraph('<b>Per Hour Cost*</b>', self.styles['Normal'])],
            ['Electricity (20-30% of 3kW)', self.format_rupee(20000), self.format_rupee(240000), self.format_rupee(120)],
            ['Assist Gas (N2/O2)', self.format_rupee(10000), self.format_rupee(120000), self.format_rupee(60)],
            ['Maintenance & Consumables', self.format_rupee(8333), self.format_rupee(100000), self.format_rupee(50)],
            [Paragraph('<b>TOTAL OPERATIONAL COST</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(38333) + '</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(460000) + '</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(230) + '</b>', self.styles['Normal'])],
        ]
        
        laser_op_table = Table(laser_op_data, colWidths=[6*cm, 3.5*cm, 3.5*cm, 4*cm])
        laser_op_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f5f5f5')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0f8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(laser_op_table)
        
        note_text = "* Per hour cost calculated based on 2,000 operating hours per year (8 hours/day × 250 working days)"
        self.story.append(Paragraph(note_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Total Cost Calculation
        self.story.append(Paragraph('<b>1.2 Total Cost of Ownership (Year 1) - 3kW Fiber Laser</b>', self.styles['SectionHeader']))
        
        laser_total_data = [
            [Paragraph('<b>Item</b>', self.styles['Normal']), 
             Paragraph('<b>Amount</b>', self.styles['Normal'])],
            ['Machine Purchase Price (3kW Fiber Laser)', self.format_rupee(4000000)],
            ['Installation & Training', self.format_rupee(200000)],
            ['Annual Operational Cost', self.format_rupee(460000)],
            [Paragraph('<b>TOTAL YEAR 1 INVESTMENT</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(4660000) + '</b>', self.styles['Normal'])],
        ]
        
        laser_total_table = Table(laser_total_data, colWidths=[12*cm, 5*cm])
        laser_total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e4f7')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(laser_total_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_waterjet_section(self):
        """Create Water Jet Cutting Machine section"""
        self.story.append(Paragraph('<b>2. WATER JET CUTTING MACHINES</b>', self.styles['CustomSubtitle']))
        
        # Machine Prices
        waterjet_price_data = [
            [Paragraph('<b>Machine Type</b>', self.styles['Normal']), 
             Paragraph('<b>Specifications</b>', self.styles['Normal']), 
             Paragraph('<b>Price Range</b>', self.styles['Normal']), 
             Paragraph('<b>Best Value</b>', self.styles['Normal'])],
            ['Pure Water Jet', 'Basic cutting', self.format_rupee(400000) + ' - ' + self.format_rupee(600000), self.format_rupee(500000)],
            ['Abrasive Water Jet', 'Standard cutting', self.format_rupee(600000) + ' - ' + self.format_rupee(1500000), self.format_rupee(1200000)],
            ['3D Water Jet', 'Advanced 3-axis', self.format_rupee(1000000) + ' - ' + self.format_rupee(2500000), self.format_rupee(1800000)],
            ['CNC Water Jet', 'Industrial grade', self.format_rupee(4500000) + ' - ' + self.format_rupee(6000000), self.format_rupee(5000000)],
            ['Portable Water Jet', 'Mobile unit', self.format_rupee(250000) + ' - ' + self.format_rupee(500000), self.format_rupee(375000)],
        ]
        
        waterjet_price_table = Table(waterjet_price_data, colWidths=[4*cm, 4*cm, 4.5*cm, 3.5*cm])
        waterjet_price_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d80')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(waterjet_price_table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Operational Costs
        self.story.append(Paragraph('<b>2.1 Operational Costs (Time-Based)</b>', self.styles['SectionHeader']))
        
        # Example calculation for Standard Abrasive Water Jet
        waterjet_op_data = [
            [Paragraph('<b>Cost Component</b>', self.styles['Normal']), 
             Paragraph('<b>Monthly Cost</b>', self.styles['Normal']), 
             Paragraph('<b>Annual Cost</b>', self.styles['Normal']), 
             Paragraph('<b>Per Hour Cost*</b>', self.styles['Normal'])],
            ['Electricity (37 kW pump)', self.format_rupee(25000), self.format_rupee(300000), self.format_rupee(150)],
            ['Abrasive Material (Garnet)', self.format_rupee(15000), self.format_rupee(180000), self.format_rupee(90)],
            ['Water & Filtration', self.format_rupee(3000), self.format_rupee(36000), self.format_rupee(18)],
            ['Maintenance & Consumables', self.format_rupee(12500), self.format_rupee(150000), self.format_rupee(75)],
            [Paragraph('<b>TOTAL OPERATIONAL COST</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(55500) + '</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(666000) + '</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(333) + '</b>', self.styles['Normal'])],
        ]
        
        waterjet_op_table = Table(waterjet_op_data, colWidths=[6*cm, 3.5*cm, 3.5*cm, 4*cm])
        waterjet_op_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f5f5f5')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0f8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(waterjet_op_table)
        
        note_text = "* Per hour cost calculated based on 2,000 operating hours per year (8 hours/day × 250 working days)"
        self.story.append(Paragraph(note_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Total Cost Calculation
        self.story.append(Paragraph('<b>2.2 Total Cost of Ownership (Year 1) - Abrasive Water Jet</b>', self.styles['SectionHeader']))
        
        waterjet_total_data = [
            [Paragraph('<b>Item</b>', self.styles['Normal']), 
             Paragraph('<b>Amount</b>', self.styles['Normal'])],
            ['Machine Purchase Price (Standard Abrasive Water Jet)', self.format_rupee(1200000)],
            ['Installation & Training', self.format_rupee(150000)],
            ['Annual Operational Cost', self.format_rupee(666000)],
            [Paragraph('<b>TOTAL YEAR 1 INVESTMENT</b>', self.styles['Normal']), 
             Paragraph('<b>' + self.format_rupee(2016000) + '</b>', self.styles['Normal'])],
        ]
        
        waterjet_total_table = Table(waterjet_total_data, colWidths=[12*cm, 5*cm])
        waterjet_total_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4e4f7')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(waterjet_total_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_comparison_section(self):
        """Create comparison section"""
        self.story.append(Paragraph('<b>3. COMPARATIVE ANALYSIS</b>', self.styles['CustomSubtitle']))
        
        comparison_data = [
            [Paragraph('<b>Parameter</b>', self.styles['Normal']), 
             Paragraph('<b>Laser Cutting (3kW)</b>', self.styles['Normal']), 
             Paragraph('<b>Water Jet Cutting (Standard)</b>', self.styles['Normal'])],
            ['Initial Machine Cost', self.format_rupee(4000000), self.format_rupee(1200000)],
            ['Installation Cost', self.format_rupee(200000), self.format_rupee(150000)],
            ['Annual Operating Cost', self.format_rupee(460000), self.format_rupee(666000)],
            ['Cost per Operating Hour', self.format_rupee(230), self.format_rupee(333)],
            ['Best For', 'Metals, High Speed', 'All Materials, No Heat'],
            ['Material Thickness Range', 'Up to 25mm', 'Up to 200mm'],
            ['Cutting Speed', 'Very Fast', 'Moderate'],
            ['Precision', 'Excellent (±0.1mm)', 'Good (±0.2mm)'],
        ]
        
        comparison_table = Table(comparison_data, colWidths=[5*cm, 6*cm, 6*cm])
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d80')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (2, 1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(comparison_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_time_based_costing(self):
        """Create detailed time-based costing section"""
        self.story.append(Paragraph('<b>4. TIME-BASED COSTING CALCULATIONS</b>', self.styles['CustomSubtitle']))
        
        self.story.append(Paragraph(
            'In India, cutting machine services are typically charged on a time-based model. '
            'Below are detailed calculations for different operational scenarios.',
            self.styles['NormalJustified']
        ))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Daily Cost Calculation
        self.story.append(Paragraph('<b>4.1 Daily Operational Cost (8 Hours)</b>', self.styles['SectionHeader']))
        
        daily_cost_data = [
            [Paragraph('<b>Machine Type</b>', self.styles['Normal']), 
             Paragraph('<b>8 Hours Cost</b>', self.styles['Normal']), 
             Paragraph('<b>16 Hours Cost</b>', self.styles['Normal']), 
             Paragraph('<b>24 Hours Cost</b>', self.styles['Normal'])],
            ['Laser Cutting (3kW)', 
             self.format_rupee(230 * 8), 
             self.format_rupee(230 * 16), 
             self.format_rupee(230 * 24)],
            ['Water Jet Cutting', 
             self.format_rupee(333 * 8), 
             self.format_rupee(333 * 16), 
             self.format_rupee(333 * 24)],
        ]
        
        daily_cost_table = Table(daily_cost_data, colWidths=[5*cm, 4*cm, 4*cm, 4*cm])
        daily_cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(daily_cost_table)
        self.story.append(Spacer(1, 0.3*cm))
        
        # Monthly Cost Calculation
        self.story.append(Paragraph('<b>4.2 Monthly Operational Cost (250 Working Days/Year)</b>', self.styles['SectionHeader']))
        
        monthly_cost_data = [
            [Paragraph('<b>Machine Type</b>', self.styles['Normal']), 
             Paragraph('<b>1 Shift (8 hrs)</b>', self.styles['Normal']), 
             Paragraph('<b>2 Shifts (16 hrs)</b>', self.styles['Normal']), 
             Paragraph('<b>3 Shifts (24 hrs)</b>', self.styles['Normal'])],
            ['Laser Cutting (3kW)', 
             self.format_rupee((230 * 8) * 20), 
             self.format_rupee((230 * 16) * 20), 
             self.format_rupee((230 * 24) * 20)],
            ['Water Jet Cutting', 
             self.format_rupee((333 * 8) * 20), 
             self.format_rupee((333 * 16) * 20), 
             self.format_rupee((333 * 24) * 20)],
        ]
        
        monthly_cost_table = Table(monthly_cost_data, colWidths=[5*cm, 4*cm, 4*cm, 4*cm])
        monthly_cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5a87')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(monthly_cost_table)
        
        note_text = "Note: Calculations assume 20 working days per month and operational costs only (excluding depreciation)"
        self.story.append(Paragraph(note_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_service_pricing(self):
        """Create service pricing section"""
        self.story.append(Paragraph('<b>5. SERVICE CHARGING RATES (Customer Pricing)</b>', self.styles['CustomSubtitle']))
        
        self.story.append(Paragraph(
            'For service providers offering cutting services to customers, typical charging rates '
            'include operational costs plus profit margin. Below are recommended service rates.',
            self.styles['NormalJustified']
        ))
        self.story.append(Spacer(1, 0.3*cm))
        
        service_rate_data = [
            [Paragraph('<b>Service Type</b>', self.styles['Normal']), 
             Paragraph('<b>Cost/Hour</b>', self.styles['Normal']), 
             Paragraph('<b>Markup (50%)</b>', self.styles['Normal']), 
             Paragraph('<b>Customer Rate/Hour</b>', self.styles['Normal']), 
             Paragraph('<b>Rate/Minute</b>', self.styles['Normal'])],
            ['Laser Cutting', self.format_rupee(230), '50%', self.format_rupee(345), self.format_rupee(5.75)],
            ['Water Jet Cutting', self.format_rupee(333), '50%', self.format_rupee(500), self.format_rupee(8.33)],
        ]
        
        service_rate_table = Table(service_rate_data, colWidths=[4*cm, 3*cm, 2.5*cm, 3.5*cm, 3*cm])
        service_rate_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d80')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        self.story.append(service_rate_table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def create_footer(self):
        """Create quotation footer"""
        self.story.append(Spacer(1, 0.5*cm))
        
        footer_data = [
            [Paragraph('<b>IMPORTANT NOTES</b>', self.styles['Normal'])],
            ['• All prices are indicative and subject to change without prior notice'],
            ['• Prices may vary based on machine specifications, manufacturer, and location'],
            ['• Installation costs include basic setup and operator training'],
            ['• Operational costs calculated based on average Indian market rates'],
            ['• Electricity rates assumed at Rs. 10 per kWh (varies by state)'],
            ['• Quotation valid for 30 days from date of issue'],
            ['• GST (18%) applicable on all purchases as per Indian regulations'],
            ['• Payment terms: 50% advance, 50% on delivery and installation'],
        ]
        
        footer_text = """
        <b>IMPORTANT NOTES:</b><br/>
        • All prices are indicative and subject to change without prior notice<br/>
        • Prices may vary based on machine specifications, manufacturer, and location<br/>
        • Installation costs include basic setup and operator training<br/>
        • Operational costs calculated based on average Indian market rates<br/>
        • Electricity rates assumed at Rs. 10 per kWh (varies by state)<br/>
        • Quotation valid for 30 days from date of issue<br/>
        • GST (18%) applicable on all purchases as per Indian regulations<br/>
        • Payment terms: 50% advance, 50% on delivery and installation<br/>
        """
        
        self.story.append(Paragraph(footer_text, self.styles['NormalJustified']))
        self.story.append(Spacer(1, 0.5*cm))
        
        # Contact Information
        contact_text = """
        <b>For further inquiries and detailed quotations, please contact:</b><br/>
        Email: info@cuttingmachines.com | Phone: +91-XXXXXXXXXX<br/>
        Website: www.cuttingmachines.com
        """
        self.story.append(Paragraph(contact_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*cm))
        
        # Signature area
        signature_data = [
            ['Prepared By:', 'Authorized Signatory:'],
            ['', ''],
            ['', ''],
        ]
        signature_table = Table(signature_data, colWidths=[8.5*cm, 8.5*cm])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('LINEBELOW', (0, 1), (0, 1), 1, colors.black),
            ('LINEBELOW', (1, 1), (1, 1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        self.story.append(signature_table)
    
    def generate(self):
        """Generate the complete PDF quotation"""
        self.create_header()
        self.create_overview()
        self.create_laser_cutting_section()
        self.create_waterjet_section()
        self.create_comparison_section()
        self.create_time_based_costing()
        self.create_service_pricing()
        self.create_footer()
        
        self.doc.build(self.story)
        print(f"PDF quotation generated successfully: {self.filename}")

if __name__ == "__main__":
    generator = QuotationGenerator("Cutting_Machines_Quotation.pdf")
    generator.generate()

