# from torchvision import transforms, utils, models
# import torch
# import matplotlib.pyplot as plt
# from torchvision.datasets import ImageFolder
# import os
# import time
# from torch.autograd import Variable
# import PIL
#
# def predict(img_path):
#     # 下载已经具备最优参数的VGG16模型
#     model = models.vgg16(pretrained=False)
#
#     # 对迁移模型进行调整
#     for parma in model.parameters():
#         parma.requires_grad = False
#
#     model.classifier = torch.nn.Sequential(torch.nn.Linear(25088, 4096),
#                                            torch.nn.ReLU(),
#                                            torch.nn.Dropout(p=0.5),
#                                            torch.nn.Linear(4096, 4096),
#                                            torch.nn.ReLU(),
#                                            torch.nn.Dropout(p=0.5),
#                                            torch.nn.Linear(4096, 6))
#
#     model.load_state_dict(torch.load('E:/毕业设计/vgg模型/medical_parameter.pkl'))
#
#     net = model.cuda()
#     torch.no_grad()
#     img = PIL.Image.open(img_path)
#     img_ = transforms(img).Compose([
#     transforms.Resize([224, 224]),
#     transforms.RandomHorizontalFlip(),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#     ])
#     img_ = img_.cuda()
#     outputs = net(img_)
#     _, predicted = torch.max(outputs,1)
#     print(predicted)
#
# if __name__=='main':
#     predict('C:/Users/dell/Desktop/test/u=2186653416,2144921991&fm=26&gp=0.jpg')


from PIL import Image
from torchvision import transforms, models
from torch.autograd import Variable as V
import torch as t
import time


class CNN():
    # 加载模型
    def loadModel(self):
        print("加载模型ing")
        self.__model = models.vgg16(pretrained=False)  # 导入网络模型
        self.__model.eval()
        # 对迁移模型进行调整
        for parma in self.__model.parameters():
            parma.requires_grad = False

        self.__model.classifier = t.nn.Sequential(t.nn.Linear(25088, 4096),
                                           t.nn.ReLU(),
                                           t.nn.Dropout(p=0.5),
                                           t.nn.Linear(4096, 4096),
                                           t.nn.ReLU(),
                                           t.nn.Dropout(p=0.5),
                                           t.nn.Linear(4096, 6))

        self.__model.load_state_dict(t.load('E:/毕业设计/vgg模型/medical_parameter.pkl'))
        print("加载模型完成")
        return

    def predict(self, imgPath):
        trans = transforms.Compose([
            transforms.Resize([224, 224]),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # 读入图片
        img = Image.open(imgPath)
        img = trans(img)  # 这里经过转换后输出的input格式是[C,H,W],网络输入还需要增加一维批量大小B
        img = img.unsqueeze(0)  # 增加一维，输出的img格式为[1,C,H,W]

        # 判断计算机的GPUs是否可用
        Use_gpu = t.cuda.is_available()
        if Use_gpu:
            self.__model = self.__model.cuda()

        input = V(img.cuda())
        score = self.__model(input)  # 将图片输入网络得到输出
        probability = t.nn.functional.softmax(score, dim=1)  # 计算softmax，即该图片属于各类的概率
        max_value, index = t.max(probability, 1)  # 找到最大概率对应的索引号，该图片即为该索引号对应的类别
        print(index)
        resultClassNumber = str(index)[8]
        lsitName = ['决明子', '天花粉', '枳实', '苍术', '苍耳子', '黄连']
        return lsitName[int(resultClassNumber)]

if __name__ == '__main__':
    cnn = CNN()
    cnn.loadModel()
    path = 'C:/Users/dell/Desktop/test/1.jpg'

    time_open = time.time()

    result = cnn.predict(path)
    print(result)

    # 输出模型训练、参数优化用时
    time_end = time.time() - time_open
    print(time_end)
