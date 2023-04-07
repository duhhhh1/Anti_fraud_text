from flask import Flask, render_template, url_for, request, jsonify
from model.TextCNN import Model as textCNN
from utils import build_dataset, build_iterator, get_time_dif
from model.FastText import Model as Fasttext
from utils_fasttext import build_dataset, build_iterator, get_time_dif
from train_eval import train, init_network
from importlib import import_module
import torch
import numpy as np
import pickle as pkl
import time
import re
import openai
import json
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16,np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)): # add this line
            return obj.tolist() # add this line
        return json.JSONEncoder.default(self, obj)   
app = Flask(__name__)
openai.api_key = "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"

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
	dataset = 'AntiScam'  # 数据集
	embedding = 'embedding_SougouNews.npz'
	embedding_y = 'random'
	x = import_module('model.TextCNN')
	y = import_module('model.FastText')
	config_x = x.Config(dataset, embedding, 0)
	config_y = y.Config(dataset, embedding_y)
	print(config_x.device,config_y.device)
	config_y.n_vocab = 3041
	UNK, PAD = '<UNK>', '<PAD>'  # 未知字，padding符号
	pad_size_x = config_x.pad_size
	pad_size_y = config_y.pad_size
	print(config_y.n_vocab,config_y.pad_size)
	model1 = x.Model(config_x).to('cpu')  # TextCNN模型
	model1.load_state_dict(torch.load('AntiScam/saved_dict/TextCNN.ckpt'))
	model2 = y.Model(config_y).to('cpu')  # FastText模型
	model2.load_state_dict(torch.load('AntiScam/saved_dict/FastText.ckpt'))  
	model1.eval()
	model2.eval()


	if request.method == 'POST':
		message = request.form['message']
		usemodel = request.form['model']
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
			
		# tokenizer = lambda x: x.split(' ') # 分字
		vocab = pkl.load(open('AntiScam/data/vocab.pkl', 'rb'))
		token = list(message)
		token_c = token.copy()
		seq_len = len(token)
		if usemodel == 'FastText':
			if pad_size_y:
				if len(token_c) < pad_size_y:
					token_c.extend([PAD] * (pad_size_y - len(token_c)))
				else:
					token_c = token_c[:pad_size_y]
			seq_len = pad_size_y
			print(seq_len,len(token_c),token_c)
			words_c = []
			for word in token_c:
				words_c.append(vocab.get(word, vocab.get(UNK)))
			print(words_c)
			def biGramHash(sequence, t, buckets):
				t1 = sequence[t - 1] if t - 1 >= 0 else 0	
				return (t1 * 14918087) % buckets

			def triGramHash(sequence, t, buckets):
				t1 = sequence[t - 1] if t - 1 >= 0 else 0
				t2 = sequence[t - 2] if t - 2 >= 0 else 0
				return (t2 * 14918087 * 18408749 + t1 * 14918087) % buckets
			
			buckets = config_y.n_gram_vocab
			bigram = []
			trigram = []
			# ------ngram------
			for i in range(pad_size_y):
				bigram.append(biGramHash(words_c, i, buckets))
				trigram.append(triGramHash(words_c, i, buckets))
			bigram = torch.LongTensor(bigram)
			trigram = torch.LongTensor(trigram)
			# print(bigram,trigram)
			sentence2 = np.array([int(x) for x in words_c[0:pad_size_y]])
			sentence2 = torch.from_numpy(sentence2)
			sentence2 = (sentence2.unsqueeze(0).type(torch.LongTensor),seq_len,bigram,trigram)
			print(sentence2)
			predict2 = model2(sentence2).detach().numpy()[0] #.cpu().detach().numpy()[0]
			print(predict2)
			score2 = max(predict2)
			label2 = np.where(predict2 == score2)[0][0]
			return json.dumps({"prediction" : label2,"message" : message_copy, "time_text" : str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))},cls=NpEncoder)
		if usemodel == 'TextCNN':
			if pad_size_x:
				if len(token) < pad_size_x:
					token.extend([PAD] * (pad_size_x - len(token)))
				else:
					token = token[:pad_size_x]
					seq_len = pad_size_x
				words = []
				for word in token:
					words.append(vocab.get(word, vocab.get(UNK)))
				# print([[int(x) for x in words[0:pad_size]]])
				sentence1 = np.array([int(x) for x in words[0:pad_size_x]])
				sentence1 = torch.from_numpy(sentence1)
				sentence1 = (sentence1.unsqueeze(0).type(torch.LongTensor),seq_len)
				predict1 = model1(sentence1).detach().numpy()[0] #.cpu().detach().numpy()[0]
				# print(predict1)
				score1 = max(predict1)
				label1 = np.where(predict1 == score1)[0][0]
			return json.dumps({"prediction" : label1,"message" : message_copy, "time_text" : str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))},cls=NpEncoder)
		if usemodel == 'ChatGPT':
			message = request.form['message']
			message_copy = message
			result = 0
			response = openai.ChatCompletion.create(
					model="gpt-3.5-turbo",
					messages =[
						{"role": "system", "content": "已知诈骗分为 冒充电商物流客服类，贷款、代办信用卡类，虚假网络投资理财类，冒充领导、熟人类，冒充公检法及政府机关类，网络游戏产品虚假交易类，刷单返利类，其他类型诈骗，虚假征信类，冒充军警购物类诈骗，虚假购物、服务类，网黑案件，网络婚恋、交友类（非虚假网络投资理财类）13个类别。判断以下文本是什么类型的诈骗并简单分析："},
						{"role": "user", "content": message_copy},
					])
			result = response.choices[0].message.content
			return json.dumps({"result" : result,"message" : message_copy,},cls=NpEncoder)

@app.route('/charts', methods=['GET', 'POST'])
def charts():
	return render_template('charts.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
	return render_template('start.html')
if __name__ == '__main__':
	app.run(debug=True)