# FMS: Fees Management System for VJTI college

 Three branches:
   . dev: Do all pushes in dev branch
   . main: Once major push is tested for conflictions. It will moved to main branch.
   . backup: We will push major updates in backup branch once tested. (In ideal scenario this branch content will not be pulled)

Always look for any updates/pulls from teammate while starting coding. If some pulls are conflicting then collaborate with teammate and solve the conflictions, do not do force push.

Project Structure: 
FMS: Main root folder
  . FMS: app module
  . static:
    . css: contains all css files
      . base.css
    . img: contains img assets
  . templates: contains all html files
    . base.html
