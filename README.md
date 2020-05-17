# ERAScan_Task

Submission And Extraction of DL Status Form Data from <a>https://parivahan.gov.in/rcdlstatus/?pur_cd=101</a> <strong> bypassing CAPTCHA
</strong>

## Python Libraries Used - 
* Scrapy
* Beautiful Soup

## How does it work - 
* Clone this repository.
* Set up a python virtual environment and activate it in your terminal. (Refer - <a>https://docs.python.org/3/tutorial/venv.html</a>)
* Open it in terminal and run the following command - 
  * ~~~ 
        pip install -r requirements.txt
    ~~~
  * ~~~ 
        scrapy crawl parivahan
    ~~~
  * Input your driving license no. when it prompts 
      ~~~ 
          Enter DL no.:
      ~~~
  * Input your DOB when it prompts 
      ~~~ 
          Enter DOB: 
      ~~~
  * The result will be printed in the terminal in raw form but of the format 
      ```javascript 
        {
            'Current_Status': 'ACTIVE',
            'Holder_Name': 'ANURAG           BREJA',
            'Date_Of_Issue': '01-Mar-2011',
            'Last_Trans_At': 'ZONAL OFFICE, WEST DELHI, JANAKPURI',
            'Old/New_DL_No': 'DL-0420110149646',
            'validity':
                {
                    'Non-Transport': 
                        {
                            'From': '01-Mar-2011', 
                            'To': '08-Feb-2026'
                        }, 
                    'Transport':
                        {
                            'From': 'NA',
                            'To': 'NA'
                        },
                    'Hazardous_Valid_Till': 'NA',
                    'Hill_Valid_Till': 'NA'
                },
            'class_vehicle': 
                {
                    'COV_Category': 'NT',
                    'Class_Vehicle': 'ADPVEH',
                    'COV_Issue_Date': '01-Mar-2011'
                }
        }
    ```

## Reference Links
* https://docs.scrapy.org/en/latest/
* http://xpather.com/
* https://readthedocs.org/projects/beautiful-soup-4/
* https://github.com/madmaze/pytesseract
