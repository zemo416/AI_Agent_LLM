#def user_info(*args):
 # print(f"args参数的类型是: {type(args)}, 内容是:{args}")

#user_info(1, 2, 3, '小明', '男孩')


#def user_info(**kwargs):
  
 # print(f"args参数的类型是:{type(kwargs)}, 内容是: {kwargs}")
# user_info(name = '小王', age=11, gender='男孩', addr='北京')



#def sum_all(*args):
  #  total = 0
   # for x in (1, 2, 3.5):
     #   total += x
   # return total
# result = sum_all(1, 2, 3.5)
# print(result)





#def sum_all(*args):
 #   total = 0
  #  for x in args:
   #     total += x
    #return total

# sum_all()



#def describe_person(**kwargs):

 #   if 'name' in kwargs and 'age' in kwargs:
  #      print(f"name={kwargs['name']}, age={kwargs['age']}")
   # else:
    #    print("missing required info")

# describe_person(name = 'xiaowang', age=11)
# describe_person(name='xiaowang')
# describe_person()


# def user_info(*args, **kwargs):
    
  #  kwargs_keys=['addr', 'age', 'name']
   # print(f"args_count={len(args)}")
    #print(f"kwargs_keys={sorted(kwargs.keys())}")
    

#user_info(1, 2, 3, name='A', age=10, addr='BJ')



#def test_func(compute):
  #  result = compute(1, 2)
   # print(type(compute))
    #print(result)

#def compute(x, y):
 #   return x / y

# test_func(compute)



#def test_func(op):
    
  #  print(op(2, 3))

# def add(a, b):
  #  return a + b

#def mul(a, b):
    #return a * b

#test_func(add)
#test_func(mul)


#def run_test(calc):
  #  data = [1, 2, 3]
   # result = calc(data)
    #print(result)

#def sum_func(data):
  #  return sum(data)


#def max_func(data):
  #  return max(data)


#run_test(sum_func)
#run_test(max_func)

#def test_func(compute):
 #   result = compute(1, 2)
  #  print(result)

#test_func(lambda x,y: x + y)
#import time

#with open("C:/Users/zemou/OneDrive/Desktop/test.txt", "r", encoding="UTF-8") as f:
    #content = f.read()
    #print(content)

    #lines = f.readlines()
    #print(type(lines))
    #print(lines)


 #   line1 = f.readline()
  #  line2 = f.readline()
   # line3 = f.readline()

   # print(line1)
   # print(line2)
   # print(line3)


#f = open("C:/Users/zemou/OneDrive/Desktop/test.txt", "r", encoding="UTF-8")

    
#content = f.read()
#count = content.count("itheima")

#print(count)
#count = 0
#for line in f:
        
     #   words = line.split(" ")
      #  for word in words:
       #         if word =="itheima":
        #                count += 1

#print(count)


#f = open("C:/Users/zemou/OneDrive/Desktop/test.txt", "a", encoding="UTF-8")
        
#f.write("\n阿萨大大达到今晚道具吊带多么寂寞就")

#f.flush()

#f.close()

#try:
 #   f = open("D:/abc.txt", "r", encoding="UTF-8")
#except:
 #   print("出现异常了,因为文件不存在,我将open的模式改为w的模式去打开")
  #  f = open("C:/Users/zemou/OneDrive/Desktop/test.txt", "w", encoding="UTF-8")

#try:

 #   print(Name)
    
#except NameError as e:
 #   print("出现了变量未定义的异常")
  #  print(e)

#try:
 #   #1 / 0
 #   print(Name)
#except (NameError, ZeroDivisionError) as e:
 #   print("出现了变量未定义 或者 除以0的异常错误")



#try:
 #  f = open("C:/Users/zemou/OneDrive/Desktop/test.txt", "a", encoding="UTF-8")
#except Exception as e:
 # print("出现异常了")
#else:
 #  print("异常清零")
#finally:
 #  print("文件关闭，强制执行")
  # f.close()


#import json


#f_us = open("C:/Users/zemou/OneDrive/Desktop/test.txt", "r", encoding="UTF-8")
#us_data = f_us.read()

#us_data = us_data.replace("sadasddnouiahndonadoandonaodnaondoimonocnoandojoimo1imdo", "dadadwaddasd")
#us_data = us_data[:-1]

#print(repr(us_data))

#us_dict = json.loads(us_data)

#print(type(us_dict))
#print(us_dict)



#import json

#with open("C:/Users/zemou/OneDrive/Desktop/test.txt", "r", encoding="UTF-8") as f:
 #   us_data = f.read().strip()


#print("RAW DATA", repr(us_data))

#if not us_data:
 #   raise ValueError("File is empty or data was removed.")

#us_dict = json.loads(us_data)

#print(type(us_dict))
#print(us_dict)


#import json

#data = [{"name": "黄泽谋", "age": 11}, {"name": "张一", "age": 21}, {"name": "2是的", "age": 551}]
#json_str = json.dumps(data, ensure_ascii=False)

#print(type(json_str))
#print(json_str)

#d = {"name": "黄泽谋", "addr": "taibei"}
#json_str = json.dumps(d, ensure_ascii=False)
#print(type(json_str))
#print(json_str)


#s = '[{"name": "的对待", "age":11}, {"name": "sdq", "age": 13}, {"name": "是的是的", "age": 16}]'
#l = json.loads(s)
#print(type(l))
#print(l)

#s = '{"name": "黄泽谋", "addr": "taibei"}'
#d = json.loads(s)
#print(type(d))
#print(d)

#import re

#s = "python itheima python sadadwadpython"

#result = re.match("python", s)
#print(result)

#result = re.search("python", s)
#print(result)

#result = re.findall("python", s)
#print(result)


#s = "itheima oido1mo1A23414djno[python]dad1489niolami  iawdhopython"

#result = re.findall('[a-zA-Z0-9]', s)
#print(result)

#r = '^[0-9a-zA-Z]{6,10}$'

#s = '12345566'
#print(re.findall(r, s))

#r = '^[1-9][0-9]{4,10}$'
#s = '12345678'
#print(re.findall(r, s))





#result = re.findall('[a-zA-Z0-9]', r)
#print(result)


#s = 'itheima hiado%^&((^@%$123onczn1823-09ojnonoj'

#result = re.findall(r'[a-zA-Z]', s)
#print(result)


#r = '^[1-9][0-9]{4,10}$'
#s = '12314145'

#print(re.findall(r, s))





#s = "abc123xyz456"

#r = r'(\d)'
#print(re.findall(r, s))

#s = "123456789"

#r = r'\d\d+(\d+)'
#print(re.findall(r, s))

#from my_package import *

#my_model2.info_print2()
#my_models1.info_print1()



#name = 'hzm'

#print(f"my name is {name},")

#print(type(name))





#sum = 0
#i = 1

#while i<= 100:
  #  sum += i
   # i += 1
    

#print((sum))

import streamlit as st

st.title("Streamlit 入门演示")
st.header("Streamlit 一级标题")
st.subheader("Streamlit 二级标题")

