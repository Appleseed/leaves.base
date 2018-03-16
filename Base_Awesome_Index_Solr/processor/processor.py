from app import db
from app.model import Document
from app.field_config import degree_triggers, site_domain_map, empi_map, empi_triggers, external_loc_map, field_mapping, loc_overrides, loc_exact_terms, loc_terms, spec_overrides, loc_removes
from sqlalchemy.orm import Session
from urllib.parse import urlparse

import configparser
import datetime
import re
import requests
import time

config = configparser.ConfigParser()
config.read('config.ini')

# Track starting time of script, needed to delete items removed from drupal
dt_started = datetime.datetime.now()

# How many items to process at once
BATCH_SIZE = 250

# Solr endpoints for each collection
PRE_EP = config['DEFAULT']['pre_ep']
POST_EP = config['DEFAULT']['post_ep']

# Return value in doc or None if key doesn't exist
def getValue(doc, field):
  if field in doc:
    return doc[field]
  else:
    return None

# Utility function to remove html tags, expects a multivalued field
def stripTags(data):
  if data == None:
    return

  for idx, val in enumerate(data):
    exp = re.compile('<.*?>')
    data[idx] = re.sub(exp, '', val)

def titleize(chars):
  result = []
  prev_letter = ' '

  for ch in chars:
      if not prev_letter.isalpha() and prev_letter != "'":
          result.append(ch.upper())
      else:
          result.append(ch.lower())

      prev_letter = ch

  return "".join(result) 

start_offset = 0


# Create a db session
sess = Session(db)

working = True
while working:
  print('Processing batch of {} items'.format(BATCH_SIZE))

  # Params to retrieve page of documents
  params = {
    'start': start_offset,
    'rows': BATCH_SIZE,
    'wt': 'json'
  }
  print(params)

  r = requests.get(PRE_EP + '/select', params=params)
  data = r.json()

  post_docs = []

  working = False
  for doc in data['response']['docs']:
    working = True

    processed = {}
    processed['physicianShowSpecialties'] = True;

    for key in field_mapping:
      processed[field_mapping[key]] = getValue(doc, key)

    # DATA PROCESSING 

    # Map Integers to Domains
    if 'physicianDomainAccess' in processed:
      # Loop over domains in pre, and set the proper domain
      for domain_key, site_domain in enumerate(processed['physicianDomainAccess']):
        if site_domain in site_domain_map:
          processed['physicianDomainAccess'][domain_key] = site_domain_map[site_domain]

    # Strip certain strings from physicianProfileURL and physicianPhoto
    if 'physicianProfileURL' in processed:
          if ( processed['physicianProfileURL'] ) :
                parsedProfileURL = urlparse(processed['physicianProfileURL'])
                processed['physicianProfileURL'] = parsedProfileURL.path

    if 'physicianPhoto' in processed:
      if ( processed['physicianPhoto'] ) :
        parsedPhotoURL   = urlparse(processed['physicianPhoto'][0])
        processed['physicianPhoto'][0] = parsedPhotoURL.path

    # Strip HTML tags from practice areas
    if 'physicianPracticeAreas' in processed:
      stripTags(processed['physicianPracticeAreas'])

    # Inject last name value into glossary (need to snag first from multivalued field)
    last_name = getValue(doc, 'tm_field_physician_lastname')
    if last_name is not None and len(last_name) > 0:
      processed['glossary'] = last_name[0]

    # Verify fields that we manipulate in processing 
    if processed['physicianSpecialties'] is None:
      processed['physicianSpecialties'] = []

    if processed['physicianLocationAddressCity'] is None:
      processed['physicianLocationAddressCity'] = []

    if processed['physicianLocationBuildingCampus'] is None:
      processed['physicianLocationBuildingCampus'] = []

    if processed['physicianLocationBuildingTitle'] is None:
        processed['physicianLocationBuildingTitle'] = []

    if processed['physicianMedicalDegree'] is None:
      processed['physicianMedicalDegree'] = []

    if processed['physicianName'] is None:
      processed['physicianName'] = []

    sub_specs = getValue(doc, 'tm_field_physician_subspecialty_ref$name')
    if sub_specs is not None:
      processed['physicianSpecialties'] = processed['physicianSpecialties'] + sub_specs

    # Use first value of name for name suggestion
    if len(processed['physicianName']) > 0:
      processed['physicianName_suggest'] = processed['physicianName'][0]
    
    # Check to see if specialties contain any trigger words
    if not set(processed['physicianSpecialties']).isdisjoint(set(empi_triggers)):
      processed['physicianShowSpecialties'] = False;

      # Remove empi triggers from the specialty list
      processed['physicianSpecialties'] = list(set(processed['physicianSpecialties']) - set(empi_triggers))

      # Loop over empi specs, check for overrides and add appropriate value
      empi_specs = []
      empi_specs.append(getValue(doc, 'ss_field_empi_specialty'))
      empi_specs.append(getValue(doc, 'ss_field_empi_subspecialty'))

      for empi_spec in empi_specs:
        if empi_spec is not None and len(empi_spec) > 0:
          empi_val = empi_spec
          if empi_val in empi_map:
            empi_val = empi_map[empi_val]
          processed['physicianSpecialties'].append(empi_val)

    # Lowercase "and' in specialties
    for i, item in enumerate(processed['physicianSpecialties']):
      processed['physicianSpecialties'][i] = item.replace(' And ', ' and ')
    
    # Check for general specialty overrides
    for override in spec_overrides:
      if override in processed['physicianSpecialties']:
        processed['physicianSpecialties'].remove(override)
        processed['physicianSpecialties'].append(spec_overrides[override])

    # Prepend external locations to regular location fields if set
    for external_loc, destination in external_loc_map.items():
      external_value = getValue(doc, external_loc)
      if external_value is not None:
        if destination not in processed:
          processed[destination] = []
        processed[destination] = external_value + processed[destination]
    
    # Do location renamings - string contains renames
    for loc_mapping in loc_terms:
      for i, item in enumerate(processed['physicianLocationBuildingCampus']):
        if item.lower().find(loc_mapping.lower()) > -1 and item.lower().find('south') == -1:
          processed['physicianLocationBuildingCampus'][i] = loc_terms[loc_mapping]

    # More location renaming - exact match renames
    for loc_mapping in loc_exact_terms:
      for i, item in enumerate(processed['physicianLocationBuildingCampus']):
        if item.lower() == loc_mapping.lower():
          processed['physicianLocationBuildingCampus'][i] = loc_exact_terms[loc_mapping] 
    
    # Check for location overrides
    for override in loc_overrides:
      if override in processed['physicianLocationBuildingCampus']:
        processed['physicianLocationBuildingCampus'].remove(override)
        processed['physicianLocationBuildingCampus'].append(titleize(loc_overrides[override]))

    # Title-ize campus names
    for i,item in enumerate(processed['physicianLocationBuildingCampus']):
      processed['physicianLocationBuildingCampus'][i] = titleize(item)

    # Don't allow unspecified gender
    if processed['physicianGender'] == 'U':
      processed['physicianGender'] = None

    # Modify cities to have consistent formatting
    for i, item in enumerate(processed['physicianLocationAddressCity']):
      processed['physicianLocationAddressCity'][i] = titleize(item)
      

    # Don't allow CRNA profiles
    if 'CRNA' in processed['physicianMedicalDegree']:
      continue

    # Set physicianIsMd which is used in boosting
    processed['physicianIsMd'] = True
    for degree in degree_triggers:
      if degree in processed['physicianMedicalDegree']:
        processed['physicianIsMd'] = False
        break

     # Remove if in loc_removes (should be always after any other processing related to locations)
    for remove_item in loc_removes:
        if remove_item in processed['physicianLocationBuildingTitle']:
          remove_index = processed['physicianLocationBuildingTitle'].index(remove_item)
          processed['physicianLocationBuildingCampus'].pop(remove_index)
          processed['physicianLocationBuildingTitle'].pop(remove_index)
          processed['physicianLocationAddress1'].pop(remove_index)
          processed['physicianLocationAddress2'].pop(remove_index)
          processed['physicianLocationAddressCity'].pop(remove_index)
          processed['physicianLocationAddressState'].pop(remove_index)
          processed['physicianLocationAddressZip'].pop(remove_index)
          processed['physicianLocationPhone'].pop(remove_index)        

    post_docs.append(processed)

    # Store processing state in sql
    sqldoc = sess.query(Document).filter(Document.solr_id == doc['id']).first()
    if sqldoc == None:
      sqldoc = Document(doc['id'])
      sess.add(sqldoc) 
    else:
      sqldoc.tick()

  # Update solr
  requests.post(POST_EP + '/update?commit=true', json=post_docs)

  # Commit SQL changes
  sess.commit()

  # Increment paging
  start_offset += BATCH_SIZE 
 
# Any records with dt_processed < dt_started were not processed which indicates deletion from drupal
print('Cleaning up deleted records...')
num_deleted = 0
for deleted in sess.query(Document).filter(Document.dt_processed < dt_started): 
  num_deleted += 1
  requests.post(POST_EP + '/update?commit=true', json = {'delete': {'id': deleted.solr_id }})
  sess.delete(deleted)
sess.commit()
print('{} records deleted'.format(num_deleted))



