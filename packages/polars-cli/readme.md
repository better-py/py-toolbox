# Excel Parser:

- Excel 表格处理工具.
- 支持 csv, xlsx, xls 等表格

## QuickStart:

- 启动脚本： [Taskfile.yml](Taskfile.yml)

- install:

```ruby
pip3 install -r requirements.txt


```

- run:

```ruby

# 默认参数：
python3 run.py


# 传入参数：
python3 run.py \
  --infile_a=input/1.xlsx \
  --infile_b=input/2.xlsx \
  --outfile=output/out.xlsx


```

## reference:

> requirements:

- https://github.com/pandas-dev/pandas
- https://github.com/pyexcel/pyexcel

> docs:

- https://www.pypandas.cn/docs/user_guide/io.html
