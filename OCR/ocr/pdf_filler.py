import json
import os
from datetime import datetime
from PyPDFForm import PdfWrapper
from faker import Faker

fake = Faker()
Faker.seed(0)

def get_primary_physician_last_name(data):
    """Extract primary physician's last name from data."""
    for encounter in data['record']['encounters']:
        if encounter['provider']['type'].lower() == 'primary':
            return f"Dr. {encounter['clinician']['attributes']['last_name']}"
    return ''

def get_race_ethnicity(data):
    """Extract race and ethnicity information from data."""
    race = data['attributes']['race'].lower()
    ethnicity = data['attributes']['ethnicity'].lower()
    
    race_map = {
        'Am Indian or Alaska Native': 'am. indian or alaska native',
        'Asian': 'asian',
        'Black': 'black',
        'Native Hawaiian or Other Pac Islander': 'native hawaiian or other pac. islander',
        'White': 'white',
    }
    
    race_values = {key: (race == value) for key, value in race_map.items()}
    race_values['Unknown_3'] = race not in race_map.values()
    race_values['undefined_14'] = race == 'other'
    
    ethnicity_value = 0 if ethnicity == 'hispanic' else 1 if ethnicity == 'nonhispanic' else 2
    
    return race_values, ethnicity_value


def parse_date(date_value):
    """Parse date from millisecond timestamp."""
    if isinstance(date_value, int):
        try:
            return datetime.fromtimestamp(date_value / 1000)
        except (OSError, ValueError):
            pass
    return None

def get_hav_vaccine_info(data):
    """Extract HAV vaccine information from data."""
    hepa = data['attributes']['immunizations']['hepa']
    hepa_adult = data['attributes']['immunizations']['hepa_adult']
    
    total_doses = len(hepa) + len(hepa_adult)
    doses_received = 0 if total_doses == 1 else 1 if total_doses == 2 else 2 if total_doses >= 3 else -1
    
    all_dates = hepa + hepa_adult
    valid_dates = [parse_date(date) for date in all_dates]
    valid_dates = [date for date in valid_dates if date is not None]
    
    if valid_dates:
        year_of_last_dose = max(valid_dates).year
    else:
        year_of_last_dose = ''
    
    return doses_received, str(year_of_last_dose), 0 if total_doses > 0 else 1

def fill_pdf(input_pdf_path, output_pdf_path, validation_path, data):
    """Fill PDF form with provided data."""
    race_values, ethnicity_value = get_race_ethnicity(data)
    doses_received, year_of_last_dose, hav_vaccine = get_hav_vaccine_info(data)
    case_phone = data['attributes']['telecom'].split('-')
    date_of_birth = data['attributes']['birthdate_as_localdate'].split('-')
    age = f"{data['attributes']['AGE']}"
    alt_result_date = fake.date()
    ast_result_date = fake.date()
    address = data['attributes']['address']
    address_1 = fake.street_address()
    address_2 = fake.secondary_address()
    admit_date =  fake.date()
    age_1 = str(2024 - int(fake.year()))
    age_2 = str(2024 - int(fake.year()))
    age_3 = str(2024 - int(fake.year()))
    age_4 = str(2024 - int(fake.year()))
    agency = fake.company()
    agency_investigating =  fake.company()
    native = race_values['Am Indian or Alaska Native']
    asian = race_values['Asian']
    black = race_values['Black']
    phone = f"  {case_phone[0]}     {case_phone[1]}-{case_phone[2]}"
    city = data['attributes']['city']
    county = data['attributes']['county']
    dob = f"  {date_of_birth[0]}     {date_of_birth[1]}       {date_of_birth[2]}"
    date_investigation_completed = fake.date()
    date_of_diagnosis = fake.date()
    date_of_lab_test = fake.date()
    date_reported = fake.date()
    email = fake.company_email()
    investigation_name = fake.name()
    investigation_start_date = fake.date()
    investigator_phone = fake.phone_number()
    reported_by = fake.name()
    reported_phone = fake.phone_number()
    patient_first_name = data['attributes']['first_name'],
    patient_last_name = data['attributes']['last_name'],
    parent_guardian =  data['attributes']['name_father'],
    physician = get_primary_physician_last_name(data),
    physician_phone = fake.phone_number(),

    form_data = {
        '1': '1',
        '1_2': '1_2',
        '2': '2',
        '2_2': '2_2',
        'AGE': age,
        'ALT SGPT Result': 'ALT SGPT Result',
        'ALT result date': alt_result_date ,
        'AST SGPT Result': 'AST SGPT Result',
        'AST result date': ast_result_date,
        'Address': address,
        'Address 1': address_1,
        'Address 2': address_2,
        'Admit date': admit_date,
        'Age 1': age_1,
        'Age 2': age_2,
        'Age 3': age_3,
        'Age 4': age_4,
        'Agency': agency,
        'Agency_Investigating': agency_investigating,
        'Am Indian or Alaska Native': native,
        'Asian': asian,
        'Assoc_child_daycare': 0,
        'Assoc_daycare': 0,
        'Assoc_outbreak': 0,
        'Babysitter': 0,
        'Bilirubin elevated': 0,
        'Bilirubin test date': 'Bilirubin test date',
        'Black': black,
        'Case Phone': phone,
        'Case Status': 0,
        'Check box if history of homelessness in last 6 months': True,
        'Child care': 0,
        'City': city,
        'Comments': 'Comments',
        'Contact': 0,
        'Contact - HH': 0,
        'County': county,
        'DATE OF BIRTH': dob,
        'DOD': 'DOD',
        'Date investigation completed': date_investigation_completed,
        'Date of Diagnosis': date_of_diagnosis,
        'Date of lab test': date_of_lab_test,
        'Date reported': date_reported,
        'Die from hepatitis': 0,
        'Discharge date': 'Discharge date',
        "Doses of HAV vaccine rec'd": doses_received,
        'Duration of Stay': 'Duration of Stay',
        'EDD': 'EDD',
        'Earliest date PH control initiated': 'Earliest date PH control initiated',
        'Email': email,
        'Epi linked': 0,
        'Evaluation of elevated liver enzymes': True,
        'Followup testing prior viral hepatitis maker': True,
        'Food_handler': 0,
        'HAIG1': 'HAIG1',
        'HAIG2': 'HAIG2',
        'HAIG3': 'HAIG3',
        'HAIG4': 'HAIG4',
        'HAV RNA': 0,
        'HAV vaccine': hav_vaccine,
        'HAV1': 'HAV1',
        'HAV2': 'HAV2',
        'HAV3': 'HAV3',
        'HAV4': 'HAV4',
        'HAV_daycare': 0,
        'HCW': 0,
        'HISPANIC': ethnicity_value,
        'Hospitalized at': 'Hospitalized at',
        'IVDU': 0,
        'If female is patient currently pregnant': 0,
        'If yes where': 'If yes where',
        'If yes where_2': 'If yes where_2',
        'IgM anti-HAV': 0,
        'Ilness End Date': 'Ilness End Date',
        'Investigated by': investigation_name,
        'Investigation start date': investigation_start_date,
        'Investigator phone': investigator_phone,
        'Jaundiced': 0,
        'Last day of work': fake.date(),
        'Last day of work_2': fake.date(),
        'NBS INVESTIGATION ID': fake.passport_number(),
        'NBS PATIENT ID': fake.passport_number(),
        'Name 1': fake.name(),
        'Name 2': fake.name(),
        'Name_3': fake.name(),
        'Name_4': fake.name(),
        'Native Hawaiian or Other Pac Islander': race_values['Native Hawaiian or Other Pac Islander'],
        'No source': 0,
        'Not_Food_handler': 0,
        'Obstetricians name address and phone 1': 'Obstetricians name address and phone 1',
        'Obstetricians name address and phone 2': 'Obstetricians name address and phone 2',
        'Onset Date': fake.date(),
        'Other Place of birth': 'Other Place of birth',
        'Other reason for testing': True,
        'Other reason for testing specified': 'Other reason for testing specified',
        'Other_2': 'Other_2',
        'Other_Contact': 0,
        'ParentGuardian': parent_guardian,
        'Patients First Name': patient_first_name,
        'Patients Last Name': patient_last_name,
        'Physician': physician,
        'Physician phone': physician_phone,
        'Place of Birth': 0 if data['attributes']['birth_country'].lower() in ['us', 'usa'] else 1,
        'Playmate_': 0,
        'Region': 'Region',
        'Relation to Case 2': 'Relation to Case 2',
        'Relation to Case 3': 'Relation to Case 3',
        'Relation to Case 4': 'Relation to Case 4',
        'Reported by': reported_by,
        'Reporter Phone': reported_phone,
        'SEX': 0 if data['attributes']['gender'].lower() in ['m', 'male'] else 1 if data['attributes']['gender'].lower() in ['f', 'female'] else 2,
        'Screening of asymptomatic patient w risk factors': True,
        'Screening of asymptomatic patient wo risk factors': True,
        'Sex Partners': 0,
        'Specify food item': 'Specify food item',
        'Specify job title or duties': fake.job(),
        'Street_drugs': 0,
        'Symptomatic': 0,
        'Symptoms of acute Hepatitis': True,
        'Testing Facility': fake.state_abbr(),
        'Total anti-HAV': 0,
        'Travel_OOC': 0,
        'Travel_OOC_3months': 0,
        'Unknown_3': race_values['Unknown_3'],
        'Unknown_testing': True,
        'Upper limit normal': 'Upper limit normal',
        'Upper limit normal_2': 'Upper limit normal_2',
        'Was a food handler': 0,
        'Was the patient hospitalized for this illness': 0,
        'Waterborne_': 0,
        'White': race_values['White'],
        'Year of last HAV vaccine dose': f" {year_of_last_dose[0]}   {year_of_last_dose[1]}    {year_of_last_dose[2]}   {year_of_last_dose[3]}" if year_of_last_dose != '' else '' ,
        'Zip': data['attributes']['zip'],
        'female_sex_partners': 0,
        'male_sex_partners': 0,
        'undefined_14': race_values['undefined_14'],
    }

    json_data = {
        'patient_first_name': patient_first_name,
        'patient_last_name': patient_last_name,
        'address': address,
        'city': city,
        'parent_guardian': parent_guardian,
        'physician': physician,
        'physician_phone': physician_phone,
        'physician_address': address_1,
        'physician_address': address_2,
        'reported_by': reported_by,
        'agency': agency,
        'agency_investigating': agency_investigating,
        'agency_phone': investigator_phone,
        'agency_email': email,
        'investigation_start_date': investigation_start_date,
        'date_investigation_completion': date_investigation_completed
    }

    json_string = json.dumps(json_data, indent=4)


    filled = PdfWrapper(input_pdf_path).fill(form_data)

    with open(output_pdf_path, 'wb') as output:
        output.write(filled.read())
    with open(validation_path, 'w') as json_output:
        json_output.write(json_string)



def process_json_folder(json_folder, pdf_template, output_folder, validation_folder):
    """Process all JSON files in a folder and generate filled PDFs."""
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            json_path = os.path.join(json_folder, filename)
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
            
            output_pdf_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
            fill_pdf(pdf_template, output_pdf_path, validation_folder, data)

if __name__ == "__main__":
    current_dir = os.getcwd()
    json_folder = os.path.join(current_dir, "json_files")
    pdf_template = os.path.join(current_dir, "hepatitis_a.pdf")
    output_folder = os.path.join(current_dir, "output_pdfs")
    validation_folder = os.path.join(current_dir, "validation_jsons")
    
    os.makedirs(output_folder, exist_ok=True)
    
    process_json_folder(json_folder, pdf_template, output_folder, validation_folder)