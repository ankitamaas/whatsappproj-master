import pywhatkit as kit
import pandas as pd
import time
from django.shortcuts import render
from django.http import JsonResponse
import pyautogui  # To simulate pressing the 'close' button

# Path to your Excel file with phone numbers
EXCEL_FILE_PATH = "Phone.xlsx"

def send_whatsapp_messages(request):
    if request.method == "POST":
        # Get the message from the form
        message = request.POST.get("message", "")
        if not message:
            return JsonResponse({"error": "Message is required."}, status=400)
        
        try:
            data = pd.read_excel(EXCEL_FILE_PATH)

            if 'Phone' not in data.columns:
                return JsonResponse({"error": "Excel file must have a column named 'Phone'."}, status=400)

            results = []
            for index, row in data.iterrows():
                phone = str(row['Phone']).strip()
                
                if not phone.startswith("+"):
                    phone = "+91" + phone  # Adjust country code if needed

                # Send the message
                try:
                    kit.sendwhatmsg_instantly(phone, message, wait_time=15)
                    time.sleep(15)  # Wait for the message to be sent
                    
                    # Close the browser window after sending the message
                    pyautogui.hotkey('ctrl', 'w')  # Simulates pressing 'Ctrl + W' to close the tab/window

                    results.append(f"Message sent to {phone}")
                except Exception as e:
                    results.append(f"Failed to send to {phone}: {e}")

            return JsonResponse({"results": results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "send_message.html")
