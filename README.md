# Forward-Engineered Point of Sale System (Python + Django)

## 📌 Project Overview

This project is a **forward-engineered and reengineered version of a legacy Java-based Point of Sale (POS) system**.
The primary goal was to modernize the legacy system by **systematically applying the Software Reengineering Process Model** and transforming it into a **web-based POS application using Python and Django**.

The new system improves:

* Code maintainability
* System scalability
* Architectural clarity
* Data persistence using a proper database
* Separation of concerns using modern frameworks

---

## 🎯 Objectives

* Analyze and understand a **legacy Java POS system**
* Identify **active, reusable, and obsolete assets**
* Perform **dependency mapping** (class-to-class, file-to-database)
* Reengineer the system using **modern technologies**
* Convert file-based storage into **database-driven architecture**
* Implement a **clean, modular Django-based solution**

---

## 🧱 Reengineering Methodology Used

The project follows the **Software Reengineering Process Model**, consisting of:

1. **Inventory Analysis**

   * Identified active source files, data files, and configuration assets
   * Classified reusable and obsolete components

2. **Dependency Analysis**

   * Class-to-class dependencies
   * File-to-database dependencies
   * Data flow and control flow relationships

3. **Architecture Redesign**

   * Converted monolithic Java logic into layered architecture
   * Introduced MVC/MVT pattern using Django

4. **Code Transformation**

   * Legacy Java classes → Python modules
   * Java GUI → Web-based Django views & templates
   * Text-file storage → Database models

5. **Forward Engineering**

   * Implemented a modern POS system using Django
   * Clean separation of UI, business logic, and data layers

---

## 🛠️ Technology Stack

| Layer           | Technology                                   |
| --------------- | -------------------------------------------- |
| Backend         | Python                                       |
| Framework       | Django                                       |
| Database        | SQLite (can be upgraded to PostgreSQL/MySQL) |
| Architecture    | MVT (Model–View–Template)                    |
| Version Control | Git & GitHub                                 |

---

## 🧩 System Architecture

The reengineered system follows a **layered architecture**:

* **Presentation Layer**

  * Django templates (Web UI)
  * Handles user interaction (Admin, Cashier)

* **Business Logic Layer**

  * Sales, Rentals, Returns
  * Inventory and Employee management

* **Data Layer**

  * Django ORM
  * Persistent database storage

---

## 📂 Project Structure

```
pos_system/
│
├── core/
│   ├── models.py        # Database models (Item, Employee, Sale, Rental)
│   ├── views.py         # Business logic & request handling
│   ├── urls.py          # Application routing
│
├── templates/
│   ├── admin/
│   ├── cashier/
│   └── transactions/
│
├── static/
│   └── css, js
│
├── manage.py
└── README.md
```

---

## 🔄 Legacy to Modern Mapping

| Legacy Java Component | Django Equivalent       |
| --------------------- | ----------------------- |
| `Employee.java`       | Django `Employee` Model |
| `Item.java`           | Django `Item` Model     |
| `POS / POR / POH`     | Django Views & Services |
| `.txt database files` | Relational Database     |
| Swing GUI             | Web-based Templates     |

---

## ✅ Key Improvements Over Legacy System

* ❌ Removed file-based `.txt` databases
* ✅ Introduced structured relational database
* ❌ Removed tightly coupled GUI logic
* ✅ Implemented clean MVC/MVT architecture
* ❌ Reduced code redundancy
* ✅ Improved scalability and extensibility

---

## 📈 Educational Outcomes

This project demonstrates:

* Practical application of **software reengineering concepts**
* Understanding of **legacy system modernization**
* Dependency analysis and architectural redesign
* Real-world migration from **desktop-based systems to web applications**

---

## 🚀 Future Enhancements

* Role-based authentication
* REST API integration
* Cloud deployment
* Barcode scanning support
* Payment gateway integration

---

## 👩‍💻 Author

**Areeba Naeem**
Software Engineering | AI & Systems
GitHub: [https://github.com/Areebanaeem123](https://github.com/Areebanaeem123)

---

## 📜 License

This project is developed for **academic and learning purposes**.
