import pyodbc

print("=" * 50)
print("ДИАГНОСТИКА ПОДКЛЮЧЕНИЯ К SQL SERVER")
print("=" * 50)

# 1. Проверяем установленные драйверы
print("\n1. Установленные ODBC драйверы:")
drivers = pyodbc.drivers()
for d in drivers:
    print(f"   - {d}")

if 'ODBC Driver 17 for SQL Server' not in drivers:
    print("\n❌ ОШИБКА: ODBC Driver 17 не установлен!")
    print("Скачай: https://go.microsoft.com/fwlink/?linkid=2248676")
else:
    print("✅ ODBC Driver 17 найден")

# 2. Пробуем разные варианты имени сервера
server_names = [
    r'localhost',
    r'localhost\SQLEXPRESS',
    r'.\SQLEXPRESS',
    r'LENOVO',
    r'LENOVO\SQLEXPRESS',
    r'(localdb)\MSSQLLocalDB',
]

print("\n2. Проверка подключения к серверам:")
for server in server_names:
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE=master;'
            f'Trusted_Connection=yes;'
        )
        print(f"   ✅ ПОДКЛЮЧЕНИЕ УСПЕШНО: {server}")
        conn.close()
    except Exception as e:
        print(f"    {server}: {str(e)[:80]}")

# 3. Если нашли рабочий сервер — проверяем базу Squishop
print("\n3. Проверка базы данных Squishop:")
working_server = None
for server in server_names:
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE=master;'
            f'Trusted_Connection=yes;'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'Squishop'")
        if cursor.fetchone():
            print(f"   ✅ База Squishop найдена на сервере: {server}")
            working_server = server

            # Проверяем таблицу Products
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE=Squishop;'
                f'Trusted_Connection=yes;'
            )
            conn2 = pyodbc.connect(conn_str)
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT COUNT(*) FROM Products")
            count = cursor2.fetchone()[0]
            print(f"   ✅ Таблица Products существует, записей: {count}")

            cursor2.execute("SELECT TOP 3 name, price FROM Products")
            print("   📦 Примеры товаров:")
            for row in cursor2.fetchall():
                print(f"      - {row.name}: {row.price} руб.")
            conn2.close()
        else:
            print(f"   ⚠️ База Squishop НЕ найдена на {server}")
        conn.close()
    except:
        pass

if working_server:
    print(f"\n✅ РАБОЧИЙ СЕРВЕР: {working_server}")
    print(f"\nСкопируй эту строку в app.py:")
    print(f"   server_name = r'{working_server}'")
else:
    print("\n❌ Не удалось найти рабочий сервер!")
    print("Проверь, что SQL Server запущен (см. инструкцию ниже)")

print("\n" + "=" * 50)