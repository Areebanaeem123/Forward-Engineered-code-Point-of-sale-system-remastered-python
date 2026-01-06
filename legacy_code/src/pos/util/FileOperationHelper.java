package pos.util;

import java.io.*;
import java.util.List;

/**
 * Helper class for common file operations.
 * Reduces code duplication across the codebase.
 */
public class FileOperationHelper {
    
    /**
     * Atomic file write operation using temp file pattern
     */
    public static void atomicWrite(String filePath, List<String> lines) throws IOException {
        File tempFile = new File(filePath + ".tmp");
        
        try (PrintWriter writer = new PrintWriter(
                new BufferedWriter(new FileWriter(tempFile)))) {
            
            for (String line : lines) {
                writer.println(line);
            }
        }
        
        // Atomic replacement
        File originalFile = new File(filePath);
        if (originalFile.exists()) {
            originalFile.delete();
        }
        tempFile.renameTo(originalFile);
    }
    
    /**
     * Reads all lines from a file
     */
    public static List<String> readAllLines(String filePath) throws IOException {
        List<String> lines = new java.util.ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                lines.add(line);
            }
        }
        return lines;
    }
    
    /**
     * Appends a line to a file
     */
    public static void appendLine(String filePath, String line) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(
                new FileWriter(filePath, true))) {
            writer.write(line);
            writer.newLine();
        }
    }
}

