from flask import Flask, render_template
import pyodbc

app = Flask(__name__)


def get_db():
    try:
        server_name = r'localhost\SQLEXPRESS'

        conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={server_name};"
            "DATABASE=Scuishop;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
        )

        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
        return None


@app.route('/')
def index():
    conn = get_db()
    if not conn:
        return "<h1>Ошибка подключения к БД</h1>"

    cursor = conn.cursor()
    cursor.execute("SELECT TOP 6 * FROM Products")
    products = cursor.fetchall()
    conn.close()

    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db()
    if not conn:
        return "Ошибка БД"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product:
        return render_template('product.html', product=product)
    return "Товар не найден", 404


if __name__ == '__main__':
    app.run(debug=True)