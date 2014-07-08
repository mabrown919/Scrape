#!/bin/bash
#default IFS assignment: IFS=$' \t\n'
fn=$1
echo "Processing $1..."
dump1=`pdftk "$1" dump_data_fields | sed 's,---,''\|'',g'`
oldIFS=$IFS
key=
value=
IFS='\|'
for i in $dump1; do
	#echo "i is: $i"
	IFS=$'\n'
	for j in $i; do
		if [[ "$j" =~ ^FieldName:.* ]]; then
			key=`echo $j | cut -d " " -f 2-`
		fi
		if [[ "$j" =~ ^FieldValue:.* ]]; then
			value=`echo $j | cut -d " " -f 2-`
		fi
	done
	key=${key// /}	#i need to remove "^#, ?$, ^%, -"; change key "990" to "Form990"; change value "(choose %)" to "NULL"; Change key "%BoardDonations" to "BoardDonations"; change XtoX(Totla|) to gift-- NVM, exclude this as it's Financial
	key=`echo "${key}" | sed 's,%,Percent,'`				# handle the %-sign in front of the fieldname
	key=`echo "${key}" | sed 's,^990,Form990,'`		# handle the 990->Form990
	key=`echo "${key}" | sed -E 's,^[1-5]{1}\.?([a-zA-Z]+)\?,\1,'`	# handle the numbers in front of fieldname & '?' at the end of the fieldname
	key=`echo "${key}" | sed -E 's/(^[1-5]{1,6})(to)?([0-9]{3,5})?(Total)?/giftSize\1\2\3\4/'`
	if [ -z "$value" ]; then
		value="NULL"
	fi	
	if [ -n "$key" ]; then
		value=`echo "${value}" | sed -E 's/\(Choose \%\)/NULL/'`
		echo "$key:$value" >> "${fn}".txt
	fi
	key=""
	value=""
	IFS=$'\n'
IFS='\|'
done
IFS=$oldIFS
