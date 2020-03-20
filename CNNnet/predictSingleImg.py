from PIL import Image
from torchvision import transforms, models
from torch.autograd import Variable as V
import torch as t
import time


class CNN():
    def __init__(self, netName):
        self.netName = netName


    # 加载模型
    def loadModel(self):
        print("加载模型ing")
        if self.netName == 0:#vgg16网络
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

            self.__model.load_state_dict(t.load('E:/毕业设计/网络模型/vggnet/vggnet16.pkl'))
            print("vgg16加载模型完成")
        elif self.netName == 1:#resnet50网络
            self.__model = models.resnet50(pretrained=False)  # 导入网络模型
            self.__model.eval()
            # 对迁移模型进行调整
            for parma in self.__model.parameters():
                parma.requires_grad = False
            fc_inputs = self.__model.fc.in_features
            self.__model.fc = t.nn.Sequential(
                t.nn.Linear(fc_inputs, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 6))
            self.__model.load_state_dict(t.load('E:/毕业设计/网络模型/resnet/resnet50.pth'))
            print("resnet50加载模型完成")
        elif self.netName == 2:#inceptionV3网络
            self.__model = models.inception_v3(pretrained=False)   # 导入网络模型
            self.__model.eval()
            # 对迁移模型进行调整
            for parma in self.__model.parameters():
                parma.requires_grad = False

            # 不知道为什么
            self.__model.aux_logits = False
            fc_inputs = self.__model.AuxLogits.fc.in_features
            self.__model.AuxLogits.fc = t.nn.Sequential(
                t.nn.Linear(fc_inputs, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 6))

            fc_inputs = self.__model.fc.in_features
            self.__model.fc = t.nn.Sequential(
                t.nn.Linear(fc_inputs, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 4096),
                t.nn.ReLU(),
                t.nn.Dropout(p=0.5),
                t.nn.Linear(4096, 6))
            self.__model.load_state_dict(t.load('E:/毕业设计/网络模型/inception/inceptionNet.pth'))
            print("inceptionV3加载模型完成")
        return

    def predict(self, imgPath):
        if self.netName == 2:  # inceptionV3网络的输入必须是299,299
            trans = transforms.Compose([
                transforms.Resize([299, 299]),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
        else:
            trans = transforms.Compose([
                transforms.Resize([224, 224]),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
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
    cnn = CNN(2)
    cnn.loadModel()
    path = 'C:/Users/dell/Desktop/test/1.jpg'

    time_open = time.time()

    result = cnn.predict(path)
    print(result)

    # 输出模型训练、参数优化用时
    time_end = time.time() - time_open
    print(time_end)
