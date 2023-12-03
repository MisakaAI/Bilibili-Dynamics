# B站动态类型

## Type

desc.type 类型
desc.dynamic_id 动态ID *https://t.bilibili.com/<dynamic_id>*
desc.timestamp 时间戳

### 1 转发动态

item.content 内容

## 2 图片动态

card.item.description
card.item.rp_id 链接 *https://www.bilibili.com/opus/<rp_id>*
card.item.pictures 图片列表
card.item.pictures[i].img_src 图片地址

### 4 文字动态

card.item.rp_id 链接 *https://www.bilibili.com/opus/<rp_id>*
card.item.content 内容

### 8 视频投稿

card.aid AV号
card.pic 封面
card.short_link_v2 短链
card.title 标题
card.tname 分区

### 64 专栏

card.id ID *https://www.bilibili.com/read/cv<id>*
card.title 标题
card.summary 摘要
card.image_urls 封面
card.category.name 分区

### 256 音频投稿

card.id ID *https://www.bilibili.com/audio/au<id>*
card.cover 封面
card.title 标题

## 2048 bilibili个性装扮