from simple_framework import SimpleFramework, response, response_json, render_html
import json

app = SimpleFramework()

@app.route('/t1', ['get'])
def t1():
    return response('djajfkasfjkajf')

@app.route('/t2', ['get'])
def t2():
    return response_json(json.dumps({
        'aaaa': 1111
    }))

@app.route('/t3', ['get'])
def t3():
    return render_html('test.html')