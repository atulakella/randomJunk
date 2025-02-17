from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import io
from PyPDF2 import PdfReader, PdfWriter
import google.generativeai as genai
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

# Gemini API setup (Replace 'YOUR_GEMINI_API_KEY' with your actual API key)
genai.configure(api_key='AIzaSyD5HvoyjOQMIBNJRrFK3O4sxDap--BVU_Q')

# Function to generate Gemini response
def generate_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        if response.text:
            cleaned_response = response.text.replace('*', '')
            return cleaned_response
        else:
            return "No response available."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate PDF report
def generate_pdf(name, age, relaxed_freq, stressed_freq, active_freq):
    # Read the template PDFs
    template_page1_path = "C:/Users/ROHITH NARAYANAN/OneDrive/Desktop/PREVIOUS SEMS/C PROGRAMMING ASSIGNMENTS/ECS AND OTHER PROJECTS/COGNILIFT/Cognilift.ai template.pdf"
    template_page2_path = "C:/Users/ROHITH NARAYANAN/OneDrive/Desktop/PREVIOUS SEMS/C PROGRAMMING ASSIGNMENTS/ECS AND OTHER PROJECTS/COGNILIFT/Cognilift.ai page 2.pdf"
    
    template_page1 = PdfReader(template_page1_path)
    template_page2 = PdfReader(template_page2_path)

    # Create a buffer for the modified second page
    packet_page2 = io.BytesIO()
    can_page2 = canvas.Canvas(packet_page2, pagesize=letter)
    width, height = letter

    # Add content to the second page
    can_page2.setFont("Helvetica-Bold", 20)  # Reduced font size
    can_page2.drawString(30, height - 70, "EEG Frequency Analysis Report")
    can_page2.setFont("Helvetica", 16)  # Reduced font size
    can_page2.drawString(30, height - 100, f"Name: {name}")
    can_page2.drawString(30, height - 130, f"Age: {age}")
    can_page2.drawString(30, height - 160, f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Add frequency data
    can_page2.setFont("Helvetica-Bold", 18)  # Reduced font size
    can_page2.drawString(30, height - 200, "Frequency Analysis:")
    can_page2.setFont("Helvetica", 14)  # Reduced font size
    y = height - 230
    for state, freq in [("Relaxed", relaxed_freq), ("Stressed", stressed_freq), ("Active", active_freq)]:
        can_page2.drawString(50, y, f"{state} State:")
        y -= 20
        for band, value in freq.items():
            can_page2.drawString(70, y, f"{band}: {value:.4f}")
            y -= 20
        y -= 15

    # Save the content to the buffer for the second page
    can_page2.save()
    packet_page2.seek(0)

    # Merge the modified second page with the template
    modified_page2 = PdfReader(packet_page2)
    template_page2.pages[0].merge_page(modified_page2.pages[0])

    # Create a buffer for the third page (Actionable Insights)
    packet_page3 = io.BytesIO()
    can_page3 = canvas.Canvas(packet_page3, pagesize=letter)

    # Add content to the third page
    can_page3.setFont("Helvetica-Bold", 20)  # Reduced font size
    can_page3.drawString(30, height - 70, "Actionable Insights")
    can_page3.setFont("Helvetica", 14)  # Reduced font size
    y = height - 100

    # Generate actionable insights using Gemini API
    insights_prompt = f"""
    The EEG frequency values for {name} (Age: {age}) are as follows:
    - Relaxed State: {relaxed_freq}
    - Stressed State: {stressed_freq}
    - Active State: {active_freq}

    Provide actionable insights in layman's terms:
    - Explain what the data means.
    - Compare the client's EEG frequencies to typical ranges for relaxation, stress, and activity.
    - Provide a simple explanation of how the client's mental states compare to normal ranges.
    """
    insights_response = generate_gemini_response(insights_prompt)

    # Add insights content to the third page with proper spacing
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    style.fontSize = 12  # Reduced font size to fit more text
    style.leading = 14  # Reduced line spacing

    # Split the response into paragraphs
    paragraphs = insights_response.split("\n")
    for paragraph_text in paragraphs:
        if paragraph_text.strip():  # Skip empty lines
            paragraph = Paragraph(paragraph_text.strip(), style)
            paragraph.wrapOn(can_page3, width - 60, height)
            paragraph_height = paragraph.wrap(width - 60, height)[1]

            # Check if the paragraph fits on the current page
            if y - paragraph_height < 100:  # Increased bottom margin to 100px
                can_page3.showPage()  # Create a new page
                y = height - 70  # Reset y position for the new page
                can_page3.setFont("Helvetica-Bold", 20)
                can_page3.drawString(30, height - 70, "Actionable Insights (Continued)")
                can_page3.setFont("Helvetica", 14)
                y = height - 100  # Reset y position after the header

            # Draw the paragraph
            paragraph.drawOn(can_page3, 30, y - paragraph_height)
            y -= paragraph_height + 10  # Add spacing after the paragraph

    # Save the content to the buffer for the third page
    can_page3.save()
    packet_page3.seek(0)

    # Merge the modified third page with the template
    modified_page3 = PdfReader(packet_page3)
    template_page3 = PdfReader(template_page2_path)  # Use the same template as the second page
    template_page3.pages[0].merge_page(modified_page3.pages[0])

    # Create a buffer for the fourth page (Stress and Activity Analysis)
    packet_page4 = io.BytesIO()
    can_page4 = canvas.Canvas(packet_page4, pagesize=letter)

    # Add content to the fourth page
    can_page4.setFont("Helvetica-Bold", 20)  # Reduced font size
    can_page4.drawString(30, height - 70, "Stress and Activity Analysis")
    can_page4.setFont("Helvetica", 14)  # Reduced font size
    y = height - 100

    # Generate analysis using Gemini API
    analysis_prompt = f"""
    The EEG frequency values for {name} (Age: {age}) are as follows:
    - Relaxed State: {relaxed_freq}
    - Stressed State: {stressed_freq}
    - Active State: {active_freq}

    Answer the following questions in detail:
       - 1)How do your EEG frequencies compare to typical ranges for relaxation, stress, and activity?
       - 2)Which frequency band was dominant?
       - 3)Why was this frequency dominant?
       - 4)What are the potential effects of having a dominant frequency band for extended periods?
    """
    analysis_response = generate_gemini_response(analysis_prompt)

    # Add analysis content to the fourth page with proper spacing
    paragraphs = analysis_response.split("\n")
    for paragraph_text in paragraphs:
        if paragraph_text.strip():  # Skip empty lines
            paragraph = Paragraph(paragraph_text.strip(), style)
            paragraph.wrapOn(can_page4, width - 60, height)
            paragraph_height = paragraph.wrap(width - 60, height)[1]

            # Check if the paragraph fits on the current page
            if y - paragraph_height < 100:  # Increased bottom margin to 100px
                can_page4.showPage()  # Create a new page
                y = height - 70  # Reset y position for the new page
                can_page4.setFont("Helvetica-Bold", 20)
                can_page4.drawString(30, height - 70, "Stress and Activity Analysis (Continued)")
                can_page4.setFont("Helvetica", 14)
                y = height - 100  # Reset y position after the header

            # Draw the paragraph
            paragraph.drawOn(can_page4, 30, y - paragraph_height)
            y -= paragraph_height + 10  # Add spacing after the paragraph

    # Save the content to the buffer for the fourth page
    can_page4.save()
    packet_page4.seek(0)

    # Merge the modified fourth page with the template
    modified_page4 = PdfReader(packet_page4)
    template_page4 = PdfReader(template_page2_path)  # Use the same template as the second page
    template_page4.pages[0].merge_page(modified_page4.pages[0])

    # Create a buffer for the fifth page (Personalized Suggestions)
    packet_page5 = io.BytesIO()
    can_page5 = canvas.Canvas(packet_page5, pagesize=letter)

    # Add content to the fifth page
    can_page5.setFont("Helvetica-Bold", 20)  # Reduced font size
    can_page5.drawString(30, height - 70, "Personalized Suggestions")
    can_page5.setFont("Helvetica", 14)  # Reduced font size
    y = height - 100

    # Generate suggestions using Gemini API
    suggestions_prompt = f"""
    Based on the age of {name} (Age: {age}), provide personalized suggestions to improve mental well-being.
    """
    suggestions_response = generate_gemini_response(suggestions_prompt)

    # If no personalized suggestions are available, provide generalized suggestions
    if "cannot generate personalized results" in suggestions_response.lower():
        suggestions_response = """
        Here are some general methods to maintain good brain waves and a relaxed mind:
        1. Practice mindfulness meditation daily.
        2. Engage in regular physical exercise.
        3. Maintain a balanced diet rich in omega-3 fatty acids.
        4. Ensure adequate sleep and a consistent sleep schedule.
        5. Reduce screen time and take regular breaks.
        6. Practice deep breathing exercises.
        7. Engage in hobbies and activities that bring joy.
        8. Limit caffeine and alcohol intake.
        9. Stay hydrated and maintain a healthy lifestyle.
        10. Seek professional help if experiencing chronic stress or anxiety.
        """

    # Add suggestions content to the fifth page with proper spacing
    paragraphs = suggestions_response.split("\n")
    for paragraph_text in paragraphs:
        if paragraph_text.strip():  # Skip empty lines
            # Format as bullet points if the line starts with a number
            if paragraph_text.strip()[0].isdigit():
                paragraph_text = "• " + paragraph_text.strip()

            paragraph = Paragraph(paragraph_text.strip(), style)
            paragraph.wrapOn(can_page5, width - 60, height)
            paragraph_height = paragraph.wrap(width - 60, height)[1]

            # Check if the paragraph fits on the current page
            if y - paragraph_height < 100:  # Increased bottom margin to 100px
                can_page5.showPage()  # Create a new page
                y = height - 70  # Reset y position for the new page
                can_page5.setFont("Helvetica-Bold", 20)
                can_page5.drawString(30, height - 70, "Personalized Suggestions (Continued)")
                can_page5.setFont("Helvetica", 14)
                y = height - 100  # Reset y position after the header

            # Draw the paragraph
            paragraph.drawOn(can_page5, 30, y - paragraph_height)
            y -= paragraph_height + 10  # Add spacing after the paragraph

    # Save the content to the buffer for the fifth page
    can_page5.save()
    packet_page5.seek(0)

    # Merge the modified fifth page with the template
    modified_page5 = PdfReader(packet_page5)
    template_page5 = PdfReader(template_page2_path)  # Use the same template as the second page
    template_page5.pages[0].merge_page(modified_page5.pages[0])

    # Create a PDF writer object
    output_pdf = PdfWriter()

    # Add the first page from the first template
    output_pdf.add_page(template_page1.pages[0])

    # Add the modified second page
    output_pdf.add_page(template_page2.pages[0])

    # Add the modified third page
    output_pdf.add_page(template_page3.pages[0])

    # Add the modified fourth page
    output_pdf.add_page(template_page4.pages[0])

    # Add the modified fifth page
    output_pdf.add_page(template_page5.pages[0])

    # Write the merged PDF to a buffer
    merged_buffer = io.BytesIO()
    output_pdf.write(merged_buffer)
    merged_buffer.seek(0)

    return merged_buffer
