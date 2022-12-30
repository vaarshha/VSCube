
import io

import torch
from image_process import read_image
from flask import Flask, render_template, request
import os

app = Flask(__name__)
import pickle


class CPU_Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
            return super().find_class(module, name)


model = CPU_Unpickler(open('T5model.pkl', 'rb')).load()

@app.route('/')
def home_page():
    return render_template('landing.html', button_name="SUBMIT")

@app.route('/page1')
def page_1():
    return render_template('copy.html')

@app.route('/page2')
def page_2():
    return render_template('index.html')

@app.route('/page3')
def page_3():
    return render_template('url.html')




@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
    text = read_image(uploaded_file.filename)
    os.remove(uploaded_file.filename)
    return render_template('index.html', Output=text)



@app.route('/', methods=['GET', 'POST'])
def data():
    if request.method == "POST":
        ARTICLE = request.form['text']
        length = len(ARTICLE)
        max_chunk = length // 6
        ARTICLE = ARTICLE.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')
        sentences = ARTICLE.split('<eos>')
        current_chunk = 0
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])

        for i in range(len(chunks)):
            if (i != 0):
                chunks[i] = "summarize:" + chunks[i]
        str = ""
        for i in chunks:
            str += model.predict(i)[0] + "."

        return render_template('index.html', Output="Hello", button_name="REDO")
