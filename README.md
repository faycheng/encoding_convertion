# encoding_convertion(编码转换)


---
encoding_convertion是一个简单的基于Python2.7文件编码转换脚本，支持将文件批量转换为指定的编码。

# 依赖
```
> pip install chardet 
```

# 使用
通过命令行执行脚本：

```
> python file_encoding_conversation.py -p aof* -t GB18030 -d
aof.c convert status:   success
```

# 参数说明
| 参数                      | 必选  |  说明  |
| --------                  | ----: | ----:  |
| -p/--pattern              | 是    |通过通配符指定需要更改编码的文件     |
| -o/--original             | 否    |手动指定文件的原始编码   |
| -t/--target               | 是    |指定文件需要变更的目标编码|
| -c/--case_sensitivity     | 否    |通配符匹配时是否大小写敏感 |
| -d/--detail               | 否    |是否显示脚本执行的运行细节  |







