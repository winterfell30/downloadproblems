#用于爬取OJ题目并且以PDF格式保存在本地   
  
####需要安装Python3、需要下载的库有Beautifulsoup、requests、pdfkit

####库的安装方法
```pip install beatuifulsoup4```  
```pip install pdfkit```  
```pip install requests```  

####使用时可以根据需要修改题号和OJ名字，如果题号是乱序的根据需要把要下载的题号写成problemidlist 

####本来想弄成命令行形式的但是考虑到乱序list的话可能用起来还不如直接改代码方便，就没有弄    

####下载下来的题目路径为pwd/ojname/ojname-problemid.pdf   
  
####本来以为会是代码量比较大的工作，实际上很多工作VJ已经做完了(感谢VJ  
  
####UVA和其他OJ不同只需要直接找到源PDF文件下载即可，所以速度也更快   
  
####有一个bf版本和一个多线程版本，多线程版本使用生产者消费者模式，1个线程爬网址，maxdownloader个线程下载。  
  
####经测试在UVA和其他OJ上多线程版本都能快大约2-3倍，优化的瓶颈应该是网速。  
  
####~~本来想弄个每个线程的进度条的，urlretrieve可以用回调函数但是pdfkit不可以，为了协调统一使用sleep刷屏了~~  
