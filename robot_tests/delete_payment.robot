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
Delete Payment
    Create Session  mysession  ${base_url}
    ${headers}=  Create Dictionary  Authorization=${basic_auth}  Content-Type=application/json
    ${body}=  Create Dictionary  purchase=${145}  amount=${100}  currency=USD
    ${body_json}=  json.Dumps  ${body}
    PUT On Session  mysession  ${base_path}  headers=${headers}  data=${body_json}

    ${get_response}=  GET On Session  mysession  ${base_path}  headers=${headers}
    ${get_response_json}=  json.Loads  ${get_response.content}
    ${all_payments}=  Get From Dictionary  ${get_response_json}  payments
    ${created_payment}=  Get From List  ${all_payments}  -1
    ${created_payment_id}=  Get From List  ${created_payment}  0
    Log To Console  paymentId: ${created_payment_id}

    ${delete_response}=  DELETE On Session  mysession  ${base_path}/${created_payment_id}  headers=${headers}
    ${delete_status_code}=  Convert To String  ${delete_response.status_code}
    ${delete_response_json}=  json.Loads  ${delete_response.content}
    ${number_of_deleted_payments}=  Get From Dictionary  ${delete_response_json}  deleted
    Should Be Equal	 ${delete_status_code}  200
    Should Be Equal As Integers  ${number_of_deleted_payments}  1

    ${new_get_response}=  GET On Session  mysession  ${base_path}  headers=${headers}
    ${new_get_response_json}=  json.Loads  ${new_get_response.content}
    ${new_payments}=  Get From Dictionary  ${new_get_response_json}  payments
    ${last_payment}=  Get From List  ${new_payments}  -1
    ${last_payment_id}=  Get From List  ${last_payment}  0
    Should Not Be Equal As Integers  ${last_payment_id}  ${created_payment_id}
