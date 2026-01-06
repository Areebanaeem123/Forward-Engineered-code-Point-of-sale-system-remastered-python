# Migration Guide: Text Files to Database

## Overview

This guide explains how to migrate from text file storage to SQLite database.

## Prerequisites

1. **SQLite JDBC Driver**
   - Download `sqlite-jdbc-3.x.x.jar` from https://github.com/xerial/sqlite-jdbc
   - Add to project classpath

2. **Backup Existing Data**
   ```bash
   cp -r Database/ Database_backup/
   ```

## Migration Steps

### Step 1: Add SQLite JDBC Driver

Add the JAR file to your project:
- **NetBeans:** Right-click project → Properties → Libraries → Add JAR/Folder
- **Command Line:** Add to classpath: `-cp sqlite-jdbc.jar:your-classes`

### Step 2: Run Migration Script

The `DatabaseConnection` class will automatically create tables on first run.

### Step 3: Migrate Data

Use the migration tool to copy data from text files to database:

```java
MigrationTool.migrateAll();
```

### Step 4: Update Code References

Replace old file-based classes with database repositories:
- `Inventory` → Use `ItemRepository`
- `Management` → Use `RentalRepository`, `CustomerRepository`
- `EmployeeManagement` → Use `EmployeeRepository`

### Step 5: Test Migration

1. Verify all data migrated correctly
2. Test all functionality
3. Compare results with backup

## Rollback Plan

If migration fails:
1. Restore from `Database_backup/`
2. Revert code changes
3. System will work with text files again

## Database Schema

See `REFACTORING_DOCUMENTATION.md` Section 4.2 for complete schema.

## Notes

- Database file: `Database/pos_system.db`
- Text files remain for backup/reference
- Can run both systems in parallel during transition

