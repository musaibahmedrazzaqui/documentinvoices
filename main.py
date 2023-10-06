import json
import math
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import json
import easygui
# Define the allowed file types
file_types = ["*.jpg", "*.jpeg", "*.pdf"]

# Open a file dialog and let the user select a file
file_path = easygui.fileopenbox(title="Select a JPG or PDF file", filetypes=["*.pdf",".jpg",".jpeg"])
model = ocr_predictor(pretrained=True)
#file_path="OPB_Part11.pdf"


if file_path:
    if file_path.lower().endswith(".pdf"):
        # Handle PDF file
        doc = DocumentFile.from_pdf(file_path)
    else:
        # Handle image file
        doc = DocumentFile.from_images(file_path)
    
    # Further processing based on doc (DocumentFile) can go here
    # For example, you can extract text or perform other operations on the document.
    
    print("Document loaded successfully.")
else:
    print("No file selected")

result = model(doc)
json_output = result.export()
json_file_path = "feed.json"
with open(json_file_path, 'w') as json_file:
    json.dump(json_output, json_file, indent=4)

print(f"JSON data has been saved to {json_file_path}")

# Load the OCR results from feed.json
with open('feed.json', 'r') as json_file:
    ocr_data = json.load(json_file)


def extract_services(pages,x_start,y_start):
    extracted_text = []
    count=0
    obj={
        
    }
    for block in pages["blocks"]:
        for line in block["lines"]:
            for word in line["words"]:
                x_min, y_min = word["geometry"]              
                x_start=math.floor(x_start * 1000)/1000
                x_min[0]=math.floor(x_min[0] * 1000) /1000
                y_start=math.floor(y_start * 1000) /1000
                x_min[1]=math.floor(x_min[1] * 1000)/1000
            #print(y_min)
                #print(x_start,x_min[0],y_start,x_min[1])
                delta_x=x_start - x_min[0]
                delta_y=y_start - x_min[1]
                #print(delta_x,delta_y)
                if abs(delta_y) <= 0.01:
                    print("***************")
                    if count==0:
                        obj["REVENUE CODE"]=word["value"]
                    elif count==1 or count==2:
                        extracted_text.append(word["value"])
                        obj["DESCRIPTION"]=' '.join(extracted_text)
                    elif count==3:
                        obj["HCPCS CODE"]=word["value"]
                    elif count==4:
                        obj["SERVICE DATE"]=word["value"]
                    elif count==5:
                        obj["SERVICE UNITS"]=word["value"]
                    elif count==6:
                        obj["SERVICE CHARGES"]=word["value"]
                    
                    count=count+1
            
    return obj

def extract_all_words_for_diagnosis_codes(pages, x_start, y_start):
    extracted_text = []
    current_line = []
   
    for block in pages["blocks"]:
        for line in block["lines"]:
            if not current_line:
                current_line = line["words"]
            for word in line["words"]:
                x_min, y_min = word["geometry"]
                
                x_start = math.floor(x_start * 1000) / 1000
                x_min[0] = math.floor(x_min[0] * 1000) / 1000
                y_start = math.floor(y_start * 1000) / 1000
                x_min[1] = math.floor(x_min[1] * 1000) / 1000

                delta_x = x_start - x_min[0]
                delta_y = y_start - x_min[1]

                if abs(delta_x) <= 0.01 and abs(delta_y) <= 0.01:
                    print("***************")
                    extracted_text.extend([word["value"] for word in current_line])
                    flag=True
                    print("INSIDE")
       

    return " ".join(extracted_text)


def extract_all_words_for_payer_name(pages, x_start, y_start):
    extracted_text = []
    current_line = []
    flag=False
    line_counter=0
    for block in pages["blocks"]:
        for line in block["lines"]:
            
            for word in line["words"]:
                x_min, y_min = word["geometry"]
                if line_counter==2:
                    break
                x_start = math.floor(x_start * 1000) / 1000
                x_min[0] = math.floor(x_min[0] * 1000) / 1000
                y_start = math.floor(y_start * 1000) / 1000
                x_min[1] = math.floor(x_min[1] * 1000) / 1000

                delta_x = x_start - x_min[0]
                delta_y = y_start - x_min[1]

                if abs(delta_x) <= 0.01 and abs(delta_y) <= 0.01:
                    print("***************")
                    extracted_text.append(word["value"])
                    flag=True
                    print("INSIDE")
                if flag==True:
                    extracted_text.append(word["value"])
                    line_counter+=1
                    print("INSIDE")
       

    return " ".join(extracted_text)

def extract_all_words_for_payer(pages, x_start, y_start):
    extracted_text = []
    current_line = []
    flag=False
    line_counter=0
    for block in pages["blocks"]:
        for line in block["lines"]:
            
            for word in line["words"]:
                x_min, y_min = word["geometry"]
                if line_counter==14:
                    break
                x_start = math.floor(x_start * 1000) / 1000
                x_min[0] = math.floor(x_min[0] * 1000) / 1000
                y_start = math.floor(y_start * 1000) / 1000
                x_min[1] = math.floor(x_min[1] * 1000) / 1000

                delta_x = x_start - x_min[0]
                delta_y = y_start - x_min[1]

                if abs(delta_x) <= 0.01 and abs(delta_y) <= 0.01:
                    print("***************")
                    extracted_text.append(word["value"])
                    flag=True
                    print("INSIDE")
                if flag==True:
                    extracted_text.append(word["value"])
                    line_counter+=1
                    print("INSIDE")
       

    return " ".join(extracted_text)

def extract_all_words_by_line(pages, x_start, y_start):
    extracted_text = []
    current_line = []

    for block in pages["blocks"]:
        for line in block["lines"]:
            if not current_line:
                current_line = line["words"]

            for word in line["words"]:
                x_min, y_min = word["geometry"]

                x_start = math.floor(x_start * 1000) / 1000
                x_min[0] = math.floor(x_min[0] * 1000) / 1000
                y_start = math.floor(y_start * 1000) / 1000
                x_min[1] = math.floor(x_min[1] * 1000) / 1000

                delta_x = x_start - x_min[0]
                delta_y = y_start - x_min[1]

                if abs(delta_x) <= 0.01 and abs(delta_y) <= 0.01:
                    print("***************")
                    extracted_text.extend([word["value"] for word in current_line])
                    print("INSIDE")

        # After processing the current line, keep track of the next three lines
        next_lines = []
        line_counter = 0
        for block in pages["blocks"]:
            for line in block["lines"]:
                if line_counter < 3:
                    next_lines.extend(line["words"])
                    line_counter += 1
                else:
                    break
        current_line = next_lines

    return " ".join(extracted_text)

# Define functions to extract text based on coordinates
def extract_text_from_coordinates(pages, x_start, y_start):
    extracted_text = []
  
    for block in pages["blocks"]:
        for line in block["lines"]:
            for word in line["words"]:
                x_min, y_min = word["geometry"]
            #print(word["value"])
            #pr

                
                x_start=math.floor(x_start * 1000)/1000
                x_min[0]=math.floor(x_min[0] * 1000) /1000
                y_start=math.floor(y_start * 1000) /1000
                x_min[1]=math.floor(x_min[1] * 1000)/1000
            #print(y_min)
                #print(x_start,x_min[0],y_start,x_min[1])
                delta_x=x_start - x_min[0]
                delta_y=y_start - x_min[1]
                #print(delta_x,delta_y)
                if abs(delta_x) <= 0.01 and abs(delta_y) <= 0.01:
                    print("***************")
                    extracted_text.append(word["value"])
                    print("INSIDE")
            
    return " ".join(extracted_text)

# Extract values based on coordinates
payer_name=extract_all_words_for_payer_name(ocr_data["pages"][0],0.06020220588235292,0.6083984375)
payer_contact=extract_all_words_for_payer(ocr_data["pages"][0],0.0715762867647059,0.19140625)
patient_control_number = extract_text_from_coordinates(ocr_data["pages"][0], 0.6453354779411764,  0.0390625)
medical_record_number = extract_text_from_coordinates(ocr_data["pages"][0], 0.6440716911764706,  0.0537109375)
type_of_bill = extract_text_from_coordinates(ocr_data["pages"][0], 0.9006204044117647, 0.052734375)
fed_tax_num=extract_text_from_coordinates(ocr_data["pages"][0], 0.6061580882352942, 0.0791015625)
statement_period_from=extract_text_from_coordinates(ocr_data["pages"][0], 0.7198988970588236,0.0791015625)
statement_period_through=extract_text_from_coordinates(ocr_data["pages"][0], 0.7957261029411764, 0.0791015625)
patients_ssn=extract_text_from_coordinates(ocr_data["pages"][0], 0.17636029411764708, 0.0908203125)
patients_name=extract_text_from_coordinates(ocr_data["pages"][0], 0.05767463235294118, 0.1025390625)
patients_address=extract_text_from_coordinates(ocr_data["pages"][0], 0.4860983455882353, 0.08984375) + ' '+extract_text_from_coordinates(ocr_data["pages"][0], 0.5379136029411765, 0.0927734375)+ ' '+ extract_text_from_coordinates(ocr_data["pages"][0], 0.5922564338235294, 0.091796875)
patients_city=extract_text_from_coordinates(ocr_data["pages"][0], 0.06525735294117646, 0.0625) + ' '+ extract_text_from_coordinates(ocr_data["pages"][0], 0.10317095588235292, 0.0615234375)
patients_state=extract_text_from_coordinates(ocr_data["pages"][0],0.7527573529411764,0.1025390625)
patients_zip_code=extract_text_from_coordinates(ocr_data["pages"][0],0.8159466911764706,0.1044921875)
patients_birth_date=extract_text_from_coordinates(ocr_data["pages"][0],0.07284007352941174,0.1357421875)
patients_sex=extract_text_from_coordinates(ocr_data["pages"][0],0.15245863970588236,0.134765625)
admission_date=extract_text_from_coordinates(ocr_data["pages"][0],0.18784466911764708,0.1357421875)
type_of=extract_text_from_coordinates(ocr_data["pages"][0],0.2952665441176471,0.1357421875)
src=extract_text_from_coordinates(ocr_data["pages"][0],0.3913143382352941,0.134765625)
code_31=extract_text_from_coordinates(ocr_data["pages"][0],0.06778492647058826,0.166015625)
occurrence_date_31=extract_text_from_coordinates(ocr_data["pages"][0],0.10569852941176472,0.1669921875)
code_32=extract_text_from_coordinates(ocr_data["pages"][0],0.17394301470588236,0.166015625)
occurrence_date_32=extract_text_from_coordinates(ocr_data["pages"][0],0.21438419117647056,0.1669921875)
code_33=extract_text_from_coordinates(ocr_data["pages"][0],0.28136488970588236,0.166015625)
occurrence_date_33=extract_text_from_coordinates(ocr_data["pages"][0],0.32180606617647056,0.1669921875)
code_34=extract_text_from_coordinates(ocr_data["pages"][0],0.38878676470588236,0.166015625)
occurrence_date_34=extract_text_from_coordinates(ocr_data["pages"][0],0.42922794117647056,0.1669921875)
code_31_b=extract_text_from_coordinates(ocr_data["pages"][0],0.06525735294117646,0.177734375)
occurrence_date_31_b=extract_text_from_coordinates(ocr_data["pages"][0],0.10569852941176472,0.1787109375)
code_39=extract_text_from_coordinates(ocr_data["pages"][0],0.5328584558823529,0.208984375)
value_codes=extract_text_from_coordinates(ocr_data["pages"][0],0.6263786764705882,0.2099609375)
code_40=extract_text_from_coordinates(ocr_data["pages"][0],0.6744025735294118,0.208984375)
value_codes_40=extract_text_from_coordinates(ocr_data["pages"][0],0.7666590073529411,0.2099609375)
page_num=extract_text_from_coordinates(ocr_data["pages"][0],0.1145450367647059,0.5791015625)+' '+extract_text_from_coordinates(ocr_data["pages"][0],0.15372242647058826,0.580078125)+' '+extract_text_from_coordinates(ocr_data["pages"][0],0.16509650735294118,0.5791015625)
creation_date=extract_text_from_coordinates(ocr_data["pages"][0],0.5530790441176471,0.5791015625)
total_amt=extract_text_from_coordinates(ocr_data["pages"][0],0.7451746323529411,0.580078125)
facility_npi=extract_text_from_coordinates(ocr_data["pages"][0],0.8108915441176471,0.5947265625)
insured_name=extract_text_from_coordinates(ocr_data["pages"][0],0.06020220588235292,0.6640625) +' '+extract_text_from_coordinates(ocr_data["pages"][0],0.10190716911764708,0.6640625)
insured_id=extract_text_from_coordinates(ocr_data["pages"][0],0.4026884191176471,0.6640625)
treatment_codes=extract_text_from_coordinates(ocr_data["pages"][0],0.4026884191176471,0.720703125)
admit_dx=extract_text_from_coordinates(ocr_data["pages"][0],0.10569852941176472,0.7822265625)
attending_npi=extract_text_from_coordinates(ocr_data["pages"][0],0.7097886029411764,0.796875)
attending_first=extract_text_from_coordinates(ocr_data["pages"][0],0.8096277573529411,0.8095703125)
attending_last=extract_text_from_coordinates(ocr_data["pages"][0],0.7312729779411764,0.810546875)
code_81=extract_text_from_coordinates(ocr_data["pages"][0],0.7312729779411764,0.849609375)
health_plan_id=extract_text_from_coordinates(ocr_data["pages"][0],0.33191636029411764,0.6083984375)
facility_contact_info=extract_all_words_by_line(ocr_data["pages"][0],0.05893841911764708,0.0380859375)
diagnosis_codes=[extract_text_from_coordinates(ocr_data["pages"][0],0.0703125,0.755859375)[2:],extract_text_from_coordinates(ocr_data["pages"][0],0.15877757352941174,0.7578125)[1:],extract_text_from_coordinates(ocr_data["pages"][0],0.2421875,0.755859375)[1:],extract_text_from_coordinates(ocr_data["pages"][0],0.32938878676470584,0.7578125)[1:],extract_text_from_coordinates(ocr_data["pages"][0],0.4127987132352941,0.755859375)[1:],extract_text_from_coordinates(ocr_data["pages"][0],0.5101102941176471,0.7578125)[1:]]
#services=[{"REVENUE CODE":extract_services(ocr_data["pages"][0],0.05388327205882354,0.275390625),"DESCRIPTION"}]
# Create the output JSON
services2=[extract_services(ocr_data["pages"][0],0.05388327205882354,0.275390625),
extract_services(ocr_data["pages"][0],0.05388327205882354,0.2890625),
extract_services(ocr_data["pages"][0],0.05388327205882354,0.302734375),
extract_services(ocr_data["pages"][0],0.05388327205882354,0.31640625),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.330078125),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.3447265625),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.357421875),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.3720703125),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.3857421875),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.3994140625),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4130859375),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4267578125),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4404296875),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4541015625),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4677734375),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4833984375),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.4970703125),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.5107421875),
extract_services(ocr_data["pages"][0],0.05388327205882354,0.5224609375),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.5380859375),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.5517578125),

extract_services(ocr_data["pages"][0],0.05388327205882354,0.5654296875)

]
# services= [{
#         "REVENUE CODE": extract_services(ocr_data["pages"][0],0.05388327205882354,0.275390625),
#         "DESCRIPTION": extract_services(ocr_data["pages"][0],0.11328125,0.27734375) + ' ' + extract_services(ocr_data["pages"][0],0.18152573529411764,0.2763671875),
#         "HCPCS CODE": extract_services(ocr_data["pages"][0],0.37741268382352944,0.27734375),
#         "SERVICE DATE": extract_services(ocr_data["pages"][0],0.11328125,0.27734375),
#         "SERVICE UNITS": extract_services(ocr_data["pages"][0],0.11328125,0.27734375),
#         "SERVICE CHARGES": extract_services(ocr_data["pages"][0],0.11328125,0.27734375),
#     },
#     {
#         "REVENUE CODE": extract_services(ocr_data["pages"][0],0.05388327205882354,0.2890625),
#         "DESCRIPTION": extract_services(ocr_data["pages"][0],0.1145450367647059,0.291015625) + ' ' + extract_services(ocr_data["pages"][0],0.18278952205882354,0.2900390625),
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "050123",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": extract_services(ocr_data["pages"][0],0.05388327205882354,0.302734375),
#         "DESCRIPTION": extract_services(ocr_data["pages"][0],0.11328125,0.3046875) + ' ' + extract_services(ocr_data["pages"][0],0.18152573529411764,0.302734375),
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "050323",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": extract_services(ocr_data["pages"][0],0.05388327205882354,0.302734375),
#         "DESCRIPTION": extract_services(ocr_data["pages"][0],0.11328125,0.3046875) + ' ' + extract_services(ocr_data["pages"][0],0.18152573529411764,0.302734375),
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "050323",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "050523",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "050523",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "050823",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "050823",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "051023",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "051023",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "051223",
#         "SERVICE UNITS": "3",
#         "SERVICE CHARGES": "165.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "051523",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97116GPKX",
#         "SERVICE DATE": "051523",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97530GP59KX",
#         "SERVICE DATE": "051523",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KX",
#         "SERVICE DATE": "051723",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97116GPKX",
#         "SERVICE DATE": "051723",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KXCQ",
#         "SERVICE DATE": "051923",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KXCQ",
#         "SERVICE DATE": "051923",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KX",
#         "SERVICE DATE": "052223",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97116GPKX",
#         "SERVICE DATE": "052223",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97110GP59KXCQ",
#         "SERVICE DATE": "052423",
#         "SERVICE UNITS": "1",
#         "SERVICE CHARGES": "55.00"
#     },
#     {
#         "REVENUE CODE": "0420",
#         "DESCRIPTION": "PHYSICAL THERP",
#         "HCPCS CODE": "97112GP59KXCQ",
#         "SERVICE DATE": "052423",
#         "SERVICE UNITS": "2",
#         "SERVICE CHARGES": "110.00"
#     }
# ]

output_json = {
    "1 FACILITY CONTACT INFORMATION": facility_contact_info,
    "3a PATIENT CONTROL NUMBER": patient_control_number,
    "3b MEDICAL RECORD NUMBER": medical_record_number,
    "4 TYPE OF BILL": type_of_bill,
    "5 FED TAX NUM": fed_tax_num,
    "6a STATEMENT PERIOD FROM": statement_period_from,
    "6b STATEMENT PERIOD THROUGH": statement_period_through,
    "8a PATIENT'S SSN": patients_ssn,
    "8b PATIENT'S NAME": patients_name,
    "9 PATIENT'S ADDRESS": patients_address,
    "9b PATIENT'S CITY": patients_city,
    "9c PATIENT'S STATE": patients_state,
    "9d PATIENT'S ZIP CODE": patients_zip_code,
    "10 PATIENT'S BIRTH DATE": patients_birth_date,
    "11 PATIENT'S SEX": patients_sex,
    "12 ADMISSION DATE": admission_date,
    "13": "Not Found",
    "14 TYPE": type_of,
    "15": "1",
    "17 STAT": src,
    "31 CODE": code_31,
    "31a OCCURENCE DATE": occurrence_date_31,
    "32 CODE": code_32,
    "32a OCCURENCE DATE": occurrence_date_32,
    "33 CODE": code_33,
    "33a OCCURENCE DATE": occurrence_date_33,
    "34 CODE": code_34,
    "34a OCCURENCE DATE": occurrence_date_34,
    "31b CODE": code_31_b,
    "31b OCCURENCE DATE": occurrence_date_31_b,
    "38 PAYER CONTACT INFORMATION": payer_contact,
    "39 CODE": code_39,
    "39a VALUE CODE AMT": value_codes,
    "40 CODE": code_40,
    "40a VALLUE CODE AMT": value_codes_40,
    "SERVICES": services2,
    "PAGE": page_num,
    "CREATION DATE": creation_date,
    "TOTAL": total_amt,
    "50 PAYER NAME": payer_name,
    "51 HEALTH PLAN ID": health_plan_id,
    "52/53": "%",
    "56 FACILITY NPI": facility_npi,
    "58 INSURED'S NAME": insured_name,
    "60 INSURED'S UNIQUE ID": insured_id,
    "63 TREATMENT AUTHORIZATION CODES": treatment_codes,
    "DIAGNOSIS CODES": diagnosis_codes,
    "69 ADMIT DX": admit_dx,
    "76 ATTENDING NPI": attending_npi,
    "ATTENDING FIRSTNAME": attending_first,
    "ATTENDING LASTNAME": attending_last,
    "81": code_81
}

# Save the output JSON to a file
with open('result.json', 'w') as output_file:
    json.dump(output_json, output_file, indent=4)

print("Output JSON saved")
