import os
import json
import logging
import shutil
import dateparser

from zipfile import ZipFile
from datetime import datetime

from main.models import Data



dateparse_settings = {'RELATIVE_BASE': datetime.fromtimestamp(0)}
logger = logging.getLogger(__name__)

class MagicGetter:
    def __init__(self, data):
        self.data = data

    def get(self, keys):
        try:
            result = self.data
            for key in keys:
                result = result[key]
            return result
        except (KeyError, TypeError, IndexError):
            return None



def convert_to_string_processor(value):
    return str(value)



def list_value_concatenation_processor(value):
    getter = MagicGetter(value)
    result = ''
    for i in range(len(value)):
        part = getter.get([i, 'value'])
        # if part is None:
        #     return
        result += part + ' '

    return result.strip()



def list_join_processor(value):
    if not isinstance(value, list) or not all(isinstance(el, str) for el in value):
        return None
    return ' '.join(value)



def date_processor(value):
    return dateparser.parse(str(value))



field_to_json_mapping = {
    'organization_name': ['properties', 'identifier', 'value'],
    'crunchbase_company_url': ['properties', 'identifier', 'permalink'],
    'founded_date': ['properties', 'founded_on', 'value'],
    'full_description': ['properties', 'description'],
    'industries': None,
    'headquarters': ['properties', 'location_identifiers'],
    'description': ['properties', 'short_description'],
    'cb_rank': ['properties', 'rank_org'],
    'linkedin': ['properties', 'linkedin', 'value'],
    'facebook': ['properties', 'facebook', 'value'],
    'last_funding_date': ['properties', 'last_funding_at'],
    'number_of_funding': ['properties', 'num_funding_rounds'],
    'funding_status': None,
    'last_equity_funding': ['properties', 'last_equity_funding_type'],
    'estimate_revenue': ['properties', 'revenue_range'],
    'operating_status': ['properties', 'operating_status'],
    'website': ['properties', 'website', 'value'],
    'twitter': ['properties', 'twitter', 'value'],
    'company_type': ['properties', 'company_type'],
    'contact_email': ['properties', 'contact_email'],
    'phone_number': ['properties', 'phone_number'],
    'industry_groups': ['properties', 'category_groups'],
    'number_of_founders': ['properties', 'num_founders'],
    'name_of_founder': ['properties', 'founder_identifiers', 0, 'value'],
    'number_of_employees': ['properties', 'num_employees_enum'],
    'total_funding_amount': ['properties', 'funding_total', 'value_usd'],
    'total_equity_funding': ['properties', 'equity_funding_total', 'value_usd'],
    'last_equity_funding_type': ['properties', 'last_equity_funding_type'],
    'top_5_investor': ['properties', 'investor_identifiers'],
    'acquisition_status': ['properties', 'acquisition_status', 0],
    'number_of_acquisition': None,
    'ipo_status': ['properties', 'ipo_status'],
    'ipo_date': None,
    'money_raised_at_ipo': None,
    'valuation_at_ipo': None,
    'monthly_visits': ['properties', 'semrush_visits_latest_month'],
    'global_traffic_rank': ['properties', 'semrush_global_rank'],
    'exit_date': ['properties', 'exited_on', 'value'],
    'closed_date': ['properties', 'closed_on', 'value'],
    'actively_hiring': None,
    'number_of_investor': ['properties', 'num_investors'],
    'number_of_lead_investor': ['properties', 'num_lead_investors'],
    'stock_symbol': None,
    'last_leadership_hiring_date': None,
    'last_layoff_mention_date': None,
    'cb_rank_organization': ['properties', 'rank_org'],
    'visit_duration': ['properties', 'semrush_visit_duration'],
    'bounce_rate': ['properties', 'semrush_bounce_rate'],
    'patent_granted': None,
    'trademarks_registered': None,
    'it_spend': None,
    'most_recent_valuation_range': ['properties', 'last_equity_funding_total', 'currency'],
    'date_of_most_recent_valuation': ['properties', 'last_funding_at'],
    'investor_type': None,
    'investment_stage': None,
    'last_funding_amount': ['properties', 'funding_total', 'value_usd'],
    'headquarters_regions': ['properties', 'location_group_identifiers', 0, 'value'],
    'diversity_spotlight': None,
    'number_of_articles': ['properties', 'num_articles'],
    'number_of_portfolio_organizations': ['properties', 'siftery_num_products'],
    'number_of_investments': None,
    'number_of_lead_investments': ['properties', 'num_lead_investors'],
    'number_of_diversity_investments': None,
    'number_of_exits': None,
    'number_of_exits_ipo': None,
    'accelerator_program_type': None,
    'accelerator_application_deadline': None,
    'accelerator_duration_weeks': None,
    'school_type': None,
    'school_program': None,
    'number_of_enrollments': None,
    'school_method': None,
    'number_of_founders_alumni': ['properties', 'num_founders'],
    'number_of_alumni': None,
    'transaction_name': ['properties', 'acquisition_identifier', 'value'],
    'acquired_by': ['properties', 'acquirer_identifier', 'value'],
    'announced_date': ['properties', 'acquisition_announced_on', 'value'],
    'price': None,
    'acquisition_type': ['properties', 'acquisition_type'],
    'acquisition_terms': None,
    'number_of_events': None,
    'hub_tags': None,
    'delisted_date': None,
    'stock_exchange': None,
    'cb_rank_school': None,
    'trend_score_7_days': ['properties', 'rank_delta_d7'],
    'trend_score_30_days': ['properties', 'rank_delta_d30'],
    'trend_score_90_days': ['properties', 'rank_delta_d90'],
    'similar_companies': ['properties', 'num_org_similarities'],
    'contact_job_departments': ['properties', 'contact_job_departments'],
    'number_of_contacts': ['properties', 'num_contacts'],
    'average_visits_6_months': ['properties', 'semrush_visits_latest_6_months_avg'],
    'monthly_visits_growth': ['properties', 'semrush_visits_mom_pct'],
    'visit_duration_growth': ['properties', 'semrush_visit_duration_mom_pct'],
    'page_views_per_visit': ['properties', 'semrush_visit_pageviews'],
    'page_views_per_visit_growth': ['properties', 'semrush_visit_pageview_mom_pct'],
    'bounce_rate_growth': ['properties', 'semrush_bounce_rate_mom_pct'],
    'monthly_rank_change': ['properties', 'semrush_global_rank_mom'],
    'monthly_rank_growth': ['properties', 'semrush_global_rank_mom_pct'],
    'active_tech_count': ['properties', 'builtwith_num_technologies_used'],
    'number_of_apps': ['properties', 'apptopia_total_apps'],
    'downloads_last_30_days': None,
    'total_products_active': ['properties', 'siftery_num_products'],
    'most_popular_patent_class': None,
    'most_popular_trademark_class': None,
    'ceo_name': None,
    'ceo_email': None,
    'ceo_phone': None,
    'ceo_linkedin': None,
    'cfo_name': None,
    'cfo_email': None,
    'cfo_phone': None,
    'cfo_linkedin': None,
    'cmo_name': None,
    'cmo_email': None,
    'cmo_phone': None,
    'cmo_linkedin': None
}


processors = dict.fromkeys(field_to_json_mapping.keys(), convert_to_string_processor)

processors['headquarters'] = list_value_concatenation_processor
processors['industry_groups'] = list_value_concatenation_processor
processors['top_5_investor'] = list_value_concatenation_processor

processors['contact_job_departments'] = list_join_processor

processors['founded_date'] = date_processor
processors['last_funding_date'] = date_processor
processors['ipo_date'] = date_processor



def parse_zip_with_jsons(uploaded_data_file):
    logger.info(f"Started processing {uploaded_data_file} in zip/json mode")

    # Unzip the file
    unzip_dir = os.path.splitext(uploaded_data_file.file.path)[0]
    with ZipFile(uploaded_data_file.file.path, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)

    # Walk through the unzipped directory
    for root, dirs, files in os.walk(unzip_dir):
        for file in files:
            filepath = os.path.join(root, file)
            parse_single_json(filepath, uploaded_data_file)

    # Clean up - remove the unzipped files
    shutil.rmtree(unzip_dir)

    uploaded_data_file.processed = True
    uploaded_data_file.save()

    logger.info(f'Finished processing {uploaded_data_file}')

    return uploaded_data_file



def parse_single_json(filepath, uploaded_data_file):
    if not filepath.endswith('.json'):
        return

    try:
        with open(filepath) as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"Got error {e}, skipping file {filepath}")

    entries = data['entities']

    uploaded_data_file.data_upload.number_of_rows += len(entries)
    uploaded_data_file.data_upload.save()

    # Create Data objects for entries
    data_objects = []
    for row in entries:
        row_getter = MagicGetter(row)
        kwargs = {}

        for field_name, keys in field_to_json_mapping.items():
            # Attempt to get value
            value = row_getter.get(keys)

            if value is None:
                continue

            # Apply processor to value
            processor = processors.get(field_name)
            value = processor(value)

            kwargs[field_name] = value

        data_objects.append(Data(
            uploaded_data_file=uploaded_data_file,
            **kwargs
        ))

    Data.objects.bulk_create(data_objects)

    logger.info(f"Finished processing {filepath} in zip/json mode. {len(data_objects)} objects created.")
