#  coding=utf-8
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import csv
#import bs4
import re

import requests
#import  pandas as ps

#excel  pip install xlrd  xlwt
import xlrd 

import xlwt
from xlutils.copy import copy

def write_excel_xls(path, sheet_name, value):
    index =  len(value)  ## 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


 
def write_excel_xls_append(path, name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    #sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    #worksheet = workbook.sheet_by_name(sheets[1])  # 获取工作簿中所有表格中的的第一个表格
    #rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.add_sheet(name)  # 获取转化后工作簿中的第一个表格
    
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")
 
 
def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()
 
# 爬取网页，网页数据下载和解析 requests,cookie
# 提取html表格 pandas , pd.read_html 
# Pandas将数据存储到execl
#检查url地址
def check_link(url):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    try: 
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        #print(r.text)
        return  r.text
    except:
        print(" cann't connect to url")

# crawl resources
def  get_contents(ulist, rurl):
    #soup = BeautifulSoup(rurl)
    
    soup = BeautifulSoup(rurl, 'lxml')
    #trs = soup.find('div', class_="TableWithRules").find_all('tr')
    #print(trs)
    
    trs = soup.find_all('tr')
    print(trs)
    #trs = soup.find_all('tr') 
    #ulist = []
    trs = trs[7:-5] 
    for tr in trs:  
        ui = [] 
        flag = False 
        for td in tr: 
            #使用正则表达式 
            if  re.search ('^CVE', td.string):
                ui.append(td.string)
            if  re.search ('command', td.string, re.IGNORECASE):
                flag  = True
                ui.append(td.string)
            #print (td.string)  
        if flag :
            ulist.append(ui) 


# save resources
def save_contents(urlist):
    try:  
        with open("数据.csv",'w') as f:  
            writer = csv.writer(f)  
            writer.writerow(['2016年中国企业500强排行榜'])  
            for i in range(len(urlist)):  
                writer.writerow([urlist[i][1],urlist[i][3],urlist[i][5]]) 
    except:
        pass

def get_command(clist):
    for il in clist:
        ui = []
        for sj in il:
            #使用正则表达式匹配
            if "CVE" in sj:
                ui.append(sj)

def main():
    urli = []
    url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=D-link"
    rs = check_link(url)
    get_contents(urli, rs)
    #提取含有CVE,command的列，利用变量名指向内存固定
    get_command(urli)

    #save_contents(urli)
    path = "./cvev1.xls"
    sheet_name = "command1"
    write_excel_xls_append(path, sheet_name,  urli)
    #write_excel_xls(path, "command", urli)

'''
得到的表格还需要处理一下，使用shell
'''

    
main()