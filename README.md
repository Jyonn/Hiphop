# 冰山押韵
## 国内首款支持二押以上的嘻哈押韵工具

> 请注意，2025-07-04 的调整影响API默认返回值。之前可以通过 `code` 为 `0` 表示成功状态，现在 `code` 默认为 `200`，而成功状态由 `identifier` 为 `OK` 表示。

|    更新日期    |                                     说明                                     |
|:----------:|:--------------------------------------------------------------------------:|
| 2025-07-04 |                              适配 smartdjango4                               |
| 2021-06-29 |                               适配 smartdjango                               |
| 2018-11-14 |                                  添加词条筛查功能                                  |
| 2018-01-23 |                                 适配 Django2                                 |
| 2018-01-01 |                               升级词典，完善 README                               |
| 2017-10-19 | 移植[StrongIceLib](https://github.com/Jyonn/StrongIceLib) (C++)到本项目 (Python) |

[C++版本](https://github.com/lqj679ssn/StrongIceLib)

### 可视化界面
```https://hiphop.6-79.cn/```

### 通用接口
#### REQUEST
```GET https://hiphop.6-79.cn/match```

**参数列表**

```phrase``` 进行匹配的拼音串。拼音之间用空格隔开，拼音可以带声调也可以不带。

```min_max_match``` 最小匹配长度。默认为```0```，表示单押、二押及以上所有押韵都返回。若为```2```，则只返回二押及以上匹配的词语。

```phrase_len``` 匹配的词语长度。默认为```0```，表示任意长度的词语都返回。若为```2```，则只返回双字词语。

```cluster``` 押韵集群。默认为```NORMAL```，还可以是```STRICT```或自定义集群。

```cluster_type``` 押韵集群类型。默认为```DEFAULT```，此时cluster选择系统自带的集群方案（```NORMAL```/```STRICT```）。如果是```CUSTOMIZE```，cluster的值为自定义集群方案。

*更多关于押韵集群参数的信息见末尾。*

**示例**

```GET https://hiphop.6-79.cn/match?phrase=xie4%20chun%20hua&min_max_match=2&phrase_len=0&cluster=NORMAL&cluster_type=DEFAULT```

#### RESPONSE
```
{
  "code": 200,
  "identifier": "OK",
  "message": "OK",
  "user_message": "OK",
  "details": [],
  "body": {
    "3": [
      "说诨话"
    ],
    "2": [
      "伦巴",
      "两目昏花",
      "准假",
      "劳动基准法",
      ……
      "龙蛇混杂",
      "龙蛇浑杂"
    ]
  }
}
```

### 集群参数
系统首先把严格押韵的单字拼音进行分组（**GROUP**），并保存在```Init/group```文件中。

| GROUP ID | PINYIN                                                                                                                                                                                                                               |
|:--------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    0     | a ba ca cha chua da dia fa ga gua ha hua jia ka kua la lia ma na pa qia sa sha shua ta wa xia ya za zha zhua                                                                                                                         |
|    1     | ai bai cai chai chuai dai gai guai hai huai kai kuai lai mai nai pai sai shai shuai tai wai zai zhai zhuai                                                                                                                           |
|    2     | an ban bian can chan chuan cuan dan dian duan fan gan guan han huan jian juan kan kuan lan lian luan man mian nan nian nuan pan pian qian quan ran ruan san shan shuan suan tan tian tuan wan xian xuan yan yuan zan zhan zhuan zuan |
|    3     | ang bang cang chang chuang dang fang gang guang hang huang jiang kang kuang lang liang mang nang niang pang qiang rang sang shang shuang tang wang xiang yang zang zhang zhuang                                                      |
|    4     | ao bao biao cao chao dao diao gao hao jiao kao lao liao mao miao nao niao pao piao qiao rao sao shao tao tiao xiao yao zao zhao                                                                                                      |
|    5     | bei dei ei fei gei hei lei mei nei pei rui shei tei wei zei zhei                                                                                                                                                                     |
|    6     | ben cen chen den en fen gen hen ken men nen pen ren sen shen wen zen zhen                                                                                                                                                            |
|    7     | beng ceng cheng deng eng feng geng heng keng leng meng neng peng reng seng sheng teng weng zeng zheng                                                                                                                                |
|    8     | bi di ji ju li lv mi ni nv pi qi qu ti xi xu yi yu                                                                                                                                                                                   |
|    9     | bie die jie jue lie lue mie nie nue pie qie que tie xie xue ye yue                                                                                                                                                                   |
|    10    | bin jin jun lin min nin pin qin xin xun yin yun                                                                                                                                                                                      |
|    11    | bing ding jing ling ming ning ping qing ting xing ying                                                                                                                                                                               |
|    12    | bo chuo cuo duo fo guo huo kuo lo luo mo nuo o po ruo shuo suo tuo wo yo zhuo zuo                                                                                                                                                    |
|    13    | bu chu cu du fu gu hu ku lu mu nu pu ru shu su tu wu zhu zu                                                                                                                                                                          |
|    14    | ce che de e ge he ke le me ne re se she te ze zhe                                                                                                                                                                                    |
|    15    | chi ci ri shi si zhi zi                                                                                                                                                                                                              |
|    16    | chong cong dong gong hong jiong kong long nong qiong rong song tong xiong yong zhong zong                                                                                                                                            |
|    17    | chou cou dou fou gou hou kou lou mou nou ou pou rou shou sou tou zhou zou                                                                                                                                                            |
|    18    | chui cui dui gui hui kui shui sui tui zhui zui                                                                                                                                                                                       |
|    19    | chun cun dun gun hun kun lun qun run shun sun tun zhun zun                                                                                                                                                                           |
|    20    | diu jiu liu miu niu qiu xiu you                                                                                                                                                                                                      |
|    21    | er                                                                                                                                                                                                                                   |

**在同一GROUP下的拼音一定相互押韵。**
为了有更高的灵活性，系统在**GROUP**之上用**CLUSTER**集群封装。

在STRICT模式下，每个GROUP是单独的CLUSTER。定义如下：

```
[CLUSTER-STRICT]
0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21
```

不同CLUSTER用分号（;）隔开，一个CLUSTER内如果有多个GROUP，则用逗号（,）隔开。中间无空格等其他字符。

又如NORMAL模式的定义如下：

```
[CLUSTER-NORMAL]
0;1,21;2;3;4;5,18;6,7;8;9;10,11;12;13;14;15;7,16;17,20;19
```

对照GROUP表格可以得出，NORMAL模式把第6，7两组划为一个集群，也就是说**ben**和**beng**为同韵。CLUSTER的划分不是**组唯一**的，如第7组和第6组在一个CLUSTER，也和第16组（**beng**和**chong**同韵）在一个CLUSTER，但第6组和第16组并不同韵。

在```GET /match```接口中，若cluster_type为```CUSTOMIZE```，用户可按如上格式自定义集群（无需```[CLUSTER-xxx]```，只需第二行），并把值通过```cluster```参数传入。