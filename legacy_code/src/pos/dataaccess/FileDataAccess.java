package pos.dataaccess;

import pos.model.Item;
import java.io.*;
import java.util.*;

/**
 * Data Access Layer for file-based storage.
 * Provides abstraction for file I/O operations.
 */
public class FileDataAccess {
    
    /**
     * Reads items from inventory file
     */
    public List<Item> readItems(String filePath) throws IOException {
        List<Item> items = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                
                String[] parts = line.split(" ");
                if (parts.length < 4) continue; // Skip invalid lines
                
                try {
                    int itemID = Integer.parseInt(parts[0]);
                    String itemName = parts[1];
                    float price = Float.parseFloat(parts[2]);
                    int amount = Integer.parseInt(parts[3]);
                    
                    items.add(new Item(itemID, itemName, price, amount));
                } catch (NumberFormatException e) {
                    // Skip invalid lines
                    continue;
                }
            }
        }
        return items;
    }
    
    /**
     * Writes items to inventory file
     */
    public void writeItems(String filePath, List<Item> items) throws IOException {
        File tempFile = new File(filePath + ".tmp");
        
        try (PrintWriter writer = new PrintWriter(
                new BufferedWriter(new FileWriter(tempFile)))) {
            
            for (Item item : items) {
                writer.printf("%d %s %.2f %d%n",
                    item.getItemID(),
                    item.getItemName(),
                    item.getPrice(),
                    item.getAmount());
            }
        }
        
        // Atomic file replacement
        File originalFile = new File(filePath);
        if (originalFile.exists()) {
            originalFile.delete();
        }
        tempFile.renameTo(originalFile);
    }
    
    /**
     * Reads employee records from file
     */
    public List<String[]> readEmployees(String filePath) throws IOException {
        List<String[]> employees = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                String[] parts = line.split(" ", 5); // Limit split to preserve password
                if (parts.length >= 5) {
                    employees.add(parts);
                }
            }
        }
        return employees;
    }
    
    /**
     * Writes employee records to file
     */
    public void writeEmployees(String filePath, List<String[]> employees) throws IOException {
        File tempFile = new File(filePath + ".tmp");
        
        try (PrintWriter writer = new PrintWriter(
                new BufferedWriter(new FileWriter(tempFile)))) {
            
            for (String[] employee : employees) {
                writer.printf("%s %s %s %s %s%n",
                    employee[0], employee[1], employee[2], employee[3], employee[4]);
            }
        }
        
        // Atomic file replacement
        File originalFile = new File(filePath);
        if (originalFile.exists()) {
            originalFile.delete();
        }
        tempFile.renameTo(originalFile);
    }
    
    /**
     * Appends line to log file
     */
    public void appendLog(String filePath, String logEntry) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new FileWriter(filePath, true))) {
            writer.write(logEntry);
            writer.newLine();
        }
    }
    
    /**
     * Reads customer rental records
     */
    public Map<Long, List<String>> readCustomerRentals(String filePath) throws IOException {
        Map<Long, List<String>> rentals = new HashMap<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String header = reader.readLine(); // Skip header
            
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                
                String[] parts = line.split(" ", 2);
                if (parts.length < 1) continue;
                
                try {
                    long phone = Long.parseLong(parts[0]);
                    List<String> rentalEntries = new ArrayList<>();
                    
                    if (parts.length > 1) {
                        String[] rentalParts = parts[1].split(" ");
                        rentalEntries.addAll(Arrays.asList(rentalParts));
                    }
                    
                    rentals.put(phone, rentalEntries);
                } catch (NumberFormatException e) {
                    // Skip invalid lines
                    continue;
                }
            }
        }
        return rentals;
    }
    
    /**
     * Writes customer rental records
     */
    public void writeCustomerRentals(String filePath, Map<Long, List<String>> rentals) throws IOException {
        File tempFile = new File(filePath + ".tmp");
        
        try (PrintWriter writer = new PrintWriter(
                new BufferedWriter(new FileWriter(tempFile)))) {
            
            // Write header
            writer.println("Phone number rentedItem1ID,rentedItem1Date,returned1Bool rentedItem2ID,rentedItem2Date,returned2Bool...etc");
            
            // Write customer records
            for (Map.Entry<Long, List<String>> entry : rentals.entrySet()) {
                writer.print(entry.getKey());
                for (String rental : entry.getValue()) {
                    writer.print(" " + rental);
                }
                writer.println();
            }
        }
        
        // Atomic file replacement
        File originalFile = new File(filePath);
        if (originalFile.exists()) {
            originalFile.delete();
        }
        tempFile.renameTo(originalFile);
    }
    
    /**
     * Reads coupon codes from file
     */
    public List<String> readCoupons(String filePath) throws IOException {
        List<String> coupons = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                coupons.add(line.trim());
            }
        }
        return coupons;
    }
}

