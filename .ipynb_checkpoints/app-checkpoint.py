import streamlit as st
import nest_asyncio
from playwright.async_api import async_playwright
import asyncio
from main import get_response, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers, modify_element
from concurrent.futures import ThreadPoolExecutor
from reportlab.pdfgen import canvas
import os
from PyPDF2 import PdfMerger
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

# Setup Google Sheets API client using credentials from secrets
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"],
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client

# Access the Google Sheet
def get_google_sheet(client, spreadsheet_url):
    sheet = client.open_by_url(spreadsheet_url).sheet1  # Opens the first sheet
    return sheet

# Read the password from the first cell
def read_password_from_sheet(sheet):
    password = sheet.cell(1, 1).value  # Reads the first cell (A1)
    return password

# Update the password in the first cell
def update_password_in_sheet(sheet, new_password):
    sheet.update_cell(1, 1, new_password)  # Updates the first cell (A1) with the new password

# Initialize gspread client and access the sheet
client = get_gspread_client()
sheet = get_google_sheet(client, st.secrets["spreadsheet"])
PASSWORD = read_password_from_sheet(sheet)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'password' not in st.session_state:
    st.session_state['password'] = PASSWORD
if 'reset_mode' not in st.session_state:
    st.session_state['reset_mode'] = False

# Function to check password
def check_password(password):
    return password == st.session_state['password']

# Password reset function
def reset_password(new_password, confirm_password):
    if new_password != confirm_password:
        st.error("Passwords do not match!")
    else:
        st.session_state['password'] = new_password
        update_password_in_sheet(sheet, new_password)
        st.session_state['reset_mode'] = False
        st.success("Password reset successfully!")

# Authentication block
if not st.session_state['authenticated']:
    st.title("Login to Chapter PDF Generator")

    password_input = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if check_password(password_input):
            st.session_state['authenticated'] = True
            st.success("Login successful!")
        else:
            st.error("Incorrect password!")

    if st.button("Reset Password?"):
        st.session_state['reset_mode'] = True

# Reset password block
if st.session_state['reset_mode']:
    st.title("Reset Password")

    old_password = st.text_input("Enter Old Password", type="password")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Reset Password"):
        if old_password == st.session_state['password']:
            reset_password(new_password, confirm_password)
        else:
            st.error("Incorrect old password!")
    
    if st.button("Back to Login"):
        st.session_state['reset_mode'] = False

if st.session_state['authenticated'] and not st.session_state['reset_mode']:
    # Install Playwright if needed
    os.system('playwright install')

    # Create a ThreadPoolExecutor to run the async function
    executor = ThreadPoolExecutor()

    # Function to convert HTML to PDF with Playwright
    nest_asyncio.apply()

    async def html_to_pdf_with_margins(html_file, output_pdf):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            await page.set_content(html_content, wait_until='networkidle')
            page_size = {
                'width': '130mm',
                'height': '197mm'
            }
            pdf_options = {
                    'path': output_pdf,
                    'width': page_size['width'],
                    'height': page_size['height'],
                    'margin': {
                        'top': '70px',
                        'bottom': '50px',
                        'left': '15px',
                        'right': '1px'
                    },
                    'print_background': True,
                }

            await page.pdf(**pdf_options)
            await browser.close()

    # Streamlit UI
    st.title("Chapter PDF Generator")
    
    def calculate_word_count(chapter_text):
        if not chapter_text:
            return 0
        
        # Initialize variables
        in_word = False
        word_count = 0
    
        for char in chapter_text:
            # Check if the character is alphanumeric using ASCII
            if char.isalnum():  # Equivalent to checking 'a-z', 'A-Z', '0-9'
                if not in_word:
                    # Start of a new word
                    in_word = True
            else:
                if in_word:
                    # End of a word
                    word_count += 1
                    in_word = False
        
        # Account for the last word if the string ends with an alphanumeric character
        if in_word:
            word_count += 1
    
        return word_count
    
    def get_word_count(html_file_path):
        # Read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        if soup.title:
            soup.title.decompose()
        # Extract text from the HTML
        text = soup.get_text()
        # st.write(text)
        
        # Calculate word count using ASCII logic
        in_word = False
        word_count = 0
    
        for char in text:
            # Check if the character is alphanumeric
            if char.isalnum():
                if not in_word:
                    # Start of a new word
                    in_word = True
            else:
                if in_word:
                    # End of a word
                    word_count += 1
                    in_word = False
    
        # Account for the last word if the string ends with an alphanumeric character
        if in_word:
            word_count += 1
    
        return word_count
    
    fonts = [
        'Adobe Jenson Pro', 'Arial', 'BemboStd', 'Caslon', 'Courier',
        'Garamond', 'Goudy', 'Helvetica', 'Hoefler TXT', 'Minion Pro',
        'Requiem Text', 'Sabon', 'SabonLTPro', 'Times-Roman'
    ]
    
    # Dynamic list to store chapter inputs
    chapter_texts = []
    num_chapters = st.number_input('How many chapters do you want to add?', min_value=1, max_value=10, step=1)

    for i in range(num_chapters):
        chapter_text = st.text_area(f'Enter the Chapter {i+1} text:')
        chapter_texts.append(chapter_text)
        word_count = calculate_word_count(chapter_text)
        st.write(f'Word count: {word_count}')
        
            
    author_name = st.text_input('Enter the Author Name:')
    book_name = st.text_input('Enter the Book Name:')
    font_size = st.text_input('Enter the Font Size')
    line_height = st.text_input('Enter the Line Spacing')

    
    font_style = st.selectbox('Select Font Style:', fonts)
    font_path = f"fonts/{font_style}.ttf"

    First_page_no = st.number_input('Enter the First Page Number:', min_value=0, max_value=1000, step=1)
    options = ['Left', 'Right']
    first_page_position = st.selectbox('Select First Page Position:', options)
    language = st.selectbox('Select Language', ['English','Hindi'])
    
    ele = []
    num_elements = st.number_input("Enter the number of different elements: ", min_value=0, max_value=10, step=1)
    for j in range(num_elements):
        element = st.text_input(f"Enter element {j + 1}:", key=f"phrase_{j+1}")
        font_style_ele = st.selectbox('Select Font Style:', fonts, key=f"style_{j+1}")
        font_size_ele = st.number_input(f"Enter font size for '{element}':", min_value=8, max_value=72, step=1, key=f"size_{j+1}")
        ele.append({
        "text": element,
        "font_style": font_style_ele,
        "font_size": font_size_ele
    })

    # Button to generate PDF
    if st.button("Generate PDF"):
        final_pdfs = []
        current_page_number = First_page_no  # Start from the user-defined first page number

        # Set the initial page position for the first chapter
        current_position = first_page_position  # "Right" or "Left" based on input
        wc = []
        async def process_chapter(idx, chapter_text):
            # Get response asynchronously
            response = await get_response(chapter_text, font_size, line_height, language, font_style, font_path)
            html_pth = save_response(response)
            modify_element(ele, html_pth)
            word_count = get_word_count(html_pth)
    
            main_pdf = f'out_{idx+1}.pdf'
            await html_to_pdf_with_margins(html_pth, main_pdf)
    
            return main_pdf, word_count

        
        async def process_all_chapters():
            tasks = [
                process_chapter(idx, chapter_text)
                for idx, chapter_text in enumerate(chapter_texts)
            ]
            return await asyncio.gather(*tasks)


        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(process_all_chapters())
        
        for idx, (main_pdf, word_count) in enumerate(results):
            total_pages = get_pdf_page_count(main_pdf)
            overlay_pdf = f"overlay_{idx+1}.pdf"
    
            # Create overlay PDF and calculate current position
            current_position = create_overlay_pdf(
                overlay_pdf, total_pages, current_page_number, book_name, author_name, font_style, font_path, current_position
            )
    
            final_pdf = f'final_{idx+1}.pdf'
            final_pdfs.append(final_pdf)
            overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)
            current_page_number += total_pages
            wc.append(word_count)        

        
        # Merge all the final PDFs into one
        merger = PdfMerger()
        for pdf in final_pdfs:
            merger.append(pdf)

        merged_pdf_path = 'merged_final.pdf'
        merger.write(merged_pdf_path)
        merger.close()

        st.success("All PDFs merged successfully into one!")

        # Provide a download button for the merged final PDF
        with open(merged_pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Final Merged PDF",
                data=pdf_file,
                file_name=merged_pdf_path,
                mime="application/pdf"
            )
        st.write("### Chapter-wise Word Count")
        for idx, count in enumerate(wc, start=1):
            st.write(f"Chapter {idx}: {count} words")
