import torch
import os
import torch.nn as nn
import numpy as np
import time
import matplotlib.pyplot as plt

from model import textCNN
import sen2inds
import textCNN_data

word2ind, ind2word = sen2inds.get_worddict('data/wordLabel.txt')
label_w2n, label_n2w = sen2inds.read_labelFile('data/label.txt')

textCNN_param = {
    'vocab_size': len(word2ind),
    'embed_dim': 60,
    'class_num': len(label_w2n),
    "kernel_num": 16,
    "kernel_size": [3, 4, 5],
    "dropout": 0.5,
}
dataLoader_param = {
    'batch_size': 60,
    'shuffle': True,
}


def main():
    #init net
    print('init net...')
    net = textCNN(textCNN_param)
    weightFile = 'weight.pkl'
    if os.path.exists(weightFile):
        print('load weight')
        net.load_state_dict(torch.load(weightFile))
    else:
        net.init_weight()
    print(net)

    # net.cuda()

    #init dataset
    print('init dataset...')
    dataLoader = textCNN_data.textCNN_dataLoader(dataLoader_param)
    valdata = textCNN_data.get_valdata()

    # 定义代价函数和优化器
    optimizer = torch.optim.Adam(net.parameters(), lr=0.01)
    # scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.1,last_epoch=-1)
    # scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30, eta_min=0.01)

    criterion = nn.NLLLoss()
    
    log = open('log_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    log.write('epoch step loss\n')
    log_test = open('log_test_{}.txt'.format(time.strftime('%y%m%d%H')), 'w')
    log_test.write('epoch step test_acc\n')
    print("training...")
    EPOCHS = 100
    x = list(range(EPOCHS))
    y = []
    for epoch in range(EPOCHS):
        for i, (clas, sentences) in enumerate(dataLoader):
            optimizer.zero_grad()
            sentences = sentences.type(torch.LongTensor)    # .cuda()
            clas = clas.type(torch.LongTensor)  # .cuda()
            out = net(sentences)
            loss = criterion(out, clas)
            loss.backward()
            optimizer.step()

            if (i + 1) % 1 == 0:
                print("epoch:", epoch + 1, "step:", i + 1, "loss:", loss.item())
                data = str(epoch + 1) + ' ' + str(i + 1) + ' ' + str(loss.item()) + '\n'
                log.write(data)
        # y.append(scheduler.get_last_lr()[0])
        # scheduler.step()
        print("save model...")
        torch.save(net.state_dict(), weightFile)
        torch.save(net.state_dict(), "model\{}_model_iter_{}_{}_loss_{:.2f}.pkl".format(time.strftime('%y%m%d%H'), epoch, i, loss.item()))  # current is model.pkl
        print("epoch:", epoch + 1, "step:", i + 1, "loss:", loss.item())      
    # plt.figure()
    # plt.plot(x,y)
    # plt.xlabel("epoch")
    # plt.ylabel("lr")
    # plt.title("lr-epoch")
    # plt.show()

if __name__ == "__main__":
    main()