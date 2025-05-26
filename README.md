### 0. 项目介绍
个人笔记系统

### 1. 环境安装

```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pyyaml xlwt xlrd opencv-python tqdm pillow cython nuitka gunicorn pytest --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host mirrors.tuna.tsinghua.edu.cn
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pyyaml xlwt xlrd opencv-python tqdm pillow cython nuitka gunicorn pytest --index-url https://mirrors.ustc.edu.cn/pypi/simple/ --trusted-host mirrors.ustc.edu.cn
conda install libpython-static
sudo apt install patchelf
sudo apt install p7zip-full
```

### 2. 后端接口

| 接口序号 | 分类序号 | 分类 | 接口内容 | 接口 url |
| ------ | ------ | ------ | ------ | ------ |
| 1 | 1 | 分类 | 新增分类 | /api/category/add |
| 2 | 2 | 分类 | 修改分类 | /api/category/modify |
| 3 | 3 | 分类 | 删除分类 | /api/category/del |
| 4 | 4 | 分类 | 查询分类 | /api/category |
| 5 | 1 | 笔记 | 新增笔记 | /api/note/add |
| 6 | 2| 笔记 | 新增图片/视频 | /api/file/upload/start /api/file/upload/chunk |
| 7 | 3 | 笔记 | 修改笔记 | /api/note/modify |
| 8 | 4 | 笔记 | 删除笔记 | /api/note/del |
| 9 | 5 | 笔记 | 查询笔记 | /api/note |
| 10 | 1 | 评论 | 新增评论 | /api/comment/add |
| 11 | 2 | 评论 | 回复评论 | /api/comment/add |
| 12 | 3 | 评论 | 删除评论 | /api/comment/del |
| 13 | 4 | 评论 | 查询笔记下评论 | /api/comment |
| 14 | 1 | 标签 | 新增标签 | /api/tag/add |
| 15 | 2 | 标签 | 修改标签 | /api/tag/modify |
| 16 | 3 | 标签 | 删除标签 | /api/tag/del |
| 17 | 1 | 关于我 | 新增一条关于我 | /api/about_me/add |
| 18 | 2 | 关于我 | 修改一条关于我 | /api/about_me/modify |
| 19 | 3 | 关于我 | 删除一条关于我 | /api/about_me/del |
| 20 | 4 | 关于我 | 查询关于我 | /api/about_me |
| 21 | 1 | 友链 | 新增友链 | /api/friend_link/add |
| 22 | 2 | 友链 | 修改友链 | /api/friend_link/modify |
| 23 | 3 | 友链 | 删除友链 | /api/friend_link/del |
| 24 | 4 | 友链 | 查询友链 | /api/friend_link |
| 25 | 1 | 访问者位置 | 获取总访问量、覆盖国家数、覆盖城市 | /api/visit_location/sum |
| 26 | 2 | 访问者位置 | 日访客分布 | /api/visit_location/day |

* 删除的笔记、图片、视频存放在删除文件夹
* 极简为第一原则
* 默认不引入数据库，存储即可见
* 博客前端和后端保持一套页面
* 提供纯静态访问方式

创建一个在线版笔记维护和展示网站，需求如下：
1,在展示页面不显示维护入口，通过url进入笔记维护页面；
2,需要支持markdown语法渲染，支持上传图片、视频，在笔记中嵌入图片、视频等静态文件；
3,后台存储笔记markdown格式原始文件;
4,需要记录每次请求相关信息，并根据请求客户端IP计算其位置，以热力图形式在全球地图上展示。
参考站点https://yhw-miracle.github.io/#/

### 3. 数据表

```python
>>> import hashlib
>>> len(hashlib.sha3_512("demo".encode("utf-8")).hexdigest())
128
>>> hashlib.sha3_512("demo".encode("utf-8")).hexdigest()
'a9210a3b1268ce3f2d9b5357dc79c1a4902cb5c5d7244589990263f1bac3d2678854031cc70444921fc6fb11ff9568dabc41a48b6bf3b808e84be58c0df4a881'
```

```python
>>> from datetime import datetime
>>> datetime.now().timestamp()
1746583780.359274
>>> datetime.fromtimestamp(datetime.now().timestamp()).strftime("%Y%m%d%H%M%S%f")
'20250507100945307658'
```

* 分类表 category

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| category_id | varchar(128) | 否 | NULL | 分类id | 主键 |
| name | varchar(256) | 否 | NULL | 分类名称 | 唯一 |
| description | varchar(256) | 否 | NULL | 分类描述 | |
| create_time | float | 否 | NULL | 创建时间 | |
| update_time | float | 是 | NULL | 修改时间 | |

* 笔记表 note

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| note_id | varcar(128) | 否 | NULL | 笔记id | 主键 |
| title | varchar(256) | 否 | NULL | 笔记标题 | |
| path | varchar(256) | 否 | NULL | 笔记路径 | 唯一 |
| category_id | varchar(128) | 否 | NULL | 分类id | 外键，关联分类表 |
| create_time | float | 否 | NULL | 创建时间 | |
| update_time | float | 是 | NULL | 修改时间 | |

* 图片表 image

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| image_id | varchar(128) | 否 | NULL | 图片id | 主键 |
| name | varchar(256) | 否 | NULL | 图片名 | |
| path | varchar(256) | 否 | NULL | 图片路径 | 唯一 |
| note_id | varchar(128) | 否 | NULL | 关联笔记 | 外键 |
| create_time | float | 否 | NULL | 创建时间 | |

* 视频表 video

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| video_id | varchar(128) | 否 | NULL | 视频id | 主键 |
| name | varchar(256) | 否 | NULL | 视频名 | |
| path | varchar(256) | 否 | NULL | 视频路径 | 唯一 |
| note_id | varchar(128) | 否 | NULL | 关联笔记 | 外键 |
| create_time | float | 否 | NULL | 创建时间 | |

* 用户表 user

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| user_id | varchar(128) | 否 | NULL | 用户id | 主键 |
| username | varchar(256) | 否 | NULL | 用户名 | 唯一 |
| email | varchar(256) | 否 | NULL | 邮箱 | 唯一 |
| create_time | float | 否 | NULL | 创建时间 | |

* 评论表 comment

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| comment_id | varchar(128) | 否 | NULL | 评论id | 主键 |
| content | text | 否 | NULL | 评论内容 | 唯一 |
| note_id | varchar(128) | 否 | NULL | 笔记id | |
| user_id | varchar(128) | 是 | NULL | 用户id | 空表示匿名评论 |
| create_time | float | 否 | NULL | 创建时间 | 唯一 |

* 标签表 tag

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| tag_id | varchar(128) | 否 | NULL | 标签id | 主键 |
| name | varchar(256) | 否 | NULL | 标签名 | 唯一 |
| create_time | float | 否 | NULL | 创建时间 | |
| update_time | float| 是 | NULL | 修改时间 | |

* 标签与笔记映射表 tag_note

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| tag_id | varchar(128) | 否 | NULL | 标签id | 主键 |
| note_id | varchar(128) | 否 | NULL | 笔记id | 主键 |
| create_time | float | 否 | NULL | 创建时间 | |

* 关于我表 about_me

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| about_me_id | varchar(128) | 否 | NULL | 关于我id | 主键 |
| content | text | 否 | NULL | 内容 | 唯一 |
| create_time | float | 否 | NULL | 创建时间 | |
| update_time | float | 是 | NULL | 修改时间 | |

* 友链表 friend_link

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| friend_link_id | varchar(128) | 否 | NULL | 友链id | 主键 |
| name | varchar(256) | 否 | NULL | 友链名称 | 唯一 |
| link | varchar(256) | 否 | NULL | 链接 | 唯一 |
| description | varchar(256) | 否 | NULL | slogan | |
| create_time | float | 否 | NULL | 创建时间 | |
| update_time | float | 是 | NULL | 修改时间 | |

* 访问信息表 visit_info

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| visit_info_id | varchar(128) | 否 | NULL | 访问信息id | 主键 |
| day | varchar(256) | 否 | NULL | 按天统计 | 唯一 |
| scheme | varchar(256) | 否 | NULL | 请求url协议 | |
| host | varchar(256) | 否 | NULL | 请求url主机 | |
| path | varchar(256) | 否 | NULL | 请求url路径 | |
| method | varchar(256) | 否 | NULL | 请求方式 | |
| path_params |  varchar(256) | 否 | NULL | 路径参数 | |
| body_params |  varchar(256) | 否 | NULL | 请求体参数 | |
| remote_addr | varchar(256) | 否 | NULL | 客户端地址 | |
| user_agent | varchar(256) | 否 | NULL | 客户端标识 | |
| cookies | varchar(256) | 否 | NULL | 客户端cookies | |
| headers | varchar(256) | 否 | NULL | 客户端请求头 | |
| create_time | float | 否 | NULL | 创建时间 | 唯一 |

* 访问位置表 visit_location

| 字段名称 | 类型 | 是否为空 | 默认值 | 描述 | 备注 |
| -------- | ------ | --- | ------ | ------ | ------ |
| visit_location_id | varchar(128) | 否 | NULL | 访问位置id | 主键 |
| day | varchar(256) | 否 | NULL | 按天统计 | 唯一 |
| ip | varchar(256) | 否 | NULL | IP | 唯一 |
| isp | varchar(256) | 否 | NULL | ISP | |
| region_id | varchar(256) | 否 | NULL | 省id | |
| region | varchar(256) | 否 | NULL | 省 | |
| city_id | varchar(256) | 否 | NULL | 城市id | |
| city | varchar(256) | 否 | NULL | 城市 | |
| district_id | varchar(256) | 否 | NULL | 地区id | |
| district | varchar(256) | 否 | NULL | 地区 | |
| country_id | varchar(256) | 否 | NULL | 乡镇id | |
| country | varchar(256) | 否 | NULL | 乡镇 | |
| lat | varchar(256) | 否 | NULL | 经度 | |
| lng | varchar(256) | 否 | NULL | 纬度 | |
| create_time | float | 否 | NULL | 创建时间 | |
| visit_info_id | varchar(128) | 否 | NULL | 关联 visit_info 表 | 外键 |

### 4. 测试接口

```bash
rm -rv data upload delete tests/category.md tests/result tests_data
tar zxvf data_v3.tar.gz
mv -v data_v3 data
pytest tests/tests_1_category.py tests/tests_2_tag.py tests/tests_3_file.py tests/tests_4_note.py tests/tests_5_comment.py tests/tests_6_about_me.py tests/tests_7_friend_link.py tests/tests_8_visit_location.py tests/tests_9_save_data.py
```
