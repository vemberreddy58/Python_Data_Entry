use  Cust_Emp


select * from dbo.Departments


USE dataentry;

 delete from dbo.PersonData 
where id in  
(select id from  
	(select *,row_number() over (partition by email order by id) rn  
	from dbo.PersonData) a  
	where rn >1)


select * from [dbo].[PersonData]


begin tran
delete from [dbo].[PersonData]
rollback 
commit 


begin 
	if exists (select 1 from [dbo].[PersonData])
	 select distinct name  from  [dbo].[PersonData]
	if not exists(select 1 from [dbo].[PersonData])
	 print 'no names'
end 



