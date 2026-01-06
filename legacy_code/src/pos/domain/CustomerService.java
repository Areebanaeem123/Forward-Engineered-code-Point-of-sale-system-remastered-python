package pos.domain;

import pos.dataaccess.FileDataAccess;
import pos.config.SystemConfig;
import java.io.IOException;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

/**
 * Service for customer-related operations.
 * Extracted from Management class to reduce God class complexity.
 */
public class CustomerService {
    private FileDataAccess dataAccess;
    private String userDatabase;
    
    public CustomerService() {
        this.dataAccess = new FileDataAccess();
        this.userDatabase = SystemConfig.USER_DB;
    }
    
    /**
     * Checks if customer exists
     */
    public boolean customerExists(long phoneNumber) {
        try {
            Map<Long, List<String>> rentals = dataAccess.readCustomerRentals(userDatabase);
            return rentals.containsKey(phoneNumber);
        } catch (IOException e) {
            System.err.println("Error checking customer: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Creates a new customer
     */
    public boolean createCustomer(long phoneNumber) {
        try {
            Map<Long, List<String>> rentals = dataAccess.readCustomerRentals(userDatabase);
            if (!rentals.containsKey(phoneNumber)) {
                rentals.put(phoneNumber, new ArrayList<>());
                dataAccess.writeCustomerRentals(userDatabase, rentals);
                return true;
            }
            return false; // Customer already exists
        } catch (IOException e) {
            System.err.println("Error creating customer: " + e.getMessage());
            return false;
        }
    }
}

