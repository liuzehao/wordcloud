# wordcloud
python:从excel中提取高频词生成词云
@[toc]
## 1.需要的库

```
pip install pandas pkuseg numpy matplotlib PIL wordcloud
```
pkuseg是一个分词器：https://github.com/lancopku/pkuseg-python 
pandas,matplottlib,PIL 用来辅助作图，pandas中包含处理excel格式的函数
wordcloud 用来生成词云
numpy用来进行科学计算
## 2.代码逻辑

> 1.从excel表中读取所需要的文字
> 2.采用分词器进行分词操作
> 3.过滤一些没用的符号，单个词
> 4.统计词频
> 5.生成词云
## 3.分块功能说明
### 3.1统计词频

```python
def count_words(sp, n):
    w = {}
    for i in sp:
        if i not in w:
            w[i] = 1
        else:
            w[i] += 1
    top = sorted(w.items(), key=lambda item:(-item[1], item[0]))
    top_n = top[:n]
    return top_n
```
输入分词后的结果，list格式。n为返回词频率由高到低前n的词。

### 3.2过滤

```python
def filter_label(l):#过滤符号和单个词
    temp=[]
    for i in l:
        if len(i)!=1 and i.find('nbsp')<0:
            temp.append(i)
    return temp
```
这部分可以根据自己需要修改，我主要是过滤掉符号，‘我，的，得’这些无意义的词，还有‘nbsp’。
### 3.3生成词云
这个地方坑比较多。我列举一下：

> 1.根据词的频率生成词云，必须先做成字典格式
> 2.需要自己读入文字格式文件，和自己选一张背景图，生成的词云将根据背景图来创建，不要自作聪明自己创建一个空的二维数组哈。



```python
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
```

