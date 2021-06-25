# py_inc_file_tail
    脚本用途：
    监控递增文件日志并输出(根据文件名排序）
    需求背景：
    flume 采集某目录中的异常日志，日志文件名依据一定的规则（比如每天一个文件 2021-06-25.log）产生，对异常日志进行格式化输出（比如打标转换为json）；flume source计划采用exec方式，即常见的      exec+tail，但是tail -F或f只能对执行时已经存在的文件进行监控输出，无法监控新文件，基于此需求开发了该脚本。
     脚本说明：
     1.要监控的是这样的一类（符合正则表达式）文件：文件必须是写完后，新生成一个文件，类似递增式产生；
     2.脚本内容可根据需求场景自行修改使用
