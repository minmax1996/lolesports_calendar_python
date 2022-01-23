# LOLesports calendar

to just create *.ics file 
```
ESPORTS_TOKEN=<token> python main.py
```

to create flask server that generates subscription file
```
ESPORTS_TOKEN=<token> flask run
```

and paste `http://127.0.0.1:5000/calendar?leagues=lcs,lec&teams=fnc,c9` something like that in create calendar subscription