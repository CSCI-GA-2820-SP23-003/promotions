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
    And I select "False" in the "Is_Site_Wide" dropdown
    And I set the "ProductID" to "05"
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
    And I should see "False" in the "Is_Site_Wide" dropdown
    And I should see "05" in the "ProductID" field