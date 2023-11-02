//986	
//numarare7

#include<algorithm>
#include<numeric>
#include "hogwarts.h"

using namespace std;

int process(vector<double>& v);
	
int main(){
	vector<double> v;
	read(v);
	cout<<process(v);
	return 0;
}

int process(vector<double>& v){
	double first = *v.begin();
	double last = *(v.end()-1);
	if(first>last) swap(first,last);
	return count_if(v.begin(),v.end(),[first,last](double n){return n<first || n>last;});
}


