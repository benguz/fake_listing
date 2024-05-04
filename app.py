from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)
data_file = 'pages.json'
admin_password = 'yourpassword'  # You should secure this better in a real app

# Ensure data file exists
if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump({}, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        password = request.form['password']
        title = request.form['title']
        description = request.form['description']

        if password == admin_password:
            with open(data_file, 'r+') as file:
                data = json.load(file)
                data[url] = {'title': title, 'description': description}
                file.seek(0)
                json.dump(data, file, indent=4)
            return redirect(url_for('page', url=url))
        else:
            return 'Incorrect password', 403

    return render_template('form.html')

@app.route('/<path:url>')
def page(url):
    with open(data_file, 'r') as file:
        data = json.load(file)
        page_data = data.get(url, None)
        if page_data:
            return render_template('page.html', title=page_data['title'], description=page_data['description'])
    return 'Page not found', 404

if __name__ == '__main__':
    app.run(debug=True)
