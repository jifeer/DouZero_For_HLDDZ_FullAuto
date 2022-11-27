"""
This file includes the torch models. We wrap the three
models into one class for convenience.
"""

import numpy as np

import torch
from torch import nn
import torch.nn.functional as F

class LandlordLstmModel(nn.Module):
    def __init__(self):
        super().__init__()
        """
        input_size 输入数据的特征维数，通常就是embedding_dim(词向量的维度)
        hidden_size　LSTM中隐层的维度
        num_layers　循环神经网络的层数
        bias　用不用偏置，default=True
        batch_first 这个要注意，通常我们输入的数据shape=(batch_size,seq_length,embedding_dim),而batch_first默认是False,
        所以我们的输入数据最好送进LSTM之前将batch_size与seq_length这两个维度调换
        dropout　默认是0，代表不用dropout
        bidirectional默认是false，代表不用双向LSTM
        """
        # 单向LSTm
        self.lstm = nn.LSTM(162, 128, batch_first=True)
        """
        nn.Linear（）是用于设置网络中的全连接层的，需要注意在二维图像处理的任务中，
        全连接层的输入与输出一般都设置为二维张量，形状通常为[batch_size, size]，不同于卷积层要求输入输出是四维张量
        in_features指的是输入的二维张量的大小，即输入的[batch_size, size]中的size。
        out_features指的是输出的二维张量的大小，即输出的二维张量的形状为[batch_size，output_size]，当然，它也代表了该全连接层的神经元个数。
        从输入输出的张量的shape角度来理解，相当于一个输入为[batch_size, in_features]的张量变换成了[batch_size, out_features]的输出张量。
        """
        self.dense1 = nn.Linear(373 + 128, 512)
        self.dense2 = nn.Linear(512, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None):
        lstm_out, (h_n, _) = self.lstm(z)
        # python  numpy 中的array, mat 取数据i:j:k 从下标i个开始到下标j-1结束，步长为k，(k为整数且不能等于0,缺省为1),","隔开依次二‘三’4等维度
        lstm_out = lstm_out[:, -1, :]
        # torch.cat() 和python中的内置函数cat()， 在使用和目的上，是没有区别的，区别在于前者操作对象是tensor。
        x = torch.cat([lstm_out, x], dim=-1)
        # print(x)
        x = self.dense1(x)
        # ReLU函数有个inplace参数，如果设为True，它会把输出直接覆盖到输入中，这样可以节省内存/显存, 小于0的，被置为0
        x = torch.relu(x)
        x = self.dense2(x)
        x = torch.relu(x)
        x = self.dense3(x)
        x = torch.relu(x)
        x = self.dense4(x)
        x = torch.relu(x)
        x = self.dense5(x)
        x = torch.relu(x)
        x = self.dense6(x)
        if return_value:
            action = dict(values=x)
            # print("return_value: ", action)
            return action
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
                '''
                print("flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon: ", action)
                '''
            else:
                action = torch.argmax(x,dim=0)[0]
                # print("else: ", action)
            return dict(action=action)

class FarmerLstmModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(162, 128, batch_first=True)
        self.dense1 = nn.Linear(484 + 128, 512)
        self.dense2 = nn.Linear(512, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None):
        lstm_out, (h_n, _) = self.lstm(z)
        lstm_out = lstm_out[:,-1,:]
        x = torch.cat([lstm_out,x], dim=-1)
        x = self.dense1(x)
        x = torch.relu(x)
        x = self.dense2(x)
        x = torch.relu(x)
        x = self.dense3(x)
        x = torch.relu(x)
        x = self.dense4(x)
        x = torch.relu(x)
        x = self.dense5(x)
        x = torch.relu(x)
        x = self.dense6(x)
        if return_value:
            return dict(values=x)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
            else:
                action = torch.argmax(x,dim=0)[0]
            return dict(action=action)

class LandlordLstmNewModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(162, 128, batch_first=True)
        self.dense1 = nn.Linear(373 + 128, 512)
        self.dense2 = nn.Linear(512, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None):
        lstm_out, (h_n, _) = self.lstm(z)
        lstm_out = lstm_out[:,-1,:]
        x = torch.cat([lstm_out,x], dim=-1)
        x = self.dense1(x)
        x = torch.relu(x)
        x = self.dense2(x)
        x = torch.relu(x)
        x = self.dense3(x)
        x = torch.relu(x)
        x = self.dense4(x)
        x = torch.relu(x)
        x = self.dense5(x)
        x = torch.relu(x)
        x = self.dense6(x)
        if return_value:
            return dict(values=x)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
            else:
                action = torch.argmax(x,dim=0)[0]
            return dict(action=action)

class FarmerLstmNewModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(162, 128, batch_first=True)
        self.dense1 = nn.Linear(484 + 128, 512)
        self.dense2 = nn.Linear(512, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None):
        lstm_out, (h_n, _) = self.lstm(z)
        lstm_out = lstm_out[:,-1,:]
        x = torch.cat([lstm_out,x], dim=-1)
        x = self.dense1(x)
        x = torch.relu(x)
        x = self.dense2(x)
        x = torch.relu(x)
        x = self.dense3(x)
        x = torch.relu(x)
        x = self.dense4(x)
        x = torch.relu(x)
        x = self.dense5(x)
        x = torch.relu(x)
        x = self.dense6(x)
        if return_value:
            return dict(values=x)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
            else:
                action = torch.argmax(x,dim=0)[0]
            return dict(action=action)

class GeneralModel(nn.Module):
    def __init__(self):
        super().__init__()
        # input: B * 32 * 57
        # self.lstm = nn.LSTM(162, 512, batch_first=True)
        self.conv_z_1 = torch.nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=(1,57)),  # B * 1 * 64 * 32
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(64),
        )
        # Squeeze(-1) B * 64 * 16
        self.conv_z_2 = torch.nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=(5,), padding=2),  # 128 * 16
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(128),
        )
        self.conv_z_3 = torch.nn.Sequential(
            nn.Conv1d(128, 256, kernel_size=(3,), padding=1), # 256 * 8
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(256),

        )
        self.conv_z_4 = torch.nn.Sequential(
            nn.Conv1d(256, 512, kernel_size=(3,), padding=1), # 512 * 4
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(512),

        )

        self.dense1 = nn.Linear(519 + 1024, 1024)
        self.dense2 = nn.Linear(1024, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None, debug=False):
        z = z.unsqueeze(1)
        z = self.conv_z_1(z)
        z = z.squeeze(-1)
        z = torch.max_pool1d(z, 2)
        z = self.conv_z_2(z)
        z = torch.max_pool1d(z, 2)
        z = self.conv_z_3(z)
        z = torch.max_pool1d(z, 2)
        z = self.conv_z_4(z)
        z = torch.max_pool1d(z, 2)
        z = z.flatten(1,2)
        x = torch.cat([z,x], dim=-1)
        x = self.dense1(x)
        x = torch.relu(x)
        x = self.dense2(x)
        x = torch.relu(x)
        x = self.dense3(x)
        x = torch.relu(x)
        x = self.dense4(x)
        x = torch.relu(x)
        x = self.dense5(x)
        x = torch.relu(x)
        x = self.dense6(x)
        if return_value:
            return dict(values=x)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
            else:
                action = torch.argmax(x,dim=0)[0]
            return dict(action=action, max_value=torch.max(x))


# 用于ResNet18和34的残差块，用的是2个3x3的卷积
class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv1d(in_planes, planes, kernel_size=(3,),
                               stride=(stride,), padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(planes)
        self.conv2 = nn.Conv1d(planes, planes, kernel_size=(3,),
                               stride=(1,), padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(planes)
        self.shortcut = nn.Sequential()
        # 经过处理后的x要与x的维度相同(尺寸和深度)
        # 如果不相同，需要添加卷积+BN来变换为同一维度
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_planes, self.expansion * planes,
                          kernel_size=(1,), stride=(stride,), bias=False),
                nn.BatchNorm1d(self.expansion * planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResnetModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.in_planes = 80
        #input 1*54*41
        self.conv1 = nn.Conv1d(40, 80, kernel_size=(3,),
                               stride=(2,), padding=1, bias=False) #1*27*80

        self.bn1 = nn.BatchNorm1d(80)

        self.layer1 = self._make_layer(BasicBlock, 80, 2, stride=2)#1*14*80
        self.layer2 = self._make_layer(BasicBlock, 160, 2, stride=2)#1*7*160
        self.layer3 = self._make_layer(BasicBlock, 320, 2, stride=2)#1*4*320
        # self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear1 = nn.Linear(320 * BasicBlock.expansion * 4 + 15 * 4, 1024)
        self.linear2 = nn.Linear(1024, 512)
        self.linear3 = nn.Linear(512, 256)
        self.linear4 = nn.Linear(256, 1)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, z, x, return_value=False, flags=None, debug=False):
        out = F.relu(self.bn1(self.conv1(z)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out.flatten(1,2)
        out = torch.cat([x,x,x,x,out], dim=-1)
        out = F.leaky_relu_(self.linear1(out))
        out = F.leaky_relu_(self.linear2(out))
        out = F.leaky_relu_(self.linear3(out))
        out = F.leaky_relu_(self.linear4(out))
        if return_value:
            return dict(values=out)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(out.shape[0], (1,))[0]
            else:
                action = torch.argmax(out,dim=0)[0]
            return dict(action=action, max_value=torch.max(out))


class BidModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.dense1 = nn.Linear(114, 512)
        self.dense2 = nn.Linear(512, 512)
        self.dense3 = nn.Linear(512, 512)
        self.dense4 = nn.Linear(512, 512)
        self.dense5 = nn.Linear(512, 512)
        self.dense6 = nn.Linear(512, 1)

    def forward(self, z, x, return_value=False, flags=None, debug=False):
        x = self.dense1(x)
        x = F.leaky_relu(x)
        # x = F.relu(x)
        x = self.dense2(x)
        x = F.leaky_relu(x)
        # x = F.relu(x)
        x = self.dense3(x)
        x = F.leaky_relu(x)
        # x = F.relu(x)
        x = self.dense4(x)
        x = F.leaky_relu(x)
        # x = F.relu(x)
        x = self.dense5(x)
        # x = F.relu(x)
        x = F.leaky_relu(x)
        x = self.dense6(x)
        if return_value:
            return dict(values=x)
        else:
            if flags is not None and flags.exp_epsilon > 0 and np.random.rand() < flags.exp_epsilon:
                action = torch.randint(x.shape[0], (1,))[0]
            else:
                action = torch.argmax(x,dim=0)[0]
            return dict(action=action, max_value=torch.max(x))

# Model dict is only used in evaluation but not training
model_dict = {}
model_dict['landlord'] = LandlordLstmModel
model_dict['landlord_up'] = FarmerLstmModel
model_dict['landlord_down'] = FarmerLstmModel
model_dict_resnet = {}
model_dict_resnet['landlord'] = ResnetModel
model_dict_resnet['landlord_up'] = ResnetModel
model_dict_resnet['landlord_down'] = ResnetModel
model_dict_resnet['bidding'] = BidModel
model_dict_general = {}
model_dict_general['landlord'] = GeneralModel
model_dict_general['landlord_up'] = GeneralModel
model_dict_general['landlord_down'] = GeneralModel
model_dict_general['bidding'] = BidModel


class General_Model:
    """
    The wrapper for the three models. We also wrap several
    interfaces such as share_memory, eval, etc.
    """
    def __init__(self, device=0):
        self.models = {}
        if not device == "cpu":
            device = 'cuda:' + str(device)
        # model = GeneralModel().to(torch.device(device))
        self.models['landlord'] = GeneralModel1().to(torch.device(device))
        self.models['landlord_up'] = GeneralModel1().to(torch.device(device))
        self.models['landlord_down'] = GeneralModel1().to(torch.device(device))
        self.models['bidding'] = BidModel().to(torch.device(device))

    def forward(self, position, z, x, training=False, flags=None, debug=False):
        model = self.models[position]
        return model.forward(z, x, training, flags, debug)

    def share_memory(self):
        self.models['landlord'].share_memory()
        self.models['landlord_up'].share_memory()
        self.models['landlord_down'].share_memory()
        self.models['bidding'].share_memory()

    def eval(self):
        self.models['landlord'].eval()
        self.models['landlord_up'].eval()
        self.models['landlord_down'].eval()
        self.models['bidding'].eval()

    def parameters(self, position):
        return self.models[position].parameters()

    def get_model(self, position):
        return self.models[position]

    def get_models(self):
        return self.models


class OldModel:
    """
    The wrapper for the three models. We also wrap several
    interfaces such as share_memory, eval, etc.
    """
    def __init__(self, device=0):
        self.models = {}
        if not device == "cpu":
            device = 'cuda:' + str(device)
        self.models['landlord'] = LandlordLstmModel().to(torch.device(device))
        self.models['landlord_up'] = FarmerLstmModel().to(torch.device(device))
        self.models['landlord_down'] = FarmerLstmModel().to(torch.device(device))

    def forward(self, position, z, x, training=False, flags=None):
        model = self.models[position]
        return model.forward(z, x, training, flags)

    def share_memory(self):
        self.models['landlord'].share_memory()
        self.models['landlord_up'].share_memory()
        self.models['landlord_down'].share_memory()

    def eval(self):
        self.models['landlord'].eval()
        self.models['landlord_up'].eval()
        self.models['landlord_down'].eval()

    def parameters(self, position):
        return self.models[position].parameters()

    def get_model(self, position):
        return self.models[position]

    def get_models(self):
        return self.models


class Model:
    """
    The wrapper for the three models. We also wrap several
    interfaces such as share_memory, eval, etc.
    """
    def __init__(self, device=0):
        self.models = {}
        if not device == "cpu":
            device = 'cuda:' + str(device)
        # model = GeneralModel().to(torch.device(device))
        self.models['landlord'] = ResnetModel().to(torch.device(device))
        self.models['landlord_up'] = ResnetModel().to(torch.device(device))
        self.models['landlord_down'] = ResnetModel().to(torch.device(device))
        self.models['bidding'] = BidModel().to(torch.device(device))

    def forward(self, position, z, x, training=False, flags=None, debug=False):
        model = self.models[position]
        return model.forward(z, x, training, flags, debug)

    def share_memory(self):
        self.models['landlord'].share_memory()
        self.models['landlord_up'].share_memory()
        self.models['landlord_down'].share_memory()
        self.models['bidding'].share_memory()

    def eval(self):
        self.models['landlord'].eval()
        self.models['landlord_up'].eval()
        self.models['landlord_down'].eval()
        self.models['bidding'].eval()

    def parameters(self, position):
        return self.models[position].parameters()

    def get_model(self, position):
        return self.models[position]

    def get_models(self):
        return self.models