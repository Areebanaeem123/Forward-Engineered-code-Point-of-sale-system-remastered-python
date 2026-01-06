package pos.database;

import java.sql.*;

/**
 * Database connection manager using SQLite.
 */
public class DatabaseConnection {
    private static final String DB_URL = "jdbc:sqlite:Database/pos_system.db";
    private static DatabaseConnection instance;
    private Connection connection;
    
    private DatabaseConnection() {
        initializeDatabase();
    }
    
    public static synchronized DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }
    
    public Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            connection = DriverManager.getConnection(DB_URL);
        }
        return connection;
    }
    
    private void initializeDatabase() {
        try {
            Class.forName("org.sqlite.JDBC");
            try (Connection conn = DriverManager.getConnection(DB_URL)) {
                createTables(conn);
            }
        } catch (ClassNotFoundException e) {
            System.err.println("SQLite JDBC driver not found. Please add sqlite-jdbc.jar to classpath.");
        } catch (SQLException e) {
            System.err.println("Error initializing database: " + e.getMessage());
        }
    }
    
    private void createTables(Connection conn) throws SQLException {
        String[] createTableStatements = {
            // Employees table
            "CREATE TABLE IF NOT EXISTS employees (" +
            "employee_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "username TEXT UNIQUE NOT NULL, " +
            "password_hash TEXT NOT NULL, " +
            "first_name TEXT NOT NULL, " +
            "last_name TEXT NOT NULL, " +
            "position TEXT NOT NULL CHECK(position IN ('Admin', 'Cashier')), " +
            "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
            
            // Items table
            "CREATE TABLE IF NOT EXISTS items (" +
            "item_id INTEGER PRIMARY KEY, " +
            "item_name TEXT NOT NULL, " +
            "price REAL NOT NULL CHECK(price >= 0), " +
            "stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0), " +
            "item_type TEXT NOT NULL CHECK(item_type IN ('Sale', 'Rental')), " +
            "created_at DATETIME DEFAULT CURRENT_TIMESTAMP, " +
            "updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
            
            // Customers table
            "CREATE TABLE IF NOT EXISTS customers (" +
            "customer_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "phone_number TEXT UNIQUE NOT NULL, " +
            "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)",
            
            // Rentals table
            "CREATE TABLE IF NOT EXISTS rentals (" +
            "rental_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "customer_id INTEGER NOT NULL, " +
            "item_id INTEGER NOT NULL, " +
            "quantity INTEGER NOT NULL CHECK(quantity > 0), " +
            "rental_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
            "return_due_date DATETIME NOT NULL, " +
            "return_date DATETIME, " +
            "is_returned INTEGER NOT NULL DEFAULT 0 CHECK(is_returned IN (0, 1)), " +
            "late_fee REAL DEFAULT 0, " +
            "FOREIGN KEY(customer_id) REFERENCES customers(customer_id), " +
            "FOREIGN KEY(item_id) REFERENCES items(item_id))",
            
            // Transactions table
            "CREATE TABLE IF NOT EXISTS transactions (" +
            "transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Sale', 'Rental', 'Return')), " +
            "employee_id INTEGER, " +
            "customer_id INTEGER, " +
            "total_amount REAL NOT NULL, " +
            "tax_amount REAL DEFAULT 0, " +
            "discount_amount REAL DEFAULT 0, " +
            "transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
            "FOREIGN KEY(employee_id) REFERENCES employees(employee_id), " +
            "FOREIGN KEY(customer_id) REFERENCES customers(customer_id))",
            
            // Transaction items table
            "CREATE TABLE IF NOT EXISTS transaction_items (" +
            "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "transaction_id INTEGER NOT NULL, " +
            "item_id INTEGER NOT NULL, " +
            "quantity INTEGER NOT NULL CHECK(quantity > 0), " +
            "unit_price REAL NOT NULL, " +
            "subtotal REAL NOT NULL, " +
            "FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id), " +
            "FOREIGN KEY(item_id) REFERENCES items(item_id))",
            
            // Coupons table
            "CREATE TABLE IF NOT EXISTS coupons (" +
            "coupon_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "coupon_code TEXT UNIQUE NOT NULL, " +
            "discount_percent REAL NOT NULL CHECK(discount_percent >= 0 AND discount_percent <= 100), " +
            "is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)), " +
            "expires_at DATETIME)",
            
            // Audit logs table
            "CREATE TABLE IF NOT EXISTS audit_logs (" +
            "log_id INTEGER PRIMARY KEY AUTOINCREMENT, " +
            "employee_id INTEGER, " +
            "action_type TEXT NOT NULL, " +
            "description TEXT, " +
            "timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " +
            "FOREIGN KEY(employee_id) REFERENCES employees(employee_id))"
        };
        
        for (String sql : createTableStatements) {
            try (Statement stmt = conn.createStatement()) {
                stmt.execute(sql);
            }
        }
    }
    
    public void close() throws SQLException {
        if (connection != null && !connection.isClosed()) {
            connection.close();
        }
    }
}

