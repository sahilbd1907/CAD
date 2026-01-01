from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
import os
import tempfile
from datetime import datetime
from typing import Dict
import random
import string

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers and headers/footers"""
    def __init__(self, *args, **kwargs):
        # Extract company_name before passing to parent
        self.company_name = kwargs.pop('company_name', 'Tech support')
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
    
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
    
    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    
    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#6b7280'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 0.75*inch, 0.5*inch, page_text)
        
        # Footer line
        self.setStrokeColor(colors.HexColor('#e5e7eb'))
        self.setLineWidth(0.5)
        self.line(0.75*inch, 0.65*inch, A4[0] - 0.75*inch, 0.65*inch)
        
        # Footer company info
        footer_text = f"{self.company_name} | Confidential Quotation"
        self.drawString(0.75*inch, 0.5*inch, footer_text)
        self.restoreState()

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.temp_dir = 'temp_pdfs'
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Company information
        self.company_name = "Tech support"
        self.company_address = "Pune, Maharashtra"
        self.company_city = "India"
        self.company_phone = "+91-XXXXXXXXXX"
        self.company_email = "info@techsupport.example"
        self.company_website = "www.techsupport.example"
        
        # Brand colors
        self.primary_color = colors.HexColor('#4f46e5')  # Indigo
        self.secondary_color = colors.HexColor('#06b6d4')  # Cyan
        self.accent_color = colors.HexColor('#10b981')  # Green
        self.dark_gray = colors.HexColor('#1f2937')
        self.light_gray = colors.HexColor('#f3f4f6')
        self.border_color = colors.HexColor('#e5e7eb')
    
    def generate_quotation(self, geometry_data: Dict, material: str, thickness: float, 
                          machining_time: float, total_cost: float) -> str:
        """
        Generate a professional PDF quotation
        """
        # Create temporary PDF file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quotation_{timestamp}.pdf"
        filepath = os.path.join(self.temp_dir, filename)
        
        # Generate quotation number
        quote_number = self._generate_quote_number()
        
        # Create PDF document with custom canvas
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4, 
            rightMargin=0.75*inch, 
            leftMargin=0.75*inch, 
            topMargin=1*inch, 
            bottomMargin=0.75*inch
        )
        
        # Build PDF content
        story = []
        
        # Professional Header
        story.extend(self._create_professional_header(quote_number))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary Box
        story.extend(self._create_executive_summary(geometry_data, material, thickness, total_cost))
        story.append(Spacer(1, 0.25*inch))
        
        # Project Details Section
        story.extend(self._create_project_details(geometry_data, material, thickness, quote_number))
        story.append(Spacer(1, 0.25*inch))
        
        # Technical Specifications
        story.extend(self._create_technical_specs(geometry_data))
        story.append(Spacer(1, 0.25*inch))
        
        # Cost Breakdown
        story.extend(self._create_detailed_cost_breakdown(geometry_data, material, thickness, 
                                                         machining_time, total_cost))
        story.append(Spacer(1, 0.25*inch))
        
        # Terms and Conditions
        story.extend(self._create_professional_terms())
        story.append(Spacer(1, 0.2*inch))
        
        # Signature Section
        story.extend(self._create_signature_section())
        
        # Build PDF with custom canvas
        doc.build(story, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, company_name=self.company_name, **kwargs))
        
        return filename
    
    def _generate_quote_number(self):
        """Generate a professional quotation number"""
        date_str = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"QT-{date_str}-{random_suffix}"
    
    def _create_professional_header(self, quote_number: str):
        """Create professional header with branding"""
        elements = []
        
        # Header table with company info and quote details
        header_data = [
            [
                self._create_header_left_cell(),
                self._create_header_right_cell(quote_number)
            ]
        ]
        
        header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('LEFTPADDING', (1, 0), (1, 0), 0),
            ('RIGHTPADDING', (1, 0), (1, 0), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        elements.append(header_table)
        
        # Decorative line
        elements.append(Spacer(1, 0.1*inch))
        line_table = Table([['']], colWidths=[7*inch], rowHeights=[0.05*inch])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), self.primary_color),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 0),
        ]))
        elements.append(line_table)
        
        return elements
    
    def _create_header_left_cell(self):
        """Create left side of header with company info"""
        company_style = ParagraphStyle(
            'CompanyName',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=8,
            leading=32
        )
        
        address_style = ParagraphStyle(
            'Address',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.dark_gray,
            spaceAfter=4,
            leading=12
        )
        
        contact_style = ParagraphStyle(
            'Contact',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=2,
            leading=11
        )
        
        content = [
            Paragraph(self.company_name, company_style),
            Paragraph(self.company_address, address_style),
            Paragraph(self.company_city, address_style),
            Spacer(1, 6),
            Paragraph(f"<b>Phone:</b> {self.company_phone}", contact_style),
            Paragraph(f"<b>Email:</b> {self.company_email}", contact_style),
            Paragraph(f"<b>Web:</b> {self.company_website}", contact_style),
        ]
        
        return content
    
    def _create_header_right_cell(self, quote_number: str):
        """Create right side of header with quotation info"""
        quote_title_style = ParagraphStyle(
            'QuoteTitle',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT,
            spaceAfter=12,
            leading=36
        )
        
        quote_label_style = ParagraphStyle(
            'QuoteLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_RIGHT,
            spaceAfter=2,
            leading=11
        )
        
        quote_value_style = ParagraphStyle(
            'QuoteValue',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.dark_gray,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT,
            spaceAfter=8,
            leading=13
        )
        
        date_str = datetime.now().strftime("%B %d, %Y")
        valid_until = (datetime.now().replace(day=1) if datetime.now().day > 15 else datetime.now()).strftime("%B %d, %Y")
        
        content = [
            Paragraph("QUOTATION", quote_title_style),
            Paragraph("Quotation Number:", quote_label_style),
            Paragraph(quote_number, quote_value_style),
            Paragraph("Date Issued:", quote_label_style),
            Paragraph(date_str, quote_value_style),
            Paragraph("Valid Until:", quote_label_style),
            Paragraph(valid_until, quote_value_style),
        ]
        
        return content
    
    def _create_executive_summary(self, geometry_data: Dict, material: str, thickness: float, total_cost: float):
        """Create executive summary box"""
        elements = []
        
        summary_data = [
            [
                self._create_summary_box("Total Cost", f"₹{total_cost:,.2f}", self.accent_color),
                self._create_summary_box("Material", material.capitalize(), self.secondary_color),
                self._create_summary_box("Thickness", f"{thickness} mm", self.primary_color),
                self._create_summary_box("Cutting Length", f"{geometry_data.get('total_length', 0):.1f} mm", colors.HexColor('#8b5cf6'))
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[1.75*inch]*4)
        summary_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(summary_table)
        return elements
    
    def _create_summary_box(self, label: str, value: str, bg_color):
        """Create a summary box element"""
        box_style = ParagraphStyle(
            'SummaryBox',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER,
            spaceAfter=4
        )
        
        value_style = ParagraphStyle(
            'SummaryValue',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        )
        
        # Create a table for the box with background
        box_data = [
            [Paragraph(label, box_style)],
            [Paragraph(value, value_style)]
        ]
        
        box_table = Table(box_data, colWidths=[1.75*inch], rowHeights=[0.3*inch, 0.4*inch])
        box_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 1), (0, 1), bg_color),
            ('BACKGROUND', (0, 0), (0, 0), colors.white),
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (0, -1), 8),
            ('RIGHTPADDING', (0, 0), (0, -1), 8),
            ('TOPPADDING', (0, 0), (0, -1), 6),
            ('BOTTOMPADDING', (0, 0), (0, -1), 6),
            ('ROWBACKGROUNDS', (0, 0), (0, -1), [colors.white, bg_color]),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ]))
        
        return box_table
    
    def _create_project_details(self, geometry_data: Dict, material: str, thickness: float, quote_number: str):
        """Create detailed project information section"""
        elements = []
        
        # Section header
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=12,
            borderWidth=0,
            borderPadding=0
        )
        elements.append(Paragraph("Project Specifications", section_header))
        
        # Two-column layout
        left_data = [
            ['<b>Quotation Reference:</b>', quote_number],
            ['<b>Project Date:</b>', datetime.now().strftime("%B %d, %Y")],
            ['<b>Material Type:</b>', material.capitalize()],
            ['<b>Material Thickness:</b>', f"{thickness} mm"],
        ]
        
        right_data = [
            ['<b>Total Cutting Length:</b>', f"{geometry_data.get('total_length', 0):.2f} mm"],
            ['<b>Estimated Time:</b>', f"{geometry_data.get('machining_time', 0):.1f} min"],
            ['<b>Complexity Score:</b>', f"{geometry_data.get('complexity_metrics', {}).get('complexity_score', 'N/A')}/100"],
            ['<b>Total Entities:</b>', str(geometry_data.get('complexity_metrics', {}).get('total_entities', 0))],
        ]
        
        # Add bounding box if available
        if 'bounding_box' in geometry_data and geometry_data['bounding_box'].get('width', 0) > 0:
            bbox = geometry_data['bounding_box']
            left_data.append(['<b>Drawing Dimensions:</b>', f"{bbox.get('width', 0):.1f} × {bbox.get('height', 0):.1f} mm"])
            right_data.append(['<b>Drawing Area:</b>', f"{bbox.get('area', 0):.1f} mm²"])
        
        left_table = Table(left_data, colWidths=[2.2*inch, 2.8*inch])
        left_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, self.border_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        right_table = Table(right_data, colWidths=[2.2*inch, 2.8*inch])
        right_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, self.border_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # Combine in two columns
        combined_data = [[left_table, right_table]]
        combined_table = Table(combined_data, colWidths=[3.5*inch, 3.5*inch])
        combined_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        elements.append(combined_table)
        return elements
    
    def _create_technical_specs(self, geometry_data: Dict):
        """Create technical specifications table"""
        elements = []
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=12
        )
        elements.append(Paragraph("Entity Breakdown", section_header))
        
        # Calculate totals
        total_entities = sum([
            geometry_data.get('line_count', 0),
            geometry_data.get('arc_count', 0),
            geometry_data.get('circle_count', 0),
            geometry_data.get('polyline_count', 0),
            geometry_data.get('spline_count', 0),
            geometry_data.get('ellipse_count', 0)
        ])
        
        def calc_percentage(count):
            return (count / max(total_entities, 1)) * 100
        
        # Helper function to safely get entity length (sum of list if it's a list)
        def get_entity_length(entity_type):
            entity_lengths = geometry_data.get('entity_lengths', {})
            length_data = entity_lengths.get(entity_type, 0)
            if isinstance(length_data, list):
                return sum(length_data) if length_data else 0.0
            elif isinstance(length_data, (int, float)):
                return float(length_data)
            else:
                return 0.0
        
        entity_data = [
            ['<b>Entity Type</b>', '<b>Count</b>', '<b>Percentage</b>', '<b>Length (mm)</b>'],
            ['Lines', str(geometry_data.get('line_count', 0)), 
             f"{calc_percentage(geometry_data.get('line_count', 0)):.1f}%",
             f"{get_entity_length('lines'):.2f}"],
            ['Arcs', str(geometry_data.get('arc_count', 0)), 
             f"{calc_percentage(geometry_data.get('arc_count', 0)):.1f}%",
             f"{get_entity_length('arcs'):.2f}"],
            ['Circles', str(geometry_data.get('circle_count', 0)), 
             f"{calc_percentage(geometry_data.get('circle_count', 0)):.1f}%",
             f"{get_entity_length('circles'):.2f}"],
            ['Polylines', str(geometry_data.get('polyline_count', 0)), 
             f"{calc_percentage(geometry_data.get('polyline_count', 0)):.1f}%",
             f"{get_entity_length('polylines'):.2f}"],
            ['Splines', str(geometry_data.get('spline_count', 0)), 
             f"{calc_percentage(geometry_data.get('spline_count', 0)):.1f}%",
             f"{get_entity_length('splines'):.2f}"],
            ['Ellipses', str(geometry_data.get('ellipse_count', 0)), 
             f"{calc_percentage(geometry_data.get('ellipse_count', 0)):.1f}%",
             f"{get_entity_length('ellipses'):.2f}"],
            ['<b>TOTAL</b>', f'<b>{total_entities}</b>', '<b>100.0%</b>', 
             f'<b>{geometry_data.get("total_length", 0):.2f}</b>']
        ]
        
        entity_table = Table(entity_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.3*inch])
        entity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, self.border_color),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, self.light_gray]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f9fafb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(entity_table)
        return elements
    
    def _create_detailed_cost_breakdown(self, geometry_data: Dict, material: str, thickness: float,
                                       machining_time: float, total_cost: float):
        """Create detailed cost breakdown section"""
        elements = []
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=12
        )
        elements.append(Paragraph("Cost Breakdown", section_header))
        
        # Calculate individual costs
        from cost_calculator import CostCalculator
        calc = CostCalculator()
        material_cost = calc.calculate_material_cost(geometry_data['total_length'], thickness, material)
        labor_cost = calc.calculate_labor_cost(machining_time, material)
        setup_cost = 500.00  # Standard setup fee
        
        subtotal = material_cost + labor_cost + setup_cost
        tax_rate = 0.18  # 18% GST
        tax_amount = subtotal * tax_rate
        # Use provided total_cost (it already includes all calculations)
        final_total = total_cost
        
        # Cost breakdown table
        cost_data = [
            ['<b>Description</b>', '<b>Specifications</b>', '<b>Quantity</b>', '<b>Unit Price</b>', '<b>Amount (₹)</b>'],
            ['Material Cost', f"{material.capitalize()} ({thickness}mm)", 
             f"{geometry_data.get('total_length', 0):.1f} mm", 
             f"₹{material_cost/max(geometry_data.get('total_length', 1), 1):.4f}/mm",
             f"₹{material_cost:,.2f}"],
            ['Labor Cost', f"CNC Machining", 
             f"{machining_time:.1f} min", 
             f"₹{calc.machine_rates.get(material.lower(), 3000.0)/60:.2f}/min",
             f"₹{labor_cost:,.2f}"],
            ['Setup & Tooling', 'Standard setup and tool change', '1', '₹500.00', '₹500.00'],
            ['', '', '', '<b>Subtotal:</b>', f'<b>₹{subtotal:,.2f}</b>'],
            ['', '', '', '<b>GST (18%):</b>', f'<b>₹{tax_amount:,.2f}</b>'],
            ['', '', '', '<b>TOTAL:</b>', f'<b>₹{final_total:,.2f}</b>']
        ]
        
        cost_table = Table(cost_data, colWidths=[1.5*inch, 1.8*inch, 1*inch, 1.2*inch, 1.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('ALIGN', (3, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -4), 9),
            ('FONTNAME', (3, -3), (4, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (3, -3), (4, -1), 10),
            ('FONTSIZE', (0, -1), (4, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.border_color),
            ('BACKGROUND', (0, 1), (-1, -4), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, self.light_gray]),
            ('BACKGROUND', (0, -3), (-1, -1), colors.HexColor('#f9fafb')),
            ('LINEBELOW', (3, -1), (4, -1), 2, self.primary_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(cost_table)
        
        # Additional notes
        elements.append(Spacer(1, 12))
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6b7280'),
            fontStyle='italic',
            alignment=TA_LEFT
        )
        elements.append(Paragraph(
            f"<i>Note: Estimated machining time: {machining_time:.1f} minutes | "
            f"Feed rate: {calc.feed_rates.get(material.lower(), 300)} mm/min | "
            f"Quote valid for 30 days</i>", 
            note_style
        ))
        
        return elements
    
    def _create_professional_terms(self):
        """Create professional terms and conditions section"""
        elements = []
        
        section_header = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.primary_color,
            fontName='Helvetica-Bold',
            spaceAfter=12
        )
        elements.append(Paragraph("Terms & Conditions", section_header))
        
        # Two-column terms layout
        terms_left = [
            "• <b>Payment Terms:</b> Net 30 days from invoice date",
            "• <b>Lead Time:</b> 2-3 weeks from order confirmation",
            "• <b>Minimum Order:</b> 1 piece",
            "• <b>Material Availability:</b> Subject to stock",
        ]
        
        terms_right = [
            "• <b>Tolerances:</b> ±0.1mm unless specified",
            "• <b>Surface Finish:</b> As machined (Ra 3.2)",
            "• <b>Quote Validity:</b> 30 days from issue date",
            "• <b>Warranty:</b> 90 days on workmanship",
        ]
        
        terms_style = ParagraphStyle(
            'TermsText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.dark_gray,
            alignment=TA_LEFT,
            spaceAfter=6,
            leading=13
        )
        
        left_content = [Paragraph(term, terms_style) for term in terms_left]
        right_content = [Paragraph(term, terms_style) for term in terms_right]
        
        # Create tables for each column
        left_table = Table([[content] for content in left_content], colWidths=[3.5*inch])
        left_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, -1), 0),
            ('TOPPADDING', (0, 0), (0, -1), 0),
            ('BOTTOMPADDING', (0, 0), (0, -1), 0),
        ]))
        
        right_table = Table([[content] for content in right_content], colWidths=[3.5*inch])
        right_table.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (0, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, -1), 0),
            ('TOPPADDING', (0, 0), (0, -1), 0),
            ('BOTTOMPADDING', (0, 0), (0, -1), 0),
        ]))
        
        # Combine
        combined_data = [[left_table, right_table]]
        combined_table = Table(combined_data, colWidths=[3.5*inch, 3.5*inch])
        combined_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        elements.append(combined_table)
        return elements
    
    def _create_signature_section(self):
        """Create signature section"""
        elements = []
        
        signature_data = [
            ['', ''],
            ['', ''],
            ['', ''],
            ['_________________________', '_________________________'],
            ['Prepared By', 'Authorized Signature'],
        ]
        
        signature_table = Table(signature_data, colWidths=[3.5*inch, 3.5*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, -2), (-1, -2), 9),
            ('FONTSIZE', (0, -1), (-1, -1), 8),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#6b7280')),
            ('TOPPADDING', (0, -2), (-1, -2), 20),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 0),
        ]))
        
        elements.append(signature_table)
        return elements
