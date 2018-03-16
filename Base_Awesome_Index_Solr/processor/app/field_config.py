# Field mapping from pre to post index
field_mapping = {
  'id': 'id',
  'im_domains' : 'physicianDomainAccess',
  'sm_field_conditions_and_treatments$name': 'physicianConditions',
  'ss_field_degree': 'physicianMedicalDegree',
  'ss_field_physician_providertype': 'physicianProviderType',
  'tm_field_physician_specialty_ref$name': 'physicianSpecialties',
  'ss_field_physician_sex': 'physicianGender',
  'ss_search_api_url': 'physicianProfileURL',
  'tm_field_physician_photo$file$url': 'physicianPhoto',
  'tm_field_name_search': 'physicianName',
  'tm_field_physician_title': 'physicianTitle',
  'tm_field_clinical_interest$value': 'physicianPracticeAreas',
  'sm_field_physician_locations_ref$name': 'physicianLocationBuildingCampus',
  'tm_field_physician_locations_ref$field_physician_location$name': 'physicianLocationBuildingTitle',
  'tm_field_physician_locations_ref$field_physician_location$street': 'physicianLocationAddress1',
  'tm_field_physician_locations_ref$field_physician_location$additional': 'physicianLocationAddress2',
  'tm_field_physician_locations_ref$field_physician_location$city': 'physicianLocationAddressCity',
  'tm_field_physician_locations_ref$field_physician_location$province': 'physicianLocationAddressState',
  'tm_field_physician_locations_ref$field_physician_location$postal_code': 'physicianLocationAddressZip',
  'tm_field_physician_locations_ref$field_physician_location$phone': 'physicianLocationPhone'
}

# Site Domain Access Map for 'im_domains' to 'physicianDomainAccess'
site_domain_map = {
  1: 'uofmhealth.org',
  2: 'mottchildren.org',
  6: 'umcvc.org',
  11: 'umwomenshealth.org',
  16: 'umkelloggeye.org'
}

# Specialty overrides for EMPI specialty field, if not specified then the EMPI value is used
empi_map = {
  'Adult Reconstructive Orthopedics': 'Orthopaedics',
  'Cardiovascular Surgery': 'Cardiovascular Medicine',
  'Cardiology': 'Cardiovascular Medicine',
  'Gynecology': 'Obstetrics & Gynecology',
  'Hematology & Oncology': 'Hematology and Oncology',
  'Obstetrics': 'Obstetrics & Gynecology',
  'Orthopedic Trauma': 'Orthopaedic Surgery',
  'Orthopedic Surgery': 'Hand Surgery (Orthopedic Surgery)',
  'Pediatric Neurology': 'Child Neurology',
  'Pediatric Orthopedics': 'Orthopaedic Surgery',
  'Radiology': 'Diagnostic Radiology',
  'Sports Medicine (Orthopaedic Surgery)': 'Sports Medicine (Internal Medicine)',
}

# These items trigger an import of EMPI specialties if any are present in the default specialty field
empi_triggers = [
  'Nurse Practitioner',
  'Physician Assistant',
  'Nurse Anesthetist-Certified Registered (CRNA)',
  'Licensed Clinical Social Worker',
  'Midwife-Certified Nurse',
  'Nurse Practitioner - Family',
  'Nurse Practitioner - Primary Care',
  'Nurse Practioner - Adult Health',
  'Nurse Practitioner - Community Health',
  'Nurse Practitioner - Pediatrics',
  'Nurse Practitioner - Acute Care',
  'Optometry'
]

# External locations need to be mapped to the regular location field
external_loc_map = {
  'tm_field_physician_locations_extern$field_external_location$name': 'physicianLocationBuildingTitle',
  'tm_field_physician_locations_extern$field_external_location$street': 'physicianLocationAddress1',
  'tm_field_physician_locations_extern$field_external_location$additional': 'physicianLocationAddress2',
  'tm_field_physician_locations_extern$field_external_location$city': 'physicianLocationAddressCity',
  'tm_field_physician_locations_extern$field_external_location$province': 'physicianLocationAddressState',
  'tm_field_physician_locations_extern$field_external_location$postal_code': 'physicianLocationAddressZip',
  'tm_field_physician_locations_extern$field_external_location$phone': 'physicianLocationAddressPhone'
}

# Certain locations should fall under another building, this map specifies the re-allocation
loc_terms = {
  'Allegiance': 'ALLEGIANCE HOSPITAL',
  'BRIARWOOD': 'WEST ANN ARBOR HEALTH CTR',
  'Burlington': 'BURLINGTON BUILDING',
  'Cancer Center': 'CANCER CENTER',
  'Cardiovascular': 'CARDIOVASCULAR CENTER',
  'Domino': 'DOMINO\'S FARMS',
  'Eisenhower': 'EISENHOWER CORPORATE PARK',
  'East Ann Arbor Health': 'E ANN ARBOR HEALTH & GERIATRIC',
  'Glacier': 'GLACIER HILLS SENIOR LIVING',
  'Med Inn': 'MED INN BUILDING',
  'Mott ': 'MOTT CHILDREN\'S HOSPITAL',
  'Upjohn': 'RACHEL UPJOHN BUILDING',
  'Taubman': 'TAUBMAN CENTER',
  'Traverwood': 'TRAVERWOOD BUSINESS PARK',
  'University Hospital': 'UNIVERSITY HOSPITAL',
  'Va Ann Arbor': 'VETERANS AFFAIRS ANN ARBOR HEALTHCARE SYSTEM',
  'Va Medical': 'VETERANS AFFAIRS ANN ARBOR HEALTHCARE SYSTEM',
  'Voigtlander': 'VONVOIGTLANDER WOMEN\'S HOSPITAL',
  'W.K. K': 'KELLOGG EYE CENTER - ANN ARBOR',
  'Ypsilanti': 'YPSILANTI HEALTH CENTER'
}

loc_exact_terms = {
  'Kellogg Eye Center': 'KELLOGG EYE CENTER - ANN ARBOR',
  'U Of M Anesthesiology': 'UNIVERSITY HOSPITAL',
  'U Of M Audiologists': 'TAUBMAN CENTER',
  'U Of M Dentistry': 'TAUBMAN CENTER',
  'U Of M Cardiac Surgery': 'FRANKEL CARDIOVASCULAR CENTER',
  'U Of M Emergency Medicine': 'UNIVERSITY HOSPITAL',
  'U Of M Endocrinology & Metabolism': 'DOMINO\'S FARMS',
  'U Of M General Medicine': 'CANTON HEALTH CENTER',
  'U Of M Geriatrics': 'E ANN ARBOR HEALTH & GERIATRIC',
  'U Of M Im Geriatrics': 'E ANN ARBOR HEALTH & GERIATRIC',
  'U Of M Internal Medicine': 'TAUBMAN CENTER',
  'U Of M Internal Medicine Cardiology': 'FRANKEL CARDIOVASCULAR CENTER',
  'U Of M Hematology Oncology': 'CANCER CENTER',
  'U Of M Nephrology': 'UNIVERSITY HOSPITAL',
  'U Of M Neurology': 'UNIVERSITY HOSPITAL',
  'U Of M Neurosurgery': 'TAUBMAN CENTER',
  'U Of M Ophthalmology': 'KELLOGG EYE CENTER - ANN ARBOR',
  'U Of M Orthopaedic Surgery': 'MOTT CHILDREN\'S HOSPITAL',
  'U Of M Pediatric Critical Care Special Services': 'MOTT CHILDREN\'S HOSPITAL',
  'U Of M Pediatric Genetics': 'MOTT CHILDREN\'S HOSPITAL',
  'U of M Psychiatry': 'UNIVERSITY HOSPITAL',
  'U Of M Psychology': 'RACHEL UPJOHN BUILDING',
  'U Of M Physical Medicine & Rehabilitation': 'BURLINGTON BUILDING',
  'U Of M Radiology': 'TAUBMAN CENTER',
  'U Of M Rahs': 'LINCOLN MIDDLE SCHOOL',
  'U Of M Rheumatology': 'TAUBMAN CENTER',
  'U Of M Urology': 'UNIVERSITY HOSPITAL',
  'University Health Service': 'UNIVERSITY HOSPITAL',
}

# Building overrides, replace one value with another
loc_overrides = {
 'ALLEGIANCE HOSPITAL': 'Henry Ford Allegiance Health',
 'CARDIOVASCULAR CENTER': 'Frankel Cardiovascular Center',
 'MOTT CHILDREN\'S HOSPITAL': 'C.S. Mott Children\'s Hospital',
 'VA Ann Arbor Healthcare System': 'VETERANS AFFAIRS ANN ARBOR HEALTHCARE SYSTEM',
 'VA  Ann Arbor Healthcare System': 'VETERANS AFFAIRS ANN ARBOR HEALTHCARE SYSTEM',
 'WEST ANN ARBOR HEALTH CTR': 'BRIARWOOD'
}

# Generic specialty override, replace one value with another
spec_overrides = {
  'Facial Plastic Surgery': 'Plastic Surgery'
}

# Downboost triggers, profiles with these degrees will appear lower in search results
degree_triggers = [
  'AuD',
  'MSW',
  'NP',
  'PA-C'
]

# Building removes, remove the location altogether if its there 
loc_removes = {
 'U of M Ophthalmology Research and Patient Care Clinic',
 'Michigan Medicine Ophthalmology Research and Patient Care Clinic'
}
