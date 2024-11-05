from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
#DB name
DATABASE = 'chocolate_house.db'
# DB connection function
def connect_db():
    return sqlite3.connect(DATABASE)

# Create Tables for Flavors, Inventory and Suggestion
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            stock TEXT NOT NULL,
            season TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            suggestion TEXT,
            allergy_concerns TEXT
        )
    ''')
    conn.commit()
    conn.close()

# App routes
@app.route('/')
def home():
    return render_template('home.html')

# Seasonal Flavors Route with CRUD
@app.route('/flavors', methods=['GET', 'POST'])
def flavors():
    #DB connection
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        stock=request.form['stock']
        season = request.form['season']
        cursor.execute('INSERT INTO flavors (name, description, stock, season) VALUES (?,?, ?, ?)', (name, description, stock, season))
        conn.commit()
        return redirect(url_for('flavors'))
#Display all Flavors
    cursor.execute('SELECT * FROM flavors')
    flavors = cursor.fetchall()
    conn.close()
    return render_template('flavors.html', flavors=flavors)

@app.route('/flavors/edit/<int:flavor_id>', methods=['GET', 'POST'])
def edit_flavor(flavor_id):
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        stock=request.form['stock']
        season = request.form['season']
        cursor.execute('UPDATE flavors SET name = ?, description = ?,stock = ?, season = ? WHERE id = ?', (name, description, stock, season, flavor_id))
        conn.commit()
        return redirect(url_for('flavors'))
#Display all Flavors
    cursor.execute('SELECT * FROM flavors WHERE id = ?', (flavor_id,))
    flavor = cursor.fetchone()
    conn.close()
    return render_template('edit_flavor.html', flavor=flavor)

@app.route('/flavors/delete/<int:flavor_id>')
def delete_flavor(flavor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flavors WHERE id = ?', (flavor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('flavors'))

# Ingredient Inventory Route with CRUD
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        quantity = request.form['quantity']
        #check existing 
        cursor.execute('SELECT * FROM inventory WHERE ingredient = ?', (ingredient,))
        existing_ingredient = cursor.fetchone()
        if existing_ingredient:
            # if ingredient exists update quantity
            cursor.execute('UPDATE inventory SET quantity = quantity + ? WHERE ingredient = ?', (quantity, ingredient))
        else:
            # If ingredient does not exist, add new
            cursor.execute('INSERT INTO inventory (ingredient, quantity) VALUES (?, ?)', (ingredient, quantity))
        conn.commit()
        return redirect(url_for('inventory'))
#Display all Ingredients 
    cursor.execute('SELECT * FROM inventory')
    ingredients = cursor.fetchall()
    conn.close()
    return render_template('inventory.html', ingredients=ingredients)

@app.route('/inventory/edit/<int:ingredient_id>', methods=['GET', 'POST'])
def edit_inventory(ingredient_id):
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        quantity = request.form['quantity']
        cursor.execute('UPDATE inventory SET ingredient = ?, quantity = ? WHERE id = ?', (ingredient, quantity, ingredient_id))
        conn.commit()
        return redirect(url_for('inventory'))
#Display all Ingredients 
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (ingredient_id,))
    ingredient = cursor.fetchone()
    conn.close()
    return render_template('edit_inventory.html', ingredient=ingredient)


@app.route('/inventory/delete/<int:ingredient_id>')
def delete_inventory(ingredient_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (ingredient_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('inventory'))


# Customer Suggestions Route with CRUD
@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        suggestion = request.form['suggestion']
        allergy_concerns = request.form['allergy_concerns']
        cursor.execute('INSERT INTO suggestions (customer_name, suggestion, allergy_concerns) VALUES (?, ?, ?)',
                       (customer_name, suggestion, allergy_concerns))
        conn.commit()
        return redirect(url_for('suggestions'))
#Display All Suggestions
    cursor.execute('SELECT * FROM suggestions')
    suggestions = cursor.fetchall()
    conn.close()
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/suggestions/edit/<int:suggestion_id>', methods=['GET', 'POST'])
def edit_suggestion(suggestion_id):
    conn = connect_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        suggestion = request.form['suggestion']
        allergy_concerns = request.form['allergy_concerns']
        cursor.execute('UPDATE suggestions SET customer_name = ?, suggestion = ?, allergy_concerns = ? WHERE id = ?',
                       (customer_name, suggestion, allergy_concerns, suggestion_id))
        conn.commit()
        return redirect(url_for('suggestions'))
#Display all Suggestions
    cursor.execute('SELECT * FROM suggestions WHERE id = ?', (suggestion_id,))
    suggestion = cursor.fetchone()
    conn.close()
    return render_template('edit_suggestion.html', suggestion=suggestion)

@app.route('/suggestions/delete/<int:suggestion_id>')
def delete_suggestion(suggestion_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM suggestions WHERE id = ?', (suggestion_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('suggestions'))
#Create Tables if they dont exist
create_tables()
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
