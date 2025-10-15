NOC-SIM:一款noc学习仿真器

主要功能：<br>
NOC-SIM基于booksim2,支持base与test两种noc配置进行对比，分析noc的参数对传输效率影响。

目录结构：<br>
booksim2文件夹：booksim2仿真器文件夹。<br>
config文件夹：base为基准noc配置，test为优化后的noc配置。<br>
output文件夹：保存booksim2的全部log以及从中提取到的warmclk，totalclk信息。<br>
python文件夹: 保存主要代码。<br>

如何使用：<br>
1、根据booksim2教程修改需要的base与test配置。<br>
2、在NOC-SIM目录下，使用 “python3 python/test.py”。<br>
3、分析运行结果。<br>
