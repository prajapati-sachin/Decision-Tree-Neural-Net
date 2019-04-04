#include <bits/stdc++.h>
using namespace std;

#define pb push_back
#define epsilon 0.01

// vector<vector<string> > datalabels;
vector<vector<int> > dataX;
vector<int> dataY;
// static int count1=0;


vector<int> continous{0, 4, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}; 
vector<int> categorical{1, 2, 3, 5, 6, 7, 8, 9, 10}; 
// Gender--Education
vector<vector<int> > categories{{0, 1}, {1, 2}, {0, 6}, {0, 3}, 
								{0, 1}, {-2, 9}, {-2, 9}, {-2, 9}, 
								{-2, 9}, {-2, 9}, {-2, 9}, {0,1},
								{0,1}, {0,1}, {0,1}, {0,1},
								 {0,1}, {0,1}, {0,1}, {0,1}, 
								 {0,1}, {0,1}, {0,1}};


double infoGain(vector<vector<int> > X, vector<int> Y, int attr);

class node{
	public:
		int positive;
		int negative;
		int total;
		int majority;
		bool isLeaf;
		int attrnum;
		int numchilds;
		vector<node*> childs;
		
		//Constructor
		node(int positive1, int negative1, int total1, int majority1, bool leaf, int attribute, int numchilds1);
};


class tree{
	public:
		node* root;
		tree();
};

node::node(int positive1, int negative1, int total1, int majority1, bool leaf, int attribute, int numchilds1){
	positive = positive1;
	negative = negative1;
	total = total1;
	majority = majority1;
	isLeaf = leaf;
	attrnum = attribute;
	numchilds = numchilds1;
	childs.pb(NULL);
}

tree::tree(){
	root=NULL;
}


void preprocessing(){
	vector<float> temp;
	int median;
	int size;
	for(int i=0;i<continous.size();i++){
		temp.clear();
		for(int j=0;j<dataX.size();j++){
			temp.pb(dataX[j][continous[i]]);
		}
		size=temp.size();
		sort(temp.begin(), temp.end());
		if(temp.size()%2==0) median = (temp[size/2]+temp[(size/2)-1])/2; 
		else median = temp[size/2];
		// cout << "median for: " << continous[i] << " = " << median << endl; 
		for(int j=0;j<dataX.size();j++){
			if(temp[j]>=median) dataX[j][continous[i]]=1;
			else dataX[j][continous[i]]=0;
		}
	}
}

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
	// vector<vector<int> > dataXT;
	// for(int i=0;i<24;i++){
	// 	introw.clear();
	// 	for(int j=0;j<dataX.size;j++){
	// 		introw.pb(dataX[j][i]);
	// 	}
	// 	dataXT.pb(introw)
	// }
}

node growTree(vector<vector<int> > X, vector<int> Y, vector<int> attributes, int count){
	int positive = 0;
	int negative = 0;
	int total = 0;
	for(int i=0;i<Y.size();i++){
		if(Y[i]==1) positive++;
		else negative++;
	}
	total = positive+negative;
	double probpos = positive*(1.0)/total;
	double probneg = negative*(1.0)/total;

	int majority = (positive>=negative) ? 1 : 0;

	if(probpos < epsilon){ node temp(positive, negative, total, majority, true, -1, 0);   return temp;}
	else if(probneg < epsilon) { node temp(positive, negative, total, majority, true, -1, 0); return temp; }
	else{
		cout << "Here" << endl;
		double max = INT_MIN;
		int max_index;
		double tempnum;
		for(int i=0; i<attributes.size(); i++){
			tempnum = infoGain(X, Y, attributes[i]);
			cout << tempnum << endl;
			if(tempnum > max){
				max = tempnum;
				max_index = i;
			}
		}
		// cout << max_index << endl;
		cout << attributes[max_index] << endl;
		cout << attributes.size() << endl;
		vector<int> new_attributes = attributes;
		int startval = categories[attributes[max_index]][0];
		int endval = categories[attributes[max_index]][1];
		int totalcategories = endval - startval + 1;
		vector<int> possiblevals;
		for(int i=0;i<totalcategories;i++) possiblevals.pb(startval+i);
		cout << "Possible vals size: "<<possiblevals.size()<< endl;
		new_attributes.erase(new_attributes.begin() + max_index);
	
		node temp(positive, negative, total, majority, false, attributes[max_index], totalcategories);
	
		for(int i=0; i< possiblevals.size(); i++){
			vector<vector<int> > tempX;
			vector<int> tempY;
			cout << "Checking for: " << possiblevals[i] << endl;
			for(int j=0;j< X.size(); j++){
				if(X[j][attributes[max_index]]==possiblevals[i]){ tempX.pb(X[j]); tempY.pb(Y[j]);}
			}
			cout << "TempX: "<<tempY.size() << endl;
			cout << "TempY: "<<tempX.size() << endl;
			cout << "-----------------------" << endl ;

			node tempo = growTree(tempX, tempY, new_attributes, count+1);
			temp.childs.pb(&tempo); 

		}

		return temp;
	}

}

double entropy(int positive, int negative){
	int total = positive + negative;
	double ent;
	if(total!=0){
		double prob_pos = positive*(1.0)/total;
		double prob_neg = negative*(1.0)/total;	
		double first = (prob_pos!=0) ? prob_pos*(log2(prob_pos)): 0;
		double second = (prob_neg!=0) ? prob_neg*(log2(prob_neg)): 0;	
		ent = (-1)*(first+second);
		// cout << first << endl;
		// cout << second << endl;

	}
	else{
		ent = 0;
	}
	return ent;
}

double infoGain(vector<vector<int> > X, vector<int> Y, int attr){
	int positive = 0;
	int negative = 0;
	int initial_total = 0;
	for(int i=0;i<Y.size();i++){
		if(Y[i]==1) positive++;
		else negative++;
	}
	initial_total = positive + negative;
	// cout << positive << endl;
	// cout << negative << endl;
	// cout << initial_total << endl;
	double initial_entropy = entropy(positive, negative); 
	// cout << initial_entropy << endl;
	int startval = categories[attr][0];
	int endval = categories[attr][1];
	int totalcategories = endval-startval+1;
	vector<int> possiblevals;
	for(int i=0;i<totalcategories;i++) possiblevals.pb(startval+i);
	double conditional_entropy=0;
	// int temppos;
	// int tempneg;
	// int temptotal;
	double cond_entropy;
	double probab;
	int total;

	for(int i=0;i<possiblevals.size();i++){
		positive = 0;
		negative = 0;
		total = 0;
		cond_entropy = 0;
		probab = 0;

		for(int j=0;j<dataX.size();j++){
			if(dataX[j][attr]==possiblevals[i]){
				if(dataY[j]==1) positive++;
				else negative++;
			}
		}
		total = positive + negative;
		// if(total==0){
		// 	cout << "attribute: " << attr << endl;
		// 	cout << "value: " << possiblevals[i] << endl;
		// 	cout << "positive: " << positive << endl;
		// 	cout << "negative: " << negative << endl;
 	// 	}
		cond_entropy = entropy(positive, negative);
		probab = total*(1.0)/initial_total;
		conditional_entropy += (cond_entropy*probab);

	}

	double information = initial_entropy - conditional_entropy;
	return information;
}

int main(){
	readdata("train.csv");
	preprocessing();
	vector<int> attrs;
	for(int i=0;i<23;i++) attrs.pb(i);
	node root = growTree(dataX, dataY, attrs, 0);
	// cout << infoGain(dataX, dataY, 0);
	// cout << dataX.size() << endl;
	// cout << dataX[20][22] << endl;
	// for(int i=0;i<dataY.size();i++){
	// 	// for(int j=0;j<dataX[i].size();j++){
	// 		cout << dataY[i];
	// 	// } 
	// 	cout << endl;
	// }

	// cout << root.numchilds << endl;
	// cout << root.attrnum << endl;

	return 0;
}


