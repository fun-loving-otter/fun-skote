from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Data(models.Model):
    uploaded_data_file = models.ForeignKey('UploadedDataFile', on_delete=models.CASCADE)

    _header_field_mapping = {
        'Organization Name': 'organization_name',
        'Crunchbase Company URL': 'crunchbase_company_url',
        'Founded Date': 'founded_date',
        'Full Description': 'full_description',
        'Industries': 'industries',
        'Headquarters': 'headquarters',
        'Description': 'description',
        'CB Rank': 'cb_rank',
        'LinkedIn': 'linkedin',
        'Facebook': 'facebook',
        'Last Funding Date': 'last_funding_date',
        'Number Of Funding': 'number_of_funding',
        'Funding Status': 'funding_status',
        'Last Equity Funding': 'last_equity_funding',
        'Estimate Revenue': 'estimate_revenue',
        'Operating Status': 'operating_status',
        'Website': 'website',
        'Twitter': 'twitter',
        'Company Type': 'company_type',
        'Contact Email': 'contact_email',
        'Phone Number': 'phone_number',
        'Industry Groups': 'industry_groups',
        'Number of Founders': 'number_of_founders',
        'Name of Founder': 'name_of_founder',
        'Number of Employees': 'number_of_employees',
        'Total Funding Amount': 'total_funding_amount',
        'Total Equity Funding': 'total_equity_funding',
        'Last Equity Funding Type': 'last_equity_funding_type',
        'Top 5 Investor': 'top_5_investor',
        'Acquisition Status': 'acquisition_status',
        'Number of Acquisition': 'number_of_acquisition',
        'IPO Status': 'ipo_status',
        'IPO Date': 'ipo_date',
        'Money Raised at IPO': 'money_raised_at_ipo',
        'Valuation at IPO': 'valuation_at_ipo',
        'Monthly Visits': 'monthly_visits',
        'Global Traffic Rank': 'global_traffic_rank',
        'Exit Date': 'exit_date',
        'Closed Date': 'closed_date',
        'Actively Hiring': 'actively_hiring',
        'Number of Investor': 'number_of_investor',
        'Number of Lead Investor': 'number_of_lead_investor',
        'Stock Symbol': 'stock_symbol',
        'Last Leadership Hiring Date': 'last_leadership_hiring_date',
        'Last Layoff Mention Date': 'last_layoff_mention_date',
        'CB Rank (Organization)': 'cb_rank_organization',
        'Visit Duration': 'visit_duration',
        'Bounce Rate': 'bounce_rate',
        'Patent Granted': 'patent_granted',
        'Trademarks Registered': 'trademarks_registered',
        'IT Spend': 'it_spend',
        'Most Recent Valuation Range': 'most_recent_valuation_range',
        'Date of Most Recent Valuation': 'date_of_most_recent_valuation',
        'Investor Type': 'investor_type',
        'Investment Stage': 'investment_stage',
        'Last Funding Amount': 'last_funding_amount',
        'Headquarters Regions': 'headquarters_regions',
        'Diversity Spotlight (US Headquarters Only)': 'diversity_spotlight',
        'Number of Articles': 'number_of_articles',
        'Number of Portfolio Organizations': 'number_of_portfolio_organizations',
        'Number of Investments': 'number_of_investments',
        'Number of Lead Investments': 'number_of_lead_investments',
        'Number of Diversity Investments': 'number_of_diversity_investments',
        'Number of Exits': 'number_of_exits',
        'Number of Exits (IPO)': 'number_of_exits_ipo',
        'Accelerator Program Type': 'accelerator_program_type',
        'Accelerator Application Deadline': 'accelerator_application_deadline',
        'Accelerator Duration (in weeks)': 'accelerator_duration_weeks',
        'School Type': 'school_type',
        'School Program': 'school_program',
        'Number of Enrollments': 'number_of_enrollments',
        'School Method': 'school_method',
        'Number of Founders (Alumni)': 'number_of_founders_alumni',
        'Number of Alumni': 'number_of_alumni',
        'Transaction Name': 'transaction_name',
        'Acquired by': 'acquired_by',
        'Announced Date': 'announced_date',
        'Price': 'price',
        'Acquisition Type': 'acquisition_type',
        'Acquisition Terms': 'acquisition_terms',
        'Number of Events': 'number_of_events',
        'Hub Tags': 'hub_tags',
        'Delisted Date': 'delisted_date',
        'Stock Exchange': 'stock_exchange',
        'CB Rank (School)': 'cb_rank_school',
        'Trend Score (7 Days)': 'trend_score_7_days',
        'Trend Score (30 Days)': 'trend_score_30_days',
        'Trend Score (90 Days)': 'trend_score_90_days',
        'Similar Companies': 'similar_companies',
        'Contact Job Departments': 'contact_job_departments',
        'Number of Contacts': 'number_of_contacts',
        'Average Visits (6 months)': 'average_visits_6_months',
        'Monthly Visits Growth': 'monthly_visits_growth',
        'Visit Duration Growth': 'visit_duration_growth',
        'Page Views / Visit': 'page_views_per_visit',
        'Page Views / Visit Growth': 'page_views_per_visit_growth',
        'Bounce Rate Growth': 'bounce_rate_growth',
        'Monthly Rank Change (#)': 'monthly_rank_change',
        'Monthly Rank Growth': 'monthly_rank_growth',
        'Active Tech Count': 'active_tech_count',
        'Number of Apps': 'number_of_apps',
        'Downloads Last 30 Days': 'downloads_last_30_days',
        'Total Products Active': 'total_products_active',
        'Most Popular Patent Class': 'most_popular_patent_class',
        'Most Popular Trademark Class': 'most_popular_trademark_class',
    }

    organization_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Organization Name')
    crunchbase_company_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Crunchbase Company URL')
    founded_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Founded Date')
    full_description = models.TextField(null=True, blank=True, verbose_name='Full Description')
    industries = models.CharField(max_length=255, null=True, blank=True, verbose_name='Industries')
    headquarters = models.CharField(max_length=255, null=True, blank=True, verbose_name='Headquarters')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    cb_rank = models.CharField(max_length=255, null=True, blank=True, verbose_name='CB Rank')
    linkedin = models.CharField(max_length=255, null=True, blank=True, verbose_name='LinkedIn')
    facebook = models.CharField(max_length=255, null=True, blank=True, verbose_name='Facebook')
    last_funding_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Funding Date')
    number_of_funding = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Funding')
    funding_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Funding Status')
    last_equity_funding = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Equity Funding')
    estimate_revenue = models.CharField(max_length=255, null=True, blank=True, verbose_name='Estimate Revenue')
    operating_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Operating Status')
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name='Website')
    twitter = models.CharField(max_length=255, null=True, blank=True, verbose_name='Twitter')
    company_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Company Type')
    contact_email = models.CharField(max_length=255, null=True, blank=True, verbose_name='Contact Email')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    industry_groups = models.CharField(max_length=255, null=True, blank=True, verbose_name='Industry Groups')
    number_of_founders = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Founders')
    name_of_founder = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name of Founder')
    number_of_employees = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Employees')
    total_funding_amount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Total Funding Amount')
    total_equity_funding = models.CharField(max_length=255, null=True, blank=True, verbose_name='Total Equity Funding')
    last_equity_funding_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Equity Funding Type')
    top_5_investor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Top 5 Investor')
    acquisition_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='Acquisition Status')
    number_of_acquisition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Acquisitions')
    ipo_status = models.CharField(max_length=255, null=True, blank=True, verbose_name='IPO Status')
    ipo_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='IPO Date')
    money_raised_at_ipo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Money Raised at IPO')
    valuation_at_ipo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Valuation at IPO')
    monthly_visits = models.CharField(max_length=255, null=True, blank=True, verbose_name='Monthly Visits')
    global_traffic_rank = models.CharField(max_length=255, null=True, blank=True, verbose_name='Global Traffic Rank')
    exit_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Exit Date')
    closed_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Closed Date')
    actively_hiring = models.CharField(max_length=255, null=True, blank=True, verbose_name='Actively Hiring')
    number_of_investor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Investors')
    number_of_lead_investor = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Lead Investors')
    stock_symbol = models.CharField(max_length=255, null=True, blank=True, verbose_name='Stock Symbol')
    last_leadership_hiring_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Leadership Hiring Date')
    last_layoff_mention_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Layoff Mention Date')
    cb_rank_organization = models.CharField(max_length=255, null=True, blank=True, verbose_name='CB Rank (Organization)')
    visit_duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='Visit Duration')
    bounce_rate = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bounce Rate')
    patent_granted = models.CharField(max_length=255, null=True, blank=True, verbose_name='Patent Granted')
    trademarks_registered = models.CharField(max_length=255, null=True, blank=True, verbose_name='Trademarks Registered')
    it_spend = models.CharField(max_length=255, null=True, blank=True, verbose_name='IT Spend')
    most_recent_valuation_range = models.CharField(max_length=255, null=True, blank=True, verbose_name='Most Recent Valuation Range')
    date_of_most_recent_valuation = models.CharField(max_length=255, null=True, blank=True, verbose_name='Date of Most Recent Valuation')
    investor_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Investor Type')
    investment_stage = models.CharField(max_length=255, null=True, blank=True, verbose_name='Investment Stage')
    last_funding_amount = models.CharField(max_length=255, null=True, blank=True, verbose_name='Last Funding Amount')
    headquarters_regions = models.CharField(max_length=255, null=True, blank=True, verbose_name='Headquarters Regions')
    diversity_spotlight = models.CharField(max_length=255, null=True, blank=True, verbose_name='Diversity Spotlight')
    number_of_articles = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Articles')
    number_of_portfolio_organizations = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Portfolio Organizations')
    number_of_investments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Investments')
    number_of_lead_investments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Lead Investments')
    number_of_diversity_investments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Diversity Investments')
    number_of_exits = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Exits')
    number_of_exits_ipo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of IPO Exits')
    accelerator_program_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Accelerator Program Type')
    accelerator_application_deadline = models.CharField(max_length=255, null=True, blank=True, verbose_name='Accelerator Application Deadline')
    accelerator_duration_weeks = models.CharField(max_length=255, null=True, blank=True, verbose_name='Accelerator Duration (Weeks)')
    school_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='School Type')
    school_program = models.CharField(max_length=255, null=True, blank=True, verbose_name='School Program')
    number_of_enrollments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Enrollments')
    school_method = models.CharField(max_length=255, null=True, blank=True, verbose_name='School Method')
    number_of_founders_alumni = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Founders (Alumni)')
    number_of_alumni = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Alumni')
    transaction_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Transaction Name')
    acquired_by = models.CharField(max_length=255, null=True, blank=True, verbose_name='Acquired By')
    announced_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Announced Date')
    price = models.CharField(max_length=255, null=True, blank=True, verbose_name='Price')
    acquisition_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Acquisition Type')
    acquisition_terms = models.CharField(max_length=255, null=True, blank=True, verbose_name='Acquisition Terms')
    number_of_events = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Events')
    hub_tags = models.CharField(max_length=255, null=True, blank=True, verbose_name='Hub Tags')
    delisted_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Delisted Date')
    stock_exchange = models.CharField(max_length=255, null=True, blank=True, verbose_name='Stock Exchange')
    cb_rank_school = models.CharField(max_length=255, null=True, blank=True, verbose_name='CB Rank (School)')
    trend_score_7_days = models.CharField(max_length=255, null=True, blank=True, verbose_name='Trend Score (7 Days)')
    trend_score_30_days = models.CharField(max_length=255, null=True, blank=True, verbose_name='Trend Score (30 Days)')
    trend_score_90_days = models.CharField(max_length=255, null=True, blank=True, verbose_name='Trend Score (90 Days)')
    similar_companies = models.CharField(max_length=255, null=True, blank=True, verbose_name='Similar Companies')
    contact_job_departments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Contact Job Departments')
    number_of_contacts = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Contacts')
    average_visits_6_months = models.CharField(max_length=255, null=True, blank=True, verbose_name='Average Visits (6 Months)')
    monthly_visits_growth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Monthly Visits Growth')
    visit_duration_growth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Visit Duration Growth')
    page_views_per_visit = models.CharField(max_length=255, null=True, blank=True, verbose_name='Page Views per Visit')
    page_views_per_visit_growth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Page Views per Visit Growth')
    bounce_rate_growth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bounce Rate Growth')
    monthly_rank_change = models.CharField(max_length=255, null=True, blank=True, verbose_name='Monthly Rank Change')
    monthly_rank_growth = models.CharField(max_length=255, null=True, blank=True, verbose_name='Monthly Rank Growth')
    active_tech_count = models.CharField(max_length=255, null=True, blank=True, verbose_name='Active Tech Count')
    number_of_apps = models.CharField(max_length=255, null=True, blank=True, verbose_name='Number of Apps')
    downloads_last_30_days = models.CharField(max_length=255, null=True, blank=True, verbose_name='Downloads Last 30 Days')
    total_products_active = models.CharField(max_length=255, null=True, blank=True, verbose_name='Total Products Active')
    most_popular_patent_class = models.CharField(max_length=255, null=True, blank=True, verbose_name='Most Popular Patent Class')
    most_popular_trademark_class = models.CharField(max_length=255, null=True, blank=True, verbose_name='Most Popular Trademark Class')

    def __str__(self):
        return self.organization_name



class DataUpload(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=255)
    size_of_files = models.CharField(max_length=255, null=True, blank=True)
    number_of_files = models.PositiveIntegerField(null=True, blank=True)
    number_of_rows = models.PositiveIntegerField(null=True, blank=True)
    number_of_columns = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name



class UploadedDataFile(models.Model):
    data_upload = models.ForeignKey(DataUpload, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploaded_data_files/')
    processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file)



class DataList(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.ManyToManyField('Data')
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255, null=True, blank=True)
