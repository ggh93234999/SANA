ls -ARl | awk '{if ($5 != "")print $1," ",$5," ",$9}' | sort -n -k 2,2 -r | awk 'BEGIN{dir=fil=tot=cnt=0}{if(cnt++<5)printf("%d:%d %s\n",cnt,$2,$3); if( $1 ~ /^d/ ) dir++; else {fil++;tot+=$2}} END{printf("Dir num: %d\nFile num: %d\nTotal: %d\n",dir,fil,tot)}'