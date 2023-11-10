#include<vector>
#include<iostream>
#include<algorithm>

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

template<typename T> void printReverse(std::vector<T>& v){
	for_each(v.rbegin(),v.rend(),[](T n){std::cout<<n<<" ";});
	std::cout<<std::endl;
}

template<typename T> T sum_if(std::vector<T>& v,bool (*condition)(int idx,int val)){
	int sum=0;
	int idx=0;
	for_each(v.begin(),v.end(),[&](T val){ if(condition(idx++,val)) sum+=val;});
	return sum;
}

bool isPrime(int n);
int cmmdc(int a,int b);
bool pie(int a,int b);
int double_map(std::vector<int>& v,void (*f)(int a,int b,int& r));
