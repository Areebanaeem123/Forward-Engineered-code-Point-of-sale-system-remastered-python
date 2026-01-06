"""
System Configuration - Singleton Pattern
Centralizes all system-wide constants and configuration
"""


class SystemConfig:
    """
    Singleton configuration class for POS system
    Contains all system-wide constants
    """
    _instance = None
    
    # Tax and discount rates
    TAX_RATE = 1.06  # 6% tax
    DISCOUNT_RATE = 0.90  # 10% discount (for coupons)
    LATE_FEE_RATE = 0.1  # 10% late fee per day
    RENTAL_PERIOD_DAYS = 14  # Standard rental period
    
    # Date formats
    DATE_FORMAT = "MM/dd/yy"
    DATETIME_FORMAT = "yyyy-MM-dd HH:mm:ss.SSS"
    
    # Credit card validation
    CREDIT_CARD_LENGTH = 16
    
    # File paths (for legacy data migration)
    EMPLOYEE_DB = "Database/employeeDatabase.txt"
    ITEM_DB = "Database/itemDatabase.txt"
    RENTAL_DB = "Database/rentalDatabase.txt"
    USER_DB = "Database/userDatabase.txt"
    COUPON_DB = "Database/couponNumber.txt"
    EMPLOYEE_LOG_FILE = "Database/employeeLogfile.txt"
    SALE_INVOICE_RECORD = "Database/saleInvoiceRecord.txt"
    RETURN_SALE_RECORD = "Database/returnSale.txt"
    TEMP_FILE = "Database/temp.txt"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemConfig, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_tax_rate(cls):
        """Get tax rate"""
        return cls.TAX_RATE
    
    @classmethod
    def get_discount_rate(cls):
        """Get discount rate"""
        return cls.DISCOUNT_RATE
    
    @classmethod
    def get_late_fee_rate(cls):
        """Get late fee rate"""
        return cls.LATE_FEE_RATE
    
    @classmethod
    def get_rental_period_days(cls):
        """Get rental period in days"""
        return cls.RENTAL_PERIOD_DAYS

