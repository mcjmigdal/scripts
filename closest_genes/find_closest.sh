#!/bin/bash
#By Migdal 13.03.17
#Using bedtools closest tool finds number of closest genes also checks
#if gene lies in inter or intra gene region

if [ ! $GTF_FILE ]; then
	echo export GTF_FILE variable pointing to gtf file of interest
	exit 2 
fi


file=$1
echo $file | grep -q -e ".bed"
if [[ $? -gt 0 ]]; then
	echo $file | grep -e "bed"
	echo Need .bed file
	exit 3 
fi
	
amount=1
sortGTF=`awk '{ if ($3=="gene") {print $1"\t"$4"\t"$5"\t"$10"\t"$6"\t"$7} }' $GTF_FILE | sort -k1,1 -k2,2n`
OUT=`echo "$sortGTF" | bedtools closest -k $amount -t "first" -D ref -a $file -b stdin | awk '{ if ($6!=".") {print $0} }'`

#Print in correct format
echo 'chr,start,end,peak_name,-log10(qvalue),gene_name,strand,distance,inter/intra'
echo "$OUT" | awk 'BEGIN { OFS=","; } { if ( $12 == "0" ) {reg="intra"; print $1,$2,$3,$4,$5,$9,$11,$12,reg} else {reg="inter"; print $1,$2,$3,$4,$5,$9,$11,$12,reg} }' \
	    | sed -e 's/"//' -e 's/";//'

exit 0
