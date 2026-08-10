What Would They Play?

A predictive model that estimates the probability of hearing a specific song at the next Dave Matthews Band show, built entirely from self-scraped historical setlist data.
All data is compiled from the DMBAlmanac, an HTML-based site developed in the early 2000s and continuously updated with every show the band has played by
notoriously obsessive fans.

URL: https://whatwouldtheyplay.streamlit.app

The problem: While one could theoretically count up the number of times a given song was played over all of DMB's shows and divide it by the number of shows overall
for a rough probability, this does not at all mimic real-world behavior. With this model, several facets of real-time touring instincts are implemented:

-A song played at nearly every show behaves very differently from one played twice a decade.
-A brand-new song with 3 plays in its first week is a different animal than an old song with 3 plays total over 20 years.
-Some songs are effectively retired; treating them the same as active rotation songs produces nonsense.

This model features four "layers", if you will, of filtering, allowing for various calculations to commence if the input song fits
any of these categories. 

-If a song was played the previous night or has not been seen at all in ten years, the probability is instantly shrunk down to 0. 
-Rare songs (≤4 historical gaps) get a shared, data-derived probability based on how often "deep cut" 
slots actually appear per show across the catalog — not an arbitrary flat share.
-Recently (ha, get it?) debuted songs without enough history to model a real cycle get a Bayesian-shrunk estimate: 
their own early play rate blended with the catalog-wide average, so a handful of plays 
in the first few shows doesn't overstate their true long-run rate.
-Established songs get a real cyclical model:
  -An exponentially weighted moving average (EWMA) over the song's last 15 performance gaps estimates its current expected return interval.
  -That feeds a hazard ratio (shows elapsed since last played ÷ expected gap), passed through a calibrated sigmoid to produce a final probability.
  -A capped hazard ratio plus a calendar-based decay factor prevent long-dormant (but not fully retired) 
  songs from mathematically saturating toward false-certainty — a bug caught and fixed through hands-on validation against known songs.

Tech Stack \n
Python is the primary language. Pandas was used for analysis, while BeautifulSoup was used for scraping.
The site is hosted on Streamlit.

Data \n
Scraped directly from DMBAlmanac.com, covering ~2,247 documented DMB shows (of ~3,600 the site tracks in total — 
the gap is almost entirely shows featuring Dave Matthews only or Dave and Tim Reynolds, alongside cancelled/rescheduled status or undocumented setlists, 
none of which wouldn't have contributed usable song-level data anyway).

Validation \n
Rather than trusting the model's formulas blindly, outputs were checked against known, real-world DMB behavior:
  -Confirmed songs played at the most recent show correctly return 0%.
  -Confirmed rare one-off songs and heavy-rotation staples land in sensible, differentiated probability ranges.
  -Caught and fixed a real bug where songs dormant for several years (but not yet at 
  the 10-year "retired" cutoff) were mathematically saturating toward ~100% probability, since their hazard 
  ratio grew unbounded — fixed with a hazard cap and a calendar-based decay factor.

Known limitations \n
-Dataset coverage is ~62% of DMBAlmanac's full show count, concentrated gaps are largely explained (cancelled/rescheduled/unknown-setlist shows).
-Sigmoid parameters (k, c) were hand-tuned against known cases rather than formally fit via logistic regression against a full historical backtest — a natural next step for further rigor.
-The dormancy decay factor is a reasonable heuristic, not derived from a formal survival-analysis model.



  
