#include <bits/stdc++.h>
using namespace std;

#define pb push_back
#define epsilon 0.01

// vector<vector<string> > datalabels;
vector<vector<int> > dataX;
vector<int> dataY;

vector<vector<int> > testX;
vector<int> testY;

vector<vector<int> > valX;
vector<int> valY;


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
		node(int positive1, int negative1, int total1, int majority1, bool leaf, int attribute);

		//Empty Constructor
		node();

		//Copy constructor
		node(const node&);

		//Add children
		void addChild(node* c);
};


class tree{
	public:
		node* root;
		tree();
};

node::node(int positive1, int negative1, int total1, int majority1, bool leaf, int attribute){
	positive = positive1;
	negative = negative1;
	total = total1;
	majority = majority1;
	isLeaf = leaf;
	attrnum = attribute;
	numchilds=0;
}

node::node(){

}

node::node(const node& n){
	positive =  n.positive;
	negative =  n.negative;
	total =  n.total;
	majority =  n.majority;
	isLeaf =  n.isLeaf;
	attrnum =  n.attrnum;
	numchilds =  n.numchilds;
	for(int i=0;i<n.childs.size();i++) childs.pb(n.childs[i]);
}

void node::addChild(node* c){
	childs.pb(c);
	numchilds++;
}

tree::tree(){
	root=NULL;
}


void preprocessingtrain(){
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
			if(dataX[j][continous[i]]>median) dataX[j][continous[i]]=1;
			else dataX[j][continous[i]]=0;
		}
	}
}

void preprocessingtest(){
	vector<float> temp;
	int median;
	int size;
	for(int i=0;i<continous.size();i++){
		temp.clear();
		for(int j=0;j<testX.size();j++){
			temp.pb(testX[j][continous[i]]);
		}
		size=temp.size();
		sort(temp.begin(), temp.end());
		if(temp.size()%2==0) median = (temp[size/2]+temp[(size/2)-1])/2; 
		else median = temp[size/2];
		// cout << "median for: " << continous[i] << " = " << median << endl; 
		for(int j=0;j<testX.size();j++){
			if(testX[j][continous[i]]>median) testX[j][continous[i]]=1;
			else testX[j][continous[i]]=0;
		}
	}
}

void preprocessingval(){
	vector<float> temp;
	int median;
	int size;
	for(int i=0;i<continous.size();i++){
		temp.clear();
		for(int j=0;j<valX.size();j++){
			temp.pb(valX[j][continous[i]]);
		}
		size=temp.size();
		sort(temp.begin(), temp.end());
		if(temp.size()%2==0) median = (temp[size/2]+temp[(size/2)-1])/2; 
		else median = temp[size/2];
		// cout << "median for: " << continous[i] << " = " << median << endl; 
		for(int j=0;j<valX.size();j++){
			if(valX[j][continous[i]]>median) valX[j][continous[i]]=1;
			else valX[j][continous[i]]=0;
		}
	}
}

void readtraindata(string name){
	fstream fin;
	fin.open(name, ios::in); 
	vector<string> row;
	vector<int> introw;
	string line, temp, word;
	int count=0;
	while(fin>>temp){
		// endl <<		cout << temp << endl;
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

void readtestdata(string name){
	fstream fin;
	fin.open(name, ios::in); 
	vector<string> row;
	vector<int> introw;
	string line, temp, word;
	int count=0;
	while(fin>>temp){
		// endl <<		cout << temp << endl;
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
			testX.pb(introw);
			testY.pb(stoi(row[24]));
		}
		count++;			
	}
}

void readvaldata(string name){
	fstream fin;
	fin.open(name, ios::in); 
	vector<string> row;
	vector<int> introw;
	string line, temp, word;
	int count=0;
	while(fin>>temp){
		// endl <<		cout << temp << endl;
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
			valX.pb(introw);
			valY.pb(stoi(row[24]));
		}
		count++;			
	}
}
node growTree(vector<vector<int> > X, vector<int> Y, vector<int> attributes){
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

	if(probpos < epsilon){ node temp(positive, negative, total, majority, true, -1);   return temp;}
	else if(probneg < epsilon) { node temp(positive, negative, total, majority, true, -1); return temp; }
	else if(attributes.size()==0) { node temp(positive, negative, total, majority, true, -1); return temp; }
	else{
		double max = INT_MIN;
		int max_index;
		double tempnum;
		for(int i=0; i<attributes.size(); i++){
			tempnum = infoGain(X, Y, attributes[i]);
			// cout << endl;
			// cout << "Atrribute num " << attributes[i] <<" :" <<tempnum << endl;
			if(tempnum > max){
				max = tempnum;
				max_index = i;
			}
		}
		// cout << max_index << endl;
		// cout << attributes[max_index] << endl;
		// cout << attributes.size() << endl;

		vector<int> new_attributes = attributes;
		int startval = categories[attributes[max_index]][0];
		int endval = categories[attributes[max_index]][1];
		int totalcategories = endval - startval + 1;
		vector<int> possiblevals;
		for(int i=0;i<totalcategories;i++) possiblevals.pb(startval+i);
		// cout << "Possible vals size: "<<possiblevals.size()<< endl;
		new_attributes.erase(new_attributes.begin() + max_index);
	
		node temp(positive, negative, total, majority, false, attributes[max_index]);
	
		for(int i=0; i< possiblevals.size(); i++){
			vector<vector<int> > tempX;
			vector<int> tempY;
			// cout << "Checking for: " << possiblevals[i] << endl;
			for(int j=0;j< X.size(); j++){
				if(X[j][attributes[max_index]]==possiblevals[i]){ tempX.pb(X[j]); tempY.pb(Y[j]);}
			}
			// cout << "TempX: "<<tempY.size() << endl;
			// cout << "TempY: "<<tempX.size() << endl;
			// cout << "-----------------------" << endl ;
			node* tempop;
			if(tempX.size()==0) {
				tempop = new node(0, 0, 0, -1, true, -1);
				// continue;
			}
			else{
				tempop = new node(growTree(tempX, tempY, new_attributes));
			}
			temp.addChild(tempop);			
			// node tempo = growTree(tempX, tempY, new_attributes);
			// temp.addChild(&tempo); 

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
	// cout <<"Initial Entropy for " << attr << ": " << initial_entropy << endl;
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

		for(int j=0;j<X.size();j++){
			if(X[j][attr]==possiblevals[i]){
				if(Y[j]==1) positive++;
				else negative++;
			}
		}
		total = positive + negative;
		// if(total==0){
		// 	cout << "attribute: " << attr << endl;
		// 	cout << "value: " << possiblevals[i] << endl;
 	// 	}
			// cout << "positive: " << positive << endl;
			// cout << "negative: " << negative << endl;

		cond_entropy = entropy(positive, negative);
		probab = (double)total/(double)initial_total;
		// cout << "Total: "<<total << " Initial Total: " << initial_total << endl;
		// cout << "Child " << possiblevals[i] << ": " << probab << endl;
		// cout << "Child " << possiblevals[i] << ": " << cond_entropy << endl;
		conditional_entropy += (cond_entropy*probab);

	}

	// cout << "Conditional Entropy for " << attr << ": " << conditional_entropy << endl;
	double information = initial_entropy - conditional_entropy;
	return information;
}

int numnodes(node* t){
	int temp=1;
	for(int i=0;i<t->childs.size();i++){
		temp+=numnodes(t->childs[i]);
	}
	return temp;
}

int getIndex(int attri, int attrival){
	// int result=-1;
	int startval = categories[attri][0];
	int endval = categories[attri][1];
	int totalcategories = endval-startval+1;
	vector<int> possiblevals;
	for(int i=0;i<totalcategories;i++){
		if((startval+i)==attrival){return i;}
	}

}

int prediction(node* root, vector<int> test){
	// cout << "Gadbad" << endl;
	node* temp = root;
	int attri;
	int attrival;
	int childindex;
	while(temp->isLeaf != true){
		attri = temp->attrnum;
		attrival =  test[attri];
		// cout << "Attribute num: " << attri << " | Atrribute Value: " << attrival << endl;
		childindex = getIndex(attri, attrival);
		// if(childindex>=temp->numchilds);
		temp = temp->childs[childindex];
	}

	return temp->majority;
}


int main(){
	readtraindata("train.csv");
	readtestdata("test.csv");
	readvaldata("val.csv");
	preprocessingtrain();
	preprocessingtest();
	preprocessingval();
	vector<int> attrs;
	for(int i=0;i<23;i++) attrs.pb(i);
	node root = growTree(dataX, dataY, attrs);
	
	// int pos=0;
	// int neg=0;
	// for(int i=0;i<dataX.size();i++){
	// 	// for(int j=0; j< dataX[i].size(); j++){
	// 	// cout << dataX[i][j]<< " " ;
	// 	if(dataX[i][5]==-2) {
	// 		pos++;
	// 		// if(dataY[i]==0)neg++;
	// 		// else pos++;
	// 	}
	// 	// }
	// 	// cout << endl;
	// }

	// cout << pos << "|"  <<endl;
	// cout << infoGain(dataX, dataY, 0);
	// cout << dataX.size() << endl;
	// cout << dataX[20][22] << endl;
	// for(int i=0;i<dataY.size();i++){
	// 	// for(int j=0;j<dataX[i].size();j++){
	// 		cout << dataY[i];
	// 	// } 
	// 	cout << endl;
	// }

	int totalnode=0;
	// cout << "Root Attribute num: " << root.attrnum << endl;
	// cout << root.numchilds << endl;
	// cout << root.childs.size() << endl;

	cout << numnodes(&root) << endl;

	// for(int i=0; i<root.childs.size();i++){
	// 	cout << "Child No. " << i << " -Attr num = " << root.childs[i]->attrnum << endl;	 
	// 	// cout << "Child No. " << i << " = " << (root.childs[i])->majority <<endl;	 
	// }
	// cout << root.attrnum << endl;


	// cout << (root.childs[0])->numchilds << endl;
	
	vector<int> predictedTest;
	int count=0;
	for(int i=0;i<testX.size();i++){
		if(prediction(&root, testX[i])==testY[i]) count++;
	}

	cout << "Acc: "<< (double)count/(double)testY.size() << endl;




	return 0;
}


