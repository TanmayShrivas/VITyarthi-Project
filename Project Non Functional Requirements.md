## Non-functional Requirements



NFR-01	Usability	Menus are numbered 1–5 (main) and 1–7 (card). Invalid choices print a short retry message.

NFR-02	Security (basic)	PIN is 4 digits; card numbers are masked in lists; delete needs explicit y 					confirmation; login is locked after 3 PIN failures for that attempt.

NFR-03	Reliability	Amount parsing uses try/except (ValueError). JSON load uses try/except for JSONDecodeError 			and KeyError.

NFR-04	Persistence	Data survives process exit when the user chooses Save \& Exit. File is written with indent=2 			for readability.

NFR-05	Maintainability	Business rules live in Card; collection and I/O live in ATMSystem; UI is separate functions.

NFR-06	Performance	All operations are in-memory O(n) over a small card set; suitable for classroom demos.

NFR-07	Portability	Uses only Python standard library; runs on Windows, Linux, and macOS with Python 3.

NFR-08	Auditability	Every deposit, withdraw (including failure), PIN change, and card creation is timestamped.

NFR-09	Localisation	Money is formatted to two decimals with the ₹ symbol.

NFR-10	Limitation	PIN is stored in plain text in JSON — acceptable for a simulator, not for production 				banking.



