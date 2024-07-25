# dmrid-contactlist-converter
Python3 scripts for DMR radio contactlists

Should get latest dmr-id contacts from radioid.net, Ukraine only
Then convert contacts to .csv radio specific format

Some users has ciryllic in names, but most of radios can't show it correctly
So, this script just transliterate ciryllic  

Current radio:  
**Anytone 878 UV II plus**

# Requirements  

1. Install Python3  
2. Install requests library  
`pip install requests`  
`pip install transliterate`  

# How to use  

Just run script 
`python3 converter.py`  

Contact list will be saved to file with current timestamp  
