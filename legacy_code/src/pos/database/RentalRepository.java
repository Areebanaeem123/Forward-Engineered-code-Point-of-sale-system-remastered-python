package pos.database;

import pos.model.ReturnItem;
import java.sql.*;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class RentalRepository {
    private DatabaseConnection dbConnection;
    
    public RentalRepository() {
        this.dbConnection = DatabaseConnection.getInstance();
    }
    
    public List<ReturnItem> getOutstandingRentals(long phoneNumber) throws SQLException {
        List<ReturnItem> returnItems = new ArrayList<>();
        
        String sql = "SELECT r.item_id, r.return_due_date, r.quantity " +
                     "FROM rentals r " +
                     "JOIN customers c ON r.customer_id = c.customer_id " +
                     "WHERE c.phone_number = ? AND r.is_returned = 0";
        
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, String.valueOf(phoneNumber));
            ResultSet rs = stmt.executeQuery();
            
            Calendar today = Calendar.getInstance();
            
            while (rs.next()) {
                Date dueDate = rs.getDate("return_due_date");
                Calendar dueCal = Calendar.getInstance();
                dueCal.setTime(dueDate);
                
                int daysLate = calculateDaysBetween(dueCal, today);
                if (daysLate > 0) {
                    returnItems.add(new ReturnItem(
                        rs.getInt("item_id"),
                        daysLate
                    ));
                }
            }
        }
        return returnItems;
    }
    
    public void markAsReturned(long phoneNumber, List<Integer> itemIds) throws SQLException {
        String sql = "UPDATE rentals SET is_returned = 1, return_date = CURRENT_TIMESTAMP " +
                     "WHERE customer_id = (SELECT customer_id FROM customers WHERE phone_number = ?) " +
                     "AND item_id = ? AND is_returned = 0";
        
        try (Connection conn = dbConnection.getConnection()) {
            conn.setAutoCommit(false);
            
            try (PreparedStatement stmt = conn.prepareStatement(sql)) {
                for (Integer itemId : itemIds) {
                    stmt.setString(1, String.valueOf(phoneNumber));
                    stmt.setInt(2, itemId);
                    stmt.addBatch();
                }
                stmt.executeBatch();
                conn.commit();
            } catch (SQLException e) {
                conn.rollback();
                throw e;
            } finally {
                conn.setAutoCommit(true);
            }
        }
    }
    
    private int calculateDaysBetween(Calendar start, Calendar end) {
        long diff = end.getTimeInMillis() - start.getTimeInMillis();
        return (int) (diff / (24 * 60 * 60 * 1000));
    }
}

