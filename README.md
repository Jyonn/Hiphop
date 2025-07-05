## 更新日志

> ⚠️ 注意：自 **2025-07-04** 起，API 的默认返回字段已调整。  
> 原先通过 `code = 0` 表示成功，现在统一返回 `code = 200`，以 `identifier = "OK"` 表示成功状态。

|    更新日期    |                                      说明                                      |
|:----------:|:----------------------------------------------------------------------------:|
| 2025-07-04 |                             兼容 `smartdjango4` 框架                             |
| 2021-06-29 |                               兼容 `smartdjango`                               |
| 2018-11-14 |                                   新增词条筛查功能                                   |
| 2018-01-23 |                                 兼容 Django 2                                  |
| 2018-01-01 |                               升级押韵词典并完善 README                               |
| 2017-10-19 | 将 [StrongIceLib](https://github.com/Jyonn/StrongIceLib)（C++ 实现）移植为 Python 版本 |

👉 C++ 版本请见：[StrongIceLib](https://github.com/lqj679ssn/StrongIceLib)

---

## 可视化界面

访问地址：[https://hiphop.6-79.cn/](https://hiphop.6-79.cn/)

---

## 通用接口说明

### 接口地址

```GET https://hiphop.6-79.cn/match```

### 请求参数

| 参数名           | 说明                                                                                   | 默认值     |
|------------------|------------------------------------------------------------------------------------------|------------|
| `phrase`         | 待匹配的拼音串，拼音间用空格隔开。支持带声调或不带声调。                                 | （必填）   |
| `min_max_match`  | 最小押韵长度。设为 `0` 表示返回所有匹配（含单押、双押等）；设为 `2` 表示返回二押及以上匹配 | `0`        |
| `phrase_len`     | 匹配词语长度。设为 `0` 表示不限制长度，设为 `2` 表示仅返回双字词                           | `0`        |
| `cluster`        | 押韵集群名。可选 `NORMAL`、`STRICT` 或自定义集群格式                                      | `NORMAL`   |
| `cluster_type`   | 集群类型，`DEFAULT` 表示使用内置集群，`CUSTOMIZE` 表示自定义集群                         | `DEFAULT`  |

📌 更多关于押韵集群参数的信息，请见文末说明。

### 请求示例

```GET https://hiphop.6-79.cn/match?phrase=xie4%20chun%20hua&min_max_match=2&phrase_len=0&cluster=NORMAL&cluster_type=DEFAULT```

### 返回示例

```json
{
  "code": 200,
  "identifier": "OK",
  "message": "OK",
  "user_message": "OK",
  "details": [],
  "body": {
    "3": ["说诨话"],
    "2": [
      "伦巴",
      "两目昏花",
      "准假",
      "劳动基准法",
      "龙蛇混杂",
      "龙蛇浑杂"
    ]
  }
}
```

---

## 押韵集群参数说明

系统将相互押韵的拼音音节先划分为分组，分组信息保存在 `Init/group` 文件中：

| 分组ID | 包含拼音                                                                                                                                                                                                                                 |
|:----:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  0   | a ba ca cha chua da dia fa ga gua ha hua jia ka kua la lia ma na pa qia sa sha shua ta wa xia ya za zha zhua                                                                                                                         |
|  1   | ai bai cai chai chuai dai gai guai hai huai kai kuai lai mai nai pai sai shai shuai tai wai zai zhai zhuai                                                                                                                           |
|  2   | an ban bian can chan chuan cuan dan dian duan fan gan guan han huan jian juan kan kuan lan lian luan man mian nan nian nuan pan pian qian quan ran ruan san shan shuan suan tan tian tuan wan xian xuan yan yuan zan zhan zhuan zuan |
|  3   | ang bang cang chang chuang dang fang gang guang hang huang jiang kang kuang lang liang mang nang niang pang qiang rang sang shang shuang tang wang xiang yang zang zhang zhuang                                                      |
|  4   | ao bao biao cao chao dao diao gao hao jiao kao lao liao mao miao nao niao pao piao qiao rao sao shao tao tiao xiao yao zao zhao                                                                                                      |
|  5   | bei dei ei fei gei hei lei mei nei pei rui shei tei wei zei zhei                                                                                                                                                                     |
|  6   | ben cen chen den en fen gen hen ken men nen pen ren sen shen wen zen zhen                                                                                                                                                            |
|  7   | beng ceng cheng deng eng feng geng heng keng leng meng neng peng reng seng sheng teng weng zeng zheng                                                                                                                                |
|  8   | bi di ji ju li lv mi ni nv pi qi qu ti xi xu yi yu                                                                                                                                                                                   |
|  9   | bie die jie jue lie lue mie nie nue pie qie que tie xie xue ye yue                                                                                                                                                                   |
|  10  | bin jin jun lin min nin pin qin xin xun yin yun                                                                                                                                                                                      |
|  11  | bing ding jing ling ming ning ping qing ting xing ying                                                                                                                                                                               |
|  12  | bo chuo cuo duo fo guo huo kuo lo luo mo nuo o po ruo shuo suo tuo wo yo zhuo zuo                                                                                                                                                    |
|  13  | bu chu cu du fu gu hu ku lu mu nu pu ru shu su tu wu zhu zu                                                                                                                                                                          |
|  14  | ce che de e ge he ke le me ne re se she te ze zhe                                                                                                                                                                                    |
|  15  | chi ci ri shi si zhi zi                                                                                                                                                                                                              |
|  16  | chong cong dong gong hong jiong kong long nong qiong rong song tong xiong yong zhong zong                                                                                                                                            |
|  17  | chou cou dou fou gou hou kou lou mou nou ou pou rou shou sou tou zhou zou                                                                                                                                                            |
|  18  | chui cui dui gui hui kui shui sui tui zhui zui                                                                                                                                                                                       |
|  19  | chun cun dun gun hun kun lun qun run shun sun tun zhun zun                                                                                                                                                                           |
|  20  | diu jiu liu miu niu qiu xiu you                                                                                                                                                                                                      |
|  21  | er                                                                                                                                                                                                                                   |

✅ 同一分组中的拼音视为严格押韵

为了增强灵活性，系统将多个分组再封装为`集群（Cluster）`，并可定义为以下模式：

### 严格模式 STRICT 示例

```text
[CLUSTER-STRICT]
0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21
```

每个分组为一个独立的押韵集群。

### 普通模式 NORMAL 示例

```text
[CLUSTER-NORMAL]
0;1,21;2;3;4;5,18;6,7;8;9;10,11;12;13;14;15;7,16;17,20;19
```

示例说明：
- 第 6 和 7 组被划入一个集群，因此 ben 和 beng 视为同韵；
- 第 7 组还与第 16 组组成另一个集群，即 beng 和 chong 也同韵；
- 但第 6 和第 16 组并不直接同韵。

### 自定义集群

当 `cluster_type` 设为 `CUSTOMIZE` 时，用户可传入自定义集群字符串（无需 `[CLUSTER-xxx]` 标签），格式如下：

```text
0;1,21;2;3;...（分号分隔集群，逗号分隔每个集群的分组）
```

并通过 cluster 参数传入即可。
