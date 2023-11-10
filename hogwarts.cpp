#include "hogwarts.h"

bool isPrime(int n){
	if(n<2){
		return false;
	}
	for(int d=2;d*d<=n;d++){
		if(n%d==0)
			return false;
	}
	return true;
}	

int cmmdc(int a,int b){
	int r;
	while(b){
		r=a%b;
		a=b;
		b=r;
	}
	return a;
}

bool pie(int a,int b){
	return cmmdc(a,b)==1;
}

int double_map(std::vector<int>& v,void (*f)(int a,int b,int& r)){
	int result=0;
	for(int i=0;i<v.size();i++){
		for(int j=i+1;j<v.size();j++){
			f(v[i],v[j],result);
		}
	}
	return result;
}


