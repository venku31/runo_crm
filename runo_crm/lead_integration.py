import frappe
from datetime import datetime
from frappe.utils import add_to_date
import requests

@frappe.whitelist()
def get_lead_from_runo():
    headers = {'Auth-Key': 'c24wMHJ5MzhueGh0MXcyNA=='}
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday_date= add_to_date(today,days=-1,as_string=True)
    url = f"https://api.runo.in/v1/crm/interactions?pageNo=1&date={yesterday_date}"
    response = frappe.parse_json((requests.request("GET", url, headers=headers)).text)
    if response.get('data'):

        if response.get('data').get('data'):
            data=response.get('data').get('data')
            for lead in data:
                
                for user_field in lead.get('userFields'):
                    if user_field.get('name') == "Source":
                        lead_source=user_field.get('value')
                
                notes=""
                lead_name= str(lead.get('customer').get('name')).replace(" ","")
                phone_no= lead.get('customer').get('phoneNumber')
                email= lead.get('customer').get('email') if lead.get('customer').get('email') else ''
                
                company_details= lead.get('customer').get('company')
                company_name = company_details.get('name') if company_details.get('name') else ''
                
                item_name=str(company_details.get('kdm').get('phoneNumber')).replace(" ","")
                qty= str(company_details.get('kdm').get('name')).replace(" ","")
                lead_name_with_qty= str(lead_name).lower().replace(str(item_name).lower(),'')
                notes= notes+f"Item Name:{company_details.get('kdm').get('phoneNumber')} <br>"+ f"Qty:{qty}"
                if lead.get('notes'):
                    notes= notes+f"<br>Notes: {lead.get('notes')}"

                lead_name=(lead_name_with_qty.replace(str(qty).lower(),'')).title()
                lead_args={'doctype':'Lead','lead_name':lead_name,'email_id':email,
                            'phone':phone_no,'company_name':company_name,'notes':notes,
                            'source':lead_source}
                lead_doc= frappe.get_doc(lead_args)
                lead_doc.insert()
                
                lead_address= {}
                address=company_details.get('address')
                if address.get('street'):
                    lead_address['address_line1']= address.get('street')
                    lead_address['address_title']= address.get('street') + " "
                if address.get('city'):
                    lead_address['city']= address.get('city')
                    lead_address['address_title']= str(lead_address.get('address_title')) if lead_address.get('address_title') else "" + address.get('city') + " "
                if address.get('state'):
                    lead_address['state']= address.get('state')
                if address.get('country'):
                    lead_address['country']= 'India'
                
                if lead_address:
                    lead_address.update({'doctype':'Address','address_type':'Billing','email_id':email,'phone':phone_no,
                                        'links':[{
                                                    'link_doctype':'Lead',
                                                    'link_name':lead_doc.name
                                            }]
                                        })
                    if not lead_address.get('address_line1'):
                        lead_address.update({'address_line1':lead_address.get('address_title')})
                    if not lead_address.get('city'):
                        lead_address.update({'city':lead_address.get('address_line1')})

                    address_doc=frappe.get_doc(lead_address)
                    address_doc.insert()
