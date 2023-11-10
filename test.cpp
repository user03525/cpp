//498	
//numararepie

#include<algorithm>
#include<numeric>
#include "hogwarts.h"

using namespace std;

template<typename T> int process(vector<T>& v){
	return double_map(v,[](int a,int b,int& rez){ rez+=pie(a,b);});
}
	
int main(){
	vector<int> v;
	read(v);
	cout<<process(v);
	return 0;
}



