### Activism Tools Against Cybertorture

#### Q.A. Metrics

##### GitHub
![python-app](https://github.com/strikles/atac/actions/workflows/python-app.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Upload Python Package](https://github.com/strikles/atac/actions/workflows/python-publish.yml/badge.svg?branch=main)](https://github.com/strikles/atac/actions/workflows/python-publish.yml)

##### Codacy
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d3de586ed5a248ca917c99e95757252c)](https://www.codacy.com/gh/strikles/atac/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=strikles/atac&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/d3de586ed5a248ca917c99e95757252c)](https://www.codacy.com/gh/strikles/atac/dashboard?utm_source=github.com&utm_medium=referral&utm_content=strikles/atac&utm_campaign=Badge_Coverage)

##### DeepSource
[![DeepSource](https://deepsource.io/gh/strikles/atac.svg/?label=active+issues&show_trend=true&token=knjxrFWrr_WNtdD2XCDeYO0i)](https://deepsource.io/gh/strikles/atac/?ref=repository-badge)
[![DeepSource](https://deepsource.io/gh/strikles/atac.svg/?label=resolved+issues&show_trend=true&token=knjxrFWrr_WNtdD2XCDeYO0i)](https://deepsource.io/gh/strikles/atac/?ref=repository-badge)

##### Codiga
[![Code Quality Score](https://api.codiga.io/project/29990/score/svg)](https://www.code-inspector.com/public/project/29990/atac/dashboard)
[![Code Grade](https://www.code-inspector.com/project/29990/status/svg)](https://www.code-inspector.com/public/project/29990/atac/dashboard)

![](assets/img/IMG_3332.JPG)

#### Summary

Cybertorture is recognized by the United Nations under A/HRC/43/49 and is used in grotesque rituals of social stratification (by cowardly colégio militar alumni, law enforcement and others recruited for the purpose) to exact extrajudicial trials and sentences as an interactive spectacle encouraging participation, mongering tensions and hatred by preying on cognitive biases.

Colégio Militar alumni have been setting standards of mediocrity and creating fascist psychopaths in law enforcement and the armed forces who have been involved in crafting synthetic “human trash” social stratification schemes and simulating mental illness with cybertorture extrajudicial trials and sentences for nearly 30 years destroying whole families and turning its members against each other to satisfy whims, entertained themselves remotely articulating tongues and jaws to force people to talk to themselves, forced people to regurgitate, defecate and urinate themselves, directed violence to children, parents and women, remotely broke teeth like cowards, set cybersodomy and vibrotactile cybertorture to simulate Van Gogh syndrome via abuse of mechanotransduction phenomena as a standard extrajudicial sentence and threatened whole families with forced incarceration and psychiatric commitments as extrajudicial methods of intimidation…

Further social stratification schemes and mediocrity standards became common place by making plagiarism a standard in the school via a tradition of passing school keys from year to year to steal exams!

Sign the petition to either close Colégio Militar (largo da Luz, Portugal) or reform and bring dignity to the school…

https://chng.it/8FtDcsvG

![](assets/img/IMG_3331.PNG)

Those who exact the extrajudicial sentences resort to directing violence towards women, parents, creating drug addicts with synthetic pain and forcing acts of self-harm for entertainment, whilst attempting to portray themselves as Artists of human degradation, social stratification and self-harm, with grotesque preludes of vibrotactile and sonic payloads of "kisses" and setting synthetic pain, articulating tongue and jaw of the subject under torture, cyber sodomy, intercourse sabotage in males (via involuntary perineum contractions resorting to rituals involving using a feather) and vibrotactile genital abuse in females (possibly resulting in Stockholm's Syndrome) as being standard in our society

> "Deus autem, primum principium rerum, comparatur ad res creatas ut artifex ad artificiata"

The procedure is hidden under a veil of medical malpractice via psychiatric fraud (violating every principle in the code of ethics set by the World Psychiatry Association), false therapy in the form of forced conventional pharmacotherapy (with an associated high risk of suicide) when it could be used to provide therapeutic payloads via the same medium, raising feelings of paranoia towards remote healthcare, neural engineering and electroceuticals where the risk of suicide would be nearly zero!

![](assets/img/28B6320C-154B-42E4-9642-8212498D9913.jpeg)

#### Since Cybertorture paired with Psychiatric Fraud and False therapy has been used for quite some time now to stratify society with extrajudicial trials and sentences for motives as repugnant as "someone not liking you" or "talking nonsense", I decided to write some tools

![](assets/img/tumblr_inline_pec2nqah2k1qlr65v_540.gif)

##### [scrape.py](scrape.py)
web scraper that gathers contact information

[scrapeme](SCRAPEME.md)

##### The current scraping algorithm is the following
```markdown
P ← starting URLs (primary queue) 
S ← ∅ (secondary queue)
V ← ∅ (visited pages)
while P ≠ ∅ do
    Pick a page v from P and download it
    V ← V ∪ {v} (mark as visited)
    N+(v) ← v’s out-links pointing to new pages (“new” means not in P, S or V)
    if |N+(v)| > t then
        R ← first t out-links N+(v)
        S ← S ∪ (v)
    end if
    P ← P ∪ R
    if P = ∅ then
        P ← S
        S ← ∅ 
    end if
```

it is based on [https://chato.cl/papers/castillo_06_controlling_queue_size_web_crawling.pdf](https://chato.cl/papers/castillo_06_controlling_queue_size_web_crawling.pdf)

![](assets/img/IMG_0729.PNG)

##### [compose.py](compose.py)
automated composition of text using markovify

![](assets/img/IMG_0999.JPG)

##### [send.py](send.py)
send script:

1.  email
2.  facebook
3.  twitter
4.  whatsapp

![](assets/img/AgreeableCoordinatedFlounder-small.gif)
