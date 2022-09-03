*** Settings ***
Library           String
Library           Collections
Library           RequestsLibrary


*** Variables ***
${base_url}               http://localhost:5000
${basic_auth}             Basic am9objpqb2hu
${base_path}              /finance/api/v1.0/payments


*** Test Cases ***
Get Payments
    Create Session  mysession  ${base_url}
    ${headers}=  Create Dictionary  Authorization=${basic_auth}  Content-Type=application/json
    ${response}=  GET On Session  mysession  ${base_path}  headers=${headers}
    ${status_code}=  Convert To String  ${response.status_code}
    Should Be Equal	 ${status_code}  200
    Should Be True	${response.content}
