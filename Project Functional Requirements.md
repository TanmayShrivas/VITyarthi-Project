## Functional Requirements

Functional requirements describe what the system must do. They are derived directly from the menus and methods in Multi Card Atm.py.

ID	Requirement	Source in code

FR-01	The system shall create a card with holder name, 4-digit PIN, opening balance, and a unique 16-digit number.	ATMSystem.add\_card / generate\_card\_number

FR-02	The system shall list all cards with masked numbers (\*\*\*\* \*\*\*\* \*\*\*\* ####) and current balances.	list\_cards / 	Card.masked\_number

FR-03	The user shall select a card by full number or last 4 digits; if several cards share the last 4 digits, the 	system shall demand the full number.	find\_card\_by\_last4

FR-04	Login shall succeed only when the PIN matches; after 3 failures the user returns to the main menu.	select\_and\_login / Card.verify\_pin

FR-05	An authenticated user shall view the exact balance of the active card.	card\_session choice 1

FR-06	Deposit shall accept a positive amount, increase balance, and log the event.	Card.deposit

FR-07	Withdraw shall reject non-positive amounts and amounts greater than balance; a failed withdraw is still 	logged.	Card.withdraw

FR-08	Mini-statement shall show the last 5 transactions newest-first, or a no-history message.	show\_mini\_statement / HISTORY\_LIMIT

FR-09	Change PIN shall require the current PIN and a new PIN of exactly 4 digits.	Card.change\_pin

FR-10	The user shall switch to another card or logout without losing other cards in memory.	card\_session choices 	6 and 7

FR-11	Delete shall require confirmation (y) and shall clear active\_card if that card was logged in.	delete\_card

FR-12	Save \& Exit shall write every card (including PIN, balance, history) to atm\_cards.json.	save\_data / to\_dict

FR-13	On startup the system shall load existing JSON; if the file is missing, start empty; if corrupt, warn and 	continue.	load\_data

FR-14	Card creation shall cancel if opening balance is invalid or negative.	main() add-card branch



