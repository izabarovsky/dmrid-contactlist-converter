# dmrid-contactlist-converter
Python3 scripts for DMR radio contactlists

Should get latest dmr-id contacts from radioid.net
Then convert contacts to .csv radio specific format

Some users has ciryllic in names, but most of radios can't show it correctly
So, this script just transliterate ciryllic  

Current radio tested:  
**Anytone 878 UV II plus**

## How to use for Anytone

Just run script  
`python3 anytone-converter.py`  

Contact list will be saved to file with current timestamp  
 `YYYYMMDD-hhmmss-anytone-contacts.csv`

## How to use for Motorola & Hytera

1. Generate simple contacts:  
`python3 simple-converter.py`

2. Export contacts from mototrbo or hytera cps, usually is .xlx format

3. Copy contacts from list, generated in step 1, into .xlx exported 

4. Import .xlx into radio

Just run script  
`python3 anytone-converter.py`  

Contact list will be saved to file with current timestamp  
 `YYYYMMDD-hhmmss-anytone-contacts.csv`  

## Countries filter

If necessary, open script `xxx-converter.py` and put required countries in variable `DMR_COUNTRIES_FILTER`  
If you wish all of them, put wildcard `%`  

## Requirements  

1. Install Python3  
2. Install requests library  
`pip3 install requests`
3. Install dataclass_wizard library  
`pip3 install dataclass_wizard`

## K2 aliases

K2 is local Kyiv repeater
If you don't know what is that, just forget

If you put `k2_call_signs.csv` file with K2 local callsigns into script directory,
script automatically replace usernames with k2-alias  (format `K2-<alias>`)  
