/* vAssocSeqLineItems supports assocation and sequence clustering data mmining models.
      - Limits data to FY2020.
      - Returns line item nested table.*/
CREATE VIEW [dbo].[vAssocSeqLineItems]
AS
SELECT     OrderNumber, LineNumber, Model
FROM         dbo.vDMPrep
WHERE     (FiscalYear = 2020)

GO

