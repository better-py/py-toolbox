# Toolbox:

- python toolbox

## packages:

- ✅ [chain](packages/chain/run.py): 链上交易数据查询

```ruby

# run:
task chain:run

```

- ✅ [rsshub](packages/rsshub/run.py): rsshub 配置格式化工具

```ruby

# run:
task rss:run

```

## env:

> requirements:

- `Python 3.9.9`
- pyenv:
    - https://github.com/hhstore/blog/issues/17
- go-task

> setup:

- pyenv:

```ruby
# with go-task:
task setup

#
# or do:
#

# install python3.9:
pyenv install 3.9.9

# create for this project:
pyenv virtualenv 3.9.9 py39-toolbox

# check:
pyenv versions

# use local:
pyenv local py39-toolbox 

# check:
python3
```

- install python requirements:

```ruby

task install

```


