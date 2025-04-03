from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL 연결 설정
db = pymysql.connect(host='localhost', user='root', password='root', database='arcade_adventure_db', cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()

# 회원가입 API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    
    try:
        cursor.execute("INSERT INTO accounts (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({"success": True, "message": "User registered successfully"})
    except pymysql.err.IntegrityError:
        return jsonify({"success": False, "message": "Username already exists"})

# 로그인 API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    cursor.execute("SELECT * FROM accounts WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"success": True, "message": "Login successful", "user_id": user["id"]})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401  # ❗ 로그인 실패 시 HTTP 401 (Unauthorized) 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
