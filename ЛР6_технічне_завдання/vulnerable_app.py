from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['GET'])
def search():
    name = request.args.get("name", "")
    
    if not name:
        return "Параметр 'name' відсутній. Використовуйте форму на головній сторінці.", 400
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    # ⚠️ НЕБЕЗПЕЧНО
    query = f"SELECT * FROM students WHERE name LIKE '%{name}%'"
    
    print("\n" + "="*60)
    print("🔓 ВРАЗЛИВИЙ ЗАПИТ:")
    print(f"   {query}")
    print("="*60 + "\n")
    
    try:
        c.execute(query)
        results = c.fetchall()
        conn.close()
        
        print(f"✓ Знайдено записів: {len(results)}")
        
        return render_template("results.html", students=results, query=query)
    except Exception as e:
        conn.close()
        print(f"❌ Помилка SQL: {e}")
        return render_template("error.html", error=str(e))

if __name__ == "__main__":
    if not os.path.exists("database.db"):
        print("\n❌ База даних не знайдена! Запустіть: python create_db.py\n")
    else:
        print("\n🔓 ВРАЗЛИВА ВЕРСІЯ: http://127.0.0.1:5000\n")
        app.run(debug=True, port=5000, host='127.0.0.1')