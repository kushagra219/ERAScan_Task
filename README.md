# ERAScan_Task

Submission And Extraction of DL Status Form Data from <a>https://parivahan.gov.in/rcdlstatus/?pur_cd=101</a> 

# Python Libraries Used - 
* Scrapy
* Beautiful Soup

# How does it work - 
* Clone this repository.
* Open it in terminal and run the following command - 
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
   * Input captcha text from the image generated in EraScan_Task/captcha.jpg as shown below - 
      ~~~ 
          Enter captcha:
      ~~~
      <img src="https://github.com/kushagra219/ERAScan_Task/blob/master/captcha.jpg">
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
      
