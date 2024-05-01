import io
import zipfile
import re
import tkinter as tk
from tkinter import filedialog

# Recursive function to get all file paths in the archive
def get_all_file_path(archive):
    return archive.namelist()

# Setup the main tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

try:
    # Open dialog to select a ZIP file
    file_path = filedialog.askopenfilename()
    print("Selected ZIP file:", file_path)
    
    with zipfile.ZipFile(file_path, 'r') as myzip:
        # Prompt for new ZIP file location and name
        newzip_path = filedialog.asksaveasfilename(defaultextension='.zip')
        print("Saving new ZIP file to:", newzip_path)
        
        with zipfile.ZipFile(newzip_path, 'w') as new_zip:
            for filename in get_all_file_path(myzip):
                print("Processing file:", filename)
                if filename.endswith('.html') or filename.endswith('.xml'):
                    with myzip.open(filename) as myfile:
                        try:
                            data = myfile.read().decode('utf-8')  # Try to decode the data as UTF-8
                            print("Successfully decoded:", filename)
                            
                            # Text processing based on file type
                            if filename.endswith('.html'):
                                # Using regular expression to specifically update <link href=/ rel=canonical>
                                new_data = re.sub(r'<link href=/ rel=canonical>', '<link href="example.com" rel=canonical>', data)
                            elif filename.endswith('.xml'):
                                new_data = re.sub(r'<loc>(.*?)</loc>', r'<loc>https://example.com\1</loc>', data)
                            else:
                                new_data = data  # Use the original data if the file doesn't need modification

                            byte_data = io.BytesIO(new_data.encode('utf-8'))  # Convert string to bytesIO object
                            
                        except UnicodeDecodeError:
                            print("Unicode decode error in file:", filename, "; Keeping original binary data.")
                            byte_data = io.BytesIO(myfile.read())  # Keep the original binary data
                        
                        file_info = zipfile.ZipInfo(filename)
                        file_info.date_time = myzip.getinfo(filename).date_time
                        file_info.compress_type = myzip.getinfo(filename).compress_type
                        new_zip.writestr(file_info, byte_data.getvalue())
                else:
                    # Directly copy the file from old ZIP to new ZIP without extraction
                    new_zip.writestr(myzip.getinfo(filename), myzip.read(filename))

except FileNotFoundError:
    print("File not found. Please check the file path.")
except zipfile.BadZipFile:
    print("Failed to open ZIP file. It may be corrupt or not a zip file.")
except Exception as e:
    print("An unexpected error occurred:", str(e))
finally:
    print("Operation completed.")
