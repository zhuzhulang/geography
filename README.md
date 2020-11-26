# geography
根据ip获取地理位置及经纬度

#### 获取IP对应的地址位置
https://github.com/out0fmemory/qqwry.dat
https://github.com/animalize/qqwry-python3
https://github.com/metowolf/qqwry.ipdb

#### 获取经纬度坐标
https://github.com/nuccch/city-geo

#### 地址位置获取经纬度

http://weixintest.carsone.net.cn/

#### 相应API

http://ip-api.com/json/{IP}

#### 代码

```
>>> from qqwry import QQwry
>>> q = QQwry()
>>> q.load_file("qqwry.dat")
>>> q.lookup("193.112.115.94")
('广东省广州市', '腾讯云')
```
