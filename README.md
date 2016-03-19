# ProtoClass

## Documents to create at start of quarter and update through Drop/Adds

* Student E-mails from the intranet then crafted onto Canvas names for the email sheet

## Workflow for group assignments

* Instructor creates groups using `group_randomizer.py`. The input is an excel spreadsheet with
  Student Names, Class Years, and Email (i.e. the first three columns from the intranet output).
  If there is a header turn on the `--header` option, make sure that the spreadsheet has a columns
  named `Name` and `Email`.
* Instructor creates the peer evaluation sheets given the group assignments and
  `generate_peer_evaluations.py`. These evaluation sheets can be uploaded to the file section of Canvas.
* Students do assignment and one student per group uploads the assignment to Canvas. Assignment
  scores and comments are delivered using the worst goddamn tool ever made (Canvas SpeedGrader).
* Export the grade sheet from Canvas.
* Run the `group_grade_filler.py` on the spreadsheet, import it back to Canvas (everyone in group
  given the same grade.

~~ Peer Evaluations are done ~~

* Export the assignment grades from Canvas
* Download the peer evaluations from Canvas
* Run the `grade_equivocater.py`  with the assignment grade sheet, directory of peer evaluations,
  and translation sheet of Canvas name to Intranet name
* Import the modified assignment grade spreadsheet to Canvas
