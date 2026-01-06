<div style="page-break-after: always;"></div>

# 📋 Point-of-Sale System
## Technical Documentation

<div align="center">

**Rebuilt Technical Documentation**  
*Reverse Engineered System Analysis*

---

| **Document Version** | **1.0** |
|---------------------|---------|
| **Date** | **2024** |
| **System Name** | **SG Technologies Point-of-Sale System** |
| **Technology Stack** | **Java Swing, File-based Persistence** |
| **Document Type** | **Technical Architecture Documentation** |

---

</div>

---

## 📑 Table of Contents

| # | Section | Page |
|---|---------|------|
| **1** | [System Architecture Overview](#1-system-architecture-overview) | |
| **2** | [Component Architecture](#2-component-architecture) | |
| **3** | [Class Structure and Hierarchy](#3-class-structure-and-hierarchy) | |
| **4** | [Data Flow Architecture](#4-data-flow-architecture) | |
| **5** | [Data Storage Architecture](#5-data-storage-architecture) | |
| **6** | [User Interface Architecture](#6-user-interface-architecture) | |
| **7** | [Business Logic Architecture](#7-business-logic-architecture) | |
| **8** | [File Format Specifications](#8-file-format-specifications) | |
| **9** | [Workflow Specifications](#9-workflow-specifications) | |
| **10** | [Dependency Graph](#10-dependency-graph) | |
| **11** | [System Configuration](#11-system-configuration) | |
| **A** | [Appendix A: Code Metrics](#appendix-a-code-metrics-summary) | |
| **B** | [Appendix B: Known Limitations](#appendix-b-known-limitations) | |

---

<div style="page-break-after: always;"></div>

## 1. System Architecture Overview

### 1.1 High-Level Architecture

The Point-of-Sale system is a **monolithic desktop application** built using Java Swing framework. The system follows a **layered architecture** with tight coupling between layers.

#### Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║          PRESENTATION LAYER (Swing UI)                        ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │  Login, Cashier, Admin, Transaction, Payment, etc.      │  ║
║  └─────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════╗
║         BUSINESS LOGIC LAYER (Domain)                          ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │  POSSystem, PointOfSale, Inventory, Management          │  ║
║  └─────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════╗
║            DATA ACCESS LAYER (File I/O)                      ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │  Direct file read/write operations                      │  ║
║  └─────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════╝
                              │
                              ▼
╔═══════════════════════════════════════════════════════════════╗
║         PERSISTENCE LAYER (Text Files)                        ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │  Database/*.txt files                                    │  ║
║  └─────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════╝
```

#### Architecture Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Type** | Monolithic Desktop Application |
| **UI Framework** | Java Swing (AWT-based) |
| **Persistence** | File-based (Plain Text) |
| **Architecture Pattern** | Layered Architecture |
| **Coupling** | Tight coupling between layers |
| **Deployment** | Single JAR file |

---

### 1.2 Architectural Patterns

The system implements several design patterns:

#### Pattern Summary Table

| Pattern | Implementation | Purpose |
|---------|----------------|---------|
| **Singleton Pattern** | `Inventory` class | Ensures single inventory instance across application |
| **Template Method Pattern** | `PointOfSale` abstract class | Defines transaction workflow template |
| **Strategy Pattern** | `POS`, `POR`, `POH` classes | Different transaction processing strategies |
| **MVC-like Pattern** | UI → Domain → Data | Separation of concerns (loosely implemented) |

#### Detailed Pattern Descriptions

**🔹 Singleton Pattern**
- **Class:** `Inventory`
- **Implementation:** Synchronized `getInstance()` method
- **Purpose:** Centralized inventory management
- **Thread Safety:** Basic synchronization (not fully thread-safe)

**🔹 Template Method Pattern**
- **Abstract Class:** `PointOfSale`
- **Template Methods:** `endPOS()`, `deleteTempItem()`, `retrieveTemp()`
- **Concrete Implementations:** `POS`, `POR`, `POH`
- **Purpose:** Common transaction workflow with transaction-specific behavior

**🔹 Strategy Pattern**
- **Context:** Transaction processing
- **Strategies:** Sale (`POS`), Rental (`POR`), Return (`POH`)
- **Purpose:** Interchangeable transaction processing algorithms

---

### 1.3 System Entry Point

**Main Entry Method:**
```java
Register.main(String[] args)
```

**Entry Point Flow:**
```
Application Start
    │
    ├─► Creates Login_Interface instance
    │
    ├─► Displays login window
    │
    └─► Waits for user authentication
```

**Key Points:**
- ✅ No command-line arguments required
- ✅ Application terminates when all windows are closed
- ✅ Single entry point for entire application

---

<div style="page-break-after: always;"></div>

## 2. Component Architecture

### 2.1 Component Categories

The system is organized into **four major component categories**:

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPONENT CATEGORIES                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. User Interface Components (9 classes)                   │
│  2. Domain/Business Logic Components (8 classes)            │
│  3. Data Model Components (3 classes)                       │
│  4. Configuration Components (3 files)                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.1.1 User Interface Components

| Component | Purpose | Key Responsibilities | Lines of Code |
|-----------|---------|---------------------|---------------|
| `Register` | Application entry point | Launches login interface | ~15 |
| `Login_Interface` | Authentication screen | Validates credentials, routes to role-based interfaces | ~122 |
| `Cashier_Interface` | Cashier main menu | Provides access to Sale, Rental, Return operations | ~157 |
| `Admin_Interface` | Administrator dashboard | Employee management, system administration | ~179 |
| `Transaction_Interface` | Transaction workspace | Orchestrates item entry, cart management, transaction completion | ~241 |
| `EnterItem_Interface` | Item entry dialog | Add/remove items from transaction cart | ~143 |
| `Payment_Interface` | Payment processing | Handles cash/electronic payment, receipt generation | ~244 |
| `AddEmployee_Interface` | Employee registration | Creates new employee accounts | ~96 |
| `UpdateEmployee_Interface` | Employee modification | Updates existing employee information | ~130 |

**Total UI Components:** 9 classes  
**Total UI Code:** ~1,327 lines

---

### 2.1.2 Domain/Business Logic Components

| Component | Purpose | Key Responsibilities | Pattern |
|-----------|---------|---------------------|---------|
| `POSSystem` | System controller | Authentication, session management, temp file recovery | Controller |
| `PointOfSale` (Abstract) | Transaction base class | Cart management, total calculation, coupon validation | Template Method |
| `POS` | Sale transaction | Sale-specific processing, invoice generation | Strategy |
| `POR` | Rental transaction | Rental recording, customer management | Strategy |
| `POH` | Return transaction | Return processing, late fee calculation | Strategy |
| `Inventory` | Inventory manager | Item database access, stock updates | Singleton |
| `Management` | Customer/Rental manager | Customer database, rental tracking, return date calculation | Service |
| `EmployeeManagement` | Employee manager | Employee CRUD operations | Service |

**Total Domain Components:** 8 classes  
**Total Domain Code:** ~1,200 lines

---

### 2.1.3 Data Model Components

| Component | Purpose | Attributes | Methods |
|-----------|---------|------------|---------|
| `Item` | Product representation | `itemID` (int)<br>`itemName` (String)<br>`price` (float)<br>`amount` (int) | Getters, `updateAmount()` |
| `Employee` | Employee representation | `username` (String)<br>`name` (String)<br>`position` (String)<br>`password` (String) | Getters, Setters |
| `ReturnItem` | Return tracking | `itemID` (int)<br>`daysSinceReturn` (int) | Getters |

**Total Data Models:** 3 classes  
**Total Model Code:** ~70 lines

---

### 2.1.4 Configuration Components

| Component | Purpose | Location | Format |
|-----------|---------|----------|--------|
| `build.xml` | Ant build script | Root directory | XML |
| `manifest.mf` | JAR manifest | Root directory | Manifest |
| `nbproject/` | NetBeans project config | Root directory | XML/Properties |

---

<div style="page-break-after: always;"></div>

## 3. Class Structure and Hierarchy

### 3.1 Inheritance Hierarchy

#### Class Hierarchy Diagram

```
                    ┌─────────────────────┐
                    │   PointOfSale       │
                    │   (abstract)        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
        │     POS      │ │   POR    │ │    POH      │
        │   (Sale)     │ │ (Rental) │ │  (Return)   │
        └──────────────┘ └──────────┘ └─────────────┘

                    ┌─────────────────────┐
                    │      JFrame         │
                    │    (Swing)         │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐   ┌─────────▼──────────┐  ┌────────▼────────┐
│ Login_        │   │ Cashier_           │  │ Admin_          │
│ Interface     │   │ Interface          │  │ Interface       │
└───────────────┘   └────────────────────┘  └─────────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐   ┌─────────▼──────────┐  ┌────────▼────────┐
│ Transaction_   │   │ EnterItem_        │  │ Payment_        │
│ Interface      │   │ Interface          │  │ Interface       │
└────────────────┘   └───────────────────┘  └─────────────────┘
        │
        └──────────────┐
                       │
        ┌──────────────▼──────────────┐
        │ AddEmployee_Interface      │
        │ UpdateEmployee_Interface   │
        └────────────────────────────┘
```

---

### 3.2 Detailed Class Specifications

#### 3.2.1 PointOfSale (Abstract Base Class)

<div style="background-color: #f0f0f0; padding: 15px; border-left: 4px solid #4CAF50; margin: 10px 0;">

**📁 Location:** `src/PointOfSale.java`  
**🎯 Purpose:** Provides common functionality for all transaction types (Sale, Rental, Return)  
**📊 Type:** Abstract Class  
**🔗 Inherits From:** None (Base Class)

</div>

**Key Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `totalPrice` | `double` | `0.0` | Running total of transaction |
| `tax` | `double` | `1.06` | Tax multiplier (6% tax) |
| `discount` | `static float` | `0.90f` | Coupon discount (10% off) |
| `databaseItem` | `List<Item>` | `new ArrayList<>()` | All items loaded from inventory |
| `transactionItem` | `List<Item>` | `new ArrayList<>()` | Items in current transaction cart |
| `inventory` | `Inventory` | `getInstance()` | Singleton inventory instance |
| `couponNumber` | `static String` | `"Database/couponNumber.txt"` | Path to coupon database |
| `tempFile` | `static String` | `"Database/temp.txt"` | Path to temporary transaction file |

**Key Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `startNew(String databaseFile)` | `boolean` | Loads inventory from specified database file |
| `enterItem(int itemID, int amount)` | `boolean` | Adds item to transaction cart |
| `updateTotal()` | `double` | Recalculates total price after item addition |
| `removeItems(int itemID)` | `boolean` | Removes item from cart and updates total |
| `coupon(String couponNo)` | `boolean` | Validates and applies coupon discount |
| `creditCard(String card)` | `boolean` | Validates credit card format (16 digits) |
| `createTemp(int id, int amount)` | `void` | Writes transaction state to temp file |
| `getTotal()` | `double` | Returns current total price |
| `getCart()` | `List<Item>` | Returns list of items in cart |
| `getCartSize()` | `int` | Returns number of items in cart |
| `endPOS(String textFile)` | `double` | ⚠️ **Abstract** - Finalizes transaction |
| `deleteTempItem(int id)` | `void` | ⚠️ **Abstract** - Removes item from temp file |
| `retrieveTemp(String textFile)` | `void` | ⚠️ **Abstract** - Restores transaction from temp file |

**Design Notes:**

> ⚠️ **Warning:** Public mutable fields violate encapsulation principles  
> ⚠️ **Warning:** Hardcoded tax rate and discount values  
> ✅ **Good:** Uses Template Method pattern effectively

---

#### 3.2.2 POS (Sale Transaction)

<div style="background-color: #e3f2fd; padding: 15px; border-left: 4px solid #2196F3; margin: 10px 0;">

**📁 Location:** `src/POS.java`  
**🎯 Purpose:** Handles standard sale transactions  
**📊 Type:** Concrete Class  
**🔗 Inherits From:** `PointOfSale`

</div>

**Transaction Flow:**

```
1. Load inventory from itemDatabase.txt
   │
2. Add items to cart
   │
3. Apply optional coupon
   │
4. Calculate total with tax
   │
5. Process payment
   │
6. Update inventory (decrement stock)
   │
7. Generate invoice record
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `endPOS(String textFile)` | • Applies tax to total<br>• Updates inventory (decrements stock)<br>• Deletes temp file<br>• Writes invoice to `saleInvoiceRecord.txt`<br>• Returns final total with tax |
| `deleteTempItem(int id)` | Removes item from temp file, preserves transaction type marker |
| `retrieveTemp(String textFile)` | Restores sale transaction from temp file |

---

#### 3.2.3 POR (Rental Transaction)

<div style="background-color: #fff3e0; padding: 15px; border-left: 4px solid #FF9800; margin: 10px 0;">

**📁 Location:** `src/POR.java`  
**🎯 Purpose:** Handles rental transactions with customer tracking  
**📊 Type:** Concrete Class  
**🔗 Inherits From:** `PointOfSale`

</div>

**Key Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `phoneNum` | `long` | Customer phone number identifier |

**Transaction Flow:**

```
1. Get customer phone number
   │
2. Validate/create customer in userDatabase.txt
   │
3. Load inventory from rentalDatabase.txt
   │
4. Add items to cart
   │
5. Calculate total with tax
   │
6. Process payment
   │
7. Record rental with return date (14 days from rental)
   │
8. Update inventory (decrement stock)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `endPOS(String textFile)` | • Applies tax to total<br>• Records rental via `Management.addRental()`<br>• Updates rental inventory<br>• Deletes temp file<br>• Returns final total |
| `deleteTempItem(int id)` | Removes item from temp file, preserves phone number |
| `retrieveTemp(String textFile)` | Restores rental transaction with phone number |

---

#### 3.2.4 POH (Return Transaction)

<div style="background-color: #fce4ec; padding: 15px; border-left: 4px solid #E91E63; margin: 10px 0;">

**📁 Location:** `src/POH.java`  
**🎯 Purpose:** Handles return transactions with late fee calculation  
**📊 Type:** Concrete Class  
**🔗 Inherits From:** `PointOfSale`

</div>

**Key Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `returnList` | `List<ReturnItem>` | List of items being returned with late fee data |
| `phone` | `long` | Customer phone number |
| `returnSale` | `boolean` | Flag indicating return type (rented vs unsatisfactory) |

**Late Fee Calculation Formula:**

```
Late Fee = Item Price × Amount × 0.1 × Days Late
```

**Transaction Flow:**

```
1. Determine return type (rented items vs unsatisfactory items)
   │
2. If rented: Get customer phone number
   │
3. Load rental history from userDatabase.txt
   │
4. Calculate days late for each item
   │
5. Calculate late fees
   │
6. Update inventory (add returned items back)
   │
7. Mark items as returned in customer record
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `endPOS(String textFile)` | • Calculates late fees (10% per day)<br>• Updates inventory (increments stock)<br>• Updates rental status<br>• Writes return log<br>• Returns total late fees |
| `deleteTempItem(int id)` | Removes item from temp file |
| `retrieveTemp(String textFile)` | Restores return transaction |

---

#### 3.2.5 Inventory (Singleton)

<div style="background-color: #f1f8e9; padding: 15px; border-left: 4px solid #8BC34A; margin: 10px 0;">

**📁 Location:** `src/Inventory.java`  
**🎯 Purpose:** Manages inventory database access and updates  
**📊 Type:** Singleton Class  
**🔗 Pattern:** Singleton (thread-safe via synchronized method)

</div>

**Key Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getInstance()` | `Inventory` | Returns singleton instance (synchronized) |
| `accessInventory(String databaseFile, List<Item> databaseItem)` | `boolean` | Reads inventory file, parses items, creates Item objects |
| `updateInventory(String databaseFile, List<Item> transactionItem, List<Item> databaseItem, boolean takeFromInventory)` | `void` | Updates item quantities, rewrites entire database file |

**File Operations:**

> ⚠️ **Warning:** Uses `FileWriter` with `false` flag to overwrite entire file  
> ⚠️ **Warning:** No transaction support - file rewrite is atomic but not transactional  
> ⚠️ **Warning:** No locking mechanism for concurrent access

---

#### 3.2.6 Management

<div style="background-color: #e8eaf6; padding: 15px; border-left: 4px solid #3F51B5; margin: 10px 0;">

**📁 Location:** `src/Management.java`  
**🎯 Purpose:** Manages customer database and rental tracking  
**📊 Type:** Service Class

</div>

**Key Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `userDatabase` | `static String` | Path to customer database file |

**Key Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `checkUser(Long phone)` | `Boolean` | Checks if customer exists in database |
| `createUser(Long phone)` | `boolean` | Creates new customer record |
| `addRental(long phone, List<Item> rentalList)` | `void` | Adds rental record to customer entry |
| `getLatestReturnDate(Long phone)` | `List<ReturnItem>` | Retrieves outstanding rentals, calculates days late |
| `updateRentalStatus(long phone, List<ReturnItem> returnedList)` | `void` | Marks items as returned, updates return date |

**File Format Handling:**

> 📝 **Note:** First line is header/format description  
> 📝 **Note:** Complex parsing logic handles multiple rentals per customer  
> 📝 **Format:** `phoneNumber item1,date1,returned1 item2,date2,returned2 ...`

---

#### 3.2.7 EmployeeManagement

<div style="background-color: #fff9c4; padding: 15px; border-left: 4px solid #FBC02D; margin: 10px 0;">

**📁 Location:** `src/EmployeeManagement.java`  
**🎯 Purpose:** Manages employee database operations  
**📊 Type:** Service Class

</div>

**Key Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `employeeDatabase` | `static String` | Path to employee database file |
| `employees` | `List<Employee>` | In-memory employee list |

**Key Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getEmployeeList()` | `List<Employee>` | Reads and returns all employees from database |
| `add(String name, String password, boolean employee)` | `void` | Generates new username, determines position, appends to file |
| `delete(String username)` | `boolean` | Removes employee, rewrites entire database file |
| `update(String username, String password, String position, String name)` | `int` | Updates employee fields, validates position, rewrites file |

**File Update Pattern:**

```
1. Read entire file into memory
   │
2. Modify data structure
   │
3. Write to temporary file
   │
4. Delete original file
   │
5. Rename temp file to original name
```

> ⚠️ **Warning:** Data loss risk if process crashes between delete and rename

---

#### 3.2.8 POSSystem

<div style="background-color: #f3e5f5; padding: 15px; border-left: 4px solid #9C27B0; margin: 10px 0;">

**📁 Location:** `src/POSSystem.java`  
**🎯 Purpose:** System-level operations - authentication, session management, temp recovery  
**📊 Type:** Controller Class

</div>

**Key Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `employeeDatabase` | `static String` | Path to employee database |
| `employees` | `List<Employee>` | Loaded employee list |
| `username`, `password`, `name` | `String` | Current session data |
| `index` | `int` | Index of logged-in employee |
| `dateFormat` | `DateFormat` | Timestamp formatter |

**Key Methods:**

| Method | Return Type | Description |
|--------|-------------|-------------|
| `logIn(String userAuth, String passAuth)` | `int` | Validates credentials, logs login, returns role code (0/1/2) |
| `logOut(String pos)` | `void` | Logs logout event to log file |
| `checkTemp()` | `boolean` | Checks if unfinished transaction exists |
| `continueFromTemp(long phone)` | `String` | Restores transaction from temp file |

**Session Management:**

> ⚠️ **Warning:** No session timeout mechanism  
> ⚠️ **Warning:** Session data stored in instance variables  
> ⚠️ **Warning:** Multiple `POSSystem` instances can exist simultaneously

---

<div style="page-break-after: always;"></div>

## 4. Data Flow Architecture

### 4.1 Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                      │
└─────────────────────────────────────────────────────────────┘

    User Input (Login_Interface)
            │
            ▼
    POSSystem.logIn(username, password)
            │
            ▼
    Read employeeDatabase.txt
            │
            ▼
    Validate credentials
            │
            ├─► Invalid ──► Return 0 (Failure)
            │
            ▼ Valid
    Write to employeeLogfile.txt
            │
            ▼
    Return role code
            │
            ├─► 1 ──► Cashier_Interface
            │
            └─► 2 ──► Admin_Interface
```

---

### 4.2 Sale Transaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    SALE TRANSACTION FLOW                    │
└─────────────────────────────────────────────────────────────┘

    Cashier_Interface → Sale Button
            │
            ▼
    Transaction_Interface("Sale")
            │
            ▼
    Create POS instance
            │
            ▼
    Load itemDatabase.txt via Inventory
            │
            ▼
    EnterItem_Interface → Add items
            │
            ▼
    PointOfSale.enterItem() → Add to cart
            │
            ▼
    PointOfSale.updateTotal() → Calculate running total
            │
            ▼
    Write to temp.txt (createTemp)
            │
            ▼
    Payment_Interface → Process payment
            │
            ▼
    POS.endPOS()
            ├── Apply tax
            ├── Update inventory (decrement stock)
            ├── Write invoice to saleInvoiceRecord.txt
            └── Delete temp.txt
            │
            ▼
    Return to Cashier_Interface
```

---

### 4.3 Rental Transaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   RENTAL TRANSACTION FLOW                    │
└─────────────────────────────────────────────────────────────┘

    Cashier_Interface → Rental Button
            │
            ▼
    Transaction_Interface("Rental")
            │
            ▼
    Get customer phone number
            │
            ▼
    Management.checkUser(phone)
            │
            ├─► Not exists ──► Management.createUser(phone)
            │
            └─► Exists ──► Continue
            │
            ▼
    Create POR instance
            │
            ▼
    Load rentalDatabase.txt via Inventory
            │
            ▼
    EnterItem_Interface → Add items
            │
            ▼
    Write to temp.txt (with phone number)
            │
            ▼
    Payment_Interface → Process payment
            │
            ▼
    POR.endPOS()
            ├── Apply tax
            ├── Management.addRental(phone, items)
            ├── Update inventory (decrement stock)
            └── Delete temp.txt
            │
            ▼
    Return to Cashier_Interface
```

---

### 4.4 Return Transaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    RETURN TRANSACTION FLOW                   │
└─────────────────────────────────────────────────────────────┘

    Cashier_Interface → Return Button
            │
            ▼
    Transaction_Interface("Return")
            │
            ▼
    Select return type
            │
            ├─► Rented Items
            │       │
            │       ├─► Get customer phone number
            │       ├─► Create POH instance with phone
            │       ├─► Load rentalDatabase.txt
            │       └─► Management.getLatestReturnDate(phone)
            │               └─► Calculate days late
            │
            └─► Unsatisfactory Items
                    │
                    ├─► Create POH instance (no phone)
                    └─► Load itemDatabase.txt
            │
            ▼
    EnterItem_Interface → Add items to return
            │
            ▼
    POH.endPOS()
            ├── Calculate late fees (if rented)
            ├── Update inventory (increment stock)
            ├── Management.updateRentalStatus() (if rented)
            └── Write to returnSale.txt
            │
            ▼
    Return to Cashier_Interface
```

---

### 4.5 Employee Management Flow

```
┌─────────────────────────────────────────────────────────────┐
│                 EMPLOYEE MANAGEMENT FLOW                     │
└─────────────────────────────────────────────────────────────┘

    Admin_Interface → Employee Action
            │
            ├─► Add Employee
            │       │
            │       ├─► AddEmployee_Interface opens
            │       ├─► Enter name and password
            │       ├─► EmployeeManagement.add()
            │       │       ├── Read employeeDatabase.txt
            │       │       ├── Generate new username
            │       │       ├── Determine position
            │       │       └── Append to file
            │       └─► Admin_Interface refreshed
            │
            ├─► Delete Employee
            │       │
            │       ├─► Enter username
            │       ├─► EmployeeManagement.delete()
            │       │       ├── Read employeeDatabase.txt
            │       │       ├── Remove from list
            │       │       ├── Write to temp file
            │       │       ├── Delete original
            │       │       └── Rename temp
            │       └─► Admin_Interface refreshed
            │
            └─► Update Employee
                    │
                    ├─► UpdateEmployee_Interface opens
                    ├─► Enter username (required)
                    ├─► Enter fields to update
                    ├─► EmployeeManagement.update()
                    │       ├── Read employeeDatabase.txt
                    │       ├── Find employee
                    │       ├── Update fields
                    │       ├── Write to temp file
                    │       ├── Delete original
                    │       └── Rename temp
                    └─► Admin_Interface refreshed
```

---

<div style="page-break-after: always;"></div>

## 5. Data Storage Architecture

### 5.1 File-Based Storage System

The system uses **plain text files** for all data persistence. No database engine is used.

**Storage Location:** `Database/` directory (relative to application root)

---

### 5.2 Database Files

| File Name | Purpose | Format | Update Frequency | Size Limit |
|-----------|---------|--------|------------------|------------|
| `employeeDatabase.txt` | Employee records | Space-delimited | On employee CRUD operations | Unlimited |
| `itemDatabase.txt` | Sale item inventory | Space-delimited | On sale/return transactions | Unlimited |
| `rentalDatabase.txt` | Rental item inventory | Space-delimited | On rental/return transactions | Unlimited |
| `userDatabase.txt` | Customer rental history | Complex format | On rental/return operations | Unlimited |
| `couponNumber.txt` | Valid coupon codes | One code per line | Read-only (manual updates) | 1000 codes |
| `employeeLogfile.txt` | Login/logout audit log | Timestamped entries | On every login/logout | Unlimited |
| `saleInvoiceRecord.txt` | Sale transaction history | Multi-line per transaction | On every sale completion | Unlimited |
| `returnSale.txt` | Return transaction history | Multi-line per return | On every return completion | Unlimited |
| `temp.txt` | Unfinished transaction state | Transaction-specific | Continuously updated | Single transaction |

---

### 5.3 File Update Patterns

#### Pattern 1: Append-Only (Logs)

**Files:** `employeeLogfile.txt`, `saleInvoiceRecord.txt`, `returnSale.txt`

**Operations:**
- ✅ Always append, never overwrite
- ✅ Preserves historical data
- ⚠️ Files grow indefinitely (no rotation)

**Risk Level:** 🟡 Medium (disk space)

---

#### Pattern 2: Read-Modify-Write (Databases)

**Files:** `employeeDatabase.txt`, `itemDatabase.txt`, `rentalDatabase.txt`, `userDatabase.txt`

**Operations:**
```
1. Read entire file into memory
   │
2. Modify data structure
   │
3. Write to temporary file
   │
4. Delete original file
   │
5. Rename temp file to original name
```

**Risk Level:** 🔴 High (data loss if crash between delete and rename)

---

#### Pattern 3: Transaction State (Temp)

**File:** `temp.txt`

**Operations:**
- Continuously overwritten during transaction
- Single transaction state at a time

**Risk Level:** 🟡 Medium (lost if application crashes)

---

<div style="page-break-after: always;"></div>

## 6. User Interface Architecture

### 6.1 UI Component Hierarchy

```
                    ┌─────────────────────┐
                    │      JFrame         │
                    │    (Swing)         │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐   ┌─────────▼──────────┐  ┌────────▼────────┐
│ Login_        │   │ Cashier_           │  │ Admin_          │
│ Interface     │   │ Interface          │  │ Interface       │
│               │   │                    │  │                 │
│ • Username    │   │ • Sale Button      │  │ • Add Cashier   │
│ • Password    │   │ • Rental Button    │  │ • Add Admin     │
│ • Login Btn   │   │ • Return Button    │  │ • Remove Emp    │
│ • Exit Btn    │   │ • Logout Button    │  │ • Update Emp    │
│               │   │                    │  │ • Cashier View │
│               │   │                    │  │ • Logout        │
└───────┬───────┘   └─────────┬──────────┘  └────────┬────────┘
        │                     │                      │
        │                     │                      │
        └─────────────────────┼──────────────────────┘
                              │
        ┌─────────────────────┼──────────────────────┐
        │                     │                      │
┌───────▼────────┐   ┌────────▼──────────┐  ┌───────▼────────┐
│ Transaction_   │   │ EnterItem_        │  │ Payment_       │
│ Interface      │   │ Interface         │  │ Interface      │
│                │   │                   │  │                │
│ • Add Item     │   │ • Item ID         │  │ • Cash Payment │
│ • Remove Item  │   │ • Amount          │  │ • Electronic    │
│ • End Trans    │   │ • Enter Button    │  │ • Confirm       │
│ • Cancel       │   │ • Exit Button     │  │ • Cancel        │
└────────────────┘   └───────────────────┘  └────────────────┘
        │
        │
┌───────▼──────────────────────────────┐
│ AddEmployee_Interface               │
│ UpdateEmployee_Interface            │
│                                     │
│ • Name                              │
│ • Password                          │
│ • Position (Update only)           │
│ • Username (Update only)            │
└─────────────────────────────────────┘
```

---

### 6.2 UI Event Handling

**Pattern:** Direct ActionListener implementation in UI classes

**Event Flow:**
```
1. User action (button click, text input)
        │
2. actionPerformed(ActionEvent) method called
        │
3. Direct method calls to domain objects
        │
4. UI updates based on return values
        │
5. Navigation to next screen
```

**Coupling:** 🔴 High coupling - UI classes directly instantiate and call domain classes

---

### 6.3 Screen Navigation

**Navigation Rules:**

| From | To | Condition |
|------|-----|-----------|
| Login | Cashier/Admin | Based on role |
| Cashier | Transaction | Sale/Rental/Return selected |
| Transaction | Payment | Items in cart |
| Payment | Cashier | After confirmation |
| Admin | Employee Management | Dialog operations |
| All screens | Login | Via Logout |

**Window Management:**
- Uses `dispose()` to close windows
- Uses `setVisible(false)` before navigation
- Creates new instances for navigation (no singleton UI controllers)

---

<div style="page-break-after: always;"></div>

## 7. Business Logic Architecture

### 7.1 Business Rules

#### 7.1.1 Tax Calculation

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Tax Rate** | 6% (multiplier: 1.06) | All sale and rental transactions | `PointOfSale.tax` |
| **Configuration** | Hardcoded | No external configuration | N/A |
| **Note** | Fixed rate, no state-based variation | Applied uniformly | N/A |

---

#### 7.1.2 Coupon Discount

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Discount Rate** | 10% (multiplier: 0.90) | Only for sale transactions | `PointOfSale.coupon()` |
| **Validation** | Must exist in `couponNumber.txt` | Case-sensitive matching | `PointOfSale.coupon()` |
| **Limit** | 1000 coupons (array size) | Hardcoded limit | `PointOfSale.coupon()` |

---

#### 7.1.3 Rental Return Period

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Return Period** | 14 days from rental date | All rental transactions | `Payment_Interface.appendReturnDate()` |
| **Calculation** | Current date + 14 days | Automatic calculation | `Calendar.add(Calendar.DATE, 14)` |

---

#### 7.1.4 Late Fee Calculation

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Late Fee Rate** | 10% of item price per day late | Return transactions for rented items | `POH.endPOS()` |
| **Formula** | `Item Price × Amount × 0.1 × Days Late` | Applied per item | `POH.endPOS()` |

**Example Calculation:**
```
Item: Potato
Price: $1.00
Amount: 2
Days Late: 5

Late Fee = $1.00 × 2 × 0.1 × 5 = $1.00
```

---

#### 7.1.5 Credit Card Validation

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Length** | Exactly 16 digits | Electronic payment processing | `PointOfSale.creditCard()` |
| **Format** | All numeric | No special characters | `PointOfSale.creditCard()` |
| **Validation** | Basic format check only | No Luhn algorithm | `PointOfSale.creditCard()` |
| **Note** | No card type validation | No expiration date check | N/A |

---

#### 7.1.6 Phone Number Validation

| Rule | Value | Application | Location |
|------|-------|-------------|----------|
| **Length** | 10 digits | Customer identification | `Transaction_Interface.getCustomerPhone()` |
| **Range** | 1000000000 to 9999999999 | Numeric validation | `Transaction_Interface.getCustomerPhone()` |
| **Format** | Long integer | No formatting required | `Transaction_Interface.getCustomerPhone()` |

---

### 7.2 Business Logic Flow

#### Transaction Processing Flow

```
┌─────────────────────────────────────────────────────────────┐
│              TRANSACTION PROCESSING FLOW                    │
└─────────────────────────────────────────────────────────────┘

1. Initialize
   └─► Load inventory database
        │
2. Build Cart
   └─► Add/remove items via UI
        │
3. Calculate
   └─► Running total updated on each change
        │
4. Apply Discounts
   └─► Coupon (if applicable)
        │
5. Apply Tax
   └─► Final total calculation
        │
6. Process Payment
   └─► Cash or electronic
        │
7. Update Inventory
   └─► Decrement/increment stock
        │
8. Record Transaction
   └─► Write to appropriate log file
        │
9. Cleanup
   └─► Delete temp file, clear cart
```

#### Inventory Management Rules

| Operation | Stock Change | Flag Value | Validation |
|-----------|--------------|------------|------------|
| **Sale** | Decrement | `takeFromInventory = true` | ⚠️ No negative stock check |
| **Rental** | Decrement | `takeFromInventory = true` | ⚠️ No negative stock check |
| **Return** | Increment | `takeFromInventory = false` | ✅ Always allowed |

#### Customer Management Rules

| Rule | Description |
|------|-------------|
| **Auto-Creation** | New customers created automatically on first rental |
| **Rental Tracking** | Each rental recorded with return date and status |
| **Return Processing** | Updates rental status and calculates fees |

---

<div style="page-break-after: always;"></div>

## 8. File Format Specifications

### 8.1 Employee Database Format

**File:** `Database/employeeDatabase.txt`

**Format:** Space-delimited, one employee per line

**Structure:**
```
username position firstName lastName password
```

**Example:**
```
110001 Admin Harry Larry 1
110002 Cashier Debra Cooper lehigh2016
110003 Admin Clayton Watson lehigh2017
```

**Field Specifications:**

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `username` | String | Numeric string | Unique identifier |
| `position` | String | "Admin" or "Cashier" | Case-sensitive |
| `firstName` | String | Single token | ⚠️ **BREAKS if contains space** |
| `lastName` | String | Single token | ⚠️ **BREAKS if contains space** |
| `password` | String | Plain text | ⚠️ **No encryption** |

**Parsing Logic:**
```java
lineSort = line.split(" ");
username = lineSort[0];
position = lineSort[1];
name = lineSort[2] + " " + lineSort[3];  // Concatenated
password = lineSort[4];
```

---

### 8.2 Item Database Format

**File:** `Database/itemDatabase.txt` or `Database/rentalDatabase.txt`

**Format:** Space-delimited, one item per line

**Structure:**
```
itemID itemName price amount
```

**Example:**
```
1000 Potato 1.0 249
1001 PlasticCup 0.5 376
1002 SkirtSteak 15.0 1055
```

**Field Specifications:**

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `itemID` | Integer | Positive integer | Unique identifier |
| `itemName` | String | Single token | ⚠️ **BREAKS if contains space** |
| `price` | Float | Positive number | Currency value |
| `amount` | Integer | Non-negative | Stock quantity |

**Parsing Logic:**
```java
lineSort = line.split(" ");
itemID = Integer.parseInt(lineSort[0]);
itemName = lineSort[1];
price = Float.parseFloat(lineSort[2]);
amount = Integer.parseInt(lineSort[3]);
```

---

### 8.3 Customer Database Format

**File:** `Database/userDatabase.txt`

**Format:** Complex space-delimited format

**Structure:**
```
Header line (format description)
phoneNumber itemID1,returnDate1,returned1 itemID2,returnDate2,returned2 ...
```

**Example:**
```
Phone number rentedItem1ID,rentedItem1Date,returned1Bool rentedItem2ID,rentedItem2Date,returned2Bool...etc
6096515668 1000,6/30/09,true 1022,6/31/11,true
7282941912 1011,11/19/15,true
1111112222 1010,11/19/15,false
```

**Field Specifications:**

| Field | Type | Format | Notes |
|-------|------|--------|-------|
| Header | String | First line | Skipped during parsing |
| `phoneNumber` | Long | 10 digits | Customer identifier |
| `itemID` | Integer | Positive integer | Rental item identifier |
| `returnDate` | String | `MM/dd/yy` | Return due date |
| `returned` | Boolean | "true" or "false" | Return status |

**Parsing Logic:**
```java
// Skip first line
line = textReader.readLine();
while ((line = textReader.readLine()) != null) {
    phone = Long.parseLong(line.split(" ")[0]);
    // Parse rental entries
    for (int i = 1; i < line.split(" ").length; i++) {
        String rental = line.split(" ")[i];
        itemID = Integer.parseInt(rental.split(",")[0]);
        returnDate = rental.split(",")[1];
        returned = Boolean.parseBoolean(rental.split(",")[2]);
    }
}
```

---

### 8.4 Coupon Database Format

**File:** `Database/couponNumber.txt`

**Format:** One coupon code per line

**Example:**
```
COUPON123
SAVE10
DISCOUNT2024
```

**Constraints:**
- No specific format requirements
- Case-sensitive matching
- Array size limit: 1000 coupons (hardcoded)

---

### 8.5 Log File Formats

#### 8.5.1 Employee Log File

**File:** `Database/employeeLogfile.txt`

**Format:** One log entry per line

**Structure:**
```
name (username position) logs into POS System. Time: yyyy-MM-dd HH:mm:ss.SSS
```

**Example:**
```
Harry Larry (110001 Admin) logs into POS System. Time: 2024-01-15 10:30:45.123
Debra Cooper (110002 Cashier) logs out of POS System. Time: 2024-01-15 14:22:10.456
```

---

#### 8.5.2 Sale Invoice Record

**File:** `Database/saleInvoiceRecord.txt`

**Format:** Multi-line per transaction

**Structure:**
```
yyyy-MM-dd HH:mm:ss.SSS
itemID itemName amount itemTotal
itemID itemName amount itemTotal
...
Total with tax: totalPrice
```

**Example:**
```
2024-01-15 10:30:45.123
1000 Potato 2 2.0
1001 PlasticCup 5 2.5
Total with tax: 4.77
```

---

#### 8.5.3 Return Sale Record

**File:** `Database/returnSale.txt`

**Format:** Multi-line per return

**Structure:**
```
(blank line)
itemID itemName amount itemTotal
itemID itemName amount itemTotal
...
(blank line)
```

---

### 8.6 Temp File Format

**File:** `Database/temp.txt`

**Format:** Transaction-specific

**Sale Format:**
```
Sale
itemID amount
itemID amount
...
```

**Rental Format:**
```
Rental
phoneNumber
itemID amount
itemID amount
...
```

**Return Format:**
```
Return
phoneNumber
itemID amount
itemID amount
...
```

**Purpose:** Allows transaction recovery after application crash

---

<div style="page-break-after: always;"></div>

## 9. Workflow Specifications

### 9.1 Complete Sale Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETE SALE WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

Step 1:  Cashier logs in → Cashier_Interface displayed
         │
Step 2:  Cashier clicks "Sale" button
         │
Step 3:  Transaction_Interface("Sale") opens
         │
Step 4:  System loads itemDatabase.txt via Inventory
         │
Step 5:  Cashier clicks "Add Item"
         │
Step 6:  EnterItem_Interface opens
         │
Step 7:  Cashier enters itemID and amount
         │
Step 8:  System validates item exists in inventory
         │
Step 9:  Item added to cart (PointOfSale.transactionItem)
         │
Step 10: Total updated (PointOfSale.updateTotal())
         │
Step 11: Temp file updated (PointOfSale.createTemp())
         │
Step 12: Transaction dialog refreshed
         │
Step 13: Steps 5-12 repeat for additional items
         │
Step 14: Cashier clicks "End Transaction"
         │
Step 15: System checks cart is not empty
         │
Step 16: Payment_Interface opens
         │
Step 17: System displays cart items and total
         │
Step 18: Cashier applies coupon (optional, Sale only)
         │
Step 19: System calculates total with tax
         │
Step 20: Cashier selects payment method:
         ├─► Cash: Enter amount, calculate change
         └─► Electronic: Enter card number, validate, optional cash back
         │
Step 21: Cashier clicks "Confirm Payment"
         │
Step 22: POS.endPOS() called:
         ├── Apply tax to total
         ├── Inventory.updateInventory() - decrement stock
         ├── Write invoice to saleInvoiceRecord.txt
         ├── Delete temp.txt
         └── Clear cart
         │
Step 23: Payment_Interface closes
         │
Step 24: Cashier_Interface displayed
```

---

### 9.2 Complete Rental Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                   COMPLETE RENTAL WORKFLOW                   │
└─────────────────────────────────────────────────────────────┘

Step 1:  Cashier logs in → Cashier_Interface displayed
         │
Step 2:  Cashier clicks "Rental" button
         │
Step 3:  System prompts for customer phone number
         │
Step 4:  System validates phone number format
         │
Step 5:  Management.checkUser(phone) called
         │
Step 6:  If new customer: Management.createUser(phone)
         │
Step 7:  Transaction_Interface("Rental") opens
         │
Step 8:  POR instance created with phone number
         │
Step 9:  System loads rentalDatabase.txt via Inventory
         │
Step 10: Cashier adds items to cart (same as Sale workflow)
         │
Step 11: Temp file includes phone number
         │
Step 12: Cashier ends transaction
         │
Step 13: Payment_Interface opens
         │
Step 14: System displays cart and calculates total with tax
         │
Step 15: Cashier processes payment
         │
Step 16: POR.endPOS() called:
         ├── Apply tax to total
         ├── Management.addRental(phone, items) - record rental
         ├── Inventory.updateInventory() - decrement stock
         └── Delete temp.txt
         │
Step 17: Return date displayed (14 days from today)
         │
Step 18: Payment confirmed
         │
Step 19: Cashier_Interface displayed
```

---

### 9.3 Complete Return Workflow (Rented Items)

```
┌─────────────────────────────────────────────────────────────┐
│              COMPLETE RETURN WORKFLOW (RENTED)               │
└─────────────────────────────────────────────────────────────┘

Step 1:  Cashier logs in → Cashier_Interface displayed
         │
Step 2:  Cashier clicks "Return" button
         │
Step 3:  System prompts: "Rented Items" or "Unsatisfactory items"
         │
Step 4:  Cashier selects "Rented Items"
         │
Step 5:  System prompts for customer phone number
         │
Step 6:  System validates phone number
         │
Step 7:  Management.checkUser(phone) - must exist
         │
Step 8:  Transaction_Interface("Return") opens
         │
Step 9:  POH instance created with phone number
         │
Step 10: System loads rentalDatabase.txt via Inventory
         │
Step 11: Management.getLatestReturnDate(phone) called:
         ├── Read userDatabase.txt
         ├── Find customer record
         ├── Find outstanding rentals (returned=false)
         ├── Calculate days late for each item
         └── Return List<ReturnItem>
         │
Step 12: Cashier adds items to return cart
         │
Step 13: System matches returned items with rental history
         │
Step 14: Cashier ends transaction
         │
Step 15: Payment_Interface opens
         │
Step 16: System calculates late fees:
         │   For each returned item:
         │   ├── Find matching rental record
         │   ├── Calculate: itemPrice × amount × 0.1 × daysLate
         │   └── Display item details and fee
         │
Step 17: System displays total late fees
         │
Step 18: Cashier processes payment (if fees > 0)
         │
Step 19: POH.endPOS() called:
         ├── Calculate late fees
         ├── Inventory.updateInventory() - increment stock
         ├── Management.updateRentalStatus() - mark as returned
         └── Write to returnSale.txt
         │
Step 20: Payment confirmed
         │
Step 21: Cashier_Interface displayed
```

---

### 9.4 Employee Management Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              EMPLOYEE MANAGEMENT WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

Step 1:  Admin logs in → Admin_Interface displayed
         │
Step 2:  Admin views employee list (loaded from database)
         │
Step 3:  Admin performs action:
         │
         ├─► Option A: Add Employee
         │       │
         │       ├─► Click "Add Cashier" or "Add Admin"
         │       ├─► AddEmployee_Interface opens
         │       ├─► Enter name and password
         │       ├─► EmployeeManagement.add() called:
         │       │       ├── Read employeeDatabase.txt
         │       │       ├── Generate new username (increment last)
         │       │       ├── Determine position
         │       │       └── Append to file
         │       └─► Admin_Interface refreshed
         │
         ├─► Option B: Delete Employee
         │       │
         │       ├─► Click "Remove Employee"
         │       ├─► Enter username
         │       ├─► EmployeeManagement.delete() called:
         │       │       ├── Read employeeDatabase.txt
         │       │       ├── Remove from list
         │       │       ├── Write to temp file
         │       │       ├── Delete original
         │       │       └── Rename temp
         │       └─► Admin_Interface refreshed
         │
         └─► Option C: Update Employee
                 │
                 ├─► Click "Update Employee"
                 ├─► UpdateEmployee_Interface opens
                 ├─► Enter username (required)
                 ├─► Enter fields to update (empty = no change)
                 ├─► EmployeeManagement.update() called:
                 │       ├── Read employeeDatabase.txt
                 │       ├── Find employee
                 │       ├── Update fields
                 │       ├── Write to temp file
                 │       ├── Delete original
                 │       └── Rename temp
                 └─► Admin_Interface refreshed
```

---

### 9.5 Transaction Recovery Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              TRANSACTION RECOVERY WORKFLOW                   │
└─────────────────────────────────────────────────────────────┘

Step 1:  Application crashes during transaction
         │
Step 2:  Temp file (temp.txt) remains on disk
         │
Step 3:  Cashier logs in → Cashier_Interface displayed
         │
Step 4:  System checks: POSSystem.checkTemp()
         │
Step 5:  If temp.txt exists:
         │
         ├─► Display dialog: "Restore unfinished transaction?"
         │
         ├─► If Yes:
         │       │
         │       ├─► Get customer phone (if Rental/Return)
         │       ├─► POSSystem.continueFromTemp(phone) called:
         │       │       ├── Read temp.txt first line (transaction type)
         │       │       ├── Create appropriate object (POS/POR/POH)
         │       │       ├── Call retrieveTemp() to restore cart
         │       │       └── Return transaction type string
         │       ├─► Transaction_Interface opens with restored cart
         │       └─► Cashier continues transaction
         │
         └─► If No:
                 │
                 ├─► Delete temp.txt
                 └─► Continue normally
```

---

<div style="page-break-after: always;"></div>

## 10. Dependency Graph

### 10.1 Class Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    CLASS DEPENDENCIES                        │
└─────────────────────────────────────────────────────────────┘

Register
└── Login_Interface

Login_Interface
├── POSSystem
└── Cashier_Interface / Admin_Interface

Cashier_Interface
├── POSSystem (temp recovery)
├── Management (customer check)
└── Transaction_Interface

Admin_Interface
├── EmployeeManagement
├── AddEmployee_Interface
├── UpdateEmployee_Interface
└── Cashier_Interface

Transaction_Interface
├── PointOfSale (POS/POR/POH)
├── Management (customer operations)
├── EnterItem_Interface
└── Payment_Interface

EnterItem_Interface
└── PointOfSale

Payment_Interface
├── PointOfSale
└── Management (return calculations)

PointOfSale (Abstract)
├── Inventory (Singleton)
└── Item

POS / POR / POH
├── PointOfSale (inherit)
├── Inventory
├── Management (POR/POH only)
└── Item

Inventory
└── Item

Management
└── ReturnItem

EmployeeManagement
└── Employee

POSSystem
└── Employee
```

---

### 10.2 File Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    FILE DEPENDENCIES                         │
└─────────────────────────────────────────────────────────────┘

Application Execution
├── Database/employeeDatabase.txt (required)
├── Database/itemDatabase.txt (required for sales)
├── Database/rentalDatabase.txt (required for rentals)
├── Database/userDatabase.txt (required for rentals/returns)
├── Database/couponNumber.txt (optional, for coupons)
└── Database/temp.txt (optional, for recovery)

Runtime File Creation:
├── Database/employeeLogfile.txt (created on first login)
├── Database/saleInvoiceRecord.txt (created on first sale)
└── Database/returnSale.txt (created on first return)
```

---

### 10.3 External Dependencies

**Java Standard Library:**

| Package | Purpose |
|---------|---------|
| `java.awt.*` | UI components (AWT) |
| `javax.swing.*` | Swing framework |
| `java.io.*` | File I/O operations |
| `java.util.*` | Collections, Date/Time |
| `java.text.*` | Date formatting |

**No External Libraries:**
- ✅ Pure Java implementation
- ✅ No third-party dependencies
- ✅ No database drivers
- ✅ No logging frameworks

---

<div style="page-break-after: always;"></div>

## 11. System Configuration

### 11.1 Build Configuration

**Build Tool:** Apache Ant (via NetBeans)

**Build File:** `build.xml`
- Imports NetBeans build implementation
- Standard Java compilation
- JAR packaging via `manifest.mf`

**Manifest File:** `manifest.mf`
- Minimal configuration
- Main-Class added automatically by build

**NetBeans Configuration:** `nbproject/`
- Project properties
- Build implementation
- IDE-specific settings

---

### 11.2 Runtime Configuration

**No Configuration Files:**
- ⚠️ All paths hardcoded in source code
- ⚠️ All business rules hardcoded (tax, discount, fees)
- ⚠️ No properties files
- ⚠️ No environment variables

**Hardcoded Paths:**
```java
"Database/employeeDatabase.txt"
"Database/itemDatabase.txt"
"Database/rentalDatabase.txt"
"Database/userDatabase.txt"
"Database/couponNumber.txt"
"Database/temp.txt"
"Database/employeeLogfile.txt"
"Database/saleInvoiceRecord.txt"
"Database/returnSale.txt"
```

**Hardcoded Business Rules:**
```java
tax = 1.06                    // 6% tax
discount = 0.90f              // 10% discount
lateFeeRate = 0.1             // 10% per day
rentalPeriod = 14             // 14 days
```

---

### 11.3 System Requirements

**Runtime:**
- Java Runtime Environment (JRE) - version not specified
- Java Swing support (included in JRE)
- File system write access to `Database/` directory

**Development:**
- Java Development Kit (JDK)
- Apache Ant (for building)
- NetBeans IDE (optional, for development)

**Operating System:**
- Designed for cross-platform (Java)
- Path handling commented out (Windows-specific code disabled)
- Assumes forward-slash path separators

---

<div style="page-break-after: always;"></div>

## Document Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024 | Initial reverse-engineered documentation | System Analysis |

---

## Appendix A: Code Metrics Summary

### Code Statistics

| Metric | Value |
|-------|-------|
| **Total Java Classes** | 20 |
| **Total Lines of Code** | ~2,500 (estimated) |
| **UI Classes** | 9 |
| **Domain Classes** | 8 |
| **Data Model Classes** | 3 |

### System Characteristics

| Characteristic | Value |
|----------------|-------|
| **File I/O Operations** | Extensive (every transaction touches multiple files) |
| **Database Files** | 9 text files |
| **External Dependencies** | None (Pure Java) |
| **Design Patterns** | 4 (Singleton, Template Method, Strategy, MVC-like) |

---

## Appendix B: Known Limitations

### Critical Limitations

| # | Limitation | Impact | Severity |
|---|------------|--------|----------|
| 1 | **No Transaction Support** | File updates are not atomic | 🔴 Critical |
| 2 | **No Concurrency Control** | Multiple users can corrupt data | 🔴 Critical |
| 3 | **No Data Validation** | Negative stock allowed | 🟡 High |
| 4 | **No Error Recovery** | File corruption causes system failure | 🔴 Critical |
| 5 | **Hardcoded Configuration** | No external configuration support | 🟡 Medium |
| 6 | **Plaintext Passwords** | Security vulnerability | 🔴 Critical |
| 7 | **Fragile File Formats** | Space-containing names break parsing | 🟡 High |
| 8 | **No Backup Mechanism** | Data loss risk on file corruption | 🔴 Critical |

### Risk Assessment

**🔴 Critical Risks:**
- Data corruption from concurrent access
- Data loss from file operation failures
- Security vulnerabilities from plaintext storage

**🟡 High Risks:**
- System failures from invalid data
- Parsing errors from malformed input

**🟢 Medium Risks:**
- Configuration inflexibility
- Maintenance difficulties

---

<div align="center">

---

**End of Technical Documentation**

*This document was generated through reverse engineering analysis of the Point-of-Sale System*

---

</div>

