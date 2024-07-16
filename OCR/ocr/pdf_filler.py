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

def fill_pdf(input_pdf_path, output_pdf_path, data):
    """Fill PDF form with provided data."""
    race_values, ethnicity_value = get_race_ethnicity(data)
    doses_received, year_of_last_dose, hav_vaccine = get_hav_vaccine_info(data)
    case_phone = data['attributes']['telecom'].split('-')
    date_of_birth = data['attributes']['birthdate_as_localdate'].split('-')

    form_data = {
        '1': '1',
        '1_2': '1_2',
        '2': '2',
        '2_2': '2_2',
        'AGE': f"{data['attributes']['AGE']}",
        'ALT SGPT Result': 'ALT SGPT Result',
        'ALT result date': fake.date(),
        'AST SGPT Result': 'AST SGPT Result',
        'AST result date': fake.date(),
        'Address': data['attributes']['address'],
        'Address 1': fake.street_address(),
        'Address 2': fake.secondary_address(),
        'Admit date': fake.date(),
        'Age 1': str(2024 - int(fake.year())),
        'Age 2': str(2024 - int(fake.year())),
        'Age 3': str(2024 - int(fake.year())),
        'Age 4': str(2024 - int(fake.year())),
        'Agency': fake.company(),
        'Agency_Investigating': fake.company(),
        'Am Indian or Alaska Native': race_values['Am Indian or Alaska Native'],
        'Asian': race_values['Asian'],
        'Assoc_child_daycare': 0,
        'Assoc_daycare': 0,
        'Assoc_outbreak': 0,
        'Babysitter': 0,
        'Bilirubin elevated': 0,
        'Bilirubin test date': 'Bilirubin test date',
        'Black': race_values['Black'],
        'Case Phone': f"  {case_phone[0]}     {case_phone[1]}-{case_phone[2]}",
        'Case Status': 0,
        'Check box if history of homelessness in last 6 months': True,
        'Child care': 0,
        'City': data['attributes']['city'],
        'Comments': 'Comments',
        'Contact': 0,
        'Contact - HH': 0,
        'County': data['attributes']['county'],
        'DATE OF BIRTH': f"  {date_of_birth[0]}     {date_of_birth[1]}       {date_of_birth[2]}",
        'DOD': 'DOD',
        'Date investigation completed': fake.date(),
        'Date of Diagnosis': fake.date(),
        'Date of lab test': fake.date(),
        'Date reported': fake.date(),
        'Die from hepatitis': 0,
        'Discharge date': 'Discharge date',
        "Doses of HAV vaccine rec'd": doses_received,
        'Duration of Stay': 'Duration of Stay',
        'EDD': 'EDD',
        'Earliest date PH control initiated': 'Earliest date PH control initiated',
        'Email': fake.company_email(),
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
        'Investigated by': fake.name(),
        'Investigation start date': fake.date(),
        'Investigator phone': fake.phone_number(),
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
        'ParentGuardian': data['attributes']['name_father'],
        'Patients First Name': data['attributes']['first_name'],
        'Patients Last Name': data['attributes']['last_name'],
        'Physician': get_primary_physician_last_name(data),
        'Physician phone': fake.phone_number(),
        'Place of Birth': 0 if data['attributes']['birth_country'].lower() in ['us', 'usa'] else 1,
        'Playmate_': 0,
        'Region': 'Region',
        'Relation to Case 2': 'Relation to Case 2',
        'Relation to Case 3': 'Relation to Case 3',
        'Relation to Case 4': 'Relation to Case 4',
        'Reported by': fake.name(),
        'Reporter Phone': fake.phone_number(),
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

    filled = PdfWrapper(input_pdf_path).fill(form_data)

    with open(output_pdf_path, 'wb') as output:
        output.write(filled.read())

def process_json_folder(json_folder, pdf_template, output_folder):
    """Process all JSON files in a folder and generate filled PDFs."""
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            json_path = os.path.join(json_folder, filename)
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
            
            output_pdf_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
            fill_pdf(pdf_template, output_pdf_path, data)

if __name__ == "__main__":
    current_dir = os.getcwd()
    json_folder = os.path.join(current_dir, "json_files")
    pdf_template = os.path.join(current_dir, "hepatitis_a.pdf")
    output_folder = os.path.join(current_dir, "output_pdfs")
    
    os.makedirs(output_folder, exist_ok=True)
    
    process_json_folder(json_folder, pdf_template, output_folder)