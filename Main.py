# cording=utf-8
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as msg
import re
import os
import subprocess
import codecs


def main():
    root=tk.Tk()
    root.title("置換機")

    menu=tk.Menu(root)
    root.config(menu=menu)

    def ClearAll():
        FilePass.set("")
        Regex.set("")
        Replaced.set("")
    def ExitApplication():
        ask=msg.askokcancel(title="終了確認",message="プログラムを終了しますか？")
        if ask==True:
            root.destroy()
    
    LoopMax=tk.IntVar()
    defaultLoopMax=100
    if LoopMax.get()==0:
        LoopMax.set(defaultLoopMax)
    ReplaceFileFlag=tk.BooleanVar()
    ReplaceFileFlag.set(False)


    def AdvancedOption():
        AdvancedOptionMenu=tk.Toplevel(root)
        AdvancedOptionMenu.title("上級者向け設定")

        AdvancedOptionFrame=tk.Frame(AdvancedOptionMenu)
        AdvancedOptionFrame.grid(row=0,column=0)
        LoopMaxLabel=tk.Label(AdvancedOptionFrame,text="最大ループ数")
        LoopMaxLabel.grid(row=0,column=0)

        flag=True
        if flag:
            temp=LoopMax.get()
            flag=False

        LoopMaxEntry=tk.Entry(AdvancedOptionFrame,textvariable=LoopMax)
        LoopMaxEntry.grid(row=0,column=1)

        ReplaceFileLabel=tk.Label(AdvancedOptionFrame,text="ファイルを上書きする")
        ReplaceFileLabel.grid(row=1,column=0)
        ReplaceFileCheckBox=tk.Checkbutton(AdvancedOptionFrame,variable=ReplaceFileFlag)
        ReplaceFileCheckBox.grid(row=1,column=1)


        def OK_CMD():
            #print(LoopMax.get())
            AdvancedOptionMenu.destroy()
        def Cancel_CMD():
            LoopMax.set(temp)
            AdvancedOptionMenu.destroy()
        def Apply_CMD():
            #print(LoopMax.get())
            pass

        ButtonsFrame=tk.Frame(AdvancedOptionFrame)
        ButtonsFrame.grid(row=2,column=1)
        OKButton=tk.Button(ButtonsFrame,text="OK",command=OK_CMD)
        OKButton.grid(row=0,column=0)
        CancelButton=tk.Button(ButtonsFrame,text="キャンセル",command=Cancel_CMD)
        CancelButton.grid(row=0,column=1)
        ApplyButton=tk.Button(ButtonsFrame,text="適用",command=Apply_CMD)
        ApplyButton.grid(row=0,column=2)

    menu_file=tk.Menu(root)
    menu_edit=tk.Menu(root)
    menu.add_cascade(label="ファイル",menu=menu_file)
    menu_file.add_command(label="新規",command=ClearAll)
    menu_file.add_command(label="閉じる",command=ExitApplication)
    menu.add_cascade(label="編集",menu=menu_edit)
    menu_edit.add_command(label="上級者向け設定",command=AdvancedOption)


    MainFrame=tk.Frame(root)
    MainFrame.grid(row=0,column=0)
    
    FileFrame=tk.Frame(MainFrame)
    FileFrame.grid(row=0,column=0,columnspan=2)
    FileNameLabel=tk.Label(FileFrame,text="入力ファイル:")
    FileNameLabel.grid(row=0,column=0)
    FilePass=tk.StringVar()
    FileEntry=tk.Entry(FileFrame,textvariable=FilePass,width=80)
    FileEntry.grid(row=0,column=1)
    ClearButton=tk.Button(FileFrame,text="×",command=lambda:FileEntry.delete(0,tk.END))
    ClearButton.grid(row=0,column=2)
    def inputFilePass():
        FilePass.set(filedialog.askopenfilename(filetypes=[('テキストファイル','*.txt')]))
        #print(FilePass.get())
    isExists=tk.BooleanVar()
    isExistsStr=tk.StringVar()
    def CheckFileExists():
        isExists.set(os.path.exists(FilePass.get()))
        if isExists.get():
            isExistsStr.set("ファイルは存在しています")
        else:
            isExistsStr.set("そのパスにファイルは存在していません")
        #print(FilePass.get())
        #print(isExists)
    isExistsLabel=tk.Label(FileFrame,text="ファイルの存在有無")
    isExistsLabel.grid(row=1,column=0)
    isExistsEntry=tk.Entry(FileFrame,textvariable=isExistsStr,state="readonly",width=80)
    isExistsEntry.grid(row=1,column=1)
    FileDialogButton=tk.Button(FileFrame,command=inputFilePass,text="ファイルを選択")
    FileDialogButton.grid(row=0,column=3)
    
    RegexFrame=tk.Frame(MainFrame)
    RegexFrame.grid(row=1,column=0)
    Regex=tk.StringVar()
    Checker=tk.StringVar()
    Regexflag=tk.BooleanVar()
    def ErrorCheck():
        reg=Regex.get()
        try:
            #print(str(reg))
            re.compile(str(reg))
        except re.error as e:
            Regexflag.set(False)
            s=e
        else:
            Regexflag.set(True)
            s="なし"
        finally:
            #print(s)
            #print(Regexflag.get())
            Checker.set(s)
    RegexLabel=tk.Label(RegexFrame,text="正規表現:")
    RegexLabel.grid(row=0,column=0)
    RegexEntry=tk.Entry(RegexFrame,textvariable=Regex,width=25)
    RegexEntry.grid(row=0,column=1)
    RegexErrorLabel=tk.Label(RegexFrame,text="正規表現エラー:")
    RegexErrorLabel.grid(row=1,column=0)
    RegexErrorChecker=tk.Entry(RegexFrame,state="readonly",textvariable=Checker,width=25)
    RegexErrorChecker.grid(row=1,column=1)

    ReplaceFrame=tk.Frame(MainFrame)
    ReplaceFrame.grid(row=1,column=1)
    ReplaceLabel=tk.Label(ReplaceFrame,text="置換後の文字列:")
    ReplaceLabel.grid(row=0,column=0)
    Replace=tk.StringVar()
    ReplaceEntry=tk.Entry(ReplaceFrame,textvariable=Replace,width=25)
    ReplaceEntry.grid(row=0,column=1)
    Replaced=tk.StringVar()
    def ReplaceCMD():
        Replaced.set(Replace.get())
    ReplacedLabel=tk.Label(ReplaceFrame,text="適用済みの文字列")
    ReplacedLabel.grid(row=1,column=0)
    ReplacedEntry=tk.Entry(ReplaceFrame,textvariable=Replaced,state="readonly",width=25)
    ReplacedEntry.grid(row=1,column=1)


    RunningFrame=tk.Frame(MainFrame)
    RunningFrame.grid(row=2,column=0)
    def RunningCMD():
        f=codecs.open('temp',"w")
        f.write("args:{\n"+\
                "\ttargetPass:\""+FilePass.get()+"\"\n"+\
                "\tregex:\""+Regex.get()+"\"\n"\
                "\treplacedText:\""+Replaced.get()+"\"\n"+\
                "\tLoopMax:"+str(LoopMax.get())+"\n"+\
                "\tReplaceFile:"+str(ReplaceFileFlag.get())+"\n"+\
                "}")
        f.close()
        subprocess.run(args=[os.getcwd()+'/Replacer'])
        msg.showinfo(title="処理完了",message="処理が終了しました")
    RunningButton=tk.Button(RunningFrame,text="Run",command=RunningCMD,height=2,width=40)
    RunningButton.grid(row=0,column=0)

    ErrorLabelsFrame=tk.Frame(RunningFrame)
    ErrorLabelsFrame.grid(row=0,column=1)
    hasErrorLabel=tk.Label(ErrorLabelsFrame,text="正規表現のエラーを確認してください")
    isNotExistsLabel=tk.Label(ErrorLabelsFrame,text="ファイルパスが不正です")

    def CanRunning():
        ErrorCheck()
        CheckFileExists()
        ReplaceCMD()
        flag=Regexflag.get()
        RunningButton["state"]="normal"
        if flag==False:
            hasErrorLabel.grid(row=0,column=0)
            RunningButton["state"]="disable"   
        else:
            hasErrorLabel.grid_forget()
        if isExists.get()==False:
            isNotExistsLabel.grid(row=1,column=0)
            RunningButton["state"]="disable"
        else:
            isNotExistsLabel.grid_forget()
        root.after(1,CanRunning)

    CanRunning()

    root.mainloop()



if __name__ =="__main__":
    main()