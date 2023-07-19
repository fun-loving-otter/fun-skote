import dateparser

from datetime import datetime

from .mappings import FIELD_TO_JSON_MAPPING
from .utilities import MagicGetter


dateparse_settings = {'RELATIVE_BASE': datetime.fromtimestamp(0)}


def convert_to_string_processor(value):
    return str(value)[:1023]



def list_value_concatenation_processor(value):
    getter = MagicGetter(value)
    result = ''
    for i in range(len(value)):
        part = getter.get([i, 'value'])
        if part is None:
            continue
        result += part + ' '

    return result.strip()[:1023]



def list_join_processor(value):
    if not isinstance(value, list) or not all(isinstance(el, str) for el in value):
        return None
    return ' '.join(value)[:1023]



def date_processor(value):
    return dateparser.parse(str(value))



processors = dict.fromkeys(FIELD_TO_JSON_MAPPING.keys(), convert_to_string_processor)

processors['headquarters'] = list_value_concatenation_processor
processors['industry_groups'] = list_value_concatenation_processor
processors['top_5_investor'] = list_value_concatenation_processor

processors['contact_job_departments'] = list_join_processor

processors['founded_date'] = date_processor
processors['last_funding_date'] = date_processor
processors['ipo_date'] = date_processor
