--select * from (select distinct file.id from file join tag where tag.file_id==file.id and tag.value like "in flames" order by file.id) as t where t.value like "in flames" ;

select * from file join (select * from (select distinct tag.file_id from tag where tag.value like "in flames") as t join tag where t.file_id==tag.file_id) as t2 where t2.file_id==file.id;
