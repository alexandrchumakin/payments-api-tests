*** Settings ***
Library           String
Library           Collections
Library           RequestsLibrary
Library           json


*** Variables ***
${base_url}               http://localhost:5000
${basic_auth}             Basic am9objpqb2hu
${base_path}              /finance/api/v1.0/payments


*** Test Cases ***
Create Payment
    Create Session  mysession  ${base_url}
    ${headers}=  Create Dictionary  Authorization=${basic_auth}  Content-Type=application/json
    ${body}=  Create Dictionary  purchase=${301}  amount=${12}  currency=EUR
    ${body_json}=  json.Dumps  ${body}
    ${response}=  PUT On Session  mysession  ${base_path}  headers=${headers}  data=${body_json}
    ${status_code}=  Convert To String  ${response.status_code}
    ${response_json}=  json.Loads  ${response.content}
    ${created_status}=  Get From Dictionary  ${response_json}  created
    Should Be Equal	 ${status_code}  200
    Should Be Equal As Integers	 ${created_status}  1
