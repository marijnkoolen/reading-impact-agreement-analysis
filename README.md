# reading-impact-agreement-analysis
Interrater agreement and impact model agreement analysis based on labeled sentences from ODBR reviews

Install requirements:
```bash
pip install -r requirements.txt
```

Usage:
```bash
$python do_analysis.py
```

Which should give the following output:
```
Reading human ratings
Plotting rating distribution
	Number of annotators: 109
Filtering sentences with at least 3 raters
Reading alpino parses of sentences
Scoring sentences on reading impact
Writing human and model ratings to spreadsheet
Plotting human model rating agreement
  Total sentences: 348 	IRA >= (0.5): 233 	IRA < (0.5): 102 	Ignored (1 or 0 non-NA ratings): 13
  Total sentences: 348 	IRA >= (0.5): 247 	IRA < (0.5): 87 	Ignored (1 or 0 non-NA ratings): 14
  Total sentences: 348 	IRA >= (0.5): 191 	IRA < (0.5): 142 	Ignored (1 or 0 non-NA ratings): 15
  Total sentences: 348 	IRA >= (0.5): 191 	IRA < (0.5): 143 	Ignored (1 or 0 non-NA ratings): 14
```
