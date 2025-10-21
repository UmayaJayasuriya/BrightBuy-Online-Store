"""
PDF Report Generation Routes
Generates formatted PDF reports using database views
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.security import get_admin_user
from datetime import datetime, date
from io import BytesIO
from typing import Optional
import mysql.connector

# Import ReportLab for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.platypus import Image as RLImage
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
except ImportError:
    raise ImportError("Please install reportlab: pip install reportlab")

router = APIRouter(prefix="/reports", tags=["reports"])


def create_header(elements, title, subtitle=None):
    """Create a styled header for PDF reports"""
    styles = getSampleStyleSheet()
    
    # Main title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(title, title_style))
    
    # Subtitle
    if subtitle:
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(subtitle, subtitle_style))
    
    # Divider
    elements.append(Spacer(1, 0.2*inch))
    return elements


def create_footer_text():
    """Generate footer text with timestamp"""
    return f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | BrightBuy Sales System"


@router.get("/quarterly-sales/{year}")
def generate_quarterly_sales_report(
    year: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """
    Generate PDF report for quarterly sales of a given year
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Fetch data from view
        cursor.execute("""
            SELECT * FROM quarterly_sales_report 
            WHERE year = %s 
            ORDER BY quarter ASC
        """, (year,))
        
        data = cursor.fetchall()
        cursor.close()
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No sales data found for year {year}")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Header
        elements = create_header(
            elements,
            f"Quarterly Sales Report - {year}",
            f"Complete sales analysis for all quarters in {year}"
        )
        
        # Summary statistics
        total_revenue = sum(row['total_revenue'] for row in data)
        total_orders = sum(row['total_orders'] for row in data)
        
        summary_style = getSampleStyleSheet()['Normal']
        summary_style.fontSize = 11
        summary_style.spaceAfter = 15
        
        summary_text = f"""
        <b>Annual Summary:</b><br/>
        Total Revenue: <b>${total_revenue:,.2f}</b> | 
        Total Orders: <b>{total_orders:,}</b> | 
        Average Order Value: <b>${total_revenue/total_orders if total_orders > 0 else 0:,.2f}</b>
        """
        elements.append(Paragraph(summary_text, summary_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Table data
        table_data = [
            ['Quarter', 'Total Orders', 'Customers', 'Revenue', 'Avg Order', 'Items Sold']
        ]
        
        for row in data:
            table_data.append([
                row['quarter_label'],
                f"{row['total_orders']:,}",
                f"{row['unique_customers']:,}",
                f"${row['total_revenue']:,.2f}",
                f"${row['average_order_value']:,.2f}",
                f"{row['total_items_sold']:,}"
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.3*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(create_footer_text(), footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=quarterly_sales_{year}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/top-selling-products")
def generate_top_selling_products_report(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(20, description="Number of top products to show"),
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """
    Generate PDF report for top-selling products in a given period
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Build query based on date filters
        if start_date and end_date:
            query = """
                SELECT p.product_id, p.product_name, c.category_name,
                       v.variant_name, v.SKU,
                       SUM(oi.quantity) as total_quantity_sold,
                       SUM(oi.quantity * oi.price) as total_revenue,
                       AVG(oi.price) as average_price,
                       COUNT(DISTINCT oi.order_id) as number_of_orders
                FROM order_item oi
                JOIN variant v ON oi.variant_id = v.variant_id
                JOIN product p ON v.product_id = p.product_id
                LEFT JOIN category c ON p.category_id = c.category_id
                JOIN orders o ON oi.order_id = o.order_id
                WHERE DATE(o.order_date) BETWEEN %s AND %s
                GROUP BY p.product_id, p.product_name, c.category_name, v.variant_name, v.SKU
                ORDER BY total_quantity_sold DESC
                LIMIT %s
            """
            cursor.execute(query, (start_date, end_date, limit))
            period_text = f"Period: {start_date} to {end_date}"
        else:
            cursor.execute("SELECT * FROM top_selling_products LIMIT %s", (limit,))
            period_text = "All Time"
        
        data = cursor.fetchall()
        cursor.close()
        
        if not data:
            raise HTTPException(status_code=404, detail="No sales data found for the specified period")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Header
        elements = create_header(
            elements,
            "Top Selling Products Report",
            period_text
        )
        
        # Summary
        total_revenue = sum(row['total_revenue'] for row in data)
        total_quantity = sum(row['total_quantity_sold'] for row in data)
        
        summary_style = getSampleStyleSheet()['Normal']
        summary_style.fontSize = 11
        summary_style.spaceAfter = 15
        
        summary_text = f"""
        <b>Summary:</b><br/>
        Top {len(data)} Products | 
        Total Units Sold: <b>{total_quantity:,}</b> | 
        Total Revenue: <b>${total_revenue:,.2f}</b>
        """
        elements.append(Paragraph(summary_text, summary_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Table data
        table_data = [
            ['Rank', 'Product', 'Category', 'Variant', 'Units Sold', 'Revenue', 'Avg Price']
        ]
        
        for idx, row in enumerate(data, 1):
            table_data.append([
                str(idx),
                row['product_name'][:20],
                (row['category_name'] or 'N/A')[:15],
                row['variant_name'][:15],
                f"{row['total_quantity_sold']:,}",
                f"${row['total_revenue']:,.2f}",
                f"${row['average_price']:,.2f}"
            ])
        
        # Create table with adjusted widths
        table = Table(table_data, colWidths=[0.5*inch, 1.8*inch, 1.2*inch, 1.2*inch, 0.9*inch, 1.1*inch, 0.9*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#E8F8F5')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle('Footer', parent=getSampleStyleSheet()['Normal'],
                                     fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(create_footer_text(), footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        filename = f"top_selling_products_{start_date or 'all_time'}_to_{end_date or 'now'}.pdf"
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/category-orders")
def generate_category_orders_report(
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """
    Generate PDF report for category-wise total number of orders
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category_order_summary ORDER BY total_revenue DESC")
        data = cursor.fetchall()
        cursor.close()
        
        if not data:
            raise HTTPException(status_code=404, detail="No category data found")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Header
        elements = create_header(
            elements,
            "Category-wise Order Summary",
            "Complete analysis of orders and revenue by product category"
        )
        
        # Summary
        total_orders = sum(row['total_orders'] for row in data)
        total_revenue = sum(row['total_revenue'] for row in data)
        
        summary_style = getSampleStyleSheet()['Normal']
        summary_style.fontSize = 11
        summary_style.spaceAfter = 15
        
        summary_text = f"""
        <b>Overall Summary:</b><br/>
        Total Categories: <b>{len(data)}</b> | 
        Total Orders: <b>{total_orders:,}</b> | 
        Total Revenue: <b>${total_revenue:,.2f}</b>
        """
        elements.append(Paragraph(summary_text, summary_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Table data
        table_data = [
            ['Category', 'Orders', 'Items Sold', 'Revenue', 'Avg Order', 'Products']
        ]
        
        for row in data:
            table_data.append([
                row['category_name'][:25],
                f"{row['total_orders']:,}",
                f"{row['total_items_sold']:,}",
                f"${row['total_revenue']:,.2f}",
                f"${row['average_order_value']:,.2f}",
                f"{row['unique_products']}"
            ])
        
        # Create table
        table = Table(table_data, colWidths=[2*inch, 1*inch, 1*inch, 1.3*inch, 1.2*inch, 0.8*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FADBD8')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle('Footer', parent=getSampleStyleSheet()['Normal'],
                                     fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(create_footer_text(), footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=category_orders_summary.pdf"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/customer-orders/{user_id}")
def generate_customer_orders_report(
    user_id: int,
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """
    Generate PDF report for customer-wise order summary and payment status
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get customer summary
        cursor.execute("""
            SELECT * FROM customer_summary_statistics 
            WHERE user_id = %s
        """, (user_id,))
        
        customer_summary = cursor.fetchone()
        
        if not customer_summary:
            raise HTTPException(status_code=404, detail=f"No orders found for customer ID {user_id}")
        
        # Get detailed orders
        cursor.execute("""
            SELECT * FROM customer_order_payment_summary 
            WHERE user_id = %s 
            ORDER BY order_date DESC
        """, (user_id,))
        
        orders = cursor.fetchall()
        cursor.close()
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Header
        elements = create_header(
            elements,
            "Customer Order & Payment Report",
            f"Complete order history for {customer_summary['full_name']} ({customer_summary['user_name']})"
        )
        
        # Customer info
        info_style = getSampleStyleSheet()['Normal']
        info_style.fontSize = 10
        info_style.spaceAfter = 10
        
        customer_info = f"""
        <b>Customer Information:</b><br/>
        Name: <b>{customer_summary['full_name']}</b> | 
        Email: <b>{customer_summary['email']}</b> | 
        User ID: <b>{customer_summary['user_id']}</b>
        """
        elements.append(Paragraph(customer_info, info_style))
        
        # Summary statistics
        summary_text = f"""
        <b>Order Statistics:</b><br/>
        Total Orders: <b>{customer_summary['total_orders']}</b> | 
        Total Spent: <b>${customer_summary['total_spent']:,.2f}</b> | 
        Avg Order: <b>${customer_summary['average_order_value']:,.2f}</b><br/>
        Completed Payments: <b>{customer_summary['completed_payments']}</b> | 
        Pending Payments: <b>{customer_summary['pending_payments']}</b> | 
        Delivered: <b>{customer_summary['delivered_orders']}</b>
        """
        elements.append(Paragraph(summary_text, info_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Orders table
        table_data = [
            ['Order ID', 'Date', 'Amount', 'Payment', 'Status', 'Delivery', 'Items']
        ]
        
        for order in orders:
            order_date = order['order_date'].strftime('%Y-%m-%d') if order['order_date'] else 'N/A'
            payment_status = (order['payment_status'] or 'N/A').upper()
            delivery_status = (order['delivery_status'] or 'N/A').upper()
            
            table_data.append([
                str(order['order_id']),
                order_date,
                f"${order['total_amount']:,.2f}",
                (order['payment_method'] or 'N/A').upper(),
                payment_status[:8],
                delivery_status[:8],
                str(order['items_in_order'])
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.7*inch, 1*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.6*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9B59B6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4ECF7')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle('Footer', parent=getSampleStyleSheet()['Normal'],
                                     fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(create_footer_text(), footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=customer_orders_{user_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/all-customers-summary")
def generate_all_customers_summary_report(
    db: mysql.connector.MySQLConnection = Depends(get_db),
    admin = Depends(get_admin_user)
):
    """
    Generate PDF report for all customers with order and payment summary
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM customer_summary_statistics 
            ORDER BY total_spent DESC 
            LIMIT 50
        """)
        
        data = cursor.fetchall()
        cursor.close()
        
        if not data:
            raise HTTPException(status_code=404, detail="No customer data found")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Header
        elements = create_header(
            elements,
            "All Customers Summary Report",
            f"Top {len(data)} customers by total spending"
        )
        
        # Summary
        total_revenue = sum(row['total_spent'] for row in data)
        total_orders = sum(row['total_orders'] for row in data)
        
        summary_style = getSampleStyleSheet()['Normal']
        summary_style.fontSize = 11
        summary_style.spaceAfter = 15
        
        summary_text = f"""
        <b>Overview:</b><br/>
        Total Customers: <b>{len(data)}</b> | 
        Total Orders: <b>{total_orders:,}</b> | 
        Total Revenue: <b>${total_revenue:,.2f}</b>
        """
        elements.append(Paragraph(summary_text, summary_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Table data
        table_data = [
            ['Name', 'Email', 'Orders', 'Total Spent', 'Avg Order', 'Completed', 'Pending']
        ]
        
        for row in data:
            table_data.append([
                row['user_name'][:15],
                row['email'][:25],
                str(row['total_orders']),
                f"${row['total_spent']:,.2f}",
                f"${row['average_order_value']:,.2f}",
                str(row['completed_payments']),
                str(row['pending_payments'])
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1.1*inch, 1.8*inch, 0.7*inch, 1*inch, 0.9*inch, 0.8*inch, 0.7*inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle('Footer', parent=getSampleStyleSheet()['Normal'],
                                     fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(create_footer_text(), footer_style))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=all_customers_summary.pdf"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
