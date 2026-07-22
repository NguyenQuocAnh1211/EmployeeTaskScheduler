from flask import Flask, render_template

app = Flask(nhóm 3)

@app.route('/')
def home():
    return render_template('index.html')

# Yêu cầu 3: Tạo thêm một trang /about
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)