# wordlist:

- 词汇表格式化工具

> 英语词汇表

- ✅️ CET4
- ✅️ CET6
- ✅️ GRE
- ✅️ TOEFL
- ✅️ IELTS

## 🔥️ 英语分级词库发布

- ✅️ https://github.com/better-edu/learn-english
- ✅️ 已经将清洗后的单词库发布到此项目，
- ✅️ 包含: `CET4, CET6, TOEFL, IELTS, GRE` 等

## 🔥️ quickstart:

- ✅️ [Taskfile.yml](./Taskfile.yml): run scripts

### install:

- ✅️ install python packages

```ruby

# install 1: under toolbox/ dir:
task word:install

# install 2: under current dir:
task install

```

### run:

```ruby
# run 1: under toolbox/
task word:run


# run 2: under crrent dir/
task run

```

### run unit test

```ruby
task word:test

# or
task test

```

## 🔥️ 英语分级词汇报告：

- ✅️ sum(CET4+CET6+TOEFL+IELTS+GRE) = 21151 个
- ✅️ 重复了接近一半，实际是 13003 个

```ruby

words num: CET4 = 4471,
words num: CET6 = 2083, 
words num: TOEFL = 3461,
words num: IELTS = 4512,
words num: GRE = 6624, 

sum(cet4+cet6+toefl+ielts+gre) = 21151 (重复了一半，实际是 13003 个）

words union: cet4_cet6 = 6027
words union: cet4_cet6_toefl = 8182
words union: cet4_cet6_toefl_ielts = 9320
words union: cet4_cet6_toefl_ielts_gre = 13003

```

## reference:

- ✅️ https://github.com/tabhub/English-words-cards
    - CET4, CET6, TOEFL, IELTS, GRE 词汇表
- ✅️ https://github.com/fanhongtao/IELTS
    - 雅思词汇表
- ✅️ https://github.com/liurui39660/3000
    - Excel版 再要你命3000
- ✅️ [新东方雅思 绿宝书 词汇词根+联想记忆法 乱序版 TXT格式可导入单词本（带释义）](https://forum.chasedream.com/thread-1382363-1-1.html)
    - 共3500+个词汇, XML 格式