# dmrid-contactlist-converter
Python3 scripts for DMR radio contactlists

Should get latest dmr-id contacts from radioid.net
Then convert contacts to .csv radio specific format

Some users has ciryllic in names, but most of radios can't show it correctly
So, this script just transliterate ciryllic  

Current radio tested:  
**Anytone 878 UV II plus**

## Countries filter

If necessary, open script `anyton-converter.py` and put required countries in variable `DMR_COUNTRIES_FILTER`  
If you wish all of them, put wildcard `%`  

## Requirements  

1. Install Python3  
2. Install requests library  
`pip install requests`  

## How to use  

Just run script 
`python3 anytone-converter.py`  

Contact list will be saved to file with current timestamp
 `YYYYMMDD-hhmmss-anytone-contacts.csv`  

## K2 aliases

K2 is local Kyiv repeater
If you don't know what is that, just forget

If you put `k2_call_signs.csv` file with K2 local callsigns into script directory,
script automatically replace usernames with k2-alias  (format `K2-<alias>`)  
