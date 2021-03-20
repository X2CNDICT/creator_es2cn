# Spanish to Chinese dictionary


### Source

* It has been parsed under `../xwang-mdict-analysis` (The es2cn parse process should be ignored, it is NOT maintained anymore). The result is refined under `src`
* `src/spanish-chinese.json`
* `src/sc-tolook.json`
* `src/sc-tofixed1.json`, `src/sc-tofixed2.json`, `src/sc-tofixed3.json`, `src/sc-tofixed4.json`


### Process

* `mkdir dst pure`

* For `vocabs`
  * `python process/process_normal.py` converts content from `src/spanish-chinese.json` to `dst/spanish-chinese.json`.
  * `python process/process_tolook.py` converts content from `src/sc-tolook.json` to `src/d1.json`, `src/d2.json` and `src/d3.json`.
  * `python process/process_dn.py` converts content from `src/d1.json` and `src/d2.json` into `dst/tolook.json`, where `src/dn.json` is byproduct.
  * `python process/process_fixed1.py` converts content from `src/sc-tofixed1.json` to `dst/sc-fixed1.json`.
  * `python process/process_fixed2.py` converts content from `src/sc-tofixed2.json` to `dst/sc-fixed2.json`.
  * `python process/process_fixed3.py` converts content from `src/sc-tofixed3.json` to `dst/sc-fixed3.json`.
  * `python process/process_fixed4.py` converts content from `src/sc-tofixed4.json` to `dst/sc-fixed4.json`.
  * `cp src/verb_variation.json dst` and `cp src/verb_variation_vos.json dst`
  * `cp -rf src/verb_inverse_variation dst` and `cp -rf src/verb_inverse_variation_vos dst`

* For `base`
  `python process/process_filter_pure.py`  

### Create mongodb

* There are two parts
  * `dst` 
    * `dst/spanish-chinese.json`
    * `dst/tolook.json`
    * `dst/sc-fixed1.json`, `dst/sc-fixed2.json`, `dst/sc-fixed3.json` and `dst/sc-fixed4.json`
    * `dst/verb_variation.json` and `dst/verb_variation_vos.json`
    * Json files under `dst/verb_inverse_variation` and  `dst/verb_inverse_variation_vos`
  * `pure`

* `python builddb/initdb.py` (Quiet complex process to deal with tiny problems)
  * Create collection `base` from folder `pure`
  * Create collections `vocabs`, `verbs_variation` and `verbs_inverse_variation` from folder `dst`

