Feature: The promotions service back-end
    As a promotions developer
    I need a RESTful catalog service
    So that I can keep track of all my promotions

Background:
    Given the following promotions
        | Title       |  Code  |  Type      | Amount  |   Start      |  End        |  Is_Site_Wide | ProductID |
        | Promo1      |   C1   |  BOGO      |   50    |  2022-11-18  | 2023-11-18  |    True     |     1     |
        | Promo2      |   C2   |  DISCOUNT  |   20    |  2022-08-13  | 2023-08-13  |    False    |    2      | 
        | Promo3      |   C3   |  FIXED     |   10    |  2022-04-01  | 2023-04-01  |    False    |     3     |
        | Promo4      |   C4   |  BOGO      |   50    |  2022-06-04  | 2023-06-04  |    True     |     4     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotions Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "Title" to "Promo5"
    And I set the "Code" to "C5"
    And I select "BOGO" in the "Type" dropdown
    And I set the "Amount" to "50"
    And I set the "Start" to "06-16-2022"
    And I set the "End" to "06-16-2023"
    And I select "True" in the "Is_Site_Wide" dropdown
    And I set the "Product ID" to "5"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    Then the "Code" field should be empty
    And the "Title" field should be empty
    And the "Type" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Promo5" in the "Title" field
    And I should see "C5" in the "Code" field
    And I should see "BOGO" in the "Type" dropdown
    And I should see "50" in the "Amount" field
    And I should see "2022-06-16" in the "Start" field
    And I should see "2023-06-16" in the "End" field
    And I should see "True" in the "Is_Site_Wide" dropdown
    And I should see "5" in the "Product ID" field

Scenario: GET a Promotion
    When I visit the "Home Page"
    And I set the "Title" to "Promo7"
    And I set the "Code" to "C7"
    And I select "FIXED" in the "Type" dropdown
    And I set the "Amount" to "70"
    And I set the "Start" to "07-17-2022"
    And I set the "End" to "07-17-2023"
    And I select "False" in the "Is_Site_Wide" dropdown
    And I set the "Product ID" to "97"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    Then the "Code" field should be empty
    And the "Title" field should be empty
    And the "Type" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Promo7" in the "Title" field
    And I should see "C7" in the "Code" field
    And I should see "FIXED" in the "Type" dropdown
    And I should see "70" in the "Amount" field
    And I should see "2022-07-17" in the "Start" field
    And I should see "2023-07-17" in the "End" field
    And I should see "False" in the "Is_Site_Wide" dropdown
    And I should see "97" in the "Product ID" field

Scenario: UPDATE a Promotion
    When I visit the "Home Page"
    And I set the "Title" to "Promo1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Promo1" in the "Title" field
    And I should see "C1" in the "Code" field
    And I should see "BOGO" in the "Type" dropdown
    And I should see "50" in the "Amount" field
    And I should see "2022-11-18" in the "Start" field
    And I should see "2023-11-18" in the "End" field
    And I should see "True" in the "Is_Site_Wide" dropdown
    And I should see "1" in the "Product ID" field
    When I change "Code" to "D94"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "D94" in the "Code" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "D94" in the results
    And I should not see "C1" in the results


Scenario: Delete a Promotion
    When I visit the "Home Page"
    And I set the "Title" to "Promo7"
    And I set the "Code" to "C7"
    And I select "FIXED" in the "Type" dropdown
    And I set the "Amount" to "70"
    And I set the "Start" to "07-17-2022"
    And I set the "End" to "07-17-2023"
    And I select "False" in the "Is_Site_Wide" dropdown
    And I set the "Product ID" to "97"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    Then the "Code" field should be empty
    And the "Title" field should be empty
    And the "Type" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Promotion has been Deleted!"
    

Scenario: List all Promotion
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see the message "Success"
    And the promotions table should be populated
    
Scenario: Activate a Promotion
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Title" to "Promo2"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "False" in the "Is_Site_Wide" dropdown
    When I press the "Activate" button
    Then I should see the message "Promotion has been Activated!"

Scenario: Deactivate a Promotion
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Title" to "Promo1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "True" in the "Is_Site_Wide" dropdown
    When I press the "Deactivate" button
    Then I should see the message "Promotion has been Deactivated!"

Scenario: Search by Promotion Code
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Code" to "C2"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "False" in the "Is_Site_Wide" dropdown
    And I should see "20" in the "Amount" field
