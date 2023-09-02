import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import PyPDF2

showSelect = True
showCombine = False


def set_show_select_button():
    # Replace this with your logic to determine whether the button should be shown
    global showCombine
    global showSelect
    if showCombine == True:
        showSelect = False  # For example, always show the button
    else:
        showSelect = True


def set_show_combine_button():
    # Replace this with your logic to determine whether the button should be shown
    global showCombine
    global showSelect
    if showCombine == True:
        showCombine = False
    else:
        showCombine = True  # For example, always show the button


def successMessage(file: str):
    return messagebox.showinfo(
        "Combine PDFs: Success Message", f"Check for the {file} file"
    )


def failureMessage():
    return messagebox.showerror(
        "Combine PDFs: Failure Message",
        "Something went wrong.",
    )


def selectPDFs():
    pdf_filepaths = filedialog.askopenfilenames(
        title="Select PDF Files To Combine",
        filetypes=[("PDF Files", "*.pdf")],
        initialdir=os.getcwd(),
    )
    # Convert file paths to file names
    pdf_files = [os.path.basename(file_path) for file_path in pdf_filepaths]
    # Print the selected PDF file names
    print("Selected PDF files:")
    for pdf_file in pdf_files:
        print(pdf_file)
    concatenated_string = ", ".join(pdf_files)

    if len(pdf_files) >= 2:
        output_label.config(text=f"Selected files: {concatenated_string}")
        select_button.destroy()
        return pdf_filepaths
    else:
        output_label.config(text=f"Please select more than one PDF.")


def combinePDFs():
    pdf_filepaths = selectPDFs()
    pdf_merger = PyPDF2.PdfMerger()
    try:
        for file_path in pdf_filepaths:
            pdf_merger.append(file_path)

        output_file = "merged.pdf"
        with open(output_file, "wb") as output_pdf:
            pdf_merger.write(output_pdf)

        successMessage(output_file)
        output_label.config(text=f"Merge Successful")

    except Exception as e:
        failureMessage()
        print(f"Error: {e}")
        output_label.config(text=f"Merge Failed")
    finally:
        pdf_merger.close()
        select_button = ttk.Button(
            master=input_frame, text="Select", command=selectPDFs
        )
        select_button.pack()
        window.quit()


# Window Creation
window = tk.Tk()

# Window Design
window.title("Combine PDF App")
window.geometry("500x450")

# Title
title_label = ttk.Label(
    master=window, text="Select the PDFs you'd like to combine.", font="Calibri 12 bold"
)
title_label.pack()

# Image
image = tk.PhotoImage(file="PDF_file_icon.png")
image_label = ttk.Label(master=window, image=image)
image_label.pack()


# Input Field
input_frame = ttk.Frame(master=window)
combine_button = ttk.Button(master=input_frame, text="Combine", command=combinePDFs)
select_button = ttk.Button(
    master=input_frame, text="Select Files and Combine", command=combinePDFs
)
select_button.pack()
input_frame.pack(pady=10)

# Output
output_label = ttk.Label(
    master=window,
    text="",
    font="Calibri 12 bold",
)
output_label.pack(pady=5)

# Run
window.mainloop()