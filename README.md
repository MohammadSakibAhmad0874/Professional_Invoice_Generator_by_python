# Professional_Invoice_Generator_by_python
# Professional Invoice Generator
![3rd](https://github.com/user-attachments/assets/8cd35195-6a06-4dbc-b4d1-8ec46a6c841e)

## Overview
This Professional Invoice Generator is a comprehensive Python application that allows users to create, preview, and export professional invoices in multiple formats. With its intuitive graphical interface, users can easily input company and customer information, add line items, apply taxes and discounts, and export invoices as PDF, JPG, or text files.



## Features
- **Company & Customer Management**: Store company details and customer information
- **Invoice Item Management**: Add, remove, and manage line items with descriptions, quantities, and rates
- **Automatic Calculations**: Automatic subtotal, tax, discount, and total calculations
- **Multiple Export Formats**: Export invoices as PDF, JPG, or text files
- **Logo Support**: Add company logos to invoices
- **Preview Functionality**: Preview invoices before exporting
- **Auto-generated Fields**: Automatic invoice numbering and date generation
- **Responsive UI**: Tabbed interface with scrollable sections

## Installation

### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)
- Pillow (PIL Fork) library
- ReportLab library

### Installation Steps
1. Clone the repository or download the source code
2. Install required dependencies:
   ```bash
   pip install pillow reportlab
   ```
3. Run the application:
   ```bash
   python invoice_generator.py
   ```

## Usage Guide

### 1. Company Information
- Fill in your company details: name, address, phone, and email
- Upload your company logo using the "Upload Logo" button (supports PNG/JPG)

### 2. Customer Information
- Enter customer details: name, address, phone, and email

### 3. Invoice Details
- Invoice number is automatically generated but can be customized
- Set invoice date and due date
- Specify payment terms (default: "Net 30")

### 4. Adding Items
1. Enter item description, quantity, and rate
2. Click "Add Item" to add to the invoice
3. Items appear in the table below with automatic amount calculation
4. Remove items by selecting and clicking "Remove Selected Item"

### 5. Taxes and Discounts
- Set tax rate percentage (e.g., 7.5 for 7.5% tax)
- Apply discount percentage if applicable

### 6. Generating and Exporting
1. Click "Generate Invoice" to preview in the Preview tab
2. Export options:
   - **Save as Text**: Save as a plain text file
   - **Download as PDF**: Export as a professional PDF document
   - **Download as JPG**: Save as an image file
3. Use "Clear All" to reset all fields

### Preview Tab
- Review your invoice before exporting
- Scroll through the entire invoice to verify all details

## Technical Details

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| tkinter | Included | GUI framework |
| PIL (Pillow) | >=8.0.0 | Image processing |
| reportlab | >=3.6.0 | PDF generation |
| datetime | Included | Date handling |

### File Structure
- `invoice_generator.py`: Main application file
- Generated files:
  - `.txt`: Text invoice
  - `.pdf`: PDF invoice
  - `.jpg`/`.png`: Image invoice

### Customization
You can modify the following aspects:
- Default currency symbol (currently Rupee - "₨")
- Invoice dimensions in PDF and image exports
- Font sizes and styles
- Color schemes
- Default payment terms

## Troubleshooting

### Common Issues
1. **Logo not appearing in exports**:
   - Ensure the image format is supported (PNG, JPG, JPEG)
   - Check file permissions
   - Try a smaller image file

2. **Calculation errors**:
   - Ensure quantity and rate fields contain only numbers
   - Verify tax and discount fields contain valid percentages

3. **Font issues in image exports**:
   - Install the required fonts on your system
   - Modify the fallback font in the code

### Error Messages
- "Please add at least one item": Add items before generating
- "Quantity and Rate must be numbers": Verify numeric values
- "Failed to save...": Check file permissions and path validity

## License
This project is open-source and available under the MIT License.

## Support
For issues or feature requests, please open an issue on the GitHub repository.

---

**Note**: This application maintains all entered data in memory while running but does not save it between sessions. Be sure to export your invoices before closing the application.
