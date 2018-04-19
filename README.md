# RFID-Access-Control
An RFID controlled lock!

With a newer Onion RFID & NFC Expansion you can now bring contactless access to control things like electromagnetic locks, LEDs, access permissions, etc. It supports reading and writing with several NFC and RFID protocols at 13.56 MHz. The Expansion is based on the popular PN532 NFC Chip and communicates with the Omega via UART1.

The program waits till you tap the card that is specified and opens the lock for 5 seconds if the card is presented, if not, it'll constantly wait till the specified tag is tapped.
