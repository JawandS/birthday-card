from flask import Flask, render_template, request, send_file
import img_gen 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        attributes = {
            'age': request.form['age'],
            'gender': request.form['gender'],
            'interests': request.form['interests'],
            'style': request.form['style'],
            'color_scheme': request.form['color_scheme']
        }
        filepath = img_gen.main(attributes)
        # display pdf
        return send_file(filepath, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
