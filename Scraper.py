from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import csv
import os
import tkinter as tk
from tkinter import filedialog

# Initialize Chrome webdriver
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get('https://web.whatsapp.com/')
input("Please log in to WhatsApp Web and press Enter after scanning the QR code...")

# Wait for the contact list to load
time.sleep(5)  # Adjust the delay as needed

# Find the chat list
chat_list = driver.find_element(By.ID, "pane-side")

# Initialize list to store all scraped contacts
unsaved_contacts = []

# Find the chat search (xpath == 'Search or start new chat' element)
chat_search = driver.find_element(By.XPATH, "//div[contains(@role, 'textbox')]")
chat_search.click()

# Count how many chat records there are below the search input by using keyboard navigation because HTML is dynamically changed depending on viewport and location in DOM
selected_chat = driver.switch_to.active_element
prev_chat_id = None
chat_count = 0
while True:
    # Navigate to next chat
    selected_chat.send_keys(Keys.DOWN)

    # Set active element to new chat (without this we can't access the elements '.text' value used below for name/time/msg)
    selected_chat = driver.switch_to.active_element

    # Check if we are on the last chat by comparing current to previous chat
    if selected_chat.id == prev_chat_id:
        break
    else:
        prev_chat_id = selected_chat.id
        chat_count += 1

    # Gather chat info (chat name, chat time, and last chat message)
    try:
        contact_name = selected_chat.find_element(By.XPATH, ".//span[contains(text(), '+')]").text
        if contact_name:
            unsaved_contacts.append(contact_name)
    except:
        pass

# specify the directory where you want to store the CSV file
root = tk.Tk()
root.withdraw()  # Hide the main window

folder_path = filedialog.askdirectory(title='Select folder to store contacts')

# create the directory if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# specify the filename of the CSV file
filename = 'unsaved_contacts.csv'

# construct the full path of the CSV file
csv_file_path = os.path.join(folder_path, filename)

# open the CSV file in write mode
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # write the header row to the CSV file
    csv_writer.writerow(['Contact'])

    # loop through the list of contacts and write each contact to the CSV file
    for contact in unsaved_contacts:
        contact = contact.replace(" ","")
        csv_writer.writerow([contact])

# Close the browser
driver.quit()