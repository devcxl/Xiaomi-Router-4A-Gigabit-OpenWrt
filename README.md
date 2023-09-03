# 小米路由器 4a 千兆版刷 OpenWRT

> 须知：本方案仅支持小米路由器 4a 千兆版 v1 版，即固件版本为`2.28.x`的小米路由器 4a 千兆版路由器

## 刷机思路

根据小米路由器 4a 千兆版 2.28.62 版本固件中的配置备份/恢复漏洞获取 RootShell，在 RootShell 中刷入 OpenWRT

## 工具准备

- 网线一条
- linux 电脑一台

  > 本文以 manjaro 系统为例

## 环境准备

1. 安装 Git

   `pacman -Sy git`

2. 安装 Python3

   `pacman -Sy python3`

3. 克隆项目代码

   `git clone https://github.com/devcxl/R4AG-OpenWRT.git`

4. 进入 R4AG-OpenWRT 目录创建 Python venv 环境

   `cd R4AG-OpenWRT && python3 -m venv .env && source .env/bin/activate`

5. 安装依赖

   `pip3 install -r requirements.txt`

## 固件降级

在小米 wifi 后台手动更改固件为项目目录中的

`firmwares/miwifi_r4a_firmware_72d65_2.28.62.bin`固件

## 开始刷机

1. 启动新终端启动本地 http 服务器

   `uvicorn main:app --host 0.0.0.0 --port 8000`

2. 获取本机内网 IP

   `ifconfig`

   > 以`192.168.31.123`为例

3. 修改`files`文件夹中的 `script.sh` 和 `speedtest_urls.xml`将文件中的 ip 替换为本机内网 IP

   `sed -i 's/192.168.31.123:8000/192.168.31.115:8000/g' files/script.sh`

   `sed -i 's/192.168.31.123:8000/192.168.31.115:8000/g' files/speedtest_urls.xml`

4. 登陆路由器后台获取`stok`

   > 地址栏中的链接示例 `stok`为`6cb7bf8731d8ffcd4e0d71d752178a0e`

   `http://miwifi.com/cgi-bin/luci/;stok=6cb7bf8731d8ffcd4e0d71d752178a0e/`

5. 修改`run.py`脚本中的`stok`值为当前`stok`

6. 运行`run.py`

   `python3 run.py`

7. 当执行`uvicorn main:app --host 0.0.0.0 --port 8000`的终端出现以下内容时，RootShell 获取成功

   ```
   INFO:     192.168.31.1:42678 - "GET /ping HTTP/1.1" 200 OK
   INFO:     192.168.31.1:34062 - "GET /files/busybox-mipsel HTTP/1.1" 200 OK
   INFO:     192.168.31.1:44882 - "GET /files/dropbearStaticMipsel.tar.bz2 HTTP/1.1" 200 OK
   ```

8. 此时可以使用`telnet`命令连接路由器

   `telnet 192.168.31.1`

   - 账号 `root`
   - 密码 `root`

9. 下载OpenWRT镜像

    `cd /tmp && curl -L http://192.168.31.123:8000/files/openwrt-22.03.5-ramips-mt7621-xiaomi_mi-router-4a-gigabit-squashfs-sysupgrade.bin --output firmware.bin`

10. 刷入镜像

    `mtd -e OS1 -r write firmware.bin OS1`

11. 等待路由器重启后，使用网线连接路由器

    - 使用OpenSSH连接`192.168.1.1`
        
        `ssh root@192.168.1.1`

    - ssh连接成功即OpenWRT刷入成功

## OpenWRT配置

1. 更换软件镜像源

    - `sed -i 's/downloads.openwrt.org/mirrors.ustc.edu.cn\/openwrt/g' /etc/opkg/distfeeds.conf`
    - `opkg update`

2. 安装汉化/美化主题

    - `opkg install luci-i18n-base-zh-cn luci-theme-material`

3. 开启wifi

    - todo

4. 安装wireguard组网

    - todo

## 参考文档

- https://github.com/acecilia/OpenWRTInvasion
- https://mirrors.ustc.edu.cn/help/openwrt.html
