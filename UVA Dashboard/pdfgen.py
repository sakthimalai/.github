import os
import streamlit as st
import textwrap
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from genAi import generate_content

def generate_pdf_report(selected_symptoms, predicted_disease_rf):
    genContent = generate_content(predicted_disease_rf + ' disease curing measure for animal with 100 word limit . give without header')
    filename = f'{predicted_disease_rf}.pdf'
    # Create a canvas object
    c = canvas.Canvas(filename, pagesize=letter)

    # Draw border
    border_padding = 30
    border_width = letter[0] - 2 * border_padding
    border_height = letter[1] - 2 * border_padding
    c.rect(border_padding, border_padding, border_width, border_height)
    
    # Add Logo
    logo_path = "D:/unisys/genai/unisys.png"  # Provide the path to your logo PNG file
    if os.path.exists(logo_path):
        c.drawImage(logo_path, border_padding, letter[1] - border_padding - 30, width=100, height=30)

    # Set font for header
    c.setFont("Helvetica-Bold", 20)
    # Add space above the header
    header_y_coordinate = letter[1] - border_padding - 30
    # Calculate the center position for the header
    header_text = "UNISYS VETERINARY ASSISTANT"
    header_text_width = c.stringWidth(header_text)
    header_x_coordinate = (letter[0] - header_text_width) / 2
    # Draw the header
    c.drawString(header_x_coordinate, header_y_coordinate, header_text)

    # Add date and day to top right
    today = datetime.date.today()
    date_text = today.strftime("%B %d, %Y")
    day_text = today.strftime("%A")
    date_day_text = f"{date_text} ({day_text})"
    date_day_text_width = c.stringWidth(date_day_text)
    c.setFont("Helvetica", 10)  # Reduce font size for date and day
    c.drawString(letter[0] - border_padding - date_day_text_width - 50, header_y_coordinate -20, date_day_text)

    # Set font for sub-header
    c.setFont("Helvetica-Bold", 16)  # Set sub-header to bold
    # Add space between header and sub-header
    sub_header_y_coordinate = header_y_coordinate - 50  # Increased space
    # Calculate the center position for the sub-header
    sub_header_text = "REPORT"
    sub_header_text_width = c.stringWidth(sub_header_text)
    sub_header_x_coordinate = (letter[0] - sub_header_text_width) / 2
    # Draw the sub-header
    c.drawString(sub_header_x_coordinate, sub_header_y_coordinate, sub_header_text)
    c.drawString(100, sub_header_y_coordinate - 20, "Selected Symptoms:")

    # Write selected symptoms to PDF
    y_coordinate = sub_header_y_coordinate - 50  # Increased space
    for symptom in selected_symptoms:
        c.drawString(120, y_coordinate, symptom)
        y_coordinate -= 20  # Adjusted y-coordinate

    c.drawString(100, y_coordinate - 20, "Predicted Disease:")
    # Write predicted disease to PDF
    c.drawString(120, y_coordinate - 40, predicted_disease_rf)  # Adjusted y-coordinate
    y_coordinate -= 60  # Increased space

    # Write additional information before GenAI content
    c.drawString(100, y_coordinate - 20, "Blood Pressure: 120")
    c.drawString(100, y_coordinate - 40, "Laziness: present")
    c.drawString(100, y_coordinate - 60, "Milk Production: Less")
    y_coordinate -= 80  # Adjusted y-coordinate

    # Write genai content to PDF
    genai_content_x_coordinate = border_padding + (border_width - c.stringWidth("Measures:")) / 2  # Centered
    c.drawString(genai_content_x_coordinate, y_coordinate, "Measures ")
    y_coordinate -= 20
    # Wrap and write GenAI content
    lines = textwrap.wrap(genContent, width=70, fix_sentence_endings=True)
    for line in lines:
        # Calculate the center position for each line of GenAI content
        line_width = c.stringWidth(line)
        x_coordinate = border_padding + (border_width - line_width) / 2  # Centered
        c.drawString(x_coordinate, y_coordinate, line)  # Adjusted x-coordinate
        y_coordinate -= 15  # Adjusted spacing between lines

    y_coordinate -= 20

    # Add report from UVA AI at the bottom
    c.setFont("Helvetica", 12)
    report_y_coordinate = border_padding + 20  # Adjusted y-coordinate
    c.drawString(border_padding, report_y_coordinate, "*report from UVA AI*")

    # Save the PDF
    c.save()
    st.download_button(label="Download PDF", data=open(filename, 'rb').read(), file_name=filename)
    return filename
