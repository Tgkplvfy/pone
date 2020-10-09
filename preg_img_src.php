<?php
//网上找了好几个，都是只能获取最后一个src，这个可以获取所有img中的src。循环可输出。

$str = '<img width="100" src="1.gif" height="100"><br><img width="100" src="2.gif" height="100"><img width="100" src="4.gif" height="100">';
preg_match_all('/<img.*?src="(.*?)".*?>/is',$str,$array);
print_r($array);

/**
 * 输出
  Array
(
    [0] => Array
        (
            [0] => <img width="100" src="1.gif" height="100">
            [1] => <img width="100" src="2.gif" height="100">
            [2] => <img width="100" src="4.gif" height="100">
        )

    [1] => Array
        (
            [0] => 1.gif
            [1] => 2.gif
            [2] => 4.gif
        )

)
 */