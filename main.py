from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import math


def lg(x):
    return math.log(x, 10)


def ln(x):
    return math.log(x, math.e)


app = Flask(__name__)
CORS(app)


# 定义路由
@app.route('/calculate', methods=['POST'])
def calculate():
    # 创建或连接到SQLite数据库
    conn = sqlite3.connect('expressions.db')

    try:
        expression = request.json['expression']
        result = eval(expression)
        c = conn.cursor()
        c.execute("INSERT INTO expressions (expression, result) VALUES (?, ?)", (expression, str(result)))
        conn.commit()
        return jsonify({'result': result})
    except Exception:
        return jsonify({'result': None, 'errMsg': '表达式异常，请检查输入'})
    finally:
        # 关闭连接
        conn.close()


@app.route('/history', methods=['GET'])
def history():
    conn = sqlite3.connect('expressions.db')
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM expressions")
        rows = c.fetchall()

        history = []
        for row in rows:
            history.append({
                'expression': row[0],
                'result': row[1]
            })
        history.reverse()
        history = history[:10]

        return jsonify({'result': history})
    finally:
        # 关闭连接
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
