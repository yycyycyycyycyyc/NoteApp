# Project 1 - NotesApp threat model

This submission models the current NotesApp implementation independently from the source code.

- `NotesApp-Numbered-DFD.pdf` contains four components, three trust boundaries, and 16 numbered logical data flows.
- `NotesApp-STRIDE-Risk.xlsx` maps one concrete STRIDE threat to every flow, scores likelihood and impact from 1 (low) to 3 (high), calculates risk, and identifies the three priority risks.

The top priorities are command injection in the admin ping function, root-container exposure through the Docker socket/project mount, and forgeable JWT authentication. Proposed controls are recommendations; the Project 1 model does not claim that all of them have been implemented.
