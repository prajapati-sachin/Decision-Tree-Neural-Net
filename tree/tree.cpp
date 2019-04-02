#include <bits/stdc++.h>
using namespace std;

#define pb push_back

vector<vector<string> > datalabels;
vector<vector<int> > dataX;
vector<int> dataY;

void readdata(string name){
	fstream fin;
	fin.open(name, ios::in); 
	vector<string> row;
	vector<int> introw;
	string line, temp, word;
	int count=0;
	while(fin>>temp){
		// cout << temp << endl;
		row.clear();
		introw.clear();
		stringstream s(temp);
		for(int i=0;i<=24;i++){
			getline(s, word, ',');
			row.pb(word);
		}
		if(count>=5){
			for(int i=1;i<=23;i++){
				// cout << row[i] << endl;
				introw.pb(stoi(row[i]));
			}
			dataX.pb(introw);
			dataY.pb(stoi(row[24]));
		}
		count++;			
	}
}

int main(){
	readdata("test.csv");
	cout << dataX.size() << endl;
	// cout << dataX[20][22] << endl;
	for(int i=0;i<dataY.size();i++){
		// for(int j=0;j<dataX[i].size();j++){
			cout << dataY[i] ;
		// } 
		cout << endl;
	}

	return 0;
}