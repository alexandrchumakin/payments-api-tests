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
Process Payments
    Create Session  mysession  ${base_url}
    ${headers}=  Create Dictionary  Authorization=${basic_auth}  Content-Type=application/json
    ${body}=  Create Dictionary  purchase=${145}  amount=${100}  currency=USD
    ${body_json}=  json.Dumps  ${body}
    PUT On Session  mysession  ${base_path}  headers=${headers}  data=${body_json}

    ${get_response}=  GET On Session  mysession  ${base_path}  headers=${headers}
    ${get_response_json}=  json.Loads  ${get_response.content}
    ${all_payments}=  Get From Dictionary  ${get_response_json}  payments
    ${created_payment}=  Get From List  ${all_payments}  -1
    ${created_payment_proc_status}=  Get From List  ${created_payment}  -1
    Should Be Equal As Integers	 ${created_payment_proc_status}  0

    ${process_response}=  POST On Session  mysession  ${base_path}  headers=${headers}
    ${process_status_code}=  Convert To String  ${process_response.status_code}
    ${process_response_json}=  json.Loads  ${process_response.content}
    ${number_of_processed_payments}=  Get From Dictionary  ${process_response_json}  processed
    Should Be Equal	 ${process_status_code}  200
    Should Be True  ${number_of_processed_payments}

    ${new_get_response}=  GET On Session  mysession  ${base_path}  headers=${headers}
    ${new_get_response_json}=  json.Loads  ${new_get_response.content}
    ${processed_payments}=  Get From Dictionary  ${new_get_response_json}  payments
    ${processed_payment}=  Get From List  ${processed_payments}  -1
    ${processed_payment_proc_status}=  Get From List  ${processed_payment}  -1
    Should Be Equal As Integers	 ${processed_payment_proc_status}  1
