import scrapy
import urllib.request as urllib3
from urllib.parse import urljoin
import bs4
from scrapy.selector import Selector

class ParivahanSpider(scrapy.Spider):
    name = 'parivahan'
    start_urls = ['https://parivahan.gov.in/rcdlstatus/?pur_cd=101']
    download_delay = 1.5

    def parse(self, response):
        dl_no = input("Enter DL no.: ")
        dob = input("Enter DOB (DD-MM-YYYY): ")
        img_rel_url = response.selector.xpath('//*[@id="form_rcdl:j_idt34:j_idt41"]/@src').get()
        img_url = urljoin("https://parivahan.gov.in", img_rel_url)
        urllib3.urlretrieve(img_url, "captcha.jpg")
        captcha = input("Enter captcha: ")
        yield scrapy.FormRequest.from_response(
            response,
            # 'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
            formdata={
            'javax.faces.partial.ajax': 'true',
            'javax.faces.source: form_rcdl':'j_idt46',
            'javax.faces.partial.execute': '@all',
            'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
            'form_rcdl:j_idt46: form_rcdl':'j_idt46',
            'form_rcdl': 'form_rcdl',
            'form_rcdl:tf_dlNO': dl_no,
            'form_rcdl:tf_dob_input': dob,
            'form_rcdl:j_idt34:CaptchaID': captcha,
            },
            callback=self.parse_result, 
            # meta={'dl_no':dl_no, 'img_rel_url':img_rel_url}
        )

    def parse_result(self, response):
        doc_el = bs4.BeautifulSoup(response.text, 'xml')
        text = doc_el.find('update').text
        sel = Selector(text=text)
        data = {
                'Current_Status': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered'][1]/tr[1]/td[2]/span[1]/text()[1]").get(),
                'Holder_Name': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered'][1]/tr[2]/td[2]/text()[1]").get(),
                'Date_Of_Issue': sel.xpath("//tr[3]/td[2]/text()[1]").get(),
                'Last_Trans_At': sel.xpath("//tr[4]/td[2]/text()[1]").get(),
                'Old/New_DL_No': sel.xpath("//tr[5]/td[2]/text()[1]").get(),
                'validity' : {
                    'Non-Transport': {
                        'From': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table'][1]/tr[1]/td[2]/text()[1]").get(),
                        'To': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table'][1]/tr[1]/td[3]/text()[1]").get()
                    },
                    'Transport': {
                        'From': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table'][1]/tr[2]/td[2]/text()[1]").get(),
                        'To': sel.xpath("//tr[2]/td[3]/text()[1]").get()
                    },
                    'Hazardous_Valid_Till': sel.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table'][2]/tr[1]/td[2]/text()[1]").get(),
                    'Hill_Valid_Till': sel.xpath("//td[4]/text()[1]").get()
                },
                'class_vehicle': {
                    'COV_Category': sel.xpath("//tr[@class='ui-widget-content ui-datatable-even'][1]/td[1]/text()[1]").get(),
                    'Class_Vehicle': sel.xpath("//tr[@class='ui-widget-content ui-datatable-even'][1]/td[2]/text()[1]").get(),
                    'COV_Issue_Date': sel.xpath("//tr[@class='ui-widget-content ui-datatable-even'][1]/td[3]/text()[1]").get()
                }
        }
        print(data)
    
    
### OTHER APPROACH ###

    # def parse(self, response):
    #     dl_no = input("Enter DL no.: ")
    #     view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()
    #     img_rel_url = response.selector.xpath('//*[@id="form_rcdl:j_idt34:j_idt41"]/@src').get()
    #     jsession_id = response.selector.xpath('//*[@id="form_rcdl"]/@action').get()
    #     print(jsession_id)
    #     jsession_id = jsession_id.split('=')[1]
    #     print('JSESSIONID={}; has_js=1'.format(jsession_id))
    #     headers = {
    #         # 'Accept': 'application/xml, text/xml, */*; q=0.01',
    #         # 'Accept-Encoding': 'gzip, deflate, br',
    #         # 'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,mt;q=0.7',
    #         # 'Connection': 'keep-alive',
    #         # 'Content-Length': 2654,
    #         # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #         'Cookie': 'JSESSIONID={}; has_js=1'.format(jsession_id),
    #         # 'Faces-Request': 'partial/ajax',
    #         # 'Host': 'parivahan.gov.in',
    #         # 'Origin': 'https://parivahan.gov.in',
    #         # 'Referer': 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101',
    #         # 'Sec-Fetch-Dest': 'empty',
    #         # 'Sec-Fetch-Mode': 'cors',
    #         # 'Sec-Fetch-Site': 'same-origin',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    #         # 'X-Requested-With': 'XMLHttpRequest'
    #     }
    #     yield scrapy.FormRequest(
    #         'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
    #         formdata={
    #             'javax.faces.partial.ajax': 'true',
    #             'javax.faces.source': 'form_rcdl:tf_dlNO',
    #             'javax.faces.partial.execute': 'form_rcdl:tf_dlNO',
    #             'javax.faces.partial.render': 'form_rcdl:tf_dlNO',
    #             'javax.faces.behavior.event': 'valueChange',
    #             'javax.faces.partial.event': 'change',
    #             'form_rcdl': 'form_rcdl',
    #             'form_rcdl:tf_dlNO': dl_no,
    #             'form_rcdl:tf_dob_input': '',
    #             'form_rcdl:j_idt34:CaptchaID': '',
    #             'javax.faces.ViewState:': view_state
    #         },
    #         callback=self.parse_dob, meta={'dl_no':dl_no, 'img_rel_url':img_rel_url, 'headers':headers}, headers=headers
    #     )

    # def parse_dob(self, response):
    #     dob = input("Enter DOB (DD-MM-YYYY): ")
    #     view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
    #     dl_no = response.meta.get('dl_no')
    #     img_rel_url = response.meta.get('img_rel_url')
    #     headers = response.meta.get('headers')
    #     yield scrapy.FormRequest(
    #         'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
    #         formdata={
    #             'javax.faces.partial.ajax': 'true',
    #             'javax.faces.source: form_rcdl':'tf_dob',
    #             'javax.faces.partial.execute': 'form_rcdl:tf_dob',
    #             'javax.faces.partial.render: form_rcdl':'tf_dob',
    #             'javax.faces.behavior.event': 'valueChange',
    #             'javax.faces.partial.event': 'change',
    #             'form_rcdl:tf_dob_input': dob,
    #             'javax.faces.ViewState': view_state
    #         },
    #         callback=self.parse_captcha, meta={'dl_no':dl_no, 'dob':dob, 'img_rel_url':img_rel_url, 'headers':headers}, headers=headers
    #     )

    # def parse_captcha(self, response):
    #     dl_no = response.meta.get('dl_no')
    #     dob = response.meta.get('dob')
    #     img_rel_url = str(response.meta.get('img_rel_url'))
    #     img_url = urljoin("https://parivahan.gov.in", img_rel_url)
    #     urllib3.urlretrieve(img_url, "captcha.jpg")
    #     captcha = input("Enter captcha: ")
    #     headers = response.meta.get('headers')
    #     view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
    #     yield scrapy.FormRequest(
    #         'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
    #         formdata={
    #             'form_rcdl': 'form_rcdl',
    #             'form_rcdl:tf_dlNO': dl_no,
    #             'form_rcdl:tf_dob_input': dob,
    #             'form_rcdl:j_idt34:CaptchaID': captcha,
    #             'javax.faces.ViewState': view_state,
    #             'javax.faces.source': 'form_rcdl:j_idt34:CaptchaID',
    #             'javax.faces.partial.event': 'blur',
    #             'javax.faces.partial.execute': 'form_rcdl:j_idt34:CaptchaID',
    #             'javax.faces.partial.render': 'form_rcdl:j_idt34:CaptchaID',
    #             'CLIENT_BEHAVIOR_RENDERING_MODE': 'OBSTRUSIVE',
    #             'javax.faces.behavior.event': 'blur',
    #             'javax.faces.partial.ajax': 'true'
    #         },
    #         callback=self.parse_final, meta = {'dl_no':dl_no, 'dob':dob, 'captcha':captcha, 'headers':headers}, headers=headers
    #     )

    # def parse_final(self, response):
    #     dl_no = response.meta.get('dl_no')
    #     dob = response.meta.get('dob')
    #     captcha = response.meta.get('captcha')
    #     headers = response.meta.get('headers')
    #     view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
    #     yield scrapy.FormRequest(
    #         'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
    #         formdata={
    #         'javax.faces.partial.ajax': 'true',
    #         'javax.faces.source: form_rcdl':'j_idt46',
    #         'javax.faces.partial.execute': '@all',
    #         'javax.faces.partial.render': 'form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl',
    #         'form_rcdl:j_idt46: form_rcdl':'j_idt46',
    #         'form_rcdl': 'form_rcdl',
    #         'form_rcdl:tf_dlNO': dl_no,
    #         'form_rcdl:tf_dob_input': dob,
    #         'form_rcdl:j_idt34:CaptchaID': captcha,
    #         # 'javax.faces.ViewState': view_state
    #     }, 
    #     callback=self.parse_result
    # ) 