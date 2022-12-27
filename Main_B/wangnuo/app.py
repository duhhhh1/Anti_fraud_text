from flask import Flask, render_template, url_for, request
from model import textCNN
import torch
from sen2inds import read_labelFile, get_worddict
import numpy as np
import time
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
	label_w2n, label_n2w = read_labelFile('data/label.txt')
	word2ind, ind2word = get_worddict('data/wordLabel.txt')
	stoplist = open('data/stopword.txt', 'r', encoding='utf_8').read().split('\n')
	pad_size = 256
	textCNN_param = {
    'vocab_size': len(word2ind),
    'embed_dim': 60,	
    'class_num': len(label_w2n),
    "kernel_num": 16,
    "kernel_size": [3, 4, 5],
    "dropout": 0.5,
	}
	clf = textCNN(textCNN_param)
	clf.load_state_dict(torch.load('weight.pkl'))
	clf.eval()

	if request.method == 'POST':
		message = request.form['message']
		message_copy = message
		message = message.replace("年", "-").replace("月", "-").replace("日", "-").replace("时", "-").replace("分", " ").strip()
		message = re.sub("\s+", "", message)
		# 2022年6月14日18时01分许 "2022年6月7日" "2014年5月"
		# [^\u4e00-\u9fa5]  除去字符
		regex_list = [r"(\d{4}-\d{1,2}-\d{1,2}-\d{1,2}-\d{1,2})|(\d{4}-\d{1,2}-\d{1,2})|(\d{4}-\d{1,2})",
					r"[_.!+-=——,$%^，：“”（）:。？、~@#￥%……&*《》<>「」{}【】()/]",
					]
		for regex in regex_list:
			pattern = re.compile(regex)
			message = re.sub(pattern,'',message)
		# print(type(message))
		# data = [message]
		# vect = cv.transform(data).toarray()
		title_seg = list(message)
		# print(title_seg)
		title_ind = []
		for w in title_seg:
			if w in stoplist:
				continue
			title_ind.append(word2ind[w])
		length = len(title_ind)
		if length > pad_size:
			title_ind = title_ind[0:pad_size]
		if length <= pad_size:
			title_ind.extend([0] * (pad_size - length))
		sentence = np.array([int(x) for x in title_ind[0:256]])
		sentence = torch.from_numpy(sentence)
		predict = clf(sentence.unsqueeze(0).type(torch.LongTensor)).cpu().detach().numpy()[0]  # .cuda()).cpu().detach().numpy()[0]
		score = max(predict)
		label = np.where(predict == score)[0][0]

	return render_template('detect.html',prediction = label, message = message_copy, time_text = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

@app.route('/charts', methods=['GET', 'POST'])
def charts():
	return render_template('charts.html')

if __name__ == '__main__':
	app.run(debug=True)