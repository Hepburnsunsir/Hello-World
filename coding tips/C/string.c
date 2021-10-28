#include <stdio.h>

#include <string.h>

//extern char *strncpy(char *dest, char *src, int n); 用法：#include 功能：把src所指由NULL结束的字符串的前n个字节复制到dest所指的数组中。 说明： 如果src的前n个字节不含NULL字符，则结果不会以NULL字符结束
int tstrncpy(){
	return 0;
}
 //strstr(str1,str2) 函数用于判断字符串str2是否是str1的子串。如果是，则该函数返回str2在str1中首次出现的地址；否则，返回NULL
//const char* strstr(const char* str1,const char* str2);
 //char* strstr(char* str1,const char* str2);
int  tstrstr(){
 char str[] ="This is a simple string"; 
 char * pch; 
 pch = strstr (str,"simple"); 
 strncpy (pch,"sample",6); 
 puts (str); 
 return 1;
}

int main(){

  
}