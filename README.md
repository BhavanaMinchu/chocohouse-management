# ChocoHouse Management

ChocoHouse Management is a web application built with Flask and SQLite to manage the seasonal chocolate flavors, ingredients inventory, and customer suggestions for a chocolate business.

## Table of Contents

1. [Features](#features)
2. [Setup](#setup)
3. [Database Structure and SQL Queries](#database-structure-and-sql-queries)
4. [Testing](#testing)
5. [Docker Setup](#docker-setup)
6. [Usage](#usage)

---

## Features

- **Manage Seasonal Flavors:** Add, update, view, and delete seasonal chocolate flavors.
- **Manage Inventory:** Keep track of ingredients, update quantities, and manage inventory items.
- **Customer Flavor Suggestions:** Accept, view, update, and delete customer suggestion.

## Setup

### Prerequisites

- **Python 3.x**
- **Flask**
- **SQLite3**

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/BhavanaMinchu/chocohouse-management.git
   cd chocohouse-management
   ```

2. Install dependencies:

   ```bash
   pip install flask
   ```

3. Initialize the database tables:
   ```bash
   python app.py
   ```

## Database Structure and SQL Queries

The database `chocolate_house.db` contains three tables:

1. **flavors**

   - `id` (INTEGER, Primary Key)
   - `name` (TEXT, not null)
   - `description` (TEXT)
   - `stock` (TEXT, not null)
   - `season` (TEXT, not null)

   **SQL Query to add a flavor**:

   ```sql
   INSERT INTO flavors (name, description, stock, season) VALUES (?, ?, ?, ?)
   ```

2. **inventory**

   - `id` (INTEGER, Primary Key)
   - `ingredient` (TEXT, not null)
   - `quantity` (INTEGER, not null)

   **SQL Query to update inventory quantity**:

   ```sql
   UPDATE inventory SET quantity = quantity + ? WHERE ingredient = ?
   ```

3. **suggestions**

   - `id` (INTEGER, Primary Key)
   - `customer_name` (TEXT)
   - `suggestion` (TEXT)
   - `allergy_concerns` (TEXT)

   **SQL Query to add a customer suggestion**:

   ```sql
   INSERT INTO suggestions (customer_name, suggestion, allergy_concerns) VALUES (?, ?, ?)
   ```

## Testing

To validate that each feature works as expected:

### 1. Verify Seasonal Flavors

- Navigate to `/flavors` to view all flavors.
- Add a new flavor and ensure it appears in the list.
- Update an existing flavor and check if changes are saved.
- Delete a flavor and confirm its removal.

### 2. Verify Ingredient Inventory

- Go to `/inventory` to view all inventory items.
- Add a new ingredient, ensuring it's listed.
- Update the quantity of an existing ingredient.
- Delete an ingredient and confirm removal.

### 3. Verify Customer Suggestions

- Navigate to `/suggestions` to view all suggestions.
- Add a suggestion and verify it appears.
- Update an existing suggestion and check for changes.
- Delete a suggestion and ensure it's removed.

## Docker Setup

### Dockerfile

Use the `Dockerfile` to containerize the application:

Build the Docker image:

```bash
docker build -t chocohouse-management .
```

Run the Docker container:

```bash
docker run -p 5000:5000 chocohouse-management
```

## Usage

Access the application at `http://localhost:5000` in your web browser.
