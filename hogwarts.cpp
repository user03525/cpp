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

void read(std::vector<int>& v){
	int n;
	std::cin>>n;
	int val;
	for(int i=0;i<n;i++){
		std::cin>>val;
		v.push_back(val);
	}
}
void print(std::vector<int>& v){
	for(auto a:v)
		std::cout<<a<<" ";
	std::cout<<std::endl;
}
