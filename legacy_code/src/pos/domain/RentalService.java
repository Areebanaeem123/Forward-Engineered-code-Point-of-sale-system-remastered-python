package pos.domain;

import pos.dataaccess.FileDataAccess;
import pos.model.ReturnItem;
import pos.util.DateCalculator;
import pos.config.SystemConfig;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * Service for rental-related operations.
 * Extracted from Management class to reduce God class complexity.
 */
public class RentalService {
    private FileDataAccess dataAccess;
    private String userDatabase;
    private SimpleDateFormat dateFormatter;
    
    // Constants for parsing
    private static final int PHONE_INDEX = 0;
    private static final int RENTAL_DATA_START_INDEX = 1;
    private static final int ITEM_ID_INDEX = 0;
    private static final int RETURN_DATE_INDEX = 1;
    private static final int RETURNED_FLAG_INDEX = 2;
    
    public RentalService() {
        this.dataAccess = new FileDataAccess();
        this.userDatabase = SystemConfig.USER_DB;
        this.dateFormatter = new SimpleDateFormat(SystemConfig.RETURN_DATE_FORMAT);
    }
    
    /**
     * Gets outstanding rentals for a customer
     */
    public List<ReturnItem> getOutstandingRentals(long phoneNumber) {
        List<ReturnItem> returnItems = new ArrayList<>();
        
        try {
            Map<Long, List<String>> rentals = dataAccess.readCustomerRentals(userDatabase);
            List<String> customerRentals = rentals.get(phoneNumber);
            
            if (customerRentals == null || customerRentals.isEmpty()) {
                return returnItems;
            }
            
            for (String rentalEntry : customerRentals) {
                ReturnItem item = parseRentalEntry(rentalEntry);
                if (item != null) {
                    returnItems.add(item);
                }
            }
            
        } catch (IOException e) {
            System.err.println("Error reading rentals: " + e.getMessage());
        }
        
        return returnItems;
    }
    
    /**
     * Parses a single rental entry string
     */
    private ReturnItem parseRentalEntry(String rentalEntry) {
        String[] parts = rentalEntry.split(",");
        if (parts.length < 3) {
            return null;
        }
        
        try {
            String returnedFlag = parts[RETURNED_FLAG_INDEX];
            if (returnedFlag.equalsIgnoreCase("true")) {
                return null; // Already returned
            }
            
            int itemId = Integer.parseInt(parts[ITEM_ID_INDEX]);
            String returnDateStr = parts[RETURN_DATE_INDEX];
            
            Date returnDate = dateFormatter.parse(returnDateStr);
            Calendar returnCal = Calendar.getInstance();
            returnCal.setTime(returnDate);
            
            int daysLate = DateCalculator.daysFromToday(returnCal);
            if (daysLate > 0) {
                return new ReturnItem(itemId, daysLate);
            }
            
        } catch (NumberFormatException | ParseException e) {
            // Skip invalid entries
            return null;
        }
        
        return null;
    }
    
    /**
     * Adds a rental record
     */
    public void addRental(long phoneNumber, List<pos.model.Item> rentalItems) {
        try {
            Map<Long, List<String>> rentals = dataAccess.readCustomerRentals(userDatabase);
            
            // Ensure customer exists
            if (!rentals.containsKey(phoneNumber)) {
                rentals.put(phoneNumber, new ArrayList<>());
            }
            
            List<String> customerRentals = rentals.get(phoneNumber);
            String currentDate = dateFormatter.format(new Date());
            
            // Add rental entries
            for (pos.model.Item item : rentalItems) {
                String rentalEntry = String.format("%d,%s,false", 
                    item.getItemID(), currentDate);
                customerRentals.add(rentalEntry);
            }
            
            dataAccess.writeCustomerRentals(userDatabase, rentals);
            
        } catch (IOException e) {
            System.err.println("Error adding rental: " + e.getMessage());
            throw new RuntimeException("Failed to add rental", e);
        }
    }
    
    /**
     * Updates rental status to returned
     */
    public void markRentalsAsReturned(long phoneNumber, List<ReturnItem> returnedItems) {
        try {
            Map<Long, List<String>> rentals = dataAccess.readCustomerRentals(userDatabase);
            List<String> customerRentals = rentals.get(phoneNumber);
            
            if (customerRentals == null) {
                return;
            }
            
            String returnDate = dateFormatter.format(new Date());
            List<String> updatedRentals = new ArrayList<>();
            
            for (String rentalEntry : customerRentals) {
                String updatedEntry = updateRentalEntryIfReturned(
                    rentalEntry, returnedItems, returnDate);
                updatedRentals.add(updatedEntry);
            }
            
            rentals.put(phoneNumber, updatedRentals);
            dataAccess.writeCustomerRentals(userDatabase, rentals);
            
        } catch (IOException e) {
            System.err.println("Error updating rental status: " + e.getMessage());
            throw new RuntimeException("Failed to update rental status", e);
        }
    }
    
    /**
     * Updates a rental entry if it's in the returned items list
     */
    private String updateRentalEntryIfReturned(String rentalEntry, 
                                                List<ReturnItem> returnedItems, 
                                                String returnDate) {
        String[] parts = rentalEntry.split(",");
        if (parts.length < 3) {
            return rentalEntry; // Invalid format, return as-is
        }
        
        try {
            int itemId = Integer.parseInt(parts[ITEM_ID_INDEX]);
            String returnedFlag = parts[RETURNED_FLAG_INDEX];
            
            // Check if this item is in returned list
            for (ReturnItem returnedItem : returnedItems) {
                if (returnedItem.getItemID() == itemId && 
                    returnedFlag.equalsIgnoreCase("false")) {
                    // Mark as returned
                    return String.format("%d,%s,true", itemId, returnDate);
                }
            }
            
        } catch (NumberFormatException e) {
            // Invalid format, return as-is
        }
        
        return rentalEntry;
    }
}

