#### ShareLaTex Templates
**These LaTex templates were from [sharelatex.com](https://www.sharelatex.com), organized by their category/template name including .zip file and preview image.**   
*[download.py](./download.py)* shows how to download templates. Unzip, and then compile.   
Download link will be updated soon!   
**Enjoying your work!**

#### How to start your own sharelatex
* Install docker    
  see [docker-install](https://github.com/docker/docker-install).
* Download sharelatex offical image 
```shell
docker pull sharelatex/sharelatex
```
* Install docker-compose    
  see [docker-compose-release](https://github.com/docker/compose/releases), do as below:
```shell
curl -L https://github.com/docker/compose/releases/download/1.17.0-rc1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

* docker-compose    
  download [docker-compose.yml](https://github.com/sharelatex/sharelatex/blob/master/docker-compose.yml) 
```
sudo docker-compose up
```

* To support Chinese
```
# install package
docker exec -it your_sharelatex_container_id /bin/bash
tlmgr update --self
tlmgr option repository http://mirrors.aliyun.com/CTAN/systems/texlive/tlnet/
tlmgr install scheme-full
# install Chinese fonts
# copy your personal windows computer's fonts folder.
# C:\\...\\Fonts, copy to /usr/share/fonts/. for example:
unzip winfonts.zip
sudo mv winfonts /usr/share/fonts/
cd /usr/share/fonts/winfonts
mkfontscale
mkfontdir
fc-cache -fv 
# below will show the Chinese fonts:
fc-list :lang=zh-cn 
```
```docker restart your container``` 

Now waiting for downloading completed.

* Enjoy yourself, all completed please visiting `http://server_ip/`

本来是写给女票的，现在给更需要的人吧!
  ​
