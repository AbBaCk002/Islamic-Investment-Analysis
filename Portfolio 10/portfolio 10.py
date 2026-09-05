# First --------------

import pdfplumber
import pandas as pd

pdf_file = r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Tenth\files\Course_Guide_A.pdf'
file_data = []

with pdfplumber.open(pdf_file) as pdf: 
    for page_number , page in enumerate(pdf.pages , start= 1 ):
        text = page.extract_text(layout=True)
        lines = text.split('\n')
        
        title = ""
        objective = ""
        concepts = ""
        
        for line in lines:
            if "Module" in line:
                title = ' '.join(line.split())
            elif "Objective" in line:
                objective = line.replace("Objectives:", "").replace("Objective:", "").strip()
            elif "Concept" in line:
                concepts = line.replace("Key concepts:", "").replace("Concepts:", "").strip()
        
        file_data.append({
            'page_number': page_number,
            'title': title,
            'objective': objective,
            'concepts': concepts
        })


fi_full = pd.DataFrame(file_data)
output_path = r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Tenth\files\First_PDF.csv'
fi_full.to_csv(output_path, index=False , sep=';' , encoding='utf-8-sig') 
print(f"تم الحفظ بنجاح في: {output_path}")



# second ----------------------------
import pdfplumber
import pandas as pd

pdf_file = r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Tenth\files\Course_Guide_B.pdf'
file_data = []

with pdfplumber.open(pdf_file) as pdf: 
    for page_number , page in enumerate(pdf.pages , start= 1 ):
        text = page.extract_text(layout=True)
        lines = text.split('\n')
        
        title = ""
        objective = ""
        concepts = ""
        
        for line in lines:
            if "Module" in line:
                title = ' '.join(line.split())
            elif "Objective" in line:
                objective = line.replace("Objectives:", "").replace("Objective:", "").strip()
            elif "Concept" in line:
                concepts = line.replace("Key concepts:", "").replace("Concepts:", "").strip()
        
        file_data.append({
            'page_number': page_number,
            'title': title,
            'objective': objective,
            'concepts': concepts
        })


se_full = pd.DataFrame(file_data)
output_path = r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Tenth\files\Second_PDF.csv'
se_full.to_csv(output_path, index=False , sep=';' , encoding='utf-8-sig') 
print(f"تم الحفظ بنجاح في: {output_path}")
#------------

third_full = pd.concat([fi_full, se_full]).reset_index().drop("index", axis=1)
output_path = r'C:\Users\Nisserine\Desktop\GOAL\Day 11\Tenth\files\Third_PDF.csv'
third_full.to_csv(output_path, index=False , sep=';' , encoding='utf-8-sig') 
print(f"تم الحفظ بنجاح في: {output_path}")
