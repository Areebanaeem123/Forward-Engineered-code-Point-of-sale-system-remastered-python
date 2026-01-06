package pos.database;

import pos.model.Item;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Repository for item data access.
 */
public class ItemRepository {
    private DatabaseConnection dbConnection;
    
    public ItemRepository() {
        this.dbConnection = DatabaseConnection.getInstance();
    }
    
    public List<Item> findAll(String itemType) throws SQLException {
        List<Item> items = new ArrayList<>();
        String sql = "SELECT item_id, item_name, price, stock_quantity " +
                     "FROM items WHERE item_type = ?";
        
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, itemType);
            ResultSet rs = stmt.executeQuery();
            
            while (rs.next()) {
                items.add(new Item(
                    rs.getInt("item_id"),
                    rs.getString("item_name"),
                    rs.getFloat("price"),
                    rs.getInt("stock_quantity")
                ));
            }
        }
        return items;
    }
    
    public Item findById(int itemId) throws SQLException {
        String sql = "SELECT item_id, item_name, price, stock_quantity " +
                     "FROM items WHERE item_id = ?";
        
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, itemId);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return new Item(
                    rs.getInt("item_id"),
                    rs.getString("item_name"),
                    rs.getFloat("price"),
                    rs.getInt("stock_quantity")
                );
            }
        }
        return null;
    }
    
    public void updateStock(int itemId, int quantityChange) throws SQLException {
        String sql = "UPDATE items SET stock_quantity = stock_quantity + ?, " +
                     "updated_at = CURRENT_TIMESTAMP WHERE item_id = ?";
        
        try (Connection conn = dbConnection.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, quantityChange);
            stmt.setInt(2, itemId);
            stmt.executeUpdate();
        }
    }
    
    public void updateStockBatch(List<Item> items) throws SQLException {
        String sql = "UPDATE items SET stock_quantity = ?, " +
                     "updated_at = CURRENT_TIMESTAMP WHERE item_id = ?";
        
        try (Connection conn = dbConnection.getConnection()) {
            conn.setAutoCommit(false);
            
            try (PreparedStatement stmt = conn.prepareStatement(sql)) {
                for (Item item : items) {
                    stmt.setInt(1, item.getAmount());
                    stmt.setInt(2, item.getItemID());
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
}

