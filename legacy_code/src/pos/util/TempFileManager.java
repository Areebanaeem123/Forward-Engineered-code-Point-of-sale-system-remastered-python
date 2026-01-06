package pos.util;

import pos.config.SystemConfig;
import java.io.*;
import java.util.List;
import pos.model.Item;

/**
 * Utility class to manage temporary transaction files.
 * Eliminates code duplication across POS, POR, POH classes.
 */
public class TempFileManager {
    
    /**
     * Deletes an item from temp file (for Sale transactions)
     */
    public static void deleteTempItem(String transactionType, List<Item> transactionItems, 
                                      int itemIdToDelete, String phoneNumber) throws IOException {
        File tempFile = new File(SystemConfig.TEMP_FILE);
        File tempFileNew = new File(SystemConfig.TEMP_FILE + ".tmp");
        
        if (!tempFile.exists()) {
            return;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(tempFile));
             BufferedWriter writer = new BufferedWriter(new FileWriter(tempFileNew))) {
            
            // Read and write transaction type
            String type = reader.readLine();
            writer.write(type);
            writer.newLine();
            
            // For Rental/Return, read and write phone number
            if (transactionType.equals("Rental") || transactionType.equals("Return")) {
                String phone = reader.readLine();
                writer.write(phone);
                writer.newLine();
            }
            
            // Write remaining items
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                
                String[] parts = line.split(" ");
                if (parts.length >= 2) {
                    try {
                        int itemId = Integer.parseInt(parts[0]);
                        if (itemId != itemIdToDelete) {
                            writer.write(line);
                            writer.newLine();
                        }
                    } catch (NumberFormatException e) {
                        // Skip invalid lines
                        continue;
                    }
                }
            }
        }
        
        // Atomic file replacement
        if (tempFile.exists()) {
            tempFile.delete();
        }
        tempFileNew.renameTo(tempFile);
    }
    
    /**
     * Creates temp file with transaction data
     */
    public static void createTempFile(String transactionType, List<Item> items, String phoneNumber) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(SystemConfig.TEMP_FILE))) {
            writer.write(transactionType);
            writer.newLine();
            
            if (phoneNumber != null && !phoneNumber.isEmpty()) {
                writer.write(phoneNumber);
                writer.newLine();
            }
            
            for (Item item : items) {
                writer.write(item.getItemID() + " " + item.getAmount());
                writer.newLine();
            }
        }
    }
    
    /**
     * Reads temp file and returns transaction type
     */
    public static String readTransactionType() throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(SystemConfig.TEMP_FILE))) {
            return reader.readLine();
        }
    }
}

