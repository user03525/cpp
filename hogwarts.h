#include<vector>
#include<iostream>

template<typename T> void read(std::vector<T>& v){
	int n;
	std::cin>>n;
	T val;
	for(int i=0;i<n;i++){
		std::cin>>val;
		v.push_back(val);
	}
}

template<typename T> void print(std::vector<T>& v){
	for(auto a:v)
		std::cout<<a<<" ";
	std::cout<<std::endl;
}

bool isPrime(int n);
