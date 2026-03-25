/* vAssocSeqOrders supports assocation and sequence clustering data mmining models.
      - Limits data to FY2020.
      - Returns order case table.*/
CREATE VIEW [dbo].[vAssocSeqOrders]
AS
SELECT DISTINCT OrderNumber, CustomerKey, Region, IncomeGroup
FROM         dbo.vDMPrep
WHERE     (FiscalYear = 2020)

GO

