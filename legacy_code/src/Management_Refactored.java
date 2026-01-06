package pos.domain;

import pos.model.ReturnItem;
import pos.model.Item;
import java.util.List;

/**
 * Refactored Management class.
 * Now delegates to specialized services instead of doing everything itself.
 * 
 * REFACTORING: Break God Class into focused services
 */
public class Management_Refactored {
    private CustomerService customerService;
    private RentalService rentalService;
    
    public Management_Refactored() {
        this.customerService = new CustomerService();
        this.rentalService = new RentalService();
    }
    
    /**
     * Checks if user exists
     */
    public Boolean checkUser(Long phone) {
        return customerService.customerExists(phone);
    }
    
    /**
     * Creates a new user
     */
    public boolean createUser(Long phone) {
        return customerService.createCustomer(phone);
    }
    
    /**
     * Gets latest return date for outstanding rentals
     */
    public List<ReturnItem> getLatestReturnDate(Long phone) {
        return rentalService.getOutstandingRentals(phone);
    }
    
    /**
     * Adds a rental record
     */
    public void addRental(long phone, List<Item> rentalList) {
        rentalService.addRental(phone, rentalList);
    }
    
    /**
     * Updates rental status to returned
     */
    public void updateRentalStatus(long phone, List<ReturnItem> returnedList) {
        rentalService.markRentalsAsReturned(phone, returnedList);
    }
}

