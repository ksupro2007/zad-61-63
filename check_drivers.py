import pyodbc

print("🔍 Драйверы, которые ВИДИТ твой Python:")
for driver in pyodbc.drivers():
    print(f"   -> '{driver}'")