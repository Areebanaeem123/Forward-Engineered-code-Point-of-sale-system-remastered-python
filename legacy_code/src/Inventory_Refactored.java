package pos.domain;

import pos.dataaccess.FileDataAccess;
import pos.model.Item;
import java.io.IOException;
import java.util.*;

/**
 * Inventory management service (Refactored).
 * Uses data access layer for file operations.
 * 
 * REFACTORING #2: Extract File I/O Operations to Data Access Layer
 */
public class Inventory_Refactored {
    private static Inventory_Refactored uniqueInstance = null;
    private FileDataAccess dataAccess;
    
    private Inventory_Refactored() {
        this.dataAccess = new FileDataAccess();
    }
    
    public static synchronized Inventory_Refactored getInstance() {
        if (uniqueInstance == null) {
            uniqueInstance = new Inventory_Refactored();
        }
        return uniqueInstance;
    }
    
    /**
     * Loads inventory from file into the provided list
     * @param databaseFile Path to inventory file
     * @param databaseItem List to populate with items
     * @return true if successful, false otherwise
     */
    public boolean accessInventory(String databaseFile, List<Item> databaseItem) {
        try {
            List<Item> items = dataAccess.readItems(databaseFile);
            databaseItem.clear();
            databaseItem.addAll(items);
            return true;
        } catch (IOException e) {
            System.err.println("Error reading inventory file: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Updates inventory based on transaction items
     * @param databaseFile Path to inventory file
     * @param transactionItem Items in transaction
     * @param databaseItem Current inventory items (will be updated)
     * @param takeFromInventory true to decrement (sale/rental), false to increment (return)
     */
    public void updateInventory(String databaseFile, List<Item> transactionItem, 
                                List<Item> databaseItem, boolean takeFromInventory) {
        // Update in-memory list
        for (Item transItem : transactionItem) {
            for (Item dbItem : databaseItem) {
                if (transItem.getItemID() == dbItem.getItemID()) {
                    int newAmount = takeFromInventory
                        ? dbItem.getAmount() - transItem.getAmount()
                        : dbItem.getAmount() + transItem.getAmount();
                    dbItem.updateAmount(newAmount);
                    break;
                }
            }
        }
        
        // Persist to file using data access layer
        try {
            dataAccess.writeItems(databaseFile, databaseItem);
        } catch (IOException e) {
            System.err.println("Error writing inventory file: " + e.getMessage());
            throw new RuntimeException("Failed to update inventory", e);
        }
    }
}

