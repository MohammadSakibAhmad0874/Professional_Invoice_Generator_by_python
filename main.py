import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

class InvoiceGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Invoice Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        
        # Variables
        self.items = []
        self.logo_path = None  # Store logo path
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Professional Invoice Generator", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Input tab
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="Invoice Details")
        
        # Preview tab
        self.preview_frame = ttk.Frame(notebook)
        notebook.add(self.preview_frame, text="Invoice Preview")
        
        self.setup_input_tab(input_frame)
        self.setup_preview_tab()
        
    def setup_input_tab(self, parent):
        # Create scrollable frame
        canvas = tk.Canvas(parent, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Company Information Section
        company_frame = ttk.LabelFrame(scrollable_frame, text="Company Information", padding=15)
        company_frame.pack(fill='x', padx=10, pady=5)
        
        # Company fields
        ttk.Label(company_frame, text="Company Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.company_name = ttk.Entry(company_frame, width=40)
        self.company_name.grid(row=0, column=1, padx=10, pady=2)
        
        ttk.Label(company_frame, text="Address:").grid(row=1, column=0, sticky='w', pady=2)
        self.company_address = tk.Text(company_frame, width=40, height=3)
        self.company_address.grid(row=1, column=1, padx=10, pady=2)
        
        ttk.Label(company_frame, text="Phone:").grid(row=2, column=0, sticky='w', pady=2)
        self.company_phone = ttk.Entry(company_frame, width=40)
        self.company_phone.grid(row=2, column=1, padx=10, pady=2)
        
        ttk.Label(company_frame, text="Email:").grid(row=3, column=0, sticky='w', pady=2)
        self.company_email = ttk.Entry(company_frame, width=40)
        self.company_email.grid(row=3, column=1, padx=10, pady=2)
        
        # Logo upload section
        ttk.Label(company_frame, text="Company Logo:").grid(row=4, column=0, sticky='w', pady=2)
        logo_frame = ttk.Frame(company_frame)
        logo_frame.grid(row=4, column=1, padx=10, pady=2, sticky='w')
        
        self.logo_status = ttk.Label(logo_frame, text="No logo uploaded")
        self.logo_status.pack(side='left', padx=(0, 10))
        
        ttk.Button(logo_frame, text="Upload Logo", command=self.upload_logo,
                  style='Custom.TButton').pack(side='left')
        
        # Customer Information Section
        customer_frame = ttk.LabelFrame(scrollable_frame, text="Customer Information", padding=15)
        customer_frame.pack(fill='x', padx=10, pady=5)
        
        # Customer fields
        ttk.Label(customer_frame, text="Customer Name:").grid(row=0, column=0, sticky='w', pady=2)
        self.customer_name = ttk.Entry(customer_frame, width=40)
        self.customer_name.grid(row=0, column=1, padx=10, pady=2)
        
        ttk.Label(customer_frame, text="Customer Address:").grid(row=1, column=0, sticky='w', pady=2)
        self.customer_address = tk.Text(customer_frame, width=40, height=3)
        self.customer_address.grid(row=1, column=1, padx=10, pady=2)
        
        ttk.Label(customer_frame, text="Customer Phone:").grid(row=2, column=0, sticky='w', pady=2)
        self.customer_phone = ttk.Entry(customer_frame, width=40)
        self.customer_phone.grid(row=2, column=1, padx=10, pady=2)
        
        ttk.Label(customer_frame, text="Customer Email:").grid(row=3, column=0, sticky='w', pady=2)
        self.customer_email = ttk.Entry(customer_frame, width=40)
        self.customer_email.grid(row=3, column=1, padx=10, pady=2)
        
        # Invoice Details Section
        invoice_frame = ttk.LabelFrame(scrollable_frame, text="Invoice Details", padding=15)
        invoice_frame.pack(fill='x', padx=10, pady=5)
        
        # Invoice fields
        ttk.Label(invoice_frame, text="Invoice Number:").grid(row=0, column=0, sticky='w', pady=2)
        self.invoice_number = ttk.Entry(invoice_frame, width=20)
        self.invoice_number.grid(row=0, column=1, padx=10, pady=2)
        self.invoice_number.insert(0, f"INV-{datetime.now().strftime('%Y%m%d%H%M')}")
        
        ttk.Label(invoice_frame, text="Invoice Date:").grid(row=0, column=2, sticky='w', pady=2)
        self.invoice_date = ttk.Entry(invoice_frame, width=20)
        self.invoice_date.grid(row=0, column=3, padx=10, pady=2)
        self.invoice_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Label(invoice_frame, text="Due Date:").grid(row=1, column=0, sticky='w', pady=2)
        self.due_date = ttk.Entry(invoice_frame, width=20)
        self.due_date.grid(row=1, column=1, padx=10, pady=2)
        
        ttk.Label(invoice_frame, text="Payment Terms:").grid(row=1, column=2, sticky='w', pady=2)
        self.payment_terms = ttk.Entry(invoice_frame, width=20)
        self.payment_terms.grid(row=1, column=3, padx=10, pady=2)
        self.payment_terms.insert(0, "Net 30")
        
        # Items Section
        items_frame = ttk.LabelFrame(scrollable_frame, text="Invoice Items", padding=15)
        items_frame.pack(fill='x', padx=10, pady=5)
        
        # Item input fields
        item_input_frame = ttk.Frame(items_frame)
        item_input_frame.pack(fill='x', pady=5)
        
        ttk.Label(item_input_frame, text="Description:").grid(row=0, column=0, sticky='w', pady=2)
        self.item_desc = ttk.Entry(item_input_frame, width=30)
        self.item_desc.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(item_input_frame, text="Quantity:").grid(row=0, column=2, sticky='w', pady=2)
        self.item_qty = ttk.Entry(item_input_frame, width=10)
        self.item_qty.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(item_input_frame, text="Rate:").grid(row=0, column=4, sticky='w', pady=2)
        self.item_rate = ttk.Entry(item_input_frame, width=10)
        self.item_rate.grid(row=0, column=5, padx=5, pady=2)
        
        ttk.Button(item_input_frame, text="Add Item", command=self.add_item,
                  style='Custom.TButton').grid(row=0, column=6, padx=10, pady=2)
        
        # Items list
        self.items_tree = ttk.Treeview(items_frame, columns=('Description', 'Quantity', 'Rate', 'Amount'), 
                                      show='headings', height=8)
        self.items_tree.heading('Description', text='Description')
        self.items_tree.heading('Quantity', text='Quantity')
        self.items_tree.heading('Rate', text='Rate')
        self.items_tree.heading('Amount', text='Amount')
        
        self.items_tree.column('Description', width=300)
        self.items_tree.column('Quantity', width=100)
        self.items_tree.column('Rate', width=100)
        self.items_tree.column('Amount', width=100)
        
        self.items_tree.pack(fill='x', pady=5)
        
        # Remove item button
        ttk.Button(items_frame, text="Remove Selected Item", command=self.remove_item,
                  style='Custom.TButton').pack(pady=5)
        
        # Tax and Total Section
        totals_frame = ttk.LabelFrame(scrollable_frame, text="Totals", padding=15)
        totals_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(totals_frame, text="Tax Rate (%):").grid(row=0, column=0, sticky='w', pady=2)
        self.tax_rate = ttk.Entry(totals_frame, width=10)
        self.tax_rate.grid(row=0, column=1, padx=10, pady=2)
        self.tax_rate.insert(0, "0")
        
        ttk.Label(totals_frame, text="Discount (%):").grid(row=0, column=2, sticky='w', pady=2)
        self.discount = ttk.Entry(totals_frame, width=10)
        self.discount.grid(row=0, column=3, padx=10, pady=2)
        self.discount.insert(0, "0")
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        ttk.Button(button_frame, text="Generate Invoice", command=self.generate_invoice,
                  style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save as Text", command=self.save_invoice,
                  style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Download as PDF", command=self.download_pdf,
                  style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Download as JPG", command=self.download_jpg,
                  style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all,
                  style='Custom.TButton').pack(side='left', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_preview_tab(self):
        # Create scrollable text widget for preview
        self.preview_text = tk.Text(self.preview_frame, wrap=tk.WORD, width=100, height=40,
                                   font=('Courier', 10), bg='white', fg='black')
        
        preview_scrollbar = ttk.Scrollbar(self.preview_frame, orient="vertical", 
                                        command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        preview_scrollbar.pack(side="right", fill="y", pady=10)
        
    def upload_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Company Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Validate image
                img = Image.open(file_path)
                self.logo_path = file_path
                self.logo_status.config(text=os.path.basename(file_path))
                messagebox.showinfo("Success", "Logo uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.logo_path = None
                self.logo_status.config(text="Invalid image")
        
    def add_item(self):
        desc = self.item_desc.get().strip()
        qty = self.item_qty.get().strip()
        rate = self.item_rate.get().strip()
        
        if not desc or not qty or not rate:
            messagebox.showerror("Error", "Please fill in all item fields")
            return
            
        try:
            qty = float(qty)
            rate = float(rate)
            amount = qty * rate
            
            self.items.append({
                'description': desc,
                'quantity': qty,
                'rate': rate,
                'amount': amount
            })
            
            self.items_tree.insert('', 'end', values=(desc, qty, f"₨{rate:.2f}", f"₨{amount:.2f}"))
            
            # Clear input fields
            self.item_desc.delete(0, tk.END)
            self.item_qty.delete(0, tk.END)
            self.item_rate.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Quantity and Rate must be numbers")
            
    def remove_item(self):
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
            
        # Get the index of selected item
        item_index = self.items_tree.index(selected[0])
        
        # Remove from items list and tree
        self.items.pop(item_index)
        self.items_tree.delete(selected[0])
        
    def calculate_totals(self):
        subtotal = sum(item['amount'] for item in self.items)
        
        try:
            discount_percent = float(self.discount.get() or 0)
            tax_percent = float(self.tax_rate.get() or 0)
        except ValueError:
            discount_percent = 0
            tax_percent = 0
            
        discount_amount = subtotal * (discount_percent / 100)
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * (tax_percent / 100)
        total = taxable_amount + tax_amount
        
        return subtotal, discount_amount, tax_amount, total
        
    def generate_invoice(self):
        if not self.items:
            messagebox.showerror("Error", "Please add at least one item")
            return
            
        subtotal, discount_amount, tax_amount, total = self.calculate_totals()
        
        # Generate invoice content
        invoice_content = self.create_invoice_template(subtotal, discount_amount, tax_amount, total)
        
        # Display in preview tab
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, invoice_content)
        
        messagebox.showinfo("Success", "Invoice generated successfully! Check the Preview tab.")
        
    def create_invoice_template(self, subtotal, discount_amount, tax_amount, total):
        company_addr = self.company_address.get(1.0, tk.END).strip()
        customer_addr = self.customer_address.get(1.0, tk.END).strip()
        
        logo_info = f"Logo: {os.path.basename(self.logo_path)}" if self.logo_path else "No logo"
        
        invoice_template = f"""
{'='*80}
                           INVOICE
{'='*80}

From:                                    To:
{self.company_name.get():<35} {self.customer_name.get()}
{company_addr.replace(chr(10), ', '):<35} {customer_addr.replace(chr(10), ', ')}
Phone: {self.company_phone.get():<27} Phone: {self.customer_phone.get()}
Email: {self.company_email.get():<27} Email: {self.customer_email.get()}
{logo_info}

{'-'*80}

Invoice Details:
Invoice Number: {self.invoice_number.get():<20} Invoice Date: {self.invoice_date.get()}
Due Date: {self.due_date.get():<26} Payment Terms: {self.payment_terms.get()}

{'-'*80}

ITEMS:
{'-'*80}
{'Description':<40} {'Qty':<8} {'Rate':<12} {'Amount':<12}
{'-'*80}
"""
        
        # Add items
        for item in self.items:
            invoice_template += f"{item['description']:<40} {item['quantity']:<8.1f} ₨{item['rate']:<11.2f} ₨{item['amount']:<11.2f}\n"
            
        invoice_template += f"""
{'-'*80}
                                                    Subtotal: ₨{subtotal:>11.2f}
                                                    Discount: ₨{discount_amount:>11.2f}
                                                    Tax:      ₨{tax_amount:>11.2f}
                                                    {'='*20}
                                                    TOTAL:    ₨{total:>11.2f}
{'-'*80}

Payment Instructions:


{'-'*80}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        return invoice_template
        
    def save_invoice(self):
        invoice_content = self.preview_text.get(1.0, tk.END)
        if not invoice_content.strip():
            messagebox.showerror("Error", "Please generate an invoice first")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Invoice"
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(invoice_content)
                messagebox.showinfo("Success", f"Invoice saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save invoice: {str(e)}")
                
    def clear_all(self):
        # Clear all input fields
        self.company_name.delete(0, tk.END)
        self.company_address.delete(1.0, tk.END)
        self.company_phone.delete(0, tk.END)
        self.company_email.delete(0, tk.END)
        self.logo_path = None
        self.logo_status.config(text="No logo uploaded")
        
        self.customer_name.delete(0, tk.END)
        self.customer_address.delete(1.0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        
        self.invoice_number.delete(0, tk.END)
        self.invoice_number.insert(0, f"INV-{datetime.now().strftime('%Y%m%d%H%M')}")
        self.invoice_date.delete(0, tk.END)
        self.invoice_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.due_date.delete(0, tk.END)
        self.payment_terms.delete(0, tk.END)
        self.payment_terms.insert(0, "Net 30")
        
        self.tax_rate.delete(0, tk.END)
        self.tax_rate.insert(0, "0")
        self.discount.delete(0, tk.END)
        self.discount.insert(0, "0")
        
        # Clear items
        self.items.clear()
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        # Clear preview
        self.preview_text.delete(1.0, tk.END)
        
        messagebox.showinfo("Success", "All fields cleared")

    def download_pdf(self):
        if not self.items:
            messagebox.showerror("Error", "Please generate an invoice first")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Invoice as PDF"
        )
        
        if filename:
            try:
                self.create_pdf_invoice(filename)
                messagebox.showinfo("Success", f"Invoice saved as PDF: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")
                
    def download_jpg(self):
        if not self.items:
            messagebox.showerror("Error", "Please generate an invoice first")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Invoice as Image"
        )
        
        if filename:
            try:
                self.create_image_invoice(filename)
                messagebox.showinfo("Success", f"Invoice saved as image: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                
    def create_pdf_invoice(self, filename):
        subtotal, discount_amount, tax_amount, total = self.calculate_totals()
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        styles = getSampleStyleSheet()
        
        # Add logo if available
        if self.logo_path:
            try:
                # Get image dimensions to maintain aspect ratio
                img = Image.open(self.logo_path)
                img_width, img_height = img.size
                aspect = img_width / img_height
                new_height = 0.75 * inch
                new_width = new_height * aspect
                
                # Create logo image
                logo = RLImage(self.logo_path, width=new_width, height=new_height)
                elements.append(logo)
                elements.append(Spacer(1, 12))
            except Exception as e:
                print(f"Error loading logo: {e}")
        
        # Title
        title_style = styles['Title']
        title_style.alignment = 1  # Center alignment
        title = Paragraph("INVOICE", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Company and Customer info table
        company_addr = self.company_address.get(1.0, tk.END).strip().replace('\n', '<br/>')
        customer_addr = self.customer_address.get(1.0, tk.END).strip().replace('\n', '<br/>')
        
        info_data = [
            ['From:', 'To:'],
            [f"<b>{self.company_name.get()}</b><br/>{company_addr}<br/>Phone: {self.company_phone.get()}<br/>Email: {self.company_email.get()}",
             f"<b>{self.customer_name.get()}</b><br/>{customer_addr}<br/>Phone: {self.customer_phone.get()}<br/>Email: {self.customer_email.get()}"]
        ]
        
        info_table = Table(info_data, colWidths=[3*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 12))
        
        # Invoice details
        details_data = [
            ['Invoice Number:', self.invoice_number.get(), 'Invoice Date:', self.invoice_date.get()],
            ['Due Date:', self.due_date.get(), 'Payment Terms:', self.payment_terms.get()]
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 12))
        
        # Items table
        items_data = [['Description', 'Quantity', 'Rate', 'Amount']]
        for item in self.items:
            items_data.append([
                item['description'],
                f"{item['quantity']:.1f}",
                f"₨{item['rate']:.2f}",
                f"₨{item['amount']:.2f}"
            ])
            
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        items_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 12))
        
        # Totals table
        totals_data = [
            ['Subtotal:', f"₨{subtotal:.2f}"],
            ['Discount:', f"₨{discount_amount:.2f}"],
            ['Tax:', f"₨{tax_amount:.2f}"],
            ['TOTAL:', f"₨{total:.2f}"]
        ]
        
        totals_table = Table(totals_data, colWidths=[4*inch, 2*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 2), 'Helvetica'),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 2), 10),
            ('FONTSIZE', (0, 3), (-1, 3), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 24))
        
       
        
        # Build PDF
        doc.build(elements)
        
    def create_image_invoice(self, filename):
        subtotal, discount_amount, tax_amount, total = self.calculate_totals()
        
        # Create image
        img_width, img_height = 800, 1100
        img = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a system font
            title_font = ImageFont.truetype("arial.ttf", 24)
            header_font = ImageFont.truetype("arial.ttf", 14)
            normal_font = ImageFont.truetype("arial.ttf", 12)
            small_font = ImageFont.truetype("arial.ttf", 10)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        y_pos = 30
        
        # Add logo if available
        if self.logo_path:
            try:
                logo_img = Image.open(self.logo_path)
                # Resize logo to fit (max 100px height)
                logo_img = ImageOps.contain(logo_img, (200, 80))
                logo_img = logo_img.convert("RGBA")
                
                # Paste logo at top center
                logo_x = (img_width - logo_img.width) // 2
                img.paste(logo_img, (logo_x, 20), logo_img)
                
                # Adjust y position below logo
                y_pos = 20 + logo_img.height + 20
            except Exception as e:
                print(f"Error loading logo: {e}")
        
        # Title
        title_text = "INVOICE"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((img_width - title_width) // 2, y_pos), title_text, fill='black', font=title_font)
        y_pos += 50
        
        # Draw line
        draw.line([(50, y_pos), (img_width - 50, y_pos)], fill='black', width=2)
        y_pos += 20
        
        # Company and Customer info
        draw.text((50, y_pos), "From:", fill='black', font=header_font)
        draw.text((400, y_pos), "To:", fill='black', font=header_font)
        y_pos += 25
        
        # Company info
        company_info = [
            self.company_name.get(),
            self.company_address.get(1.0, tk.END).strip(),
            f"Phone: {self.company_phone.get()}",
            f"Email: {self.company_email.get()}"
        ]
        
        # Customer info
        customer_info = [
            self.customer_name.get(),
            self.customer_address.get(1.0, tk.END).strip(),
            f"Phone: {self.customer_phone.get()}",
            f"Email: {self.customer_email.get()}"
        ]
        
        for i, (comp_line, cust_line) in enumerate(zip(company_info, customer_info)):
            draw.text((50, y_pos + i * 20), comp_line, fill='black', font=normal_font)
            draw.text((400, y_pos + i * 20), cust_line, fill='black', font=normal_font)
        
        y_pos += 100
        
        # Invoice details
        draw.line([(50, y_pos), (img_width - 50, y_pos)], fill='black', width=1)
        y_pos += 15
        
        invoice_details = [
            f"Invoice Number: {self.invoice_number.get()}",
            f"Invoice Date: {self.invoice_date.get()}",
            f"Due Date: {self.due_date.get()}",
            f"Payment Terms: {self.payment_terms.get()}"
        ]
        
        for i, detail in enumerate(invoice_details):
            x_pos = 50 if i % 2 == 0 else 400
            y_offset = (i // 2) * 20
            draw.text((x_pos, y_pos + y_offset), detail, fill='black', font=normal_font)
        
        y_pos += 60
        
        # Items header
        draw.line([(50, y_pos), (img_width - 50, y_pos)], fill='black', width=1)
        y_pos += 15
        
        # Items table header
        draw.text((50, y_pos), "Description", fill='black', font=header_font)
        draw.text((400, y_pos), "Qty", fill='black', font=header_font)
        draw.text((500, y_pos), "Rate", fill='black', font=header_font)
        draw.text((600, y_pos), "Amount", fill='black', font=header_font)
        y_pos += 25
        
        draw.line([(50, y_pos), (img_width - 50, y_pos)], fill='black', width=1)
        y_pos += 15
        
        # Items
        for item in self.items:
            draw.text((50, y_pos), item['description'][:40], fill='black', font=normal_font)
            draw.text((400, y_pos), f"{item['quantity']:.1f}", fill='black', font=normal_font)
            draw.text((500, y_pos), f"₨{item['rate']:.2f}", fill='black', font=normal_font)
            draw.text((600, y_pos), f"₨{item['amount']:.2f}", fill='black', font=normal_font)
            y_pos += 20
        
        y_pos += 20
        draw.line([(50, y_pos), (img_width - 50, y_pos)], fill='black', width=1)
        y_pos += 15
        
        # Totals
        totals = [
            f"Subtotal: ₨{subtotal:>11.2f}",
            f"Discount: ₨{discount_amount:>11.2f}",
            f"Tax: ₨{tax_amount:>11.2f}",
            f"TOTAL: ₨{total:>11.2f}"
        ]
        
        for total_line in totals:
            draw.text((500, y_pos), total_line, fill='black', font=normal_font)
            y_pos += 20
        
        # Final total with emphasis
        draw.line([(450, y_pos), (img_width - 50, y_pos)], fill='black', width=2)
        y_pos += 30
        
        # Footer
        
        
        # Save image
        img.save(filename, 'JPEG' if filename.lower().endswith('.jpg') else 'PNG', quality=95)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceGenerator(root)
    root.mainloop()