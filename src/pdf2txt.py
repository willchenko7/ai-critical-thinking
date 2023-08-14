import PyPDF2
import os

def extract_text_from_pdf(pdf_name,train_pages,test_pages):
    pdf_path = os.path.join("pdfs",pdf_name)
    train_text = ""
    test_text = ""
    max_page = max(max(all_train_pages),max(all_test_pages))
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # Check if the PDF has any pages
        i = 0
        if len(pdf_reader.pages) > 0:
            for page in pdf_reader.pages:
                if i + 1 in train_pages:
                    train_text += page.extract_text()
                elif i + 1 in test_pages:
                    test_text += page.extract_text()
                elif i + 1 > max_page:
                    break
                i += 1
    return train_text,test_text

def trainPages2AllPages(train_pages):
    all_pages = []
    for page_range in train_pages:
        for page in range(page_range[0],page_range[1]+1):
            all_pages.append(page)
    return all_pages

def txt2csv(text):
    #Goal: given a string of text, split it into a list of lines and then write it to a csv file
    #step 0: remove all new line characters
    text = text.replace("\n"," ")
    #step 1: split the text separated by spaces
    lines = text.split(" ")
    #step 2: split every n words into a new line
    n = 20
    new_lines = []
    for i in range(0,len(lines),n):
        new_lines.append('"' + " ".join(lines[i:i+n])+ '"' )
    #step 3: write the new lines to a csv file, 
    #ecnlose the each line with double quotes to prevent commas from being interpreted as a new column
    with open(os.path.join("pdfs",'train.csv'), "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(new_lines))
    return

if __name__ == "__main__":
pdf_name = "IntermediateAlgebra2e-WEB.pdf"
train_pages = [
    [13,28], #chapter 1.1
    [32,46], #chapter 1.2
    [51,61], #chapter 1.3
    [65,78], #chapter 1.4
    [82,91], #chapter 1.5
    [94,101], #chapter 1 review
    ]
all_train_pages = trainPages2AllPages(train_pages)
test_pages = [
    [29,20],#chapter 1.1 test
    [47,49],#chapter 1.2 test
    [62,64],#chapter 1.3 test
    [79,80],#chapter 1.4 test
    [92,93],#chapter 1.5 test
    [102,106],#chapter 1 review test
]
all_test_pages = trainPages2AllPages(test_pages)
train_text,test_text = extract_text_from_pdf(pdf_name,all_train_pages,all_test_pages)
print(text)
with open(os.path.join("pdfs",pdf_name[:-4]+'-train.txt'), "w", encoding="utf-8") as output_file:
    output_file.write(train_text)
with open(os.path.join("pdfs",pdf_name[:-4]+'-test.txt'), "w", encoding="utf-8") as output_file:
    output_file.write(test_text)

txt2csv(train_text)