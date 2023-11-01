//491
//suma2

#include<algorithm>
#include<numeric>
#include "hogwarts.h"


using namespace std;

void process(vector<int>& v);
	
int main(){
	vector<int> v;
	read(v);
	process(v);
	return 0;
}

void process(vector<int>& v){
	pair<int,int> positions={-1,-1};
	int index=0;
	bool locked=false;
	for_each(v.begin(),v.end(),[&positions,&index,&locked](int n){if(n%2==0){if(!locked){positions.first=index;locked=true;}positions.second=index;}index++;});
	if(positions.first!=-1)
		cout<<accumulate(v.begin()+positions.first,v.begin()+positions.second+1,0);
	else
		cout<<"NU EXISTA";
}


