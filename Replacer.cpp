#include <string>
#include <regex>
#include <iostream>
#include <fstream>

using namespace std;

int main(){
    ifstream tempfile;
    string argv[6];
    try{
        tempfile.open("temp");
        string tempArg;
        string str;
        int tempLength;
        while(getline(tempfile,tempArg)){
            //cout << tempArg<< endl;
            if(tempArg=="args:{"){
                cout << "FileStart"<<endl;
            }else if(tempArg.find("\ttargetPass:")==0){
                str="\ttargetPass:";
                tempLength=tempArg.length();
                argv[1]=tempArg.substr(str.length());
                argv[1].erase(0,1);
                argv[1].erase(argv[1].length()-1);
                cout<< "argv[1]:" << argv[1] << endl;
            }else if(tempArg.find("\tregex:")==0){
                str="\tregex:";
                tempLength=tempArg.length();
                argv[2]=tempArg.substr(str.length());
                argv[2].erase(0,1);
                argv[2].erase(argv[2].length()-1);
                cout<< "argv[2]:" << argv[2] << endl;
            }else if(tempArg.find("\treplacedText:")==0){
                str="\treplacedText:";
                tempLength=tempArg.length();
                argv[3]=tempArg.substr(str.length());
                argv[3].erase(0,1);
                argv[3].erase(argv[3].length()-1);
                cout<< "argv[3]:" << argv[3] << endl;
            }else if(tempArg.find("\tLoopMax:")==0){
                str="\tLoopMax:";
                argv[4]=tempArg.substr(str.length());
                cout<< "argv[4]:" << argv[4] << endl;
            }else if(tempArg.find("\tReplaceFile:")==0){
                str="\tReplaceFile:";
                argv[5]=tempArg.substr(str.length());
                cout<< "argv[5]:" << argv[5] << endl;
            }else if(tempArg=="}"){
                cout << "FileEND" << endl;
                break;
            }
        }
    }catch(string e){
        cout << "Argv is invalid"<< endl;
        return -1;
    }
    string InputFilename=argv[1];
    string isReplacedRegexStr(argv[2]);
    regex isReplacedRegex(argv[2]);
    string Replacedstring=argv[3];
    //cout << InputFilename<<endl<<isReplacedRegexStr<<endl<<Replacedstring<<endl;
    int LoopMax;
    bool ReplaceFile;
    LoopMax=stoi(argv[4]);
    string temp=argv[5];
    if(temp=="True"){
        ReplaceFile=true;
    }else{
        ReplaceFile=false;
    }
    string OutputFileName;
    int dot_position=InputFilename.find_last_of('.');
    if(dot_position==string::npos){
        cout << "Filename is invalid";
        return -1;
    }
    if(ReplaceFile==true){
        OutputFileName="temp.txt";
    }else{
        OutputFileName=InputFilename.substr(0,dot_position)+" - Replaced"+InputFilename.substr(dot_position);
    }
    ifstream InputFile;
    ofstream OutputFile;
    InputFile.open(InputFilename,ios::in);
    OutputFile.open(OutputFileName,ios::out);
    string reading_line_buffer;
    int cnt=0;
    while(getline(InputFile,reading_line_buffer)){
        temp=reading_line_buffer;
        cnt=0;
        while(regex_search(temp,isReplacedRegex)){
            string _temp;
            _temp=temp;
            temp=regex_replace(temp,isReplacedRegex,Replacedstring);
            cnt++;
            if(_temp==temp || cnt>=LoopMax){
                break;
            }
        }
        OutputFile << temp << endl;
    }
    InputFile.close();
    OutputFile.close();
    if(ReplaceFile==true){
        remove(InputFilename.c_str());
        rename(OutputFileName.c_str(),InputFilename.c_str());
    }
}