# 冰山押韵
## 国内首款支持二压以上的嘻哈押韵工具

[C++版本](https://github.com/lqj679ssn/StrongIceLib)

### 可视化界面
```https://hiphop.6-79.cn/```

### 通用接口
#### REQUEST
```GET https://hiphop.6-79.cn/match```

**参数列表**

```phrase``` 进行匹配的拼音串。拼音之间用空格隔开，拼音可以带声调也可以不带

```min_max_match``` 最小匹配长度。默认为0，表示单压、二压及以上所有押韵都返回。若为2，则只返回二压及以上匹配的词语。

```phrase_len``` 匹配的词语长度。默认为0，表示任意长度的词语都返回。若为2，则只返回双字词语。

**示例**

```GET https://hiphop.6-79.cn/match?phrase=xie4%20chun%20hua&min_max_match=2&phrase_len=0```

#### RESPONSE
```
{
  "code": 0,
  "msg": "ok",
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
