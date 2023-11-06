//2858	
//pv

#include<algorithm>
#include<numeric>
#include "hogwarts.h"

using namespace std;

template<typename T> void process(vector<T>& v){
	printReverse(v);
	cout<<sum_if(v,[](int idx,int val){return val%2==0;})<<endl;
	cout<<sum_if(v,[](int idx,int val){return idx%2!=0;})<<endl;
	cout<<count_if(v.begin(),v.end(),[](int n){return n%10==0;})<<endl;
	cout<<sum_if(v,[](int idx,int val){return idx%2==0 && val%3==0;})<<endl;
}
	
int main(){
	vector<int> v;
	read(v);
	process(v);
	return 0;
}



