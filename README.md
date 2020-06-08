# Dispatch Report
This program was used to autogenerate daily dispatch reports. Prior to this, dispatchers spent significant time copy data from various sources to create the daily report. This program saved significant time, prevented errors and ensured a standardized report by pulling data from the various APIs, formatting it, and sending it to a google sheet.

## Use
- Run `main.py` to make a report
- Main calls a number of classes/modules from `modules/`
- Initial experiments are in `old_examples/`

## API Docs
- [Deputy Employee Management](https://www.deputy.com/api-doc/API)
- [Fleetio Vehicle Management](https://developer.fleetio.com/docs/overview)
