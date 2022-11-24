## 代码加密

### 说明

`*.pyc` 是由 `*.py` 编译而成的二进制格式文件。

在`MircoPython`中 `*.py` 可编译为`*.mpy`文件，这与`*.pyc` 相似。

### 安装

pip install mpy-cross -i https://pypi.tuna.tsinghua.edu.cn/simple

### 加密

* 命令行：mpy-cross.exe *.py
* 拖拽：将 py 文件拖拽到 mpy-cross.exe 上

### 调用

![upload_and_run_mpy](image\upload_and_run_mpy.png)

### 报错

错误：ValueError: incompatible .mpy file

解决方法：保证自己的固件版本和工具版本相同。

![1.tool_vsersion](image\tool_vsersion.png)

