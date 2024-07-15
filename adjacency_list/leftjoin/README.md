# SQL Sample

## SELECT all directories
```
SELECT
  CASE
  WHEN d21.name IS NOT NULL THEN
  CONCAT("21", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/', d17.name, '/', d18.name, '/', d19.name, '/', d20.name, '/', d21.name, '/')
  WHEN d20.name IS NOT NULL THEN
  CONCAT("20", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/', d17.name, '/', d18.name, '/', d19.name, '/', d20.name, '/')
  WHEN d19.name IS NOT NULL THEN
  CONCAT("19", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/', d17.name, '/', d18.name, '/', d19.name, '/')
  WHEN d18.name IS NOT NULL THEN
  CONCAT("18", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/', d17.name, '/', d18.name, '/')
  WHEN d17.name IS NOT NULL THEN
  CONCAT("17", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/', d17.name, '/')
  WHEN d16.name IS NOT NULL THEN
  CONCAT("16", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/', d16.name, '/')
  WHEN d15.name IS NOT NULL THEN
  CONCAT("15", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/', d15.name, '/')
  WHEN d14.name IS NOT NULL THEN
  CONCAT("14", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/', d14.name, '/')
  WHEN d13.name IS NOT NULL THEN
  CONCAT("13", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/', d13.name, '/')
  WHEN d12.name IS NOT NULL THEN
  CONCAT("12", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/', d12.name, '/')
  WHEN d11.name IS NOT NULL THEN
  CONCAT("11", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/', d11.name, '/')
  WHEN d10.name IS NOT NULL THEN
  CONCAT("10", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/', d10.name, '/')
  WHEN d9.name IS NOT NULL THEN
  CONCAT("09", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/', d9.name, '/')
  WHEN d8.name IS NOT NULL THEN
  CONCAT("08", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/', d8.name, '/')
  WHEN d7.name IS NOT NULL THEN
  CONCAT("07", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/', d7.name, '/')
  WHEN d6.name IS NOT NULL THEN
  CONCAT("06", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/', d6.name, '/')
  WHEN d5.name IS NOT NULL THEN
  CONCAT("05", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/', d5.name, '/')
  WHEN d4.name IS NOT NULL THEN
  CONCAT("04", '+', d1.name, '/', d2.name, '/', d3.name, '/', d4.name, '/') 
  WHEN d3.name IS NOT NULL THEN
  CONCAT("03", '+', d1.name, '/', d2.name, '/', d3.name, '/')
  WHEN d2.name IS NOT NULL THEN
  CONCAT("02", '+', d1.name, '/', d2.name, '/')
  WHEN d1.name IS NOT NULL THEN
  CONCAT("01", '+', d1.name, '/')
  END AS directory_path
FROM
  directories d1
LEFT OUTER JOIN directories d2
  ON d1.id = d2.parent_directory_id
LEFT OUTER JOIN directories d3 
  ON d2.id = d3.parent_directory_id
LEFT OUTER JOIN directories d4
  ON d3.id = d4.parent_directory_id
LEFT OUTER JOIN directories d5
  ON d4.id = d5.parent_directory_id
LEFT OUTER JOIN directories d6
  ON d5.id = d6.parent_directory_id
LEFT OUTER JOIN directories d7
  ON d6.id = d7.parent_directory_id
LEFT OUTER JOIN directories d8
  ON d7.id = d8.parent_directory_id
LEFT OUTER JOIN directories d9
  ON d8.id = d9.parent_directory_id
LEFT OUTER JOIN directories d10
  ON d9.id = d10.parent_directory_id
LEFT OUTER JOIN directories d11
  ON d10.id = d11.parent_directory_id
LEFT OUTER JOIN directories d12
  ON d11.id = d12.parent_directory_id
LEFT OUTER JOIN directories d13
  ON d12.id = d13.parent_directory_id
LEFT OUTER JOIN directories d14
  ON d13.id = d14.parent_directory_id
LEFT OUTER JOIN directories d15
  ON d14.id = d15.parent_directory_id
LEFT OUTER JOIN directories d16
  ON d15.id = d16.parent_directory_id
LEFT OUTER JOIN directories d17
  ON d16.id = d17.parent_directory_id
LEFT OUTER JOIN directories d18
  ON d17.id = d18.parent_directory_id
LEFT OUTER JOIN directories d19
  ON d18.id = d19.parent_directory_id
LEFT OUTER JOIN directories d20
  ON d19.id = d20.parent_directory_id
LEFT OUTER JOIN directories d21
  ON d20.id = d21.parent_directory_id
WHERE d1.id = 1;
```
