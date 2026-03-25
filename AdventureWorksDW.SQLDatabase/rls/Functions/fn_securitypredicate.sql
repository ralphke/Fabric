CREATE   FUNCTION rls.fn_securitypredicate(@value AS VARCHAR(60)) 
   RETURNS TABLE  
WITH SCHEMABINDING  
AS  
   RETURN SELECT 1 AS fn_securitypredicate_result   
WHERE @value = USER_NAME();

GO

