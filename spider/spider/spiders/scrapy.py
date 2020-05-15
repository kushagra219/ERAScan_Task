import scrapy
import urllib.request as urllib3
from urllib.parse import urljoin

class ParivahanSpider(scrapy.Spider):
    name = 'parivahan'
    start_urls = ['https://parivahan.gov.in/rcdlstatus/?pur_cd=101']
    download_delay = 1.5

    def parse(self, response):
        dl_no = input("Enter DL no.: ")
        view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/@value').get()
        img_rel_url = response.selector.xpath('//*[@id="form_rcdl:j_idt34:j_idt41"]/@src').get()
        yield scrapy.FormRequest(
            'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
            formdata={
                'javax.faces.partial.ajax': 'true',
                'javax.faces.source': 'form_rcdl:tf_dlNO',
                'javax.faces.partial.execute': 'form_rcdl:tf_dlNO',
                'javax.faces.partial.render': 'form_rcdl:tf_dlNO',
                'javax.faces.behavior.event': 'valueChange',
                'javax.faces.partial.event': 'change',
                'form_rcdl': 'form_rcdl',
                'form_rcdl:tf_dlNO': dl_no,
                # form_rcdl:tf_dob_input: 
                # form_rcdl:j_idt34:CaptchaID:
                'javax.faces.ViewState:': view_state
            },
            callback=self.parse_dob, meta={'dl_no':dl_no, 'img_rel_url':img_rel_url}
        )

    def parse_dob(self, response):
        dob = input("Enter DOB (DD-MM-YYYY): ")
        view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
        dl_no = response.meta.get('dl_no')
        img_rel_url = response.meta.get('img_rel_url')
        yield scrapy.FormRequest(
            'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
            formdata={
                'javax.faces.partial.ajax': 'true',
                'javax.faces.source: form_rcdl':'tf_dob',
                'javax.faces.partial.execute': 'form_rcdl:tf_dob',
                'javax.faces.partial.render: form_rcdl':'tf_dob',
                'javax.faces.behavior.event': 'valueChange',
                'javax.faces.partial.event': 'change',
                'form_rcdl:tf_dob_input': dob,
                'javax.faces.ViewState': view_state
            },
            callback=self.parse_captcha, meta={'dl_no':dl_no, 'dob':dob, 'img_rel_url':img_rel_url}
        )

    def parse_captcha(self, response):
        dl_no = response.meta.get('dl_no')
        dob = response.meta.get('dob')
        img_rel_url = str(response.meta.get('img_rel_url'))
        img_url = urljoin("https://parivahan.gov.in", img_rel_url)
        urllib3.urlretrieve(img_url, "captcha.jpg")
        captcha = input("Enter captcha: ")
        view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
        yield scrapy.FormRequest(
            'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
            formdata={
                'form_rcdl': 'form_rcdl',
                'form_rcdl:tf_dlNO': dl_no,
                'form_rcdl:tf_dob_input': dob,
                'form_rcdl:j_idt34:CaptchaID': captcha,
                'javax.faces.ViewState': view_state,
                'javax.faces.source': 'form_rcdl:j_idt34:CaptchaID',
                'javax.faces.partial.event': 'blur',
                'javax.faces.partial.execute': 'form_rcdl:j_idt34:CaptchaID',
                'javax.faces.partial.render': 'form_rcdl:j_idt34:CaptchaID',
                'CLIENT_BEHAVIOR_RENDERING_MODE': 'OBSTRUSIVE',
                'javax.faces.behavior.event': 'blur',
                'javax.faces.partial.ajax': 'true'
            },
            callback=self.parse_final, meta = {'dl_no':dl_no, 'dob':dob, 'captcha':captcha}
        )

    def parse_final(self, response):
        dl_no = response.meta.get('dl_no')
        dob = response.meta.get('dob')
        captcha = response.meta.get('captcha')
        view_state = response.selector.xpath('//*[@id="j_id1:javax.faces.ViewState:0"]/text()').get()
        yield scrapy.FormRequest(
            'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml',
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
            'javax.faces.ViewState': view_state
        }, 
        callback=self.parse_result
    ) 

    def parse_result(self, response):
        print(response.text)
        yield {

        }