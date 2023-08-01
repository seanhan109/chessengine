from neural_net import ChessNet, train
import os
import pickle
import numpy as np
import torch


def train_nn(net_to_train="i.tar",save_as="o.tar"):
    #gather data by playing oneself
    data_path = "./datasets/iter1/"
    datasets = []
    for idx,file in enumerate(os.listdir(data_path)):
        filename = os.path.join(data_path, file)
        with open(filename, 'rb') as fo:
            datasets.extend(pickle.load(fo,encoding='bytes'))


    data_path = "./datasets/iter0/"
    for idx, file in enumerate(os.listdir(data_path)):
        filename = os.path.join(data_path, file)
        with open(filename, 'rb') as fo:
            datasets.extend(pickle.load(fo,encoding='bytes'))

    datasets = np.array(datasets)

    #train the neural net

    net = ChessNet()
    cuda = torch.cuda.is_available()
    if cuda:
        net.cuda()
    current_net_filename = os.path.join("./model_data/", net_to_train)

    checkpoint = torch.load(current_net_filename)
    net.load_state_dict(checkpoint['state_dict'])
    train(net, datasets)
    
    torch.save({'state_dict': net.state_dict()}, os.path.join("./model_data/", save_as))


if __name__ == "__main__":
    train_nn()  