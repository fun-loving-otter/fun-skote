import os
import tempfile
from pathlib import Path

from django.db import models
from django.db.models import Sum, Index
from django.contrib.auth import get_user_model

from celery.result import AsyncResult

from main.consts import action_names
from main.consts.data_header_field_mapping import HEADER_FIELD_MAPPING

User = get_user_model()

TEMP_DIR = Path(tempfile.gettempdir()).resolve()


class Data(models.Model):
    uploaded_data_file = models.ForeignKey('UploadedDataFile', on_delete=models.CASCADE, db_index=True)

    _header_field_mapping = HEADER_FIELD_MAPPING

    _hidden_fields = {
        'website',
        'crunchbase_company_url',
        'linkedin',
        'facebook',
        'twitter',
        'email',
        'contact_email',
    }

    _searchable_fields = {
        'char': {
            'organization_name',
            'full_description',
            'industries',
            'description',
            'linkedin',
            'facebook',
            'twitter',
            'website',
            'industry_groups'
        },
        'date_range': {
            'founded_date',
            'last_funding_date',
            'ipo_date'
        },
        'int_range': {
            'estimate_revenue',
            'number_of_employees',
            'total_funding_amount',
            'total_equity_funding',
            'money_raised_at_ipo',
            'valuation_at_ipo',
        },
        'select': {
            'headquarters',
        }
    }

    organization_name = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Organization Name', db_index=True)
    crunchbase_company_url = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Crunchbase Company URL')
    founded_date = models.DateField(max_length=1023, null=True, blank=True, verbose_name='Founded Date', db_index=True)
    full_description = models.TextField(null=True, blank=True, verbose_name='Full Description')
    industries = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Industries')
    headquarters = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Headquarters', db_index=True)
    description = models.TextField(null=True, blank=True, verbose_name='Description', db_index=True)
    cb_rank = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CB Rank')
    linkedin = models.CharField(max_length=1023, null=True, blank=True, verbose_name='LinkedIn')
    facebook = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Facebook')
    last_funding_date = models.DateField(max_length=1023, null=True, blank=True, verbose_name='Last Funding Date', db_index=True)
    number_of_funding = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Funding')
    funding_status = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Funding Status')
    last_equity_funding = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Last Equity Funding')
    estimate_revenue = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Estimate Revenue', db_index=True)
    operating_status = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Operating Status')
    website = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Website')
    twitter = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Twitter')
    company_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Company Type')
    contact_email = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Contact Email')
    phone_number = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Phone Number')
    industry_groups = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Industry Groups')
    number_of_founders = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Founders')
    name_of_founder = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Name of Founder')
    number_of_employees = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Employees', db_index=True)
    total_funding_amount = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Total Funding Amount', db_index=True)
    total_equity_funding = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Total Equity Funding', db_index=True)
    last_equity_funding_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Last Equity Funding Type')
    top_5_investor = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Top 5 Investor')
    acquisition_status = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Acquisition Status')
    number_of_acquisition = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Acquisitions')
    ipo_status = models.CharField(max_length=1023, null=True, blank=True, verbose_name='IPO Status')
    ipo_date = models.DateField(max_length=1023, null=True, blank=True, verbose_name='IPO Date', db_index=True)
    money_raised_at_ipo = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Money Raised at IPO', db_index=True)
    valuation_at_ipo = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Valuation at IPO', db_index=True)
    monthly_visits = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Monthly Visits')
    global_traffic_rank = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Global Traffic Rank')
    exit_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Exit Date')
    closed_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Closed Date')
    actively_hiring = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Actively Hiring')
    number_of_investor = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Investors')
    number_of_lead_investor = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Lead Investors')
    stock_symbol = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Stock Symbol')
    last_leadership_hiring_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Last Leadership Hiring Date')
    last_layoff_mention_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Last Layoff Mention Date')
    cb_rank_organization = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CB Rank (Organization)')
    visit_duration = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Visit Duration')
    bounce_rate = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Bounce Rate')
    patent_granted = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Patent Granted')
    trademarks_registered = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Trademarks Registered')
    it_spend = models.CharField(max_length=1023, null=True, blank=True, verbose_name='IT Spend')
    most_recent_valuation_range = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Most Recent Valuation Range')
    date_of_most_recent_valuation = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Date of Most Recent Valuation')
    investor_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Investor Type')
    investment_stage = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Investment Stage')
    last_funding_amount = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Last Funding Amount')
    headquarters_regions = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Headquarters Regions')
    diversity_spotlight = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Diversity Spotlight')
    number_of_articles = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Articles')
    number_of_portfolio_organizations = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Portfolio Organizations')
    number_of_investments = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Investments')
    number_of_lead_investments = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Lead Investments')
    number_of_diversity_investments = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Diversity Investments')
    number_of_exits = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Exits')
    number_of_exits_ipo = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of IPO Exits')
    accelerator_program_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Accelerator Program Type')
    accelerator_application_deadline = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Accelerator Application Deadline')
    accelerator_duration_weeks = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Accelerator Duration (Weeks)')
    school_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='School Type')
    school_program = models.CharField(max_length=1023, null=True, blank=True, verbose_name='School Program')
    number_of_enrollments = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Enrollments')
    school_method = models.CharField(max_length=1023, null=True, blank=True, verbose_name='School Method')
    number_of_founders_alumni = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Founders (Alumni)')
    number_of_alumni = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Alumni')
    transaction_name = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Transaction Name')
    acquired_by = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Acquired By')
    announced_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Announced Date')
    price = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Price')
    acquisition_type = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Acquisition Type')
    acquisition_terms = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Acquisition Terms')
    number_of_events = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Events')
    hub_tags = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Hub Tags')
    delisted_date = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Delisted Date')
    stock_exchange = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Stock Exchange')
    cb_rank_school = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CB Rank (School)')
    trend_score_7_days = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Trend Score (7 Days)')
    trend_score_30_days = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Trend Score (30 Days)')
    trend_score_90_days = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Trend Score (90 Days)')
    similar_companies = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Similar Companies')
    contact_job_departments = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Contact Job Departments')
    number_of_contacts = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Contacts')
    average_visits_6_months = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Average Visits (6 Months)')
    monthly_visits_growth = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Monthly Visits Growth')
    visit_duration_growth = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Visit Duration Growth')
    page_views_per_visit = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Page Views per Visit')
    page_views_per_visit_growth = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Page Views per Visit Growth')
    bounce_rate_growth = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Bounce Rate Growth')
    monthly_rank_change = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Monthly Rank Change')
    monthly_rank_growth = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Monthly Rank Growth')
    active_tech_count = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Active Tech Count')
    number_of_apps = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Number of Apps')
    downloads_last_30_days = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Downloads Last 30 Days')
    total_products_active = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Total Products Active')
    most_popular_patent_class = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Most Popular Patent Class')
    most_popular_trademark_class = models.CharField(max_length=1023, null=True, blank=True, verbose_name='Most Popular Trademark Class')
    ceo_name = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CEO Name')
    ceo_email = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CEO Email')
    ceo_phone = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CEO Phone')
    ceo_linkedin = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CEO Linkedin')
    cfo_name = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CFO Name')
    cfo_email = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CFO Email')
    cfo_phone = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CFO Phone')
    cfo_linkedin = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CFO Linkedin')
    cmo_name = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CMO Name')
    cmo_email = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CMO Email')
    cmo_phone = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CMO Phone')
    cmo_linkedin = models.CharField(max_length=1023, null=True, blank=True, verbose_name='CMO Linkedin')

    class Meta:
        ordering = ['organization_name', '-pk']


    def __str__(self):
        return self.organization_name



class DataUpload(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=255)
    size_of_files = models.PositiveIntegerField(null=True, blank=True)
    number_of_files = models.PositiveIntegerField(default=0)
    number_of_rows = models.PositiveIntegerField(default=0)
    number_of_columns = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


    def str_size_of_files(self):
        size_bytes = self.size_of_files

        if not size_bytes:
            return str(size_bytes)

        """Converts the given file size in bytes to a human-readable format."""
        # Define the units and their respective labels
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        # Iterate over the units and divide the size by 1024 at each step
        for unit in units:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        # If the size is larger than the largest unit (TB), return it in TB
        return f"{size_bytes:.2f} {units[-1]}"



class UploadedDataFile(models.Model):
    data_upload = models.ForeignKey(DataUpload, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_data_files/')
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return os.path.basename(str(self.file))


    @classmethod
    def get_upload_temp_dir(cls, user):
        target_directory = TEMP_DIR / "jfl" / "DataUploads" / str(user.id)
        os.makedirs(target_directory, exist_ok=True)
        return target_directory


    @classmethod
    def get_file_name(cls, file, upload_id):
        return f"{upload_id}_{file.name}"


    @classmethod
    def get_chunk_name(cls, file, upload_id, chunk_index):
        chunk_name = f"{cls.get_file_name(file, upload_id)}_chunk_{chunk_index}"
        return chunk_name


    def get_celery_result(self):
        if getattr(self, 'celery_result', None):
            return self.celery_result

        if not self.celery_task_id:
            return

        self.celery_result = AsyncResult(self.celery_task_id)
        return self.celery_result



class DataExport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    info = models.CharField(max_length=1023)



class DataList(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.ManyToManyField('Data')
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return (str(self.name))



class DataPackageBenefits(models.Model):
    action_credits = models.IntegerField(default=0)
    add_to_list_credits = models.IntegerField(default=0)
    export_credits = models.IntegerField(default=0)
    package = models.OneToOneField('payments.SubscriptionPackage', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.package.name)


    def get_credits_for_action(self, action, raise_error=True):
        if action == action_names.ACTION:
            return self.action_credits
        elif action == action_names.ADD_TO_LIST:
            return self.add_to_list_credits
        elif action == action_names.EXPORT:
            return self.export_credits

        # If neither action matched:
        if raise_error:
            raise AttributeError(f'No credits found for action {action}')
        else:
            return 0



class UserThrottledActionEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    amount = models.IntegerField(default=1)

    class Meta:
        indexes = [
            Index(fields=['user']),
            Index(fields=['action']),
        ]

    @classmethod
    def get_mapped_usage(cls, user, subscription):
        q = cls.objects.filter(user=user).values('action').annotate(total_amount=Sum('amount')).order_by('action')

        usage = {}

        for item in q:
            action_name = item['action']
            used = item['total_amount']
            if subscription:
                credits = subscription.package.datapackagebenefits.get_credits_for_action(action_name, raise_error=False)
            else:
                credits = 0
            usage[action_name] = {
                'used': used,
                'remaining': credits - used,
                'credits': credits
            }

        return usage



class DataColumnVisibility(models.Model):
    field_name = models.CharField(max_length=1023, unique=True)
    header = models.CharField(max_length=1023)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.field_name


    @classmethod
    def get_visible(cls):
        columns = cls.objects.filter(visible=True).values_list('header', 'field_name')
        headers = []
        field_names = []
        for col in columns:
            headers.append(col[0])
            field_names.append(col[1])

        return headers, field_names


    @classmethod
    def get_visible_headers(cls):
        headers = cls.objects.filter(visible=True).values_list('header', flat=True)
        return list(headers)


    @classmethod
    def get_visible_field_names(cls):
        field_names = cls.objects.filter(visible=True).values_list('field_name', flat=True)
        return list(field_names)
