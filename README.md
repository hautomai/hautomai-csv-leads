# csv-leads

Utility for merging and de-duplicating batches of lead CSVs exported from
different sources.

Place the source batches in `Leads/`, then:

```bash
python3 merge_leads.py
```

It writes `merged_leads.csv` (all rows, union of headers) and
`merged_leads_dedup.csv` (deduplicated on email). Column names are preserved
from the first file that defines them.

No lead data is included in this repository.
