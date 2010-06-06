--SELECT COUNT(*)
DELETE
FROM feed_entries
WHERE id NOT IN (
	SELECT entry_id FROM  classifications_entries
)
--AND updated < '2010-04-01 00:00:00.000000'
--AND NOT updated IS NULL;
AND updated IS NULL;
--ORDER BY id DESC
--LIMIT 1000
--commit;

-- 2009-09-30 22:00:00.000000
-- 2009-01-01 00:00:00.000000
/*
SELECT MIN(updated)
FROM feed_entries
WHERE NOT updated IS NULL
*/
