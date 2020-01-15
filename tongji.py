import pandas as pd 
import pkuseg
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageSequence
from wordcloud import WordCloud,ImageColorGenerator
def count_words(sp, n):
    w = {}
    # sp = s.split()
    # print(sp)
    # TODO:     `q  Count the number of occurences of each word in s
    for i in sp:
        if i not in w:
            w[i] = 1
        else:
            w[i] += 1
    # TODO: Sort the occurences in descending order (alphabetically in case of ties)
    top = sorted(w.items(), key=lambda item:(-item[1], item[0]))
    top_n = top[:n]
    # TODO: Return the top n most frequent words.
    return top_n
def filter_label(l):#过滤符号和单个词
    temp=[]
    for i in l:
        if len(i)!=1 and i.find('nbsp')<0:
            temp.append(i)
    return temp
def DrawWordcloud(read_name):#生成词云
    image = Image.open('back.jpg')#作为背景形状的图
    graph = np.array(image)
    #参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    wc = WordCloud(font_path = 'simsun.ttc', background_color = 'White', max_words = 50, mask = graph)


    # fp = pd.read_csv(read_name)#读取词频文件
    # name = list(fp.name)#词
    # value = fp.val#词的频率
    name=[]
    value=[]
    for t in read_name:
        name.append(t[0])
        value.append(t[1])
    for i in range(len(name)):
      name[i] = str(name[i])
    #   print(name[i])
      #注意因为要显示中文，所以需要转码
      name[i] = name[i].encode('gb2312').decode('gb2312')
    dic = dict(zip(name, value))#词频以字典形式存储
    print(dic)

    wc.generate_from_frequencies(dic)#根据给定词频生成词云
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off")#不显示坐标轴
    plt.show()
    wc.to_file('Wordcloud.png')#保存的图片命名为Wordcloud.png
#1.读入excel
df=pd.read_excel('2019all.xlsx')#这个会直接默认读取到这个Excel的第一个表单
data=df.ix[:,['反映内容']].values#0表示第一行 这里读取数据并不包含表头，要注意哦！
#2.分词
seg = pkuseg.pkuseg()           # 以默认配置加载模型

texts=[]
for t in range(len(data)):
    ###去重
    if t+1!=len(data):
        if len(data[t][0])==len(data[t+1][0]):
            continue
    text = seg.cut(str(data[t][0])) # 进行分词
    #3.过滤分词
    text=filter_label(text)
    # print(text)
    texts.extend(text)
#4.统计
# print(texts)
top_n=count_words(texts,500)
DrawWordcloud(top_n)