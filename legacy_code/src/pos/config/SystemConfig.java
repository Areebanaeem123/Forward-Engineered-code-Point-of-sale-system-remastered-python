package pos.config;

/**
 * Centralized system configuration.
 * All business rules and file paths are defined here.
 */
public class SystemConfig {
    // Business Rules
    public static final double TAX_RATE = 1.06;              // 6% tax
    public static final float COUPON_DISCOUNT_RATE = 0.90f;  // 10% discount
    public static final double LATE_FEE_RATE = 0.1;          // 10% per day
    public static final int RENTAL_PERIOD_DAYS = 14;         // 14 days rental period
    
    // File Paths
    public static final String DATABASE_DIR = "Database/";
    public static final String EMPLOYEE_DB = DATABASE_DIR + "employeeDatabase.txt";
    public static final String ITEM_DB = DATABASE_DIR + "itemDatabase.txt";
    public static final String RENTAL_DB = DATABASE_DIR + "rentalDatabase.txt";
    public static final String USER_DB = DATABASE_DIR + "userDatabase.txt";
    public static final String COUPON_DB = DATABASE_DIR + "couponNumber.txt";
    public static final String TEMP_FILE = DATABASE_DIR + "temp.txt";
    public static final String LOG_FILE = DATABASE_DIR + "employeeLogfile.txt";
    public static final String INVOICE_FILE = DATABASE_DIR + "saleInvoiceRecord.txt";
    public static final String RETURN_FILE = DATABASE_DIR + "returnSale.txt";
    
    // Validation Rules
    public static final int CREDIT_CARD_LENGTH = 16;
    public static final long MIN_PHONE = 1000000000L;
    public static final long MAX_PHONE = 9999999999L;
    public static final int MAX_COUPONS = 1000;
    
    // Date Formats
    public static final String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss.SSS";
    public static final String RETURN_DATE_FORMAT = "MM/dd/yy";
    
    private SystemConfig() {
        // Prevent instantiation
    }
}

