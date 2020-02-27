# reading-impact-agreement-analysis

This repository contains code and auxiliary materials for the article **Captivating, splendid or instructive? Assessing the impact of reading in online book reviews** by [Peter Boot](http://peterboot.nl/) and [Marijn Koolen](http://marijnkoolen.com/#/). 

This article introduces a prediction model for reading impact expressed in book reviews. The model is evaluated against human judgements on how individual sentences in online book reviews express various types of impact. To validate the human ratings as a gold standard dataset, we performed an analysis of interrater agreement. The article contains the context in which this is done and describes the IRA analysis briefly. 

A detailed explanation of our choices for IRA statistics is available here: [Interrater Agreement](interrater-agreement.md).

The code in this repository is used to do the analysis.

## Running the code

All code is in Python 3.

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

Removing sentences with fewer than 3 raters

Analyzing null distributions

	emotional_scale
		rating: 0 	freq: 264 	ratio: 0.27
		rating: 1 	freq: 98 	ratio: 0.1
		rating: 2 	freq: 125 	ratio: 0.13
		rating: 3 	freq: 227 	ratio: 0.23
		rating: 4 	freq: 260 	ratio: 0.27
		mean: 2.124229979466119 variance: 2.4701931955694043

	style_scale
		rating: 0 	freq: 503 	ratio: 0.52
		rating: 1 	freq: 134 	ratio: 0.14
		rating: 2 	freq: 118 	ratio: 0.12
		rating: 3 	freq: 103 	ratio: 0.11
		rating: 4 	freq: 116 	ratio: 0.12
		mean: 1.173511293634497 variance: 2.102337362808799

	reflection_scale
		rating: 0 	freq: 379 	ratio: 0.39
		rating: 1 	freq: 95 	ratio: 0.1
		rating: 2 	freq: 145 	ratio: 0.15
		rating: 3 	freq: 176 	ratio: 0.18
		rating: 4 	freq: 179 	ratio: 0.18
		mean: 1.6724845995893223 variance: 2.4625488575657024

	narrative_scale
		rating: 0 	freq: 375 	ratio: 0.39
		rating: 1 	freq: 84 	ratio: 0.09
		rating: 2 	freq: 120 	ratio: 0.12
		rating: 3 	freq: 175 	ratio: 0.18
		rating: 4 	freq: 220 	ratio: 0.23
		mean: 1.7751540041067762 variance: 2.65888986334639

	all
		rating: 0 	freq: 1521 	ratio: 0.39
		rating: 1 	freq: 411 	ratio: 0.11
		rating: 2 	freq: 508 	ratio: 0.13
		rating: 3 	freq: 681 	ratio: 0.17
		rating: 4 	freq: 775 	ratio: 0.2
		mean: 1.6863449691991785 variance: 2.5391975237067235

Reading alpino parses of sentences
Scoring sentences on reading impact
Writing human and model ratings to spreadsheet
	writing ratings to spreadsheet file reading_impact_questionnaire_data.xlsx

Calculating interrater agreement using the inverse triangular null-distribution
	emotional_scale     	mean IRA: 0.6212097514180848 	stdev IRA: 0.4031332654623196
	style_scale         	mean IRA: 0.6508100362267029 	stdev IRA: 0.410555850315281
	reflection_scale    	mean IRA: 0.48362946279612945 	stdev IRA: 0.45354349187167586
	narrative_scale     	mean IRA: 0.491273267314934 	stdev IRA: 0.48301007982598076

	writing per sentence IRA score distribution to file images/per_sentence_ira_distribution.png

Plotting human model rating agreement for IRA >= 0.5

	Impact scale    	Total sentences	IRA >= 0.5	IRA < 0.5	Ignored (1 or 0 non-NA ratings)
	emotional_scale     	348		231		102		15
	style_scale         	348		244		89		15
	reflection_scale    	348		191		142		15
	narrative_scale     	348		190		143		15

Performing Mann-Whitney U test for IRA >= 0.5

	emotional_scale
		R model X = 0: 21692.5 	R model X >= 1: 5103.5
		N model X = 0: 167 	N model X >= 1: 64
		U model X = 0: 7664.5 	U model X >= 1: 3023.5
		U: 3023.5 	p: 9.104959071390422e-08

	style_scale
		R model X = 0: 29295.0 	R model X >= 1: 595.0
		N model X = 0: 225 	N model X >= 1: 19
		U model X = 0: 3870.0 	U model X >= 1: 405.0
		U: 405.0 	p: 3.447530409743655e-11

	reflection_scale
		R model X = 0: 17900.5 	R model X >= 1: 435.5
		N model X = 0: 185 	N model X >= 1: 6
		U model X = 0: 695.5 	U model X >= 1: 414.5
		U: 414.5 	p: 0.13688354103866712

	narrative_scale
		R model X = 0: 16773.0 	R model X >= 1: 1372.0
		N model X = 0: 165 	N model X >= 1: 25
		U model X = 0: 3078.0 	U model X >= 1: 1047.0
		U: 1047.0 	p: 2.0229277261513342e-05

Making model boxplots for IRA>= 0.5
	writing box plot to file images/model-comparison-boxplot-IRA-0.5.png

```
