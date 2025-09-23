use  Cust_Emp


select * from dbo.Departments


USE dataentry;

delete from dbo.PersonData 
where id in  
(select id from  
	(select *,row_number() over (partition by email order by id) rn  
	from dbo.PersonData) a  
	where rn >1)