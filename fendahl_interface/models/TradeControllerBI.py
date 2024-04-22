from odoo import models, fields


class TradeControllerBI(models.Model):
    _name = 'trade.controller.bi'
    _description = 'Trade Controller BI'
    
    # Integer Fields
    deal_master_id = fields.Integer(string='Deal Master ID')
    segment_id = fields.Integer(string='Segment ID')
    logistic_contract_id = fields.Integer(string='Logistic Contract ID')
    inter_comp_trade_number = fields.Integer(string='Inter Company Trade Number')
    master_contract_id = fields.Integer(string='Master Contract ID')
    inter_company_buy_id = fields.Integer(string='Inter Company Buy ID')
    inter_company_sell_id = fields.Integer(string='Inter Company Sell ID')
    deal_sheet_master_id = fields.Integer(string='Deal Sheet Master ID')
    efp_deal_master_id = fields.Integer(string='EFP Deal Master ID')
    chartering_instrument_id = fields.Integer(string='Chartering Instrument ID')
    company_agreement_id = fields.Integer(string='Company Agreement ID')
    trade_blotter_process_master_id = fields.Integer(string='Trade Blotter Process Master ID')
    transfer_number = fields.Integer(string='Transfer Number')
    nomination_key = fields.Integer(string='Nomination Key')
    offer_number = fields.Integer(string='Offer Number')
    parent_link_trade_id = fields.Integer(string='Parent Link Trade ID')
    file_import_id = fields.Integer(string='File Import ID')
    ref_physical_id = fields.Integer(string='Ref Physical ID')
    lock_id = fields.Integer(string='Lock ID')
    modify_person_id = fields.Integer(string='Modify Person ID')
    customer_id = fields.Integer(string='Customer ID')
    
    # Char Fields
    external_ref = fields.Char(string='External Reference', size=250)
    internal_company = fields.Char(string='Internal Company', size=250)
    counterpart_company = fields.Char(string='Counterpart Company', size=250)
    trader_person = fields.Char(string='Trader Person', size=752)
    segment_section_code = fields.Char(string='Segment Section Code', size=250)
    commodity = fields.Char(string='Commodity', size=250)
    delivery_term = fields.Char(string='Delivery Term', size=250)
    strategy = fields.Char(string='Strategy', size=250)
    location = fields.Char(string='Location', size=250)
    qty_uom = fields.Char(string='Quantity UOM', size=250)
    calendar = fields.Char(string='Calendar', size=250)
    delivery_schedule = fields.Char(string='Delivery Schedule', size=250)
    settlement_currency = fields.Char(string='Settlement Currency', size=250)
    settlement_uom = fields.Char(string='Settlement UOM', size=250)
    settlement_payment_term = fields.Char(string='Settlement Payment Term', size=250)
    venture_code = fields.Char(string='Venture Code', size=250)
    trade_link_id = fields.Char(string='Trade Link ID', size=250)
    trade_link_code = fields.Char(string='Trade Link Code', size=100)
    exchange_contract = fields.Char(string='Exchange Contract', size=250)
    exchange_ref = fields.Char(string='Exchange Reference', size=250)
    broker_ref = fields.Char(string='Broker Reference', size=250)
    broker2_company = fields.Char(string='Broker2 Company', size=250)
    exchange = fields.Char(string='Exchange', size=250)
    trade_price = fields.Char(string='Trade Price', size=500)
    price_currency = fields.Char(string='Price Currency', size=250)
    price_uom = fields.Char(string='Price UOM', size=250)
    commodity_group = fields.Char(string='Commodity Group', size=250)
    stage_name = fields.Char(string='Stage Name', size=500)
    current_stage_name = fields.Char(string='Current Stage Name', size=500)
    load_location = fields.Char(string='Load Location', size=250)
    discharge_location = fields.Char(string='Discharge Location', size=250)
    account = fields.Char(string='Account', size=250)
    book = fields.Char(string='Book', size=250)
    brand = fields.Char(string='Brand', size=250)
    shape = fields.Char(string='Shape', size=250)
    grade = fields.Char(string='Grade', size=250)
    fund = fields.Char(string='Fund', size=250)
    origin = fields.Char(string='Origin', size=250)
    segment_reference = fields.Char(string='Segment Reference', size=100)
    portfolio = fields.Char(string='Portfolio', size=250)
    qs_type = fields.Char(string='QS Type', size=250)
    financing_account = fields.Char(string='Financing Account', size=250)
    customer_reference = fields.Char(string='Customer Reference', size=250)
    business_unit = fields.Char(string='Business Unit', size=250)
    portfolio_segment = fields.Char(string='Portfolio Segment', size=250)
    trade_admin = fields.Char(string='Trade Admin', size=752)
    operator = fields.Char(string='Operator', size=752)
    mot = fields.Char(string='MOT', size=250)
    bill_to_party_counterpart = fields.Char(string='Bill To Party Counterpart', size=250)
    payer_counterpart = fields.Char(string='Payer Counterpart', size=250)
    ship_to_party_counterpart = fields.Char(string='Ship To Party Counterpart', size=250)
    invoice_presented_by_counterpart = fields.Char(string='Invoice Presented By Counterpart', size=250)
    intercompany_template_code = fields.Char(string='Intercompany Template Code', size=500)
    link_type = fields.Char(string='Link Type', size=250)
    internal_storage = fields.Char(string='Internal Storage', size=250)
    internal_portfolio = fields.Char(string='Internal Portfolio', size=250)
    internal_strategy = fields.Char(string='Internal Strategy', size=250)
    quote_stdformula = fields.Char(string='Quote StdFormula', size=500)
    vessel_name = fields.Char(string='Vessel Name', size=250)
    trade_sub_status = fields.Char(string='Trade Sub Status', size=250)
    trade_type = fields.Char(string='Trade Type', size=250)
    pricing_type = fields.Char(string='Pricing Type', size=250)
    mailing_address = fields.Char(string='Mailing Address', size=1000)
    shipping_address = fields.Char(string='Shipping Address', size=1000)
    billing_address = fields.Char(string='Billing Address', size=1000)
    reference_number = fields.Char(string='Reference Number', size=250)
    hs_code_type = fields.Char(string='HS Code Type', size=250)
    company_sector = fields.Char(string='Company Sector', size=250)
    internal_reference = fields.Char(string='Internal Reference', size=250)
    un_number = fields.Char(string='UN Number', size=500)
    un_packaging_code = fields.Char(string='UN Packaging Code', size=250)
    reach_registration_no = fields.Char(string='REACH Registration No', size=250)
    hs_code_general = fields.Char(string='HS Code General', size=250)
    hs_code_local = fields.Char(string='HS Code Local', size=250)
    hs_code_total = fields.Char(string='HS Code Total', size=500)
    commodity_group2 = fields.Char(string='Commodity Group 2', size=250)
    exch_contract_type = fields.Char(string='Exch Contract Type', size=250)
    internal_reference1 = fields.Char(string='Internal Reference 1', size=250)
    security_id = fields.Char(string='Security ID', size=250)
    trade_status = fields.Char(string='Trade Status', size=250)
    agreement_type_name = fields.Char(string='Agreement Type Name', size=250)
    agreement_type_code = fields.Char(string='Agreement Type Code', size=500)
    crop_year = fields.Char(string='Crop Year', size=250)
    variety = fields.Char(string='Variety', size=250)
    contract_type = fields.Char(string='Contract Type', size=250)
    asset = fields.Char(string='Asset', size=250)
    clearing_broker = fields.Char(string='Clearing Broker', size=250)
    cash_broker = fields.Char(string='Cash Broker', size=250)
    vehicle = fields.Char(string='Vehicle', size=1000)
    vehicle_mot_type = fields.Char(string='Vehicle MOT Type', size=250)
    line_space = fields.Char(string='Line Space', size=250)
    cleared = fields.Char(string='Cleared', size=250)
    description = fields.Char(string='Description', size=500)
    specification_code = fields.Char(string='Specification Code', size=250)
    packaging_code = fields.Char(string='Packaging Code', size=250)
    license_code = fields.Char(string='License Code', size=250)
    mtm_pricing_type = fields.Char(string='MTM Pricing Type', size=250)
    qty_periodicity_type = fields.Char(string='Qty Periodicity Type', size=250)
    company_agreement_type = fields.Char(string='Company Agreement Type', size=250)
    curve_category = fields.Char(string='Curve Category', size=250)
    index_type = fields.Char(string='Index Type', size=250)
    cp_term = fields.Char(string='CP Term', size=250)
    segment_status = fields.Char(string='Segment Status', size=250)
    last_valued_date = fields.Char(string='Last Valued Date', size=250)
    internal_business_unit = fields.Char(string='Internal Business Unit', size=250)
    product_code = fields.Char(string='Product Code', size=250)
    fx_amount_currency = fields.Char(string='FX Amount Currency', size=250)
    product_symbol = fields.Char(string='Product Symbol', size=250)
    lot_equivalent = fields.Float(string='Lot Equivalent', digits=(24, 9))
    strategy_l1 = fields.Char(string='Strategy L1', size=250)
    strategy_l2 = fields.Char(string='Strategy L2', size=250)
    strategy_l3 = fields.Char(string='Strategy L3', size=250)
    strategy_l4 = fields.Char(string='Strategy L4', size=250)
    strategy_l5 = fields.Char(string='Strategy L5', size=250)
    custom_trade_number = fields.Char(string='Custom Trade Number', size=250)
    custom_section_number = fields.Char(string='Custom Section Number', size=250)
    trigger_expiration_date = fields.Datetime(string='Trigger Expiration Date')
    region_location = fields.Char(string='Region Location', size=250)
    flow_start_date = fields.Datetime(string='Flow Start Date')
    flow_end_date = fields.Datetime(string='Flow End Date')
    ship_to_location = fields.Char(string='Ship To Location', size=250)
    quote = fields.Char(string='Quote', size=250)
    service_level_enum = fields.Char(string='Service Level Enum', size=250)
    pipeline_rate_matrix = fields.Char(string='Pipeline Rate Matrix', size=250)
    mtm_curve = fields.Char(string='MTM Curve', size=250)
    price = fields.Float(string='Price', digits=(23, 8))
    pricing_term = fields.Char(string='Pricing Term', size=250)
    payment_term = fields.Char(string='Payment Term', size=250)
    contact_person = fields.Char(string='Contact Person', size=752)
    bill_to_location = fields.Char(string='Bill To Location', size=250)
    location_bs_option = fields.Char(string='Location BS Option', size=250)
    remaining_lots = fields.Float(string='Remaining Lots', digits=(23, 8))
    leg_type = fields.Char(string='Leg Type', size=250)
    weight_final_at = fields.Char(string='Weight Final At', size=250)
    actual_price = fields.Float(string='Actual Price', digits=(24, 9))
    actual_price_uom = fields.Char(string='Actual Price UOM', size=250)
    actual_price_ccy = fields.Char(string='Actual Price CCY', size=250)
    broker_sub_account = fields.Char(string='Broker Sub Account', size=250)
    capacity_quantity = fields.Float(string='Capacity Quantity', digits=(23, 8))
    schedule_enum = fields.Char(string='Schedule Enum', size=250)
    certificate_no = fields.Char(string='Certificate No', size=250)
    inventory_type_display_name = fields.Char(string='Inventory Type DisplayName', size=250)
    strike_price = fields.Float(string='Strike Price', digits=(23, 9))
    hs_code = fields.Char(string='HS Code', size=250)
    unallocated_link_trade_qty = fields.Float(string='Unallocated Link Trade Qty', digits=(23, 8))
    delivery_basis_of = fields.Char(string='Delivery Basis Of', size=250)
    put_call = fields.Char(string='Put/Call', size=250)
    underlying_product_code = fields.Char(string='Underlying Product Code', size=250)
    status_enum = fields.Boolean(string='Status Enum')
    bi_record_creation_date = fields.Datetime(string='BI Record Creation Date')
    
    # Datetime Fields
    trade_input_date = fields.Datetime(string='Trade Input Date')
    trigger_allocation_method = fields.Char(string='Trigger Allocation Method', size=250)
    financing_transfer_date = fields.Datetime(string='Financing Transfer Date')
    declaration_date = fields.Datetime(string='Declaration Date')
    expiry_date = fields.Datetime(string='Expiry Date')
    expiration_date = fields.Datetime(string='Expiration Date')
    finalized_date = fields.Datetime(string='Finalized Date')
    trade_last_modified_date = fields.Datetime(string='Trade Last Modified Date')
    prompt_date = fields.Datetime(string='Prompt Date')
    last_modify_date = fields.Datetime(string='Last Modify Date')
    
    # Boolean Fields
    is_not_for_own_use = fields.Boolean(string='Is Not For Own Use')
    is_embedded_derivative = fields.Boolean(string='Is Embedded Derivative')
    is_financially_settled = fields.Boolean(string='Is Financially Settled')
    offer_sheet_mapped_to_deal = fields.Boolean(string='Offer Sheet Mapped To Deal')
    is_tas_trade = fields.Boolean(string='Is TAS Trade', default=False)
    is_park_and_loan = fields.Boolean(string='Is Park And Loan', default=False)
    is_pool = fields.Boolean(string='Is Pool', default=False)
    is_hazardous_enum = fields.Boolean(string='Is Hazardous Enum', default=False)
    is_reach = fields.Boolean(string='Is REACH', default=False)
    is_coa_check = fields.Boolean(string='Is COA Check', default=False)
    is_animal_feed = fields.Boolean(string='Is Animal Feed', default=False)
    is_vendor = fields.Boolean(string='Is Vendor', default=False)
    is_customer = fields.Boolean(string='Is Customer', default=False)
    is_service_provider = fields.Boolean(string='Is Service Provider', default=False)
    is_producer_manufacturing = fields.Boolean(string='Is Producer/Manufacturing', default=False)
    is_repacker_tollerer = fields.Boolean(string='Is Repacker/Tollerer', default=False)
    is_other = fields.Boolean(string='Is Other', default=False)
    is_composite = fields.Boolean(string='Is Composite', default=False)
    is_mtm_overwrite = fields.Boolean(string='Is MTM Overwrite', default=False)
    is_mtm_default = fields.Boolean(string='Is MTM Default', default=False)
    is_attachment_available = fields.Boolean(string='Is Attachment Available')
    is_notes_available = fields.Boolean(string='Is Notes Available')
    is_finalized = fields.Boolean(string='Is Finalized', default=False)
    is_time_spread = fields.Boolean(string='Is Time Spread', default=False)
    is_imported_trade = fields.Boolean(string='Is Imported Trade', default=False)
    is_structured_deal = fields.Boolean(string='Is Structured Deal')
    is_internal = fields.Boolean(string='Is Internal')
    is_intercompany_pricing = fields.Boolean(string='Is Intercompany Pricing', default=False)
    is_invoiced = fields.Boolean(string='Is Invoiced', default=False)
    is_trade_lock = fields.Boolean(string='Is Trade Lock', default=False)
    is_call_gas = fields.Boolean(string='Is Call Gas', default=False)
    is_ice_deal = fields.Boolean(string='Is ICE Deal', default=False)
    is_contract_not_required = fields.Boolean(string='Is Contract Not Required', default=False)
    is_ddp = fields.Boolean(string='Is DDP', default=False)
    is_force_majeure = fields.Boolean(string='Is Force Majeure', default=False)
    is_term_allocated_to_barge_freight = fields.Boolean(string='Is Term Allocated to Barge Freight', default=False)
    
    # Decimal/Float Fields
    lot = fields.Float(string='Lot', digits=(27, 9))
    lot_size = fields.Float(string='Lot Size', digits=(27, 9))
    trade_qty = fields.Float(string='Trade Quantity', digits=(28, 9))
    total_allocated_qty = fields.Float(string='Total Allocated Qty', digits=(21, 6))
    open_allocated_qty = fields.Float(string='Open Allocated Qty', digits=(21, 6))
    concentrate_enum = fields.Integer(string='Concentrate Enum')  # Assuming Integer type based on context
    planning_quantity = fields.Float(string='Planning Quantity', digits=(23, 8))
    shipping_quantity = fields.Float(string='Shipping Quantity', digits=(23, 8))
    hourly_daily_qty = fields.Float(string='Hourly/Daily Qty', digits=(23, 8))
    shelf_life = fields.Float(string='Shelf Life', digits=(24, 9))
    # price = fields.Float(string='Price', digits=(23, 8))
    # strike_price = fields.Float(string='Strike Price', digits=(23, 9))
    # remaining_lots = fields.Float(string='Remaining Lots', digits=(23, 8))
    # capacity_quantity = fields.Float(string='Capacity Quantity', digits=(23, 8))
    # actual_price = fields.Float(string='Actual Price', digits=(24, 9))
    
    # Text Fields
    letter_of_credit = fields.Text(string='Letter Of Credit')
    udf1 = fields.Text(string='UDF1')
    udf2 = fields.Text(string='UDF2')
    udf3 = fields.Text(string='UDF3')
    udf4 = fields.Text(string='UDF4')
    udf5 = fields.Text(string='UDF5')
    udf6 = fields.Text(string='UDF6')
    udf7 = fields.Text(string='UDF7')
    udf8 = fields.Text(string='UDF8')
    udf9 = fields.Text(string='UDF9')
    udf10 = fields.Text(string='UDF10')
    material = fields.Text(string='Material')
    # mtm_pricing_type = fields.Text(string='MTM Pricing Type')