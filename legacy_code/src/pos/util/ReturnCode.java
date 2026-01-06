package pos.util;

/**
 * Constants for return codes.
 * Replaces magic numbers with meaningful constants.
 */
public class ReturnCode {
    // Login return codes
    public static final int LOGIN_FAILED = 0;
    public static final int LOGIN_CASHIER = 1;
    public static final int LOGIN_ADMIN = 2;
    
    // Employee update return codes
    public static final int EMPLOYEE_NOT_FOUND = -1;
    public static final int EMPLOYEE_FOUND = 0;
    public static final int INVALID_POSITION = -2;
    
    // Array indices for employee parsing
    public static final int EMPLOYEE_USERNAME_INDEX = 0;
    public static final int EMPLOYEE_POSITION_INDEX = 1;
    public static final int EMPLOYEE_FIRSTNAME_INDEX = 2;
    public static final int EMPLOYEE_LASTNAME_INDEX = 3;
    public static final int EMPLOYEE_PASSWORD_INDEX = 4;
    
    // Array indices for item parsing
    public static final int ITEM_ID_INDEX = 0;
    public static final int ITEM_NAME_INDEX = 1;
    public static final int ITEM_PRICE_INDEX = 2;
    public static final int ITEM_AMOUNT_INDEX = 3;
    
    private ReturnCode() {
        // Prevent instantiation
    }
}

