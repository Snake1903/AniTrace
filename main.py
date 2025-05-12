from flask import Flask, request, jsonify, render_template, redirect, url_for
import urllib.parse
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #GET URL FROM THE FORM
        url = request.form['url']
        image = request.files.get('image')
        if url:
            response = requests.get("https://api.trace.moe/search?url={}"
                        .format(urllib.parse.quote_plus(f"{url}"))).json()            
        elif image:
            response = requests.post("https://api.trace.moe/search",
                        files={'image': image},).json()
            

        result = response.get('result', [])    
        return redirect(url_for('result', result=str(result)))

    return render_template('index.html')

@app.route('/result', methods=['GET'])
def result():
    results = request.args.get('result')
    if results:
        results = eval(results)
        return render_template('result.html', results=results)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
