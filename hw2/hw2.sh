"hw2.sh" 52L, 1569C written
bsd1 [/u/cs/105/0516073] -lin0516073- cat hw2.sh
#!/bin/sh


input(){
	ID=$(dialog --title "Student ID" --inputbox "Please input the student ID:"  10 40 --output-fd 1)
	PW=$(dialog --title "PassWord" --insecure --passwordbox "Please input the Password:"  10 40 --output-fd 1)
    dialog --clear
}
#=========================================
getcode(){
    garbage=$(curl -s -D 0.cookie https://portal.nctu.edu.tw/captcha/pic.php)
    curl -s -b 0.cookie -D 1.cookie -o tmp.png https://portal.nctu.edu.tw/captcha/pitctest/pic.php

    code=$(curl -s -F 'image=@tmp.png' https://nasa.cs.nctu.edu.tw/sap/2017/hw2/captcha-solver/api/)
}
#========================================
goin(){
    re=$(curl -b 0.cookie -D 2.cookie -d "username=$ID&password=$PW&seccode=$code&Submit2=登入(Login)&pwdtype=static" https://portal.nctu.edu.tw/portal/chkpas.php?)

}

#========================================
allin(){
	rm *.cookie
    getcode;
    goin;
    rm tmp.png
    case $re in
		*"replace"*)
	   		allin;
        ;;
		*"login"*)
			dialog --title "Worng ID or Worng PW" --msgbox "Worng ID or PW\nYou need to try again" 10 40;
			input;
			allin;
		;;
        *)
             clear;
             echo "";
             echo login success
        ;;
    esac
}
#========================================
getad(){
    tmp=$(curl -s -b 0.cookie -D 3.cookie 'https://portal.nctu.edu.tw/portal/relay.php?D=cos' | node extractFormdata.js)
	curl -s -b 3.cookie -d $tmp -D 4.cookie https://course.nctu.edu.tw/index.asp | iconv -f big5 -t utf-8
	curl -s -b 4.cookie  https://course.nctu.edu.tw/index.asp | iconv -f big5 -t utf-8
	clear;
    curl  -b 4.cookie https://course.nctu.edu.tw/adSchedule.asp | iconv -f big5 -t utf-8 | awk 'BEGIN{cnt=0} {if($0 ~ /[^<table>]<br>/){if(cnt % 7 == 0){printf("AnewLine%d\n",cnt/7);} printf("%s\n",$0); cnt=cnt+1;}if($0 ~ /&nbsp/){if(cnt %7==0 )printf("AnewLine%d\n",cnt/7); printf(".\n");cnt++}}' | sed 's/<br>//' | sed 's/	//g' | sed 's///g' | sed 's/ //g' | awk 'BEGIN{cnt=0;printf("Monday Tuesday Wednesday Thursday Friday Saturday Sunday\n")} {if(cnt % 8 == 0)printf("\n"); else printf("%s ",$0); cnt++;} END{printf("\n")}' | column -t

}
#========================================
input;
allin;
getad;

rm *.cookie

